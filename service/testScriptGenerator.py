import copy
import requests

from model.constant.testScriptConstant import STATUS_VALIDATE_SCRIPT,RESPONSE_BODY_TYPE_CHECK_SCRIPT,BEARER_TOKEN_SET_SCRIPT
from model.enum.testScriptTypeEnum import TestScriptTypeEnum
from model.constant.requestParameterValueConstant import AUTTHENTICATION_DETAIL

class TestScriptGeneratoe:   
        
    def generateTestScriptForCollection(self, postmanCollection):
        for item in postmanCollection['item']:
            self.addTestScript(item,TestScriptTypeEnum.VALIDATE_STATUS.value) 
            self.addTestScript(item,TestScriptTypeEnum.VALIDATE_RESPONSE_BODY_TYPE.value)            
        return self.addAuthorizationPreScriptForCollection(postmanCollection);
    
    def addTestScript(self, item, testScriptType):            
        if 'item' in item:
            for subItem in item['item']:
                self.addTestScript(subItem,testScriptType)
        else:            
            for event in item["event"]:
                if event["listen"] == "test":
                    if TestScriptTypeEnum.VALIDATE_STATUS.value == testScriptType:
                        newScript = copy.deepcopy(STATUS_VALIDATE_SCRIPT).replace("{{status_code}}",str(item["expectedStatus"]))
                        event["script"]["exec"].append(newScript)
                    elif TestScriptTypeEnum.VALIDATE_RESPONSE_BODY_TYPE.value == testScriptType:
                        event["script"]["exec"].append(self.getResponseBodyValidateScript(item))
                        
    def getResponseBodyValidateScript(self, item):        
        script = None     
        if item["respons"] is not None:
            if str(item["expectedStatus"]) in  item["respons"]: 
                responseObj = item["respons"][str(item["expectedStatus"])]               
                if responseObj["content"] is not None:               
                    if responseObj["content"]["type"] is not None:
                        if responseObj["content"]["type"] == "object": 
                            script = """
pm.test('Response should be a object', function () { 
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.not.be.null;
    pm.expect(jsonData).to.not.be.empty;
    pm.expect(jsonData).to.be.an('object');"""
                            properties = list(responseObj["content"]["properties"].keys())
                            for properti in properties:
                                script = script+"""
    pm.expect(jsonData).to.have.property('"""+properti+"""');""" 
                            script = script+"""
});"""
                        elif responseObj["content"]["type"] == "array":  
                            script = """
pm.test('Response should be an array', function () {
    let jsonData = pm.response.json();
    pm.expect(jsonData).to.not.be.null;
    pm.expect(jsonData).to.not.be.empty;
    pm.expect(jsonData).to.be.an('array');
    jsonData.forEach((item, index) => {
        pm.test(`Check properties`, function () {"""   
                            if responseObj["content"].get("properties") is not None:                                
                                properties = list(responseObj["content"]["properties"].keys())
                                for properti in properties:
                                    script = script+"""    
            pm.expect(item).to.have.property('"""+properti+"""');"""    
                            else:
                                if responseObj["content"]["itemType"] == "integer":
                                   responseObj["content"]["itemType"] = "number" 
                                script = script+"""
            pm.expect(item).to.be.a('"""+responseObj["content"]["itemType"]+"""');"""
                            script = script+"""
        });
   });
});"""  
                        else:   
                            script = copy.deepcopy(RESPONSE_BODY_TYPE_CHECK_SCRIPT).replace("{{response_body_type}}",responseObj["content"]["type"])
        return script
    
    def addAuthorizationPreScriptForCollection(self, postmanCollection):
        script= {
            "type": "text/javascript",
            "exec":[copy.deepcopy(BEARER_TOKEN_SET_SCRIPT).replace("{{access_token}}",self.getAuthToken())]
            }
        preScript = {
            "listen": "prerequest",
            "script":script
            
            }
        postmanCollection["event"] = [preScript]
        return postmanCollection
    
    def getAuthToken(self):
        headers = {'Content-Type': 'application/json'}
        requestBody = {}        
        if AUTTHENTICATION_DETAIL["requestBody"] is not None:
            requestBody = AUTTHENTICATION_DETAIL["requestBody"]
        else:
            requestBody = {AUTTHENTICATION_DETAIL["userNameKey"]: AUTTHENTICATION_DETAIL["userName"],AUTTHENTICATION_DETAIL["passwordKey"]: AUTTHENTICATION_DETAIL["password"]}  
        response = requests.post(AUTTHENTICATION_DETAIL["authUrl"], json=requestBody, headers=headers)
        tokenPathList = AUTTHENTICATION_DETAIL["tokenPath"].split('.')
        token = response.json()
        for tokenPath in tokenPathList:
            token = token[tokenPath]
        return token 
        
            
              
    
    
    
    
    
    
    
    
        