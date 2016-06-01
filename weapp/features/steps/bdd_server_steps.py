# coding:utf8
# bdd server相关的step

import base64
import decimal
import json
import os
from cgi import parse_qs
from datetime import datetime, date
from wsgiref.simple_server import WSGIRequestHandler, make_server
from wsgiref.util import setup_testing_defaults
from features import environment

from behave import *

BDD_SERVER2PORT = {
	'weapp': 8170,
	'weizoom_card': 8171,
	'apiserver': 8172
}


def _default(obj):
	if isinstance(obj, datetime):
		return obj.strftime('%Y-%m-%d %H:%M:%S')
	elif isinstance(obj, date):
		return obj.strftime('%Y-%m-%d')
	elif isinstance(obj, decimal.Decimal):
		return str(obj)
	else:
		return ''


def _set_context_attrs(context, context_kvs):
	for k, v in context_kvs.items():
		if v:
			setattr(context, k, v)


def _git_shell(git_command):
	try:
		return os.popen(git_command).read().strip()
	except:
		return None


try:
	git_dir = os.path.abspath(_git_shell('git rev-parse --git-dir'))
	project_dir = os.path.dirname(git_dir)
	self_name = project_dir.split(os.sep)[-1]
except BaseException as e:
	print(e)
	self_name = "You should install Git!!"
	print(self_name)

os.system("title {}_bdd_server".format(self_name))


class BDDRequestHandler(WSGIRequestHandler):
	def handle(self):
		WSGIRequestHandler.handle(self)

		if 'shutdown=1' in self.raw_requestline:
			import threading
			threading.Thread(target=self.shutdown_server()).start()

	def shutdown_server(self):
		server = self.server

		def inner_shutdown():
			server.shutdown()
			server.server_close()
			print('[bdd server] server is shutdown now!')

		return inner_shutdown


@given(u'启动BDD Server')
def step_impl(context):
	# A relatively simple WSGI application. It's going to print(out the)
	# environment dictionary after being updated by setup_testing_defaults
	def simple_app(environ, start_response):
		setup_testing_defaults(environ)

		status = '200 OK'
		headers = [('Content-type', 'text/plain')]

		start_response(status, headers)

		# the environment variable CONTENT_LENGTH may be empty or missing
		try:
			request_body_size = int(environ.get('CONTENT_LENGTH', 0))
		except (ValueError):
			request_body_size = 0

		# When the method is POST the query string will be sent
		# in the HTTP request body which is passed by the WSGI server
		# in the file like wsgi.input environment variable.
		request_body = environ['wsgi.input'].read(request_body_size)
		post = parse_qs(request_body)
		step_data = json.loads(post['data'][0])
		step = step_data['step'].strip()

		# 0:成功，1：业务失败，2：异常
		result = 0
		if step == '__reset__':
			print('*********************** run step **********************')
			print(u'Reset bdd environment...')
			environment.after_scenario(context, context.scenario)
			environment.before_scenario(context, context.scenario)

			resp = {
				'result': result
			}

			return base64.b64encode(json.dumps(resp))
		else:
			_set_context_attrs(context, json.loads(step_data['context_attrs']))

			if step_data['context_text']:
				step_content = step_data['context_text']
			else:
				step_content = step_data['context_table']
			step = u'%s\n"""\n%s\n"""' % (step_data['step'], step_content)
			print('*********************** run step **********************')
			print(step)

			context_attrs = {}
			traceback = ''

			try:
				context.execute_steps(step)
			except AssertionError:
				result = 1
				from core.exceptionutil import full_stack
				print('*********************** failure **********************')
				traceback = full_stack()
				print(traceback.decode('utf-8'))

			except:
				result = 2
				from core.exceptionutil import full_stack
				print('*********************** exception **********************')
				traceback = full_stack()
				print(traceback.decode('utf-8'))

			else:
				result = 0
				context_attrs = context._stack[0]

			resp = {
				'result': result,
				'traceback': traceback,
				'context_attrs': context_attrs
			}
			return base64.b64encode(json.dumps(resp, default=_default))

	port = BDD_SERVER2PORT.get(self_name, 0)
	assert port, "{} is not valid name.You can't change the git repository name!".format(self_name)

	httpd = make_server('', 8170, simple_app, handler_class=BDDRequestHandler)
	print("[{} bdd server] Serving on port {}...".format(self_name, port))
	httpd.serve_forever()
