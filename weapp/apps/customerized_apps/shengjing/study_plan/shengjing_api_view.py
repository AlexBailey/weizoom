# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

from watchdog.utils import watchdog_info, watchdog_error, watchdog_fatal
from core.exceptionutil import unicode_full_stack

#===============================================================================
# get_session_id : 获取session_id
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_session_id import ShengjingSessionID
def get_session_id():
	session = ShengjingSessionID()
	session_id = session.get_session_id_data()
	return session_id


#===============================================================================
# get_invitation_list : 获取get_invitation_list
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_get_invitation_list import ShengjingGetInvitationList
def get_invitation_list(session_id, phone):
	invitation = ShengjingGetInvitationList(session_id, phone)
	data = invitation.get_invitation_list()
	return data


#===============================================================================
# get_invitation_list : 获取get_invitation_list
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_get_captcha import ShengjingGetCaptcha
def get_captcha(session_id, phone):
	capthca = ShengjingGetCaptcha(session_id, phone)
	data = capthca.get_captcha_data()
	return data


#===============================================================================
# get_invitation_list : 获取get_invitation_list
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_captcha_verify import ShengjingCaptchaVerify
def get_captcha_verify(session_id, phone, capthca):
	verify = ShengjingCaptchaVerify(session_id, phone, capthca)
	data = verify.get_captcha_verify_data()
	return data


#===============================================================================
# get_learn_plan_list : 获取get_learn_plan_list
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_get_learn_plan import ShengjingGetLearnPlan
def get_learn_plan_list(session_id, phone, company_name):
	verify = ShengjingGetLearnPlan(session_id, phone, company_name)
	data = verify.get_learn_plan_list()
	return data


#===============================================================================
# get_confirm_learn_plan : 学习计划确认
#===============================================================================
from apps.customerized_apps.shengjing.api_core.shengjing_confirm_learn_plan import ShengjingConfirmLearnPlan
def get_confirm_learn_plan(session_id, phone, learn_id, webapp_user_id):
	verify = ShengjingConfirmLearnPlan(session_id, phone, learn_id, webapp_user_id)
	data = verify.get_confirm_learn_plan()
	return data


#===============================================================================
# mobile_get_invitation_list : 获取二维码列表页面
#===============================================================================
def mobile_get_invitation_list(phone):
	session_id = get_session_id()
	if session_id:
		return get_invitation_list(session_id, phone)

	return None


#===============================================================================
# mobile_get_captcha : 获取 获取验证码
#===============================================================================
def mobile_get_captcha(phone):
	session_id = get_session_id()
	if session_id:
		return get_captcha(session_id, phone)

	return None


#===============================================================================
# mobile_get_captcha_verify : 获取 检验验证码结果
#===============================================================================
def mobile_get_captcha_verify(phone, captcha):
	session_id = get_session_id()
	if session_id:
		return get_captcha_verify(session_id, phone, captcha)

	return None


#===============================================================================
# mobile_get_learn_plan_list : 获取 学习计划
#===============================================================================
def mobile_get_learn_plan_list(phone, company_name):
	session_id = get_session_id()
	if session_id:
		return get_learn_plan_list(session_id, phone, company_name)

	return None


#===============================================================================
# mobile_get_confirm_learn_plan : 学习计划确认
#===============================================================================
def mobile_get_confirm_learn_plan(phone, learn_id, webapp_user_id):
	session_id = get_session_id()
	if session_id:
		return get_confirm_learn_plan(session_id, phone, learn_id, webapp_user_id)

	return None

