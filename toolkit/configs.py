# -*- coding: utf-8 -*-
from esb.utils import SmartHost
# 系统名的小写形式要与系统包名保持一致 SYSTEM_NAME = 'MY_APP'
SYSTEM_NAME="MY_APP"

host = SmartHost(
	# 这里的地址在基础环境中需要配置host指向FlaskApi地址
	# 确保handle函数中的请求地址正确
    host_prod='myapp.sctux.com:5000',  
)
