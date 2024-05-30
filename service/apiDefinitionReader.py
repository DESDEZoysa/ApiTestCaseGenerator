from model.constant.requestParameterValueConstant import PARAMETER_STRING_VALUE
from model.enum.dataTypeEnum import DataTypeEnum
from model.enum.requestParameterTypeEnum import RequestParameterTypeEnum
from model.enum.requestTypeEnum import RequestTypeEnum

class ApiDefinitionReader:
            
    def getAllPossibleValueForParameter(self, parameterType):
        if(parameterType == DataTypeEnum.STRING.value):            
            return PARAMETER_STRING_VALUE      
    
    def getTestDataForQueryParameters(self, parameters):      
        queryParameters = [queryParameter for queryParameter in parameters if queryParameter['in'] == RequestParameterTypeEnum.QUERY.value]
        queryParameterTestDat = {}
        for parameter in queryParameters:
            queryParameterTestDat[parameter['name']] = self.getAllPossibleValueForParameter(parameter['schema']['type'])
        return queryParameterTestDat    
    
    def getUrlDic(self, data):
        requestDic = {
            RequestTypeEnum.GET.value: [],
            RequestTypeEnum.POST.value: [],
            RequestTypeEnum.PUT.value: []
        } 
        baseUrl = data['servers'][0]['url']
        paths = data['paths']    
        for url in list(paths.keys()):     
            methodDic = paths[url]  
            for method in list(methodDic.keys()):            
                requestDetails = {'url':baseUrl+url,'name':method+'_'+url} 
                if methodDic[method].get("parameters") is not None: 
                    requestDetails['queryParameterTestData'] = self.getTestDataForQueryParameters(methodDic[method].get("parameters"))
                requestDic[method].append(requestDetails) 
        return requestDic 

  
