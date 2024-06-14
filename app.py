import json

import model.constant.filePathConstant as FilePathConstant
from service.apiDefinitionReader import ApiDefinitionReader
from service.postmanCollectionGenerator import PostmanCollectionGenerator
from service.postmanCollectionFormatter import PostmanCollectionFormatter
from service.testScriptGenerator import TestScriptGeneratoe

apiDefinitionReader = ApiDefinitionReader()
postmanCollectionGenerator = PostmanCollectionGenerator()
postmanCollectionFormatter = PostmanCollectionFormatter()
testScriptGeneratoe = TestScriptGeneratoe()

with open(FilePathConstant.API_DEFINITION_PATH) as file:
    data = json.load(file)    
requestDic = apiDefinitionReader.getUrlDic(data)  
postmanCollection = postmanCollectionGenerator.generatePostmanCollection(requestDic)
postmanCollection = postmanCollectionFormatter.formatPostmanCollection(postmanCollection)
postmanCollection = testScriptGeneratoe.generateTestScriptForCollection(postmanCollection)
with open(FilePathConstant.POSTMAN_COLLECTION_PATH, "w") as file:    
    json.dump(postmanCollection, file, indent=4)






    
