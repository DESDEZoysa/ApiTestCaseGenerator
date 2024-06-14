from collections import defaultdict

class PostmanCollectionFormatter:
    
    def formatPostmanCollection(self, postmanCollection):        
        nested_dict = self.buildNestedDict(postmanCollection["item"])
        nested_list = self.dictToNestedList(nested_dict)
        postmanCollection["item"] = nested_list
        return postmanCollection
    
    def buildNestedDict(self, itemList):
        nested_dict = lambda: defaultdict(nested_dict)
        root = nested_dict()
        for item in itemList:
            parts = item['name'].split('/')
            d = root
            for part in parts[:-1]:
                d = d[part]
            d[parts[-1]] = item
        return root
    
    def dictToNestedList(self, nested_dict):
        result = []
        for key, value in nested_dict.items():
            if isinstance(value, defaultdict):
                result.append({
                    "name": key,
                    "item": self.dictToNestedList(value)
                })
            else:
                formatted_item = {
                    "name": key,
                    "request": value["request"],
                    "respons":value["respons"],
                    "expectedStatus":value["expectedStatus"],
                    "event":self.getEventArray()
                }
                result.append(formatted_item)
        return result
    
    def getEventArray(self):
        event = [
            {
                "listen": "test",
                "script": {
                    "type": "text/javascript",
                    "exec": []
                }
            }
        ]
        return event    
    
        
        
        

            
        
    

