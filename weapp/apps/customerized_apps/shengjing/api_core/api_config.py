# -*- coding: utf-8 -*-
__author__ = 'liupeiyu'

import datetime
import hashlib

class ShengjingAPIConfig(object):
	"""
	盛景接口的配置信息
	"""

	def __init__(self, session_Id=None):
		self.session_Id = session_Id


	# 认证相关接口的 Method
	method_who_am_I = "WhoAmI"

	# 获取学员的邀请函列表接口 的 Method
	method_get_invitation_list = 'GetInvitationList'

	# 提交在线预约信息接口 的 Method
	method_submit_booking = 'SubmitBooking'

	# 获取短信验证码（客户端调用本接口时，服务端进行验证码的生成、短信发送） 的 Method
	method_get_captcha = 'GetCaptcha'

	# 检验验证码 的 Method
	method_captcha_verify = 'CaptchaVerify'

	# 版本号
	version = '1.0'


	# 访问的应用ID
	# app_key
	# app_id = "88888888"
	app_id = "ESI0098732DX1WZ"	

	# app_key 令牌（初始令牌的规则见另外说明）
	app_key = "99999999"

	# 获取了SessionID后依据规定算法得到访问令牌Key；
	def get_app_key(self):
		if self.session_Id:
			self.__arithmetic_key_by_other()
		else:
			self.__arithmetic_key_by_who_am_i()

		return self.app_key


	def __day_difference(self):
		d1 = datetime.datetime(1970,1,1)
		d2 = datetime.datetime.now()
		return (d2-d1).days

	"""
	握手时（WhoAmI）,获取Key的算法为
		①获取1970.01.01 00:00:00到北京时间当前日期的“天数”，以 D 表示；
		②在AppID字符串之后缀上（追加）D （D转为字符串），以 S 表示；
		③取S字符串的32位MD5（x2）值，以M表示；
		④取M字符串的中间16位的大写得到的字符串，即为Key。
	"""
	def __arithmetic_key_by_who_am_i(self):
		# 1. 计算天数
		D = self.__day_difference()

		# 2. appID字符串追加
		S = '{}{}'.format(self.app_id, D)

		# 3. MD5
		M = hashlib.md5(S).hexdigest()

		# 4. 取中间16位的大写字符串
		self.app_key = M[8:24].upper()
		return self.app_key


	"""
	其它接口，获取Key的算法为：
		①从WhoAmI接口获取的SessionID转为数值，以 I 表示；
		②获取1970.01.01 00:00:00到北京时间当前日期的“天数”，以 D 表示；
		③将 I 和 D 算术相加，所得数值转为字符串,以 S1 表示；
		④在AppID字符串之后缀上（追加）S1，以 S 表示；
		⑤取S字符串的32位MD5（x2）值，以M表示；
		⑥取M字符串的中间16位的大写得到的字符串，即为Key。
	"""
	def __arithmetic_key_by_other(self):
		# 2. 计算天数
		D = self.__day_difference()

		# 3. I 和 D 算术相加
		S1 = int(self.session_Id) + D

		# 4. appID字符串追加
		S = '{}{}'.format(self.app_id, S1)

		# 5. MD5
		M = hashlib.md5(S).hexdigest()

		# 6. 取中间16位的大写字符串
		self.app_key = M[8:24].upper()
		return self.app_key


	"""
	返回的错误编码
	"""
	CODE_SUCCESS = 0
	CODE_PERMISSION_DENIED = -1
	CODE_METHOD_ERROR = 2
	CODE_ERROR = 3
	CODE_PARAM_ERROR = 4
	CODE_SESSION_FAILURE = 9
	CODE_SESSION_NOT = 10
	CODE_SESSION_EXPIRES = 16
	CODE_SESSION_ERROR = 17

	CODES = {
		CODE_SUCCESS: "访问正常",
		CODE_PERMISSION_DENIED: "当前用户/访问没有权限或没有授权",
		CODE_METHOD_ERROR: "命令字错误",
		CODE_ERROR: "发生了未知的错误",
		CODE_PARAM_ERROR: "不可识别的参数",
		CODE_SESSION_FAILURE: "Session已过期或错误",
		CODE_SESSION_NOT: "当前用户没有签到码",
		CODE_SESSION_EXPIRES: "签到码已过期",
		CODE_SESSION_ERROR: "无效的签到码"
	}
