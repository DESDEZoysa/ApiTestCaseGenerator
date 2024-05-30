import json

from service.apiDefinitionReader import ApiDefinitionReader
from service.postmanCollectionGenerator import PostmanCollectionGenerator

apiDefinitionReader = ApiDefinitionReader()
postmanCollectionGenerator = PostmanCollectionGenerator()

with open('resources/api_definition.json') as file:
    data = json.load(file)
    
requestDic = apiDefinitionReader.getUrlDic(data)
collection = postmanCollectionGenerator.generatePostmanCollection(requestDic,data)
with open('resources/postman_collectio.json', 'w') as file:    
    json.dump(collection, file, indent=4)




    
