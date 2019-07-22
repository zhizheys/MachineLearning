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
    # request.encoding = 'utf-8'
    # if 'q' in request.GET:
    #     message = '你搜索的内容为: ' + request.GET['q']
    # else:
    #     message = '你提交了空表单'
    # return HttpResponse(message)

    sender ='multi.client.aibbny@bnymellon.com'
    subject = 'Invesco STIC EUR Liquidity daily nav/factor/yield information - 03/25/2019'
    fileName = 'INVESCO _Invesco STIC Global Series EUR_PRICESHEET_II_20190325.xls'


    predictLabel, accuracy = pd.getPredictInfo(sender,subject,fileName)

    result = {"apiResult":"success","deliveryId": predictLabel, "accuracy": str(accuracy)}
    # json返回为中文
    return HttpResponse(json.dumps(result, ensure_ascii=False), content_type="application/json,charset=utf-8")