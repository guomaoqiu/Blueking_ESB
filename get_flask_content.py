# -*- coding: utf-8 -*-
import json

from django import forms

from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs

class GetFlaskContent(Component):
    
    sys_name = configs.SYSTEM_NAME

    # Form处理参数校验
    class Form(BaseComponentForm):
        app_id = forms.CharField(label=u'业务ID', required=True)

        # clean方法返回的数据可通过组件的form_data属性获取
        def clean(self):
            data = self.cleaned_data
	    print data
            return {
                'app_id': data['app_id'],
            }

    # 组件处理入口
    def handle(self):
        # 获取Form clean处理后的数据
        data = self.form_data

        # 设置当前操作者
        data['operator'] = self.current_user.username

        # 请求系统接口
        response = self.outgoing.http_client.get(
            host= configs.host,
            path='/get_flask_content/',
            data=json.dumps(data),
        )

        # 对结果进行解析
        code = str(response['code'])
        if code == '0':
            result = {
                'result': True,
                'data': response['data'],
            }
        else:
            result = {
                'result': False,
                'message': result['extmsg']
            }

        # 设置组件返回结果，payload为组件实际返回结果
        self.response.payload = result
