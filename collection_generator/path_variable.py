from urllib.parse import urlparse
import itertools


class PathVariable:
    def generate_test_cases_for_path_variables(self, api_request, method):
        request_list = []
        if api_request['path_variable_test_data'] is not None:
            for index, parameter_combination \
                    in enumerate(self.get_parameter_combination_list(api_request['path_variable_test_data'])):
                item = {'name': api_request['name'] + "_TEST_" + str(index),
                        'request':
                            self.get_request(api_request, method, parameter_combination, 'path')}
                request_list.append(item)
        return request_list

    @staticmethod
    def get_parameter_combination_list(input_data):
        keys = list(input_data.keys())
        lists = [input_data[key] for key in keys]
        combinations = list(itertools.product(*lists))
        combinations_dicts = [{keys[i]: combination[i] for i in range(len(keys))} for combination in combinations]
        return combinations_dicts

    def get_request(self, request_object, method, parameter_combination, parameter_type):
        request = {'method': method.upper(), 'url': self.get_url_obj_for_postman_collection(request_object,
                                                                                            parameter_combination,
                                                                                            parameter_type)}
        return request

    @staticmethod
    def get_url_obj_for_postman_collection(request_obj, parameter_combination, parameter_type):
        row: str = request_obj['url']
        parsed_url = urlparse(request_obj['url'])
        query = []
        url = {}
        if parameter_type == 'path':
            for key in list(parameter_combination.keys()):
                row = row.replace("{" + key + "}", parameter_combination[key])
        url['row'] = row
        url['protocol'] = parsed_url.scheme
        url['host'] = parsed_url.hostname.split('.')
        url['path'] = parsed_url.path[1:].split('/')
        url['query'] = query
        if parsed_url.port is not None:
            url['port'] = parsed_url.port
        return url
