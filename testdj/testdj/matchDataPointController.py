# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from keras.models import  load_model
from . import predictMappingDataPoint as pd
from . import jsonHelper
import traceback
import os

rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fileRootPath = rootPath + '/testdj'
model = load_model(fileRootPath + '/matchDataPoint/model_keras_matchDataPoint.h5')


# 接收请求数据
@csrf_exempt
def getMatchInfo(request):
    request.encoding = 'utf-8'
    result=None

    try:
        print('----------body', request.body)
        bodyInfo = json.loads(request.body)
        dataContent=bodyInfo['fileName']

        print('----------body content', dataContent)

        predictItem = pd.PredictMap()
        predictLabel, accuracy = predictItem.getPredictInfo(model,dataContent)
        accuracy = '%.5f'%accuracy

        if predictLabel != None:
            predictLabel = str(predictLabel).upper()

        result = {"apiCode":1,"message":'',"apiResult":"success","dataPointName": predictLabel, "accuracy": accuracy}

    except (Exception) as e:
        print(traceback.format_exc())
        result = {"apiCode":0,"message":str(e),"apiResult": "error", "dataPointName": '', "accuracy": ''}

    # json返回为中文
    return HttpResponse(json.dumps(result, cls=jsonHelper.NpEncoder), content_type="application/json,charset=utf-8")


