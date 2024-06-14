from model.constant.requestParameterValueConstant import PARAMETER_STRING_VALUE,PARAMETER_EMAIL_VALUE,PARAMETER_INTEGER_VALUE,PARAMETER_DATE_TIME_VALUE,PARAMETER_MOBILE_VALUE,PARAMETER_BOOLEAN_VALUE
from model.enum.dataTypeEnum import DataTypeEnum
from model.enum.requestParameterTypeEnum import RequestParameterTypeEnum
from model.enum.requestTypeEnum import RequestTypeEnum
from model.enum.parameterFormatEnum import ParameterFormatEnum


class ApiDefinitionReader:  
    
    def getUrlDic(self, data):
        requestDic = {
            "name":data['info']['title'], 
            RequestTypeEnum.GET.value: [],
            RequestTypeEnum.POST.value: [],
            RequestTypeEnum.PUT.value: []
        } 
        baseUrl = data['servers'][0]['url']
        paths = data['paths']    
        components = data['components']  
        for url in list(paths.keys()):     
            methodDic = paths[url]  
            for method in list(methodDic.keys()): 
                requestDetails = {'url':baseUrl+url,'name':url+"/"+method,"responses":self.getResponsesFormatList(components,methodDic[method].get("responses"))}
                if methodDic[method].get("parameters") is not None: 
                    requestDetails['queryParameterTestData'] = self.getTestDataForQueryParameters(methodDic[method].get("parameters"))
                requestDic[method].append(requestDetails) 
        return requestDic 
    
    def getResponsesFormatList(self, components, responses):
        for status in list(responses.keys()):
            respons = responses[status]
            if respons.get("content") is not None: 
                contentType = None
                if respons["content"].get("*/*") is not None:
                    contentType = "*/*"                        
                elif respons["content"].get("application/json") is not None:
                    contentType = "application/json"                         
                if contentType is not None: 
                    if respons["content"][contentType]["schema"].get("type") is not None:
                        if respons["content"][contentType]["schema"].get("type") == "array":
                            if respons["content"][contentType]["schema"].get("items") is not None:
                                if respons["content"][contentType]["schema"]["items"].get("$ref") is not None:
                                    contentCopmonentPath = respons["content"][contentType]["schema"]["items"]["$ref"][2:]
                                    respons["content"] = self.getResponseContent(components,contentCopmonentPath)
                                else:
                                    respons["content"] = {"itemType":respons["content"][contentType]["schema"]["items"]["type"]}
                                respons["content"]["type"] = "array"
                            else:
                                respons["content"] = None 
                        elif respons["content"][contentType]["schema"].get("type") == "string":
                            respons["content"]={"type":"string"}
                        elif respons["content"][contentType]["schema"].get("type") == "boolean":
                            respons["content"]={"type":"boolean"}
                        elif respons["content"][contentType]["schema"].get("type") == "integer":
                            respons["content"]={"type":"number"}
                         
                    else:
                        if respons["content"][contentType]["schema"].get("$ref") is not None: 
                            contentCopmonentPath = respons["content"][contentType]["schema"]["$ref"][2:]
                            respons["content"] = self.getResponseContent(components,contentCopmonentPath) 
                            respons["content"]["type"] = "object"
                        else:
                            respons["content"] = None 
            else:
                 respons["content"] = None            
        return responses      
    
    def getResponseContent(self, components, contentCopmonentPath):
        contentCopmonentPathList = contentCopmonentPath.split("/")[1:]          
        contentCopmonent = components
        for path in contentCopmonentPathList:
            contentCopmonent = contentCopmonent[path]        
        return contentCopmonent
        
    def getTestDataForQueryParameters(self, parameters):      
        queryParameters = [queryParameter for queryParameter in parameters if queryParameter['in'] == RequestParameterTypeEnum.QUERY.value]
        queryParameterTestDat = {}
        for parameter in queryParameters:
            if parameter['schema'].get("format") is not None:             
                queryParameterTestDat[parameter['name']] = self.getAllPossibleValueForParameter(parameter['schema']['type'],parameter['schema']['format'])
            elif parameter['schema'].get("enum") is not None: 
                queryParameterTestDat[parameter['name']] = {"200":parameter['schema'].get("enum"),"400":[]}
            else:
                queryParameterTestDat[parameter['name']] = self.getAllPossibleValueForParameter(parameter['schema']['type'],None)                
        return queryParameterTestDat   
    
    def getAllPossibleValueForParameter(self, parameterType, parameterFormat):        
        if parameterType == DataTypeEnum.STRING.value:
            if parameterFormat is not None:
                if ParameterFormatEnum.EMAIL.value == parameterFormat:
                    return PARAMETER_EMAIL_VALUE 
                elif ParameterFormatEnum.DATE_TIME.value == parameterFormat:
                    return PARAMETER_DATE_TIME_VALUE
                elif ParameterFormatEnum.PHONE.value in parameterFormat or ParameterFormatEnum.MOBILE.value in parameterFormat: 
                    return PARAMETER_MOBILE_VALUE
                else:
                    return PARAMETER_STRING_VALUE
            else:
                return PARAMETER_STRING_VALUE 
        elif parameterType == DataTypeEnum.INTEGER.value:            
            return PARAMETER_INTEGER_VALUE
        elif parameterType == DataTypeEnum.BOOLEAN.value:
            return PARAMETER_BOOLEAN_VALUE
  
