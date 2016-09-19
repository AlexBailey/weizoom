#coding:utf8
"""
取消“团购”超时的未付款订单的
"""
from datetime import datetime, timedelta
import time
import logging

from django.core.management.base import BaseCommand, CommandError

from core.exceptionutil import unicode_full_stack
from watchdog.utils import watchdog_error, watchdog_info, watchdog_warning

from mall import models as mall_models
from account.models import UserProfile
from mall.module_api import update_order_status
from django.conf import settings
from bdem import msgutil


class Command(BaseCommand):
    help = "send coupon expired remained"
    args = ''

    def handle(self, **options):
        """
        取消“团购”超时的未付款订单的
        """
        try:
            webapp_ids = []
            relations = mall_models.OrderHasGroup.objects.filter(
                    group_status=mall_models.GROUP_STATUS_ON
                )
            for relation in relations:
                if relation.webapp_id not in webapp_ids:
                    webapp_ids.append(relation.webapp_id)

            webapp_id2user = dict([(user_profile.webapp_id, user_profile.user)for user_profile in UserProfile.objects.filter(webapp_id__in=webapp_ids)])
            order_ids = []
            orders = mall_models.Order.objects.filter(
                    order_id__in=[r.order_id for r in relations],
                    status=mall_models.ORDER_STATUS_NOT,
                    created_at__lte=datetime.now() - timedelta(minutes=15)
                )
            for order in orders:
                try:
                    update_order_status(webapp_id2user[order.webapp_id], 'cancel', order)
                    relations.filter(order_id=order.order_id).update(group_status=mall_models.GROUP_STATUS_failure)
                    logging.info(u"团购15分钟未支付订单order_id:%s取消成功" % order.order_id)
                    order_ids.append(order.order_id)
                except:
                    notify_msg = u"团购未支付订单{}，取消失败, cause:\n{}".format(order.order_id, unicode_full_stack())
                    watchdog_error(notify_msg)
                    continue
            watchdog_info({
                'hint': 'cancel_group_order_and_notify_pay',
                'order_ids': 'order_ids',
                'uuid': 'cancel_group_order_and_notify_pay'
            })
            if not settings.IS_UNDER_BDD and order_ids:
                # BDD时不发消息
                topic_name = "order-close"
                data = {
                    "name": "cancel_group_order_and_notify_pay",
                    "data": {
                        "order_ids": order_ids
                    }
                }
                msg_name = "cancel_order"
                msgutil.send_message(topic_name, msg_name, data)
        except:
            notify_msg = u"团购未支付订单取消失败, cause:\n{}".format(unicode_full_stack())
            watchdog_error(notify_msg)

        print "success"