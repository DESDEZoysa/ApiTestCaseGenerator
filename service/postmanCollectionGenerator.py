from urllib.parse import urlparse
import itertools

class PostmanCollectionGenerator:
       
    def generatePostmanCollection(self, requestDic):
        postmanCollection = {}
        postmanCollection['info'] = {'name':requestDic["name"],"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"}
        item = []
        for method in list(requestDic.keys()):        
            for requestObj in requestDic[method]:  
                if method == 'get':
                    if requestObj.get("queryParameterTestData") is not None:    
                        item.extend(self.generateTestRequestAccordingToQueryParameters(requestObj,method)) 
        postmanCollection['item'] = item
        return postmanCollection 
    
    def generateTestRequestAccordingToQueryParameters(self, requestObj, method):          
        requestList = []
        if requestObj['queryParameterTestData'] is not None:
            for index, parameterCombination in enumerate(self.getParameterCombinationList(requestObj['queryParameterTestData'])):
                item = {}
                item['name'] = requestObj['name'][1:]+"/TEST_"+str(index)     
                item['request'] =  self.getRequestObjFroPostmanCollection(requestObj,method,parameterCombination,'query') 
                item["respons"] = requestObj["responses"]  
                item["expectedStatus"] = item['request']["url"]["expectedStatus"] 
                requestList.append(item)     
        return requestList  
                
    def getParameterCombinationList(self, data):    
        result = []
        keys = list(data.keys())
        status_codes = ["200", "400"]
        for status_code in status_codes:
            values_lists = [data[key][status_code] for key in keys]
            for combination in itertools.product(*values_lists):
                entry = {keys[i]: combination[i] for i in range(len(keys))}
                entry["expectedStatus"] = int(status_code)
                result.append(entry)
        if len(keys) > 1:
            for key in keys:
                other_keys = [k for k in keys if k != key]
                for invalid_value in data[key]["400"]:
                    for valid_values_combination in itertools.product(
                        *[data[k]["200"] for k in other_keys]
                    ):
                        entry = {other_keys[i]: valid_values_combination[i] for i in range(len(other_keys))}
                        entry[key] = invalid_value
                        entry["expectedStatus"] = 400
                        result.append(entry) 
        return result 
    
    def getRequestObjFroPostmanCollection(self, requestObj, method, parameterCombination, parameterType):
        request = {}
        request['method'] = method.upper()
        request['url'] = self.getUrlObjForPostmanCollection(requestObj,parameterCombination,parameterType)
        return request
    
    def getUrlObjForPostmanCollection(self, requestObj,parameterCombination, parameterType): 
        parsed_url = urlparse(requestObj['url'])
        row = requestObj['url']
        query = []
        url = {} 
        if(parameterType == 'query'):
            row=row+"?"  
            parameterKeyList = list(parameterCombination.keys())
            parameterKeyList.remove("expectedStatus")
            for key in parameterKeyList:
                 row=row+"key="+str(parameterCombination[key])+"&"
                 query.append({"key":key,"value":parameterCombination[key]})                 
            row = row[:-1]
        url['row'] = row    
        url['protocol'] = parsed_url.scheme 
        url['host'] = parsed_url.hostname.split('.')
        url['path'] = parsed_url.path[1:].split('/')
        url['query'] = query
        url["expectedStatus"] = parameterCombination["expectedStatus"]
        if parsed_url.port is not None:
            url['port'] = parsed_url.port
        return url 

                
 

    

