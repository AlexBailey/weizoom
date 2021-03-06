# -*- coding: utf-8 -*-
import sys
import datetime
import copy

reload(sys)
sys.setdefaultencoding("utf-8")
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

import json
from mall import models as mall_models

from market_tools.tools.weizoom_card import models as wz_models

records = wz_models.WeizoomCardHasOrder.objects.all()

print('----start...')

for record in records:
	try:
		if record.order_id != '-1' and record.event_type == '使用':
			order_id = record.order_id
			card_id = wz_models.WeizoomCard.objects.filter(id=record.card_id).first().weizoom_card_id
			info = mall_models.OrderCardInfo.objects.filter(order_id=order_id).first()
			if info:
				used_card = json.loads(info.used_card) + [card_id]
				info.used_card = json.dumps(list(set(used_card)))
				info.save()
			else:
				mall_models.OrderCardInfo.objects.create(
					order_id=order_id,
					trade_id=-1,
					used_card=json.dumps([card_id])
			)
	except BaseException as e:
		print("record.id:{},e:{}".format(record.id, e))

print('end...')
