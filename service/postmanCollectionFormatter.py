import json
from collections import defaultdict

class PostmanCollectionFormatter:
    
    def formatPostmanCollection(self, postmanCollection):        
        nested_dict = self.build_nested_dict(postmanCollection["item"])
        nested_list = self.dict_to_nested_list(nested_dict)
        postmanCollection["item"] = nested_list
        return postmanCollection
    
    def build_nested_dict(self, itemList):
        nested_dict = lambda: defaultdict(nested_dict)
        root = nested_dict()
        for item in itemList:
            parts = item['name'].split('/')
            d = root
            for part in parts[:-1]:
                d = d[part]
            d[parts[-1]] = item
        return root
    
    def dict_to_nested_list(self, nested_dict):
        result = []
        for key, value in nested_dict.items():
            if isinstance(value, defaultdict):
                result.append({
                    "name": key,
                    "item": self.dict_to_nested_list(value)
                })
            else:
                formatted_item = {
                    "name": key,
                    "request": value["request"]
                }
                result.append(formatted_item)
        return result
        

            
        
    

