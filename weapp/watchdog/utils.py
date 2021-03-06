#coding:utf8
"""@package weapp.watchdog.utils

Watchdog接口
"""

# 异步service

from django.conf import settings
import sys
import json
#from core.exceptionutil import full_stack

#from .models import Message, WeappMessage
from .tasks import send_watchdog
from .tasks import _watchdog
#from weapp.settings import weapp_settings.TASKQUEUE_ENABLED
import weapp.settings as weapp_settings
from .models import WATCHDOG_ALERT, WATCHDOG_DEBUG,WATCHDOG_EMERGENCY,WATCHDOG_ERROR,WATCHDOG_FATAL,WATCHDOG_INFO,WATCHDOG_NOTICE,WATCHDOG_WARNING
import logging

from eaglet.core import watchdog

__author__ = 'victor'

def message_json(user_id, message, type):
	message_dict = {}
	message_dict["user_id"] = user_id
	message_dict["message"] = message
	message_dict["service_name"] = settings.SERVICE_NAME
	message_dict["type"] = type
	return json.dumps(message_dict)

def watchdog_debug(message, type='WEB', user_id='0', db_name='default'):
	"""
	用异步方式发watchdog

	异步方式调用 weapp.services.send_watchdog_service.send_watchdog()
	"""
	watchdog.debug(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# result = None
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_DEBUG >= settings.WATCH_DOG_LEVEL:
	# 		result = send_watchdog.delay(type, message, WATCHDOG_DEBUG, user_id, db_name)
	# else:
	# 	if WATCHDOG_DEBUG >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_DEBUG, user_id, db_name)
	#
	# # logging.DEBUG(message_json(user_id,message, type))
	# return result


def watchdog_info(message, type='WEB', user_id='0', db_name='default'):
	"""
	用异步方式发watchdog

	异步方式调用 weapp.services.send_watchdog_service.send_watchdog()
	"""
	watchdog.info(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# result = None
	# #print("weapp_settings.TASKQUEUE_ENABLED: {}".format(weapp_settings.TASKQUEUE_ENABLED))
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_INFO >= settings.WATCH_DOG_LEVEL:
	# 		result = send_watchdog.delay(type, message, WATCHDOG_INFO, user_id, db_name)
	# else:
	# 	if WATCHDOG_INFO >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_INFO, user_id, db_name)
	# # logging.info(message_json(user_id, message, type))
	# return result


def watchdog_notice(message, type='WEB', user_id='0', db_name='default'):
	"""
	用异步方式发watchdog

	异步方式调用 weapp.services.send_watchdog_service.send_watchdog()
	"""
	watchdog.warning(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# result = None
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_NOTICE>= settings.WATCH_DOG_LEVEL:
	# 		result = send_watchdog.delay(type, message, WATCHDOG_NOTICE, user_id, db_name)
	# else:
	# 	if WATCHDOG_NOTICE >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_NOTICE, user_id, db_name)
	# # logging.info(message_json(user_id, message, type))
	# return result


def watchdog_warning(message, type='WEB', user_id='0', db_name='default'):
	"""
	用异步方式发watchdog

	异步方式调用 weapp.services.send_watchdog_service.send_watchdog()
	"""
	watchdog.warning(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# result = None
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_WARNING>= settings.WATCH_DOG_LEVEL:
	# 		result = send_watchdog.delay(type, message, WATCHDOG_WARNING, user_id, db_name)
	# else:
	# 	if WATCHDOG_NOTICE >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_NOTICE, user_id, db_name)
	# # logging.warning(message_json(user_id, message, type))
	# return result


def watchdog_error(message, type='WEB', user_id='0', noraise=False, db_name='default'):
	result = None
	# logging.error(message_json(user_id, message, type))
	watchdog.error(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_ERROR >= settings.WATCH_DOG_LEVEL:
	# 		result = send_watchdog.delay(type, message, WATCHDOG_ERROR, user_id, db_name)
	# 	if settings.DEBUG and (not noraise):
	# 		exception_type, value, tb = sys.exc_info()
	# 		if exception_type:
	# 			raise exception_type, exception_type(value), sys.exc_info()[2]
	# else:
	# 	if WATCHDOG_ERROR >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_ERROR, user_id, db_name)
	# 	if settings.DEBUG and (not noraise):
	# 		exception_type, value, tb = sys.exc_info()
	# 		if exception_type:
	# 			raise exception_type, exception_type(value), sys.exc_info()[2]
	#
	# return result


def watchdog_fatal(message, type='WEB', user_id='0', noraise=False, db_name='default'):
	result = None
	# logging.error(message_json(user_id, message, type))
	watchdog.error(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_FATAL >= settings.WATCH_DOG_LEVEL:
	# 		send_watchdog.delay(type, message, WATCHDOG_FATAL, user_id, db_name)
	# 	if settings.DEBUG and (not noraise):
	# 		exception_type, value, tb = sys.exc_info()
	# 		if exception_type:
	# 			raise exception_type, exception_type(value), sys.exc_info()[2]
	# else:
	# 	if WATCHDOG_FATAL >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_FATAL, user_id, db_name)
	# 	if settings.DEBUG and (not noraise):
	# 		exception_type, value, tb = sys.exc_info()
	# 		if exception_type:
	# 			raise exception_type, exception_type(value), sys.exc_info()[2]
	# return result


def watchdog_alert(message, type='WEB', user_id='0', db_name='default'):
	# logging.critical(message_json(user_id, message, type))
	watchdog.alert(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# result = None
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_ALERT >= settings.WATCH_DOG_LEVEL:
	# 		send_watchdog.delay(type, message, WATCHDOG_ALERT, user_id, db_name)
	# else:
	# 	if WATCHDOG_ALERT >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_ALERT, user_id, db_name)
	# return result


def watchdog_js_analysis(message, type='JS_Analysis', user_id='0', db_name='default'):
	# logging.critical(message_json(user_id, message, type))
	watchdog.info(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# result = None
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_ALERT >= settings.WATCH_DOG_LEVEL:
	# 		send_watchdog.delay(type, message, WATCHDOG_INFO, user_id, db_name)
	# else:
	# 	if WATCHDOG_ALERT >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_INFO, user_id, db_name)
	# return result


def watchdog_emergency(message, type='WEB', user_id='0', db_name='default'):
	# logging.critical(message_json(user_id, message, type))
	watchdog.critical(message=message, log_type=type, user_id=user_id, server_name='weapp')
	# result = None
	# if weapp_settings.TASKQUEUE_ENABLED:
	# 	if WATCHDOG_EMERGENCY >= settings.WATCH_DOG_LEVEL:
	# 		send_watchdog.delay(type, message, WATCHDOG_EMERGENCY, user_id, db_name)
	# else:
	# 	if WATCHDOG_EMERGENCY >= settings.WATCH_DOG_LEVEL:
	# 		_watchdog(type, message, WATCHDOG_EMERGENCY, user_id, db_name)
	# return result
