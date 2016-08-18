# -*- coding: utf-8 -*-

import time
import logging
import datetime
from django.core.management.base import BaseCommand, CommandError
from market_tools.tools.distribution.models import ChannelDistributionQrcodeSettings, ChannelDistributionQrcodeHasMember, \
                                                    ChannelDistributionDetail, ChannelDistributionFinish
from mall.models import Order
from modules.member.models import WebAppUser
from django.db.models import F


class Command(BaseCommand):
    """
    微信用户下单后, 更新二维码绑定用户收到的佣金

    """
    def __init__(self):
        start_datetime = datetime.datetime.strptime('2016-8-18 10:59', "%Y-%m-%d %H:%M")
        eleven_days_ago = datetime.datetime.now() - datetime.timedelta(days=11)  # 只处理11天之前的数据
        self.start_time = max(start_datetime, eleven_days_ago)
        super(Command , self).__init__()

    help = ''
    args = ''

    def handle(self, *args, **options):
        # 所有的绑过的{memberid: qrcode_id}
        member_ids = []

        member_id_to_qrocde_id ={}
        members = ChannelDistributionQrcodeHasMember.objects.all()
        for member in members:
            # members_dict[member.member_id] = member.channel_qrcode_id
            member_id_to_qrocde_id[member.member_id] = member.channel_qrcode_id

        web_app_users = WebAppUser.objects.filter(member_id__in=(member_id_to_qrocde_id.keys()))
        web_app_user_dict = {web_app_user.id: web_app_user.member_id for web_app_user in web_app_users}
        # web_app_user_list = {web_app_user.id: web_app_user.member_id for web_app_user in web_app_users}

        members_dict = {}
        for web_app_user in web_app_users:
            members_dict[web_app_user.id] = member_id_to_qrocde_id[web_app_user.member_id]

        # 取出所有的订单
        orders = Order.objects.filter(created_at__gt=self.start_time, status=5, supplier_user_id=0)  # 搜索大于启动时间, 并已完成的订单

        finish_order_list = []  # 从数据库取出所有结算过的信息
        finish_orders = ChannelDistributionFinish.objects.all()
        for finish_order in finish_orders:
            finish_order_list.append(finish_order.order_id)

        qrcodes_dict = {}  # 所有渠道分销二维码信息 {qrcode_id: qrcode}

        qrcodes = ChannelDistributionQrcodeSettings.objects.all()
        print 'members_dict', members_dict
        for qrcode in qrcodes:  # 二维码id: 二维码
            qrcodes_dict[qrcode.id] = qrcode
        for order in orders:
            # print '>>>order.id=', order.id
            logging.info(order.id)
            print order.webapp_user_id
            # 如果此订单的购买者之前绑过渠道分销二维码

            # if members_dict.has_key(order.webapp_user_id) and order.id not in finish_order_list:
            if order.webapp_user_id in web_app_user_dict.keys() and order.id not in finish_order_list:
                # qrcode = ChannelDistributionQrcodeSettings.objects.filter(id=members_dict[order.webapp_user_id])
                order_qrcode = qrcodes_dict[members_dict[order.webapp_user_id]]  # 此订单会员绑定的二维码
                conform_minimun_return_rate = True if order.final_price /order.product_price > order_qrcode.minimun_return_rate / 100.0 else False  # 满足最低返现折扣
                print '订单已绑定'
                if order_qrcode.distribution_rewards:  # 如果返佣金
                    if order_qrcode.return_standard:  # 有返回天数限制
                        if order.created_at > datetime.datetime.now() - datetime.timedelta(
                                days=order_qrcode.return_standard):
                            return None
                    if conform_minimun_return_rate:  # 如果满足最低返现标准

                        commission = order.final_price * (order_qrcode.commission_rate / 100.0)

                        ChannelDistributionQrcodeHasMember.objects.filter(member_id=web_app_user_dict[order.webapp_user_id]).update(
                            cost_money = F('cost_money') + order.final_price,
                            buy_times = F('buy_times') + 1,
                            commission_not_add = F('commission_not_add') + commission
                        )
                        ChannelDistributionQrcodeSettings.objects.filter(id=order_qrcode.id).update(
                            will_return_reward=F('will_return_reward') + commission,
                            total_transaction_volume=F('total_transaction_volume') + order.final_price,
                            current_transaction_amount=F('current_transaction_amount') + order.final_price
                        )
                        print u'Order %s is finish, satisfy the standard of cashback' % order.id
                        print ChannelDistributionQrcodeHasMember.objects.get(member_id=web_app_user_dict[order.webapp_user_id]).commission_not_add
                    else:
                        ChannelDistributionQrcodeHasMember.objects.filter(member_id=web_app_user_dict[order.webapp_user_id]).update(
                            cost_money = F('cost_money') + order.final_price,
                            buy_times = F('buy_times') + 1,
                        )
                        ChannelDistributionQrcodeSettings.objects.filter(id=order_qrcode.id).update(
                            total_transaction_volume=F('total_transaction_volume') + order.final_price,
                            current_transaction_amount=F('current_transaction_amount') + order.final_price
                        )
                        print u'Order %s is finish, dont satisfy the standard of cashback' % order.id

                    ChannelDistributionDetail.objects.create(
                        channel_qrcode_id=order_qrcode.id,
                        money=order.final_price,
                        # member_id=order_qrcode.bing_member_id,
                        member_id=web_app_user_dict[order.webapp_user_id],
                        order_id=order.id
                    )
                    ChannelDistributionFinish.objects.create(
                        order_id=order.id,
                        order_time=order.created_at
                    )


            else:  # 没有绑定过不处理
                pass
