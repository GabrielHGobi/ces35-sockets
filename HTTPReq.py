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
        m_request = re.findall('(GET|POST|PUT|HEAD) (\S*) HTTP/1\.1\r\n', message, re.S)
        m_headers = re.findall('(\S*): ([\S ]*)\r\n', message, re.S)
        if m_request is None:
            self._BadRequest = True
        else:
            self._method = m_request[0][0]
            if m_request[0][1] == '/':
                self._URL = '/index.html'
            else:
                self._URL = m_request[0][1]    
            self._headers = {}
            for i in range(len(m_headers)):
                self._headers[m_headers[i][0]] = m_headers[i][1]
            self._body = " "
            self._BadRequest = False
