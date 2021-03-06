# -*- coding: utf-8 -*-
__author__ = 'cl'

from datetime import datetime, date
import os

from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from core import resource
from mall.promotion import models as promotion_models
from mall import export
from core.jsonresponse import create_response
from core import paginator
from mall.models import Order
from mall.promotion.models import COUPONSTATUS,COUPON_STATUS_USED
from modules.member.models import MemberGrade, MemberFollowRelation, Member

from utils.string_util import byte_to_hex
from modules.member import models as member_models
from weapp import settings

COUNT_PER_PAGE = 20

FIRST_NAV_NAME  = export.MALL_PROMOTION_AND_APPS_FIRST_NAV


class RedEnvelopeParticipances(resource.Resource):
    app = "apps/red_envelope"
    resource = "red_envelope_participances"

    @login_required
    def get(request):
        """
        红包分析页面
        """
        rule_id = request.GET.get('id', None)
        redEnvelope2Order_data = promotion_models.RedEnvelopeToOrder.objects.filter(red_envelope_rule_id=rule_id)
        received_count = redEnvelope2Order_data.count() #领取人数
        rule_data = promotion_models.RedEnvelopeRule.objects.get(id=rule_id)
        coupon_rule = promotion_models.CouponRule.objects.get(id=rule_data.coupon_rule_id)
        relations = promotion_models.RedEnvelopeParticipences.objects.filter(red_envelope_rule_id=rule_id)
        coupon_ids = [r.coupon_id for r in relations]
        coupons = promotion_models.Coupon.objects.filter(id__in=coupon_ids)
        coupon_id2coupon = dict([c.id, c] for c in coupons)
        new_member_count = 0         #新关注人数
        consumption_sum = 0          #产生消费额
        total_use_count = relations.filter(coupon__status=COUPON_STATUS_USED).count()     #使用人数

        #加上引入的数字
        orders = Order.objects.filter(coupon_id__in=coupon_ids, status=5)
        coupon_id2order = {}
        for order in orders:
            cur_coupon_id = order.coupon_id
            coupon_id2order[cur_coupon_id] = order
        for relation in relations:
            #求用优惠券的情况下，该红包规则下的总消费额
            cur_coupon = coupon_id2coupon[relation.coupon_id]
            if cur_coupon.status == 1 and relation.introduced_by == 0:
                if cur_coupon.id in coupon_id2order:
                    order = coupon_id2order[cur_coupon.id]
                    consumption_sum = consumption_sum + order.final_price + order.postage
            new_member_count += relation.introduce_new_member
            received_count += relation.introduce_received_number
            consumption_sum += relation.introduce_sales_number
        c = RequestContext(request, {
            'first_nav_name': FIRST_NAV_NAME,
            'second_navs': export.get_promotion_and_apps_second_navs(request),
            'second_nav_name': export.MALL_APPS_SECOND_NAV,
            'third_nav_name': export.MALL_APPS_RED_ENVELOPE_NAV,
            'new_member_count': new_member_count,
            'received_count': received_count,
            'consumption_sum': '%.2f' % consumption_sum,
            'total_use_count': total_use_count,
            'red_envelope_id': rule_id,
            'red_envelope_name': rule_data.name,
            'red_envelope_start_time': rule_data.start_time.strftime("%Y-%m-%d"),
            'red_envelope_end_time': rule_data.end_time.strftime("%Y-%m-%d"),
            'limit_time': rule_data.limit_time,
            'is_timeout': False if rule_data.end_time > datetime.now() else True,
            'receive_method': rule_data.receive_method,
            'coupon_rule_id': coupon_rule.id
        })
        return render_to_response('red_envelope/templates/editor/red_envelope_participances.html', c)


    def get_datas(request):
        owner_id = request.user_profile.user_id
        member_name = request.GET.get('member_name', '')
        grade_id = request.GET.get('grade_id', '')
        coupon_status = request.GET.get('coupon_status', '')
        red_envelope_rule_id = request.GET.get('id',0)
        receive_method = request.GET.get('receive_method','')
        #引入
        introduced_by = request.GET.get('introduced_by',0)
        relation_id = request.GET.get('relation_id',0)
        rule_id = request.GET.get('rule_id',0)
        #导出
        is_export = request.GET.get('is_export',0)
        selected_ids = request.GET.get('selected_ids',0)
        #排序
        sort_attr = request.GET.get('sort_attr', '-created_at')
        _update_member_bring_new_member_count(red_envelope_rule_id)

        if is_export:
            if selected_ids:
                selected_ids = selected_ids.split(",")
                relations = promotion_models.RedEnvelopeParticipences.objects.filter(
                    owner_id = owner_id,
                    red_envelope_rule_id=red_envelope_rule_id,
                    red_envelope_relation_id__in=selected_ids,
                    introduced_by=0
                )
            else:
                relations = promotion_models.RedEnvelopeParticipences.objects.filter(
                    owner_id = owner_id,
                    red_envelope_rule_id=red_envelope_rule_id,
                    introduced_by=0
                )
        else:
            if introduced_by:
                relations = promotion_models.RedEnvelopeParticipences.objects.filter(
                    owner_id = owner_id,
                    red_envelope_rule_id=rule_id,
                    red_envelope_relation_id=relation_id,
                    introduced_by=introduced_by
                )
            else:
                relations = promotion_models.RedEnvelopeParticipences.objects.filter(
                    owner_id = owner_id,
                    red_envelope_rule_id=red_envelope_rule_id,
                    introduced_by=0
                )

        all_member_ids = [relation.member_id for relation in relations]
        all_members = member_models.Member.objects.filter(id__in=all_member_ids)

        #筛选会员
        if member_name:
            hexstr = byte_to_hex(member_name)
            members = all_members.filter(username_hexstr__contains=hexstr)
            all_members = members
        elif grade_id:
            members = all_members.filter(grade_id=grade_id)
        else:
            members = all_members
        member_ids = []
        member_id2member = {}
        for member in members:
            member_ids.append(member.id)
            member_id2member[member.id] = member

        #优惠券查找
        relations = relations.filter(member_id__in=member_ids)
        if coupon_status:
            final_relations_ids = []
            for relation in relations:
                if str(coupon_status) == '1':
                    if relation.coupon.status == int(coupon_status):
                        final_relations_ids.append(relation.id)
                else:
                    if relation.coupon.status !=1:
                        final_relations_ids.append(relation.id)
            relations = relations.filter(id__in=final_relations_ids)

        #处理排序,需要放在分页之前
        relations = relations.order_by(sort_attr)

        if not is_export:
            #进行分页
            count_per_page = int(request.GET.get('count_per_page', COUNT_PER_PAGE))
            cur_page = int(request.GET.get('page', '1'))
            pageinfo, relations = paginator.paginate(relations, cur_page, count_per_page, query_string=request.META['QUERY_STRING'])

        # 获取被使用的优惠券对应订单信息
        coupon_ids = [c.coupon_id for c in relations if c.coupon.status == COUPON_STATUS_USED]
        orders = Order.get_orders_by_coupon_ids(coupon_ids)
        if orders:
            coupon_id2order_id = dict([(o.coupon_id, o.id) for o in orders])
        else:
            coupon_id2order_id = {}


        member_ids = []
        for sub_relation in relations:
            member_ids.append(sub_relation.member_id)

        #获取关注关系l
        member_follow_relation = MemberFollowRelation.objects.filter(member_id__in=member_ids)

        #只保存新会员的最后一条记录l
        member_id2follower_member_id ={}
        for member in member_follow_relation:
            member_id2follower_member_id[member.member_id] = member.follower_member_id

        members = Member.objects.filter(id__in=member_ids)
        member_id2member = dict([(m.id, m) for m in members])

        grade_ids = [m.grade_id for m in members]
        grades = MemberGrade.objects.filter(id__in=grade_ids)
        grade_id2grade = dict([(g.id, g.name) for g in grades])

        items = []
        for relation in relations:
            cur_member = member_id2member[relation.member_id]
            cur_grade_id = cur_member.grade_id
            if receive_method == 'True':
                if cur_member.is_subscribed and cur_grade_id:
                    grade = grade_id2grade[cur_grade_id]
                else:
                    grade = u"会员"
            else:
                if cur_member.is_subscribed:
                    if relation.is_new:
                        if member_id2follower_member_id[relation.member_id] == relation.introduced_by:
                            grade = u"新会员"
                        else:
                            grade = u"非会员"
                    else:
                        grade = grade_id2grade[cur_grade_id]
                else:
                    grade = u"非会员"
            try:
                name = cur_member.username.decode('utf8')
            except:
                name = cur_member.username_hexstr
            items.append({
                'id': relation.red_envelope_relation_id,
                'member_id': relation.member_id,
                'username': cur_member.username_for_title,
                'name': name,
                'username_truncated': cur_member.username_truncated,
                'participant_icon': relation.member.user_icon,
                'introduce_received_number_count': relation.introduce_received_number,
                'introduce_new_member_count': relation.introduce_new_member,
                'introduce_used_number_count': relation.introduce_used_number,
                'introduce_sales_number': '%.2f' %  relation.introduce_sales_number,
                'created_at': relation.created_at.strftime("%Y-%m-%d"),
                'coupon_status': relation.coupon.status,
                'coupon_status_name': COUPONSTATUS[relation.coupon.status]['name'],
                'order_id': coupon_id2order_id[relation.coupon_id] if coupon_id2order_id.has_key(relation.coupon_id) else '',
                'grade': grade,
                'receive_method': receive_method
            })

        if is_export:
            return  items
        else:
            return pageinfo, items

    @login_required
    def api_get(request):
        """
        获取advanced table
        """
        pageinfo, items = RedEnvelopeParticipances.get_datas(request)
        sort_attr = request.GET.get('sort_attr', '-created_at')
        response_data = {
			'items': items,
			'pageinfo': paginator.to_dict(pageinfo),
			'sortAttr': sort_attr,
			'data': {}
		}
        response = create_response(200)
        response.data = response_data
        return response.get_response()

def _update_member_bring_new_member_count(red_envelope_rule_id=None):
    """
    更新红包引入新会员的数量
    """
    if not red_envelope_rule_id:
        return

    relations = promotion_models.RedEnvelopeParticipences.objects.filter(
            red_envelope_rule_id=red_envelope_rule_id,
            introduced_by=0
        )
    member_ids = []
    for relation in relations:
        member_ids.append(relation.member.id)

    sub_relations = promotion_models.RedEnvelopeParticipences.objects.filter(
        red_envelope_rule_id=red_envelope_rule_id,
        introduced_by__in=member_ids,
        is_new=True
    )
    sub_member_ids = []
    for sub_relation in sub_relations:
        sub_member_ids.append(sub_relation.member_id)

    #获取关注关系l
    member_follow_relation = MemberFollowRelation.objects.filter(member_id__in=sub_member_ids)

    #只保存新会员的最后一条记录l
    member_id2follower_member_id ={}
    for member in member_follow_relation:
        member_id2follower_member_id[member.member_id] = member.follower_member_id

    for relation in relations:
        count = 0
        for sub_relation in sub_relations:
            if sub_relation.member.is_subscribed \
                    and sub_relation.is_new \
                    and relation.red_envelope_relation_id == sub_relation.red_envelope_relation_id \
                    and sub_relation.introduced_by == member_id2follower_member_id[sub_relation.member_id]:
                count += 1
        relation.introduce_new_member = count
        relation.save()

########################################################################
# get_red_members_filter_params: 获取过滤参数
########################################################################
class RedEnvelopeParticipancesFilter(resource.Resource):
    app = "apps/red_envelope"
    resource = "red_members_filter_params"

    @login_required
    def api_get(request):
        webapp_id = request.user_profile.webapp_id
        coupon_status = [{
            "id": 0,
            "name": u'未使用'
        },{
            "id": 1,
            "name": u'已使用'
        }]

        grades = []
        for grade in MemberGrade.get_all_grades_list(webapp_id):
            grades.append({
                "id": grade.id,
                "name": grade.name
            })

        response = create_response(200)
        response.data = {
            'coupon_status': coupon_status,
            'grades': grades
        }
        return response.get_response()

class redParticipances_Export(resource.Resource):
    '''
	批量导出
	'''
    app = 'apps/red_envelope'
    resource = 'red_participances_export'

    @login_required
    def api_get(request):
        """
        分析导出
        """
        export_id = int(request.GET.get('id'))
        download_excel_file_name = u'红包分析详情.xls'
        excel_file_name = 'red_details_'+datetime.now().strftime('%H_%M_%S')+'.xls'
        dir_path_suffix = '%d_%s' % (request.user.id, date.today())
        dir_path = os.path.join(settings.UPLOAD_DIR, dir_path_suffix)

        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        export_file_path = os.path.join(dir_path,excel_file_name)
        #Excel Process Part
        try:
            import xlwt
            relations = RedEnvelopeParticipances.get_datas(request)
            fields_pure = []
            export_data = []

            #from sample to get fields4excel_file
            fields_pure.append(u'编号')
            fields_pure.append(u'下单会员')
            fields_pure.append(u'会员状态')
            fields_pure.append(u'引入领取人数')
            fields_pure.append(u'引入使用人数')
            fields_pure.append(u'引入新关注')
            fields_pure.append(u'引入消费额')
            fields_pure.append(u'领取时间')
            fields_pure.append(u'使用状态')

            #processing data
            num = 0
            for relation in relations:
                export_record = []
                num = num+1
                name = relation["name"]
                grade_name = relation["grade"]
                introduce_received_number_count = relation["introduce_received_number_count"]
                introduce_used_number_count = relation["introduce_used_number_count"]
                introduce_new_member_count = relation["introduce_new_member_count"]
                introduce_sales_number = relation["introduce_sales_number"]
                created_at = relation["created_at"]
                status = '已使用' if relation["coupon_status"] == 1 else '未使用'
                # don't change the order
                export_record.append(num)
                export_record.append(name)
                export_record.append(grade_name)
                export_record.append(introduce_received_number_count)
                export_record.append(introduce_used_number_count)
                export_record.append(introduce_new_member_count)
                export_record.append(introduce_sales_number)
                export_record.append(created_at)
                export_record.append(status)
                export_data.append(export_record)

            #workbook/sheet
            wb = xlwt.Workbook(encoding='utf-8')
            ws = wb.add_sheet('id%s'%export_id)
            header_style = xlwt.XFStyle()

            ##write fields
            row = col = 0
            for h in fields_pure:
                ws.write(row,col,h)
                col += 1

            ##write data
            if export_data:
                row = 1
                lens = len(export_data[0])
                for record in export_data:
                    row_l = []
                    for col in range(lens):
                        record_col= record[col]
                        if type(record_col)==list:
                            row_l.append(len(record_col))
                            for n in range(len(record_col)):
                                data = record_col[n]
                                ws.write(row+n,col,data)
                        else:
                            ws.write(row,col,record[col])
                    if row_l:
                        row = row + max(row_l)
                    else:
                        row += 1
                try:
                    wb.save(export_file_path)
                except Exception, e:
                    print 'EXPORT EXCEL FILE SAVE ERROR'
                    print e
                    print '/static/upload/%s/%s'%(dir_path_suffix,excel_file_name)
            else:
                ws.write(1,0,'')
                wb.save(export_file_path)
            response = create_response(200)
            response.data = {'download_path':'/static/upload/%s/%s'%(dir_path_suffix,excel_file_name),'filename':download_excel_file_name,'code':200}
        except Exception, e:
            print e
            response = create_response(500)

        return response.get_response()