

#根据前面预测的模型，对数据进行情感分析

import pickle
from sklearn.feature_extraction.text import CountVectorizer
import tensorflow as tf
from . import utilHelpe
import os

class PredictMap:
    global graph
    graph = tf.get_default_graph()

    def predictInfo(self,modelItem,fileInfo):

        rootPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        fileRootPath = rootPath + '/testdj'

        targetLabel = 'No found'
        #load 词向量模型
        fileVector = open( fileRootPath + '/vectorizer_matchDeliveryId_wordModel.pkl','rb')
        vectorizer = pickle.load(fileVector)
        fileVector.close()

        #load mapping delivery id model
        model = modelItem

        testStr=[fileInfo]
        loaded_vec = CountVectorizer(decode_error="replace", vocabulary=vectorizer)
        x_testStr = loaded_vec.transform(testStr)

        print(model.summary())

        with graph.as_default():
            prediction=model.predict(x_testStr)
            prediction_class=model.predict_classes(x_testStr)
            maxSimilar = prediction[0].max()

        #load 词向量模型
        labelFilePath = open(fileRootPath + '/vectorizer_matchDeliveryId_labelModel.pkl','rb')
        labelDic = pickle.load(labelFilePath)
        labelFilePath.close()


        loaded_label_vec = CountVectorizer(decode_error="replace", vocabulary=labelDic)
        loaded_label_vec.fit(labelDic)

        #get dic info
        keys = loaded_label_vec.vocabulary.keys()
        for k in keys:
            if loaded_label_vec.vocabulary[k] == prediction_class[0]:
                targetLabel = k
                break

        return  targetLabel,maxSimilar

    def createContentInfo(self,strArray):
        contentInfo=''

        strUtil = utilHelpe.MyStringUtil()

        if strArray != None and len(strArray) > 0:
            for j in strArray:
                j = strUtil.removeSpecialCharacter(j)
                j = strUtil.removeStopWord(j)
                contentInfo = contentInfo + ' ' + j

        return contentInfo.strip()


    def getPredictInfo(self,modelItem,sender,subject,fileName):

        contentArray = [sender,subject,fileName]
        fileInfo = self.createContentInfo(contentArray)
        predictLabel,accuracy =self.predictInfo(modelItem,fileInfo)
        print('predict delivery id is: ',predictLabel)
        print('predict accuracy is: ', accuracy)

        return predictLabel,accuracy
