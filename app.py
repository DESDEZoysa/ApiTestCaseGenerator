import json

import model.constant.filePathConstant as FilePathConstant
from service.apiDefinitionReader import ApiDefinitionReader
from service.postmanCollectionGenerator import PostmanCollectionGenerator

apiDefinitionReader = ApiDefinitionReader()
postmanCollectionGenerator = PostmanCollectionGenerator()

with open(FilePathConstant.API_DEFINITION_PATH) as file:
    data = json.load(file)
    
requestDic = apiDefinitionReader.getUrlDic(data)
collection = postmanCollectionGenerator.generatePostmanCollection(requestDic,data)
with open(FilePathConstant.POSTMAN_COLLECTION_PATH, "w") as file:    
    json.dump(collection, file, indent=4)




    
