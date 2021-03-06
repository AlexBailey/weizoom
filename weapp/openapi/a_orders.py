# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from core import resource
from core import paginator
import wapi as api_resource
from core.jsonresponse import create_response

class OrderList(resource.Resource):
    """
    订单列表资源
    """
    app = "openapi"
    resource = "order_list"

    def post(request):

        response = create_response(200)
        response.data = {}
        access_token = request.POST.get('access_token','')
        found_begin_time = request.POST.get('found_begin_time','')
        found_end_time = request.POST.get('found_end_time','')
        pay_begin_time = request.POST.get('pay_begin_time','')
        pay_end_time = request.POST.get('pay_end_time','')
        order_status = request.POST.get('order_status','')
        order_id = request.POST.get('order_id','')
        cur_page = request.POST.get('cur_page',1)
        orders,pageinfo,count = api_resource.get('open', 'orders', {'access_token':access_token,
													 'found_begin_time':found_begin_time,
													 'found_end_time':found_end_time,
													 'pay_begin_time':pay_begin_time,
													 'pay_end_time':pay_end_time,
                                                     'order_status':order_status,
                                                     'order_id':order_id,
                                                     'cur_page':cur_page
                                                      })
        response.data = {}
        response.data['pageinfo'] = paginator.to_dict(pageinfo)
        response.data['count'] = count
        response.data['items'] = orders
        return response.get_response()


