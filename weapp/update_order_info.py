# -*- coding: utf-8 -*-
import sys
import datetime
import copy
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "weapp.settings")

from django.core.management import execute_from_command_line

execute_from_command_line(sys.argv)

import json
from mall import models as mall_models
from eaglet.utils.resource_client import Resource


##########################################处理数据更新############################################################
def update_info(index_start,index_stop):
    relations = mall_models.OrderHasProduct.objects.filter(id__range=[index_start,index_stop])
    product_ids = [r.product_id for r in relations]
    id2product = dict([(product.id, product) for product in mall_models.Product.objects.filter(id__in=product_ids)])
    n = 0
    for relation in relations:
        product = id2product[relation.product_id]
        product.fill_specific_model(relation.product_model_name)
        l = []
        if product.custom_model_properties:
            for pro in product.custom_model_properties:
                l.append(pro['property_value'])
        mall_models.OrderHasProduct.objects.filter(id=relation.id).update(
            weight=product.weight,
            thumbnail_url=product.thumbnails_url,
            product_model_name_texts=json.dumps(l),
            product_model_id = product.model.id
        )
        n += 1
        print n,"==================================="


if __name__ == "__main__":
    from django.db.models import Max, Min
    max_id = mall_models.OrderHasProduct.objects.filter(created_at__gte='2016-12-01 00:00:00').aggregate(Max('id'))
    print max_id,'=============================='
    min_id = mall_models.OrderHasProduct.objects.filter(created_at__gte='2016-12-01 00:00:00').aggregate(Min('id'))
    print min_id,'=============================='
    update_info(int(min_id['id__min']),int(max_id['id__max']))
    print "=============================done"

######################################################################################################
