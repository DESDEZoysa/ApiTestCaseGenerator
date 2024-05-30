from model.constant.requestParameterValueConstant import PARAMETER_STRING_VALUE,PARAMETER_EMAIL_VALUE
from model.enum.dataTypeEnum import DataTypeEnum
from model.enum.requestParameterTypeEnum import RequestParameterTypeEnum
from model.enum.requestTypeEnum import RequestTypeEnum
from model.enum.parameterFormatEnum import ParameterFormatEnum

class ApiDefinitionReader:
            
    def getAllPossibleValueForParameter(self, parameterType, parameterFormat):
        if(parameterType == DataTypeEnum.STRING.value):
            if parameterFormat is not None:
                if ParameterFormatEnum.EMAIL.value == parameterFormat:
                    return PARAMETER_EMAIL_VALUE 
            else:
                return PARAMETER_STRING_VALUE 
                
    def getTestDataForQueryParameters(self, parameters):      
        queryParameters = [queryParameter for queryParameter in parameters if queryParameter['in'] == RequestParameterTypeEnum.QUERY.value]
        queryParameterTestDat = {}
        for parameter in queryParameters:
            if parameter['schema'].get("format") is not None:             
                queryParameterTestDat[parameter['name']] = self.getAllPossibleValueForParameter(parameter['schema']['type'],parameter['schema']['format'])
            else:
                queryParameterTestDat[parameter['name']] = self.getAllPossibleValueForParameter(parameter['schema']['type'],None)                
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

  
