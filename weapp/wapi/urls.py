# -*- coding: utf-8 -*-

import mall
import stats
import auth
import openapi
import member
import wzcard

import qrcode

import new_product

import views
from django.conf.urls import *

urlpatterns = patterns('',
	(r'^(.+)/(.+)/', views.api_wrapper),
)
