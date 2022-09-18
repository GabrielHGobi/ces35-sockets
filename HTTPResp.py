import re

class HTTPResp:
    def __init__(self):
        self._status_code = None
        self._status_phrase = ''
        self._headers = {}
        self._body = ''

    def set_status_code(self, status_code: int):
        self._status_code = status_code

    def get_status_code(self):
        return self._status_code

    def set_status_phrase(self, status_phrase: str):
        self._status_phrase = status_phrase

    def get_status_phrase(self):
        return self._status_phrase

    def add_header_field(self, header_field_name: str, value: str):
        self._headers[str(header_field_name)] = str(value)

    def set_body(self, body: str):
        self._body = body
    
    def encode(self):
        message = 'HTTP/1.1' + ' ' + str(self._status_code) + ' ' + self._status_phrase + '\r\n'
        for header_field_name, value in self._headers.items():
            message += header_field_name + ' ' + value + '\r\n'
        message += '\r\n'
        message += self._body
        return message.encode(encoding='UTF-8')
    
    def parse(self, byte_stream: str):
        message = byte_stream.decode(encoding='UTF-8')
        m_response = re.search('HTTP/1\.1 ([0-9]*) ([a-zA-z ]+)\r\n'\
                    '(?:(\S*) (\S*)\r\n)*\r\n(.*)', message, re.S)
        if m_response is None:
            print("Invalid protocol")
        else:
            self._status_code = int(m_response.group(1))
            self._status_phrase = m_response.group(2)    
            self._headers = {}
            i = 3
            n = len(m_response.groups())
            while i < n and not m_response.group(i) is None:
                self._headers[m_response.group(i)] = m_response.group(i+1)
                i += 2
            self._body = m_response.group(n)


class HTTPRespNotFound(HTTPResp):
    def __init__(self):
        super().__init__()
        self.set_status_code(404)
        self.set_status_phrase("Not Found")

class HTTPRespBadRequest(HTTPResp):
    def __init__(self):
        super().__init__()
        self.set_status_code(400)
        self.set_status_phrase("Bad Request")

class HTTPRespOK(HTTPResp):
    def __init__(self):
        super().__init__()
        self.set_status_code(200)
        self.set_status_phrase("OK")
