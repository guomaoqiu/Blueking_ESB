# -*- coding: utf-8 -*-
import json
from django import forms
from common.forms import BaseComponentForm
from components.component import Component
from .toolkit import configs

class GetFlaskContent(Component):
    """
    @api {get} /api/c/compapi/my_app/get_flask_content/
    @apiName get_flask_content
    @apiGroup API-MYAPP
    @apiVersion 1.0.0
    @apiDescription 获取Flask_ApiContent
    @apiParam {string} app_code 应用标识，即应用 ID
    @apiParam {string} app_secret 应用私密 key，可以通过 蓝鲸智云开发者中心 -> 点击应用ID -> 基本信息 获取
    @apiParam {string} bk_token 当前用户登录态，bk_token与username必须一个有效，bk_token可以通过Cookie获取
    @apiParam {string} app_id 业务ID

    @apiParamExample {json} Request-Example:
        {
            "app_code": "esb_test",
            "app_secret": "xxx",
            "bk_token": "xxx",
            "app_id": "xxx",
        }
    @apiSuccessExample {json} Success-Response
        HTTP/1.1 200 OK
            {
              "code": "00",
              "content": "xxxxx",
              "result": true,
              "request_id": "xxxx",
              "message": "调用第三方接口成功.",
              "data": "esb_test"
            }
    """
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
