# -*- coding: utf-8 -*-

MALL_CARD_FIRST_NAV = 'card'
MALL_CARD_MANAGER_NAV = 'manager'
MALL_CARD_CENSUS_NAV = 'census'
MALL_CARD_PERMISSIONS_NAV='permissions'

MALL_CARD_TOTAL_CENSUS_NAV = 'total_cencus'
MALL_CARD_BY_CARD_NAV = 'by_card_cencus'
MALL_CARD_BY_CHANNEL_NAV = 'by_channel_cencus'

MONEY_CARD_MANAGER_CREATE_NAV = 'cards'
MONEY_CARD_MANAGER_RECHARGE_NAV = 'recharge'

CARD_NAV = {
    'section': u'微众卡',
    'navs': [
        {
            'name': MALL_CARD_MANAGER_NAV,
            'title': u'制卡管理',
            'url': '/card/cards/get/',
            'third_navs':[{
                'name': MONEY_CARD_MANAGER_CREATE_NAV,
                'title': u'制卡',
                'url': '/card/cards/get/',
            }, {
                'name': MONEY_CARD_MANAGER_RECHARGE_NAV,
                'title': u'卡充值',
                'url': '/card/recharge/get/',
            }]
        },
        {
            'name': MALL_CARD_CENSUS_NAV,
            'title': u'数据统计',
            'url': '/card/overview/get/',
            'third_navs':[
                {
                    'name': MALL_CARD_TOTAL_CENSUS_NAV,
                    'title': u'整体概览',
                    'url': '/card/overview/get/',
                },
                {
                    'name': MALL_CARD_BY_CARD_NAV,
                    'title': u'按卡号统计',
                    'url': '/card/cards_num_census/get/',
                },
                {
                    'name': MALL_CARD_BY_CHANNEL_NAV,
                    'title': u'按渠道统计',
                    'url': '/card/cards_channel_census/get/',
                },
            ]
        },
        {
            'name': MALL_CARD_PERMISSIONS_NAV,
            'title': u'用户权限管理',
            'url': '/card/cardmanager/get/',
            'uservalue': True,
        },
    ]
}


def get_card_second_navs(request):
    """
    获取"微众卡管理"部分的下级导航
    """
    if request.user.username == 'manager':
        second_navs = [CARD_NAV]
    else:
        second_navs = [CARD_NAV]
    return second_navs
