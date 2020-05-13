# _*_ coding: utf-8 _*_
__author__ = 'Yang Haibo'
__date__ = '2020/5/13 10:08'

from django.forms.widgets import Input
from django.template import loader
from django.utils.safestring import mark_safe


class TelInput(Input):
    """
    # 自定义widgets在手机号后加上发送验证码和相应js代码
    """
    input_type = 'text'
    template_name = "widgets/tel.html"

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        template = loader.get_template(self.template_name).render(context)
        return mark_safe(template)