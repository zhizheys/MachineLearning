# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from . import predictByKerasMappingDeliveryId as pd
from . import jsonHelper
import os

# 表单
def search_info(request):
    return render_to_response('searchinfo.html')


# 接收请求数据
@csrf_exempt
def search(request):

    request.encoding = 'utf-8'
    result=None

    try:
        print('----------body', request.body)
        bodyInfo = json.loads(request.body)
        sender = bodyInfo['sender']
        subject = bodyInfo['subject']
        fileName = bodyInfo['fileName']
        print('----------post',request.POST)
        # sender =request.POST.get('sender','')
        # subject = request.POST.get('subject','')
        # fileName = request.POST.get('fileName','')
        # #name = request.POST.get('name', '')  # 发布会名称

        print('----------3333333', sender,subject,fileName)

        predictLabel, accuracy = pd.getPredictInfo(sender,subject,fileName)
        accuracy = '%.5f'%accuracy

        print('----------predict result ', predictLabel, accuracy)

        result = {"apiCode":1,"message":'',"apiResult":"success","deliveryId": predictLabel, "accuracy": accuracy}

    except (Exception) as e:
        result = {"apiCode":0,"message":e,"apiResult": "error", "deliveryId": '', "accuracy": ''}

    # json返回为中文
    return HttpResponse(json.dumps(result, cls=jsonHelper.NpEncoder), content_type="application/json,charset=utf-8")


