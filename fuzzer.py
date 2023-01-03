from enum import Enum
from typing import List
from abc import ABC, abstractmethod, abstractproperty

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
        self.args_to_fuzz = [self.prepare_args(word) for word in self.wordlist.read().strip().split('\n')]
        self.response = dict()
        self.request_mode = ERequestType.GET
        
    @abstractmethod
    def prepare_args(self, word_to_replace: str) -> str: ...

    @abstractmethod
    def make_request(self, fuzz_arg: str, out_responses: dict[str, requests.Response]) -> None: ...
    
    @abstractproperty
    def final_args(self): ...
    
    def start(self) -> None:
        for arg in self.final_args:
            thread = threading.Thread(target=self.make_request, args=(arg, self.response))
            thread.start()
            
    def cleanup(self) -> None:
        self.session.close()
        self.wordlist.close()

class URLFuzzer(Fuzzer):
    ''' Child class of Fuzzer which bruteforces URLs and endpoints'''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    '''
    Returns the final fuzzing argument, in this case it returns all the URLs.
    @param: None
    @return: List of URLs replaced with words from wordlist at FUZZ index.
    '''
    @property
    def final_args(self) -> List[str]:
        return self.args_to_fuzz
    
    '''
    Prepares the fuzzing arguments and caches them into `self.args_to_fuzz` inside constructor.
    In this case it replaces all the FUZZ instances in URLs with words from wordlist
    @param: word_to_replace - Word from wordlist to replace with FUZZ keyword.
    @return: str            - Returns the replaced argument
    '''
    def prepare_args(self, word_to_replace: str) -> str:
        url, fuzz_idx = self.fuzz_arg['url']
        final_arg = f'{url[:fuzz_idx]}{word_to_replace}{url[fuzz_idx+4:]}'
        return final_arg

    '''
    Sends the HTTP request with respective `fuzz_arg` which is passed to the url parameter in `self.session.get`.
    @param: fuzz_arg - The arg inside `self.final_arg`
    @param: out_response - A dictionary to cache responses for later use.
    @return: None
    '''
    def make_request(self, fuzz_arg: str, out_responses: dict[str, requests.Response]) -> None:
        try:
            response = requests.get(url=fuzz_arg, headers=self.headers, allow_redirects=False)
            # TODO: Filtering by status code, line, word and size.
            if response.status_code == 200:
                print(f'{fuzz_arg} => Code [{response.status_code}]')
        except Exception as e:
            pass
    
class HeaderFuzzer(Fuzzer):
    ''' Child class of Fuzzer which bruteforces subdomains and headers '''
    
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    '''
    Returns the final fuzzing argument, in this case it returns all the headers.
    @param: None
    @return: List of headers replaced with words from wordlist at FUZZ index.
    '''
    @property
    def final_args(self) -> List[dict[str, str]]:
        return [parse.craft_headers(arg) for arg in self.args_to_fuzz]
    
    '''
    Prepares the fuzzing arguments and caches them into `self.args_to_fuzz` inside constructor.
    In this case it replaces all the FUZZ instances in header with words from wordlist
    @param: word_to_replace - Word from wordlist to replace with FUZZ keyword.
    @return: str            - Returns the replaced argument
    '''
    def prepare_args(self, word_to_replace: str) -> str:
        header, fuzz_idx = self.fuzz_arg['headers']
        final_arg = f'{header[:fuzz_idx]}{word_to_replace}{header[fuzz_idx+4:]}'
        return final_arg
    
    '''
    Sends the HTTP request with respective `fuzz_arg` which is passed to the header parameter in `self.session.get`.
    @param: fuzz_arg - The arg inside `self.final_arg`
    @param: out_response - A dictionary to cache responses for later use.
    @return: None
    '''
    def make_request(self, fuzz_arg: str, out_responses: dict[str, requests.Response]) -> None:
        try:
            response = requests.get(url=self.url, headers=fuzz_arg, allow_redirects=False)
            # TODO: Filtering by status code, line, word and size.
            if response.status_code == 200:
                print(f'{fuzz_arg} => Code [{response.status_code}]')
        except Exception as e:
            pass
        

def get_fuzzer(parsed_args, **kwargs) -> Fuzzer:
    ''' Fuzzer factory to return respective fuzzer based on key in parsed_arg dictionary '''
    
    if 'url' in parsed_args:
        return URLFuzzer(**kwargs)
    elif 'headers' in parsed_args:
        return HeaderFuzzer(**kwargs)