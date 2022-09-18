import re

class HTTPReq():
    def __init__(self):
        self._URL = ''
        self._method = ''
        self._headers = {}
        self._body = ''
        self._BadRequest = False


    def set_URL(self, fileURL: str):
        self._URL = fileURL

    def get_URL(self):
        return self._URL

    def set_method(self, method: str):
        self._method = method

    def get_method(self):
        return self._method
    
    def add_header_field(self, header_field_name: str, value: str):
        self._headers[str(header_field_name)] = str(value)

    def set_body(self, body: str):
        self._body = body

    def is_BadRequest(self):
        return self._BadRequest

    def encode(self):
        message = '' + self._method + ' ' + self._URL + ' ' + 'HTTP/1.1' + '\r\n'
        for header_field_name, value in self._headers.items():
            message += header_field_name + ': ' + value + '\r\n'
        message += '\r\n'
        message += self._body
        return message.encode(encoding='UTF-8')

    def parse(self, byte_stream: str):
        message = byte_stream.decode(encoding='UTF-8')
        m_request = re.search('(GET|POST|PUT|HEAD) (\S*) HTTP/1\.1\r\n'\
                    '(?:(\S*) (\S*)\r\n)*\r\n(.*)', message, re.S)
        if m_request is None:
            self._BadRequest = True
        else:
            self._method = m_request.group(1)
            self._URL = m_request.group(2)    
            self._headers = {}
            i = 3
            n = len(m_request.groups())
            while i < n and not m_request.group(i) is None:
                self._headers[m_request.group(i)] = m_request.group(i+1)
                i += 2
            self._body = m_request.group(n)
            self._BadRequest = False
