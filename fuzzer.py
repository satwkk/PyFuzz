from enum import Enum
from abc import ABC, abstractmethod

import parse
import requests
import threading

class EArgType(Enum):
    NONE = 0
    URL = 1
    HEADER = 2
    
class ERequestType(Enum):
    NONE = 0
    GET = 1
    POST = 2

class Fuzzer(ABC):
    ''' Base fuzzer class '''
    
    def __init__(self, **kwargs) -> None:
        self.fuzz_arg = kwargs.get('args')
        self.url = kwargs.get('url')
        self.headers = parse.craft_headers(kwargs.get('headers'))
        self.wordlist = open(kwargs.get('wordlist'), 'r')
        self.timeout = kwargs.get('timeout')
        self.filter_by = kwargs.get('filter_by')
        self.session = requests.Session()
        self.final_args = [self.prepare_args(word) for word in self.wordlist.read().strip().split('\n')]
        self.response = dict()
        self.mode = EArgType.NONE
        self.request_mode = ERequestType.GET
        
    @abstractmethod
    def prepare_args(self, word_to_replace: str) -> str: ...

    @abstractmethod
    def make_request(self, fuzz_arg: str, out_responses: dict[str, requests.Response]): ...
            
    def start(self) -> None:
        for arg in self.final_args:
            thread = threading.Thread(target=self.make_request, args=(arg, self.response))
            thread.daemon = True
            thread.start()
            
    def cleanup(self) -> None:
        self.session.close()
        self.wordlist.close()

class URLFuzzer(Fuzzer):
    ''' Child class of Fuzzer which bruteforces URLs and endpoints'''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def prepare_args(self, word_to_replace: str) -> str:
        url, fuzz_idx = self.fuzz_arg['url']
        final_arg = f'{url[:fuzz_idx]}{word_to_replace}{url[fuzz_idx+4:]}'
        return final_arg

    def make_request(self, fuzz_arg: str, out_responses: dict[str, requests.Response]):
        response = self.session.get(url=fuzz_arg, headers=self.headers, timeout=self.timeout, allow_redirects=False)
        out_responses[fuzz_arg] = response
        print(f'{fuzz_arg} => Code [{response.status_code}]')
    
class HeaderFuzzer(Fuzzer):
    ''' Child class of Fuzzer which bruteforces subdomains and headers '''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def prepare_args(self, word_to_replace: str) -> str:
        header, fuzz_idx = self.fuzz_arg['headers']
        final_arg = f'{header[:fuzz_idx]}{word_to_replace}{header[fuzz_idx+4:]}'
        return final_arg

    def make_request(self, fuzz_arg: str, out_responses: dict[str, requests.Response]):
        response = self.session.get(url=self.url, headers=parse.craft_headers(fuzz_arg), timeout=self.timeout, allow_redirects=False)
        out_responses[fuzz_arg] = response
        print(f'{fuzz_arg} => Code [{response.status_code}]')
   
   
def get_fuzzer_factory(parsed_args, **kwargs) -> Fuzzer:
        if 'url' in parsed_args:
            return URLFuzzer(**kwargs)
        elif 'headers' in parsed_args:
            return HeaderFuzzer(**kwargs)