import json
import random

from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.profile import region_provider
from aliyunsdkcore.request import CommonRequest
from django.core.cache import cache
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import User
from user.views import writeBrowse, getLocalTime

ACCESS_KEY_ID = "LTAI4Fz1fzYDUTi8kbTXsze4"
ACCESS_KEY_SECRET = "6CKrTVHcuqZ4PRNX5fdVZs9OFhe27V"

# 注意：不要更改
REGION = "cn-hangzhou"
PRODUCT_NAME = "Dysmsapi"
DOMAIN = "dysmsapi.aliyuncs.com"


@csrf_exempt
def sendSMS(request):
    """
    同一个签名，对同一个手机号的发送频率
        1分钟内短信发送条数不超过：1
        1小时内短信发送条数不超过：5
        1个自然日内短信发送条数不超过：10
    :param request: 用户请求
    :param phone: 用户的手机号码
    :return: 请求结果
    """
    phone = request.POST.get('phone')
    login_user = User.objects.all().filter(u_phone=phone)
    exist = login_user.exists()
    if exist is False:
        return JsonResponse({"code": '0', "data": '您的手机未注册'})
    client = AcsClient(ACCESS_KEY_ID, ACCESS_KEY_SECRET, REGION)
    region_provider.add_endpoint(PRODUCT_NAME, REGION, DOMAIN)
    
    request = CommonRequest()
    
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https')  # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')
    
    # 生成四位数字随机数
    list_num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
    validate_out = random.sample(list_num, 4)
    validate_res = str(validate_out[0]) + str(validate_out[1]) + str(validate_out[2]) + str(validate_out[3])
    # print(validate_res)
    
    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phone)
    request.add_query_param('SignName', "fym音乐推荐系统")
    request.add_query_param('TemplateCode', "SMS_189520300")
    request.add_query_param('TemplateParam', {'code': validate_res})
    
    response = client.do_action_with_exception(request)
    # python2:  print(response)
    # 格式转换为json
    result = str(response, encoding='utf-8')
    response_json = json.loads(result)
    
    if response_json['Code'] == "OK":
        exist = cache.get(phone, 'NOT_EXISTS')
        # 以 手机-验证码 的方式缓存5分钟
        if exist == 'NOT_EXISTS':
            cache.add(phone, validate_res, 60 * 5)
        return JsonResponse({"code": 200, "data": '验证码已发送到您的手机'})
    else:
        return JsonResponse({'code': response_json['Code'], 'data': response_json['Message']})


@csrf_exempt
def validSMS(request):
    phone = request.POST.get('phone')
    sms_code = request.POST.get('sms')
    login_user = User.objects.all().filter(u_phone=phone)
    user_exist = login_user.exists()
    if user_exist is False:
        return JsonResponse({"code": '0', "data": '您的手机未注册'})
    login_user = login_user[0]
    sms_exist = cache.get(phone, 'NOT_EXISTS')
    if sms_exist == 'NOT_EXISTS':
        return JsonResponse({"code": '0', "data": '请再次发送验证码'})
    elif sms_exist == sms_code:
        # 将用户信息写入session
        request.session["username"] = login_user.u_name
        request.session["password"] = login_user.u_password
        request.session["sings"] = ''
        request.session["songs"] = ''
        # 信息进行记录
        writeBrowse(user_name=login_user.u_name, user_click_time=getLocalTime(), desc="登录系统")
        # todo
        return JsonResponse({"code": 200, "data": {
            "username": login_user.u_name,
            "songs": '',
            "sings": ''
        }})
    else:
        return JsonResponse({"code": '0', "data": '验证码不匹配'})
