class Target():
    def __init__(self, host, port, service):
        self._host = host.rstrip().lstrip()
        self._port = port
        self._service = service.rstrip().lstrip()

    def prettify(self):
        if self._service:
            return '{}:{}/{}'.format(self._host, self._port, self._service)
        else:
            return '{}:{}'.format(self._host, self._port)
    
    def get_host(self):
        return self._host
    
    def get_port(self):
        return self._port
    
    def get_service(self):
        return self._service


class VulnerabilityTarget(Target):
    def __init__(self, host, port, service, vulnerability): 
        super(VulnerabilityTarget, self).__init__(host, port, service)
        self._vuln = vulnerability
