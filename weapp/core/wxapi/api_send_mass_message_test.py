# -*- coding: utf-8 -*-

"""
用于测试与微信api的交互

验证系统中提供的api接口中访问对应微信api接口
时地址是否正确，参数是否正确
"""

__author__ = 'chuter'


import unittest
import json

if __name__ == '__main__':
	import sys
	sys.path.insert(0, '../../')
	sys.path.insert(0, '../')

from test import test_env_with_db as test_env
test_env.init()

import api_settings
import weixin_api
import weixin_error_codes as errorcodes

from weixin.user.models import WeixinMpUser, WeixinMpUserAccessToken
from new_weixin_api import *
from custom_message import TextCustomMessage
from util import *
#from custom_message import TextCustomMessage, build_custom_message_json_str

fake_response_json_str = '{"errcode":0, "errmsg":""}'


class SendMaxMsgApiTestCase(unittest.TestCase):
	dummy_access_token_str  = 'ZTbOOqwf0qYtrKkDmDBLLpbfCY-04jYfQXv1rN3wu0M0zEMcnrX06zObAX_--jqk'
	dummy_openid = 'ommVKt1I6wUuB0mM3SNjPZfd4mOw'
	dummy_msg = TextCustomMessage(u'测试')
	def setUp(self):
		WeixinMpUserAccessToken.objects.all().delete()
		self.weixin_http_client = WeixinHttpClient()
		self.api = WeixinApi(self._create_dummy_certified_mpuser_access_token(), self.weixin_http_client)

	def tearDown(self):
		WeixinMpUserAccessToken.objects.all().delete()

	def test_userinfo_get(self):
		#weixin_api.head_img_saver = dummy_head_img_saver

		#result = self.api.send_custom_msg(self.dummy_openid, self.dummy_msg)
		news_media_id = '3g1jgm7n8-lUFM_MUiVK0UuZ5zYhOGs33_QAZMGX5fQbAn3IMhDdfFA6tELi-K6b'
		mesage = NewsMessage([self.dummy_openid], news_media_id)
		result = self.api.send_mass_message(mesage)
		print result
		# self.assertEqual(errcode, error_response.errcode)
	

	def _assert_url_contains(self, parts, url):
		for part in parts:
			self.assertTrue(url.find(part) >= 0)

	def _create_dummy_certified_mpuser_access_token(self):
		return WeixinMpUserAccessToken.objects.create(
			mpuser = self._create_dummy_mpuser(),
			app_id = '-',
			app_secret = '-',
			access_token = self.dummy_access_token_str,
			created_at = '2001-01-01 00:00:00',
			#is_certified = True,
			#is_service = True
			)

	def _create_dummy_mpuser(self):
		return WeixinMpUser.objects.create(
			owner = test_env.getTestUser(),
			username = 'dummy_user_name',
			password = 'dummy_password',
			is_certified = True,
			is_service = True
			)

if __name__ == '__main__':
	test_env.start_test_withdb()