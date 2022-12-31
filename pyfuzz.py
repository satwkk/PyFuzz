from typing import List
from args import Arg
from enum import Enum
from banner import banner
import parse
import threading

import requests
import sys

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
        self.parsed_arg = kwargs.get('args')
        self.arg_name, self.arg = self.parsed_arg
        self.wordlist = open(kwargs.get('wordlist'), 'r')
        self.timeout = kwargs.get('timeout')
        self.filter_by = kwargs.get('filter_by')
        self.session = requests.Session()
        self.mode = EArgType.NONE
        self.request_mode = ERequestType.GET
    
    def prepare_url(self, word_to_replace: str) -> str:
        final_url = f'{self.arg.url[:self.arg.index]}{word_to_replace}{self.arg.url[self.arg.index+4:]}'
        return final_url
    
    def craft_headers(self):
        pass
                
    def make_request(self, url: str, out_responses: dict[str, requests.Response]):
        if self.mode == EArgType.URL:
            if self.request_mode == ERequestType.GET:
                response = self.session.get(url=url)
                
                # Perform operations here (printing, debug, etcc)
                # ...
                
                out_responses[url] = response
            elif self.request_mode == ERequestType.POST:
                pass
        elif self.mode == EArgType.HEADER:
            pass
        
    def detect_modes(self) -> None:
        if self.arg_name == 'url':
            self.mode = EArgType.URL
        elif self.arg_name == 'headers':
            self.mode = EArgType.HEADER
            
    def start(self) -> None:
        self.detect_modes()
        words = self.wordlist.read().strip().split('\n')
        response = {}
        for word in words:
            final_url = self.prepare_url(word)
            thread = threading.Thread(target=self.make_request, args=(final_url, response))
            # thread.daemon = True
            thread.start()
            
    def cleanup(self) -> None:
        self.session.close()
        self.wordlist.close()
        
        
if __name__ == '__main__':
    
    print(banner)
    
    url = sys.argv[1]
    wordlist = sys.argv[2]
    headers = sys.argv[3]

    args = Arg(url=url, headers=headers, wordlist=wordlist)
    arg_name, parsed_args = parse.parse_args(args)
    
    fuzzer = Fuzzer(args=(arg_name, parsed_args), wordlist=args.wordlist, timeout=0, filter_by="")
    fuzzer.start()
    fuzzer.cleanup()
