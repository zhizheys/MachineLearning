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
    print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    request.encoding = 'utf-8'
    result=None

    try:

        if 'sender' in request.POST:
            sender = request.POST['sender']

        if 'subject' in request.POST:
            subject = request.POST['subject']

        if 'fileName' in request.POST:
            fileName = request.POST['fileName']


        predictLabel, accuracy = pd.getPredictInfo(sender,subject,fileName)
        accuracy = '%.5f'%accuracy

        result = {"apiCode":1,"message":'',"apiResult":"success","deliveryId": predictLabel, "accuracy": accuracy}

    except Exception:
        result = {"apiCode":0,"message":Exception,"apiResult": "error", "deliveryId": '', "accuracy": ''}

    # json返回为中文
    return HttpResponse(json.dumps(result, cls=jsonHelper.NpEncoder), content_type="application/json,charset=utf-8")