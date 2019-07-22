# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
import json
from . import predictByKerasMappingDeliveryId as pd

# 表单
def search_info(request):
    return render_to_response('searchinfo.html')


# 接收请求数据
def search(request):

    request.encoding = 'utf-8'
    if 'sender' in request.GET:
        sender = request.GET['sender']

    if 'subject' in request.GET:
        subject = request.GET['subject']

    if 'fileName' in request.GET:
        fileName = request.GET['fileName']


    predictLabel, accuracy = pd.getPredictInfo(sender,subject,fileName)

    result = {"apiResult":"success","deliveryId": predictLabel, "accuracy": str(accuracy)}
    # json返回为中文
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")