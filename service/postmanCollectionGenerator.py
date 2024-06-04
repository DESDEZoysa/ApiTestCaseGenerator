from urllib.parse import urlparse
import itertools

class PostmanCollectionGenerator:
    
    def getCollectionName(self, data):
        return data['info']['title']   
    
    def getUrlObjForPostmanCollection(self, requestObj,parameterCombination, parameterType):
        parsed_url = urlparse(requestObj['url'])
        row = requestObj['url']
        query = []
        url = {} 
        if(parameterType == 'query'):
            row=row+"?"
            for key in list(parameterCombination.keys()):
                 row=row+"key="+str(parameterCombination[key])+"&"
                 query.append({"key":key,"value":parameterCombination[key]})
            row = row[:-1]
        url['row'] = row    
        url['protocol'] = parsed_url.scheme 
        url['host'] = parsed_url.hostname.split('.')
        url['path'] = parsed_url.path[1:].split('/')
        url['query'] = query
        if parsed_url.port is not None:
            url['port'] = parsed_url.port
        return url 
    
    def getParameterCombinationList(self, input_data):        
        keys = list(input_data.keys())
        lists = [input_data[key] for key in keys]
        combinations = list(itertools.product(*lists))
        combinations_dicts = [{keys[i]: combination[i] for i in range(len(keys))} for combination in combinations]
        return combinations_dicts
    
    def getRequestObjFroPostmanCollection(self, requestObj, method, parameterCombination, parameterType):
        request = {}
        request['method'] = method.upper()
        request['url'] = self.getUrlObjForPostmanCollection(requestObj,parameterCombination,parameterType)
        return request
    
    def generateTestRequestAccordingToQueryParameters(self, requestObj, method):
        requestList = []
        if requestObj['queryParameterTestData'] is not None:
            for index, parameterCombination in enumerate(self.getParameterCombinationList(requestObj['queryParameterTestData'])):
                item = {}
                item['name'] = requestObj['name'][1:]+"/TEST_"+str(index)     
                item['request'] =  self.getRequestObjFroPostmanCollection(requestObj,method,parameterCombination,'query') 
                requestList.append(item)     
        return requestList     
       
    def generatePostmanCollection(self, requestDic, data):
        postmanCollection = {}
        postmanCollection['info'] = {'name':self.getCollectionName(data),"schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"}
        item = []
        for method in list(requestDic.keys()):        
            for requestObj in requestDic[method]:  
                if method == 'get':
                    if requestObj.get("queryParameterTestData") is not None:    
                        item.extend(self.generateTestRequestAccordingToQueryParameters(requestObj,method)) 
        postmanCollection['item'] = item
        return postmanCollection 
                

                
 

    

