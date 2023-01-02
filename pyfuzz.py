from enum import Enum
from banner import banner
from optparse import OptionParser

import parse
import requests
import threading

# Add any default headers here if you want to add them to your requests
default_headers = """
    User-Agent: Leet hacker zone
"""

class EArgType(Enum):
    NONE = 0
    URL = 1
    HEADER = 2
    
class ERequestType(Enum):
    NONE = 0
    GET = 1
    POST = 2

class Fuzzer:
    def __init__(self, **kwargs) -> None:
        self.fuzz_arg = kwargs.get('args')
        self.url = kwargs.get('url')
        self.headers = parse.craft_headers(kwargs.get('headers'))
        self.wordlist = open(kwargs.get('wordlist'), 'r')
        self.timeout = kwargs.get('timeout')
        self.filter_by = kwargs.get('filter_by')
        self.session = requests.Session()
        self.mode = EArgType.NONE
        self.request_mode = ERequestType.GET

    def detect_modes(self) -> None:
        if 'url' in self.fuzz_arg:
            self.mode = EArgType.URL
        elif 'headers' in self.fuzz_arg:
            self.mode = EArgType.HEADER
            
    def prepare_args(self, word_to_replace: str) -> str:
        if self.mode == EArgType.URL:
            url, fuzz_idx = self.fuzz_arg['url']
            final_arg = f'{url[:fuzz_idx]}{word_to_replace}{url[fuzz_idx+4:]}'

        elif self.mode == EArgType.HEADER:
            header, fuzz_idx = self.fuzz_arg['headers']
            final_arg = f'{header[:fuzz_idx]}{word_to_replace}{header[fuzz_idx+4:]}'

        return final_arg

    def make_request(self, fuzz_arg: str, out_responses: dict[str, requests.Response]):
        if self.mode == EArgType.URL:
            response = self.session.get(url=fuzz_arg, headers=self.headers, timeout=self.timeout)
            out_responses[fuzz_arg] = response

        elif self.mode == EArgType.HEADER:
            response = self.session.get(url=self.url, headers=parse.craft_headers(fuzz_arg), timeout=self.timeout)
            out_responses[fuzz_arg] = response

        #! DEBUG
        print(f'[{response.status_code}] => {fuzz_arg}')
            
    def start(self) -> None:
        self.detect_modes()
        words = self.wordlist.read().strip().split('\n')
        response = {}
        for word in words:
            fuzz_arg = self.prepare_args(word)
            thread = threading.Thread(target=self.make_request, args=(fuzz_arg, response))
            thread.daemon = True
            thread.start()
            
    def cleanup(self) -> None:
        self.session.close()
        self.wordlist.close()
        
if __name__ == '__main__':
    print(banner)

    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url", help="Url to fuzz")
    parser.add_option("-w", "--wordlist", dest="wordlist", help="Wordlist for bruteforcing")
    parser.add_option("-H", "--headers", dest="headers", help="Headers to provide for http/https request", )
    parser.add_option("-t", "--timeout", dest="timeout", help="Timeout for http/https request to complete")

    option, args = parser.parse_args()

    parsed_args = parse.parse_args(parser, option)
    fuzzer = Fuzzer(
        args=parsed_args, 
        url=option.url, 
        headers=option.headers if option.headers else default_headers, 
        wordlist=option.wordlist, 
        timeout=int(option.timeout) if option.timeout else None, 
        filter_by=""
        )

    fuzzer.start()
    fuzzer.cleanup()
