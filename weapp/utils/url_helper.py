# -*- coding: utf-8 -*-

__author__ = 'chuter'

def get_path_digest(path):
	if path is None:
		return None
	return md5.new(path).hexdigest()

def add_query_part_to_request_url(url, key, value):
	if url is None or len(url) == 0:
		return '/'

	if url.find('?') >= 0:
		return "{}&{}={}".format(url, key, value)
	else:
		if url.endswith('/'):
			return "?{}={}".format(key, value)	
		else:
			return "/?{}={}".format(key, value)	

def remove_querystr_filed_from_request_url(request, remove_filed):
	if type(request) == str:
		orig_full_path = request
	else:
		try:
			orig_full_path = request.get_full_path()
		except:
			orig_full_path = request
		

	path_and_query = orig_full_path.split('?')
	if len(path_and_query) == 1:
		return orig_full_path

	path = path_and_query[0]
	query = path_and_query[1]
	query_parts = query.split('&')
	if len(query_parts) == 1:
		if query_parts[0].startswith(remove_filed):
			return path
		else:
			return orig_full_path
	else:
		remain_query_parts = []
		for query_part in query_parts:
			if query_part.startswith(remove_filed+'='):
				continue
			remain_query_parts.append(query_part)

		if len(remain_query_parts) > 0:
			return "{}?{}".format(path, '&'.join(remain_query_parts))
		else:
			return path

import urllib
def complete_get_request_url(protocol, domain, url_path, param_dict={}):
	query_str_parts = []
	for key, value in param_dict.items():
		query_str_part = "{}={}".format(key, urllib.quote(value))
		query_str_parts.append(query_str_part)

	query_str = '&'.join(query_str_parts)

	if not url_path.startswith('/'):
		url_path = '/' + url_path

	if len(query_str) > 0:
		return "{}://{}{}?{}".format(protocol, domain, url_path, query_str)
	else:
		return "{}://{}{}".format(protocol, domain, url_path)

#add by bert
def remove_querystr_filed_from_request_path(orig_full_path, remove_filed):

	path_and_query = orig_full_path.split('?')
	if len(path_and_query) == 1:
		return orig_full_path

	path = path_and_query[0]
	query = path_and_query[1]
	query_parts = query.split('&')
	if len(query_parts) == 1:
		if query_parts[0].startswith(remove_filed):
			return path
		else:
			return orig_full_path
	else:
		remain_query_parts = []
		for query_part in query_parts:
			if query_part.startswith(remove_filed+'='):
				continue
			remain_query_parts.append(query_part)

		if len(remain_query_parts) > 0:
			return "{}?{}".format(path, '&'.join(remain_query_parts))
		else:
			return path

from urlparse import urlparse
def get_market_tool_name_from(path):
	query_str = urlparse(path).query
	name = None
	if 'module=market_tool:' in query_str:
		query_list = query_str.split('&')
		for query in query_list:
			if 'module=market_tool:' in query:
				split_list = query.split(':')
				name = split_list[1]
				break
		return name
	else:
		return None