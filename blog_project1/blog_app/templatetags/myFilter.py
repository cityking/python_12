# coding: utf-8
from django import template
register = template.Library()


def month_upper(value):
	return ['一','二','三','四','五','六','七','八','九','十','十一','十二'][int(value)-1]

register.filter('month_upper', month_upper)
