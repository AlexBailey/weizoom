# -*- coding: utf-8 -*-

CONFIGS = {}


def init_config(options):
	CONFIGS.update(options)


def get_config_for(task):
	return CONFIGS.get(task, {})


def register_task(name, tasks, config_dict=None):
	import sys
	registry = sys.modules['registry']
	tasks_type = type(tasks)
	if tasks_type == str:
		task_name = tasks
		task_func = registry.get_task(task_name)
		if not task_func:
			raise RuntimeError('Can not register task "%s", no task for "%s"' % (name, task_name))
		registry.register(name, {
			"original_name": task_name,
			"task_func": task_func,
			"config_dict": config_dict
		})
	elif tasks_type == list:
		task_funcs = []
		for task_name in tasks:
			task_func = registry.get_task(task_name)
			if not task_func:
				raise RuntimeError('Can not register task "%s", no task for "%s"' % (name, task_name))
			else:
				task_funcs.append({
					"original_name": task_name,
					"task_func": task_func
				})
		registry.register(name, task_funcs)


def run_task(name, config_dict=None):
	import runner
	runner.run_task([name], config_dict)

