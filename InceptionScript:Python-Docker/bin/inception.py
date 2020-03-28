import requests
import json

class InceptionTools():
    def __init__(self, datacenter):
        self.datacenter = datacenter
    
    def dc_data(self):
        try:
            res_data = requests.get('http://dynconfig.'+self.datacenter+'.tivo.com:50000/MonitoringUrls')
            return json.loads(res_data.text)
        except Exception:
            print('NetworkError: Please check settings')
            sys.exit()

    def environment(self):
        dc_env = []
        data = self.dc_data()
        for elements in data['dynconfigMonitoringServerUrls']:
            dc_env.append(elements['environment'])
        return list(set(dc_env))


class Service(InceptionTools):
    def __init__(self, datacenter, environment = None):
        super().__init__(datacenter)
        self.environment = environment
        
    def all_service(self):
        all_service = []
        data = super().dc_data()
        for elements in data['dynconfigMonitoringServerUrls']:
            for values in elements['url']:
                all_service.append(values['container'])
        return list(set(all_service))
                
    def specific_service(self):
        specific_service = []
        data = super().dc_data()
        for elements in data['dynconfigMonitoringServerUrls']:
            for values in elements['url']:
                if elements['environment'] == self.environment:
                    specific_service.append(values['container'])
        return list(set(specific_service))


class Server(InceptionTools):
    def __init__(self, datacenter, environment = None, service = None):
        super().__init__(datacenter)
        self.environment = environment
        self.service = service

    def specific_service(self):
        specific_service = []
        data = super().dc_data()
        for service in self.service:
            for elements in data['dynconfigMonitoringServerUrls']:
                for contents in elements['url']:
                    if elements['environment'] == self.environment and contents['container'] == service:
                        specific_service.append(elements['server'])
        return specific_service

    def all_server(self):
        all_server = []
        data = super().dc_data()
        for server in data['dynconfigMonitoringServerUrls']:
            all_server.append(server['server'])
        return all_server
    
    def specific_server(self):
        specific_server = []
        data = super().dc_data()
        for elements in data['dynconfigMonitoringServerUrls']:
            if elements['environment'] == self.environment:
                specific_server.append(elements['server'])
        return specific_server
