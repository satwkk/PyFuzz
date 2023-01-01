from args import Arg
from enum import Enum
from typing import List
from banner import banner

import sys
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
        
    def detect_modes(self) -> None:
        if self.arg_name == 'url':
            self.mode = EArgType.URL
        elif self.arg_name == 'headers':
            self.mode = EArgType.HEADER
            
    def prepare_statement(self, word_to_replace: str) -> str:
        if self.mode == EArgType.URL:
            final_statement = f'{self.arg.url[:self.arg.index]}{word_to_replace}{self.arg.url[self.arg.index+4:]}'
        elif self.mode == EArgType.HEADER:
            final_statement = f'{self.arg.headers[:self.arg.index]}{word_to_replace}{self.arg.headers[self.arg.index+4:]}'
        return final_statement

    def make_request(self, final_fuzz_str: str, out_responses: dict[str, requests.Response]):
        if self.mode == EArgType.URL:
            response = self.session.get(url=final_fuzz_str, headers=parse.craft_headers(self.arg.headers))
            out_responses[final_fuzz_str] = response

        elif self.mode == EArgType.HEADER:
            response = self.session.get(url=self.arg.url, headers=parse.craft_headers(final_fuzz_str))
            out_responses[final_fuzz_str] = response

        #! DEBUG
        if response.status_code == 200:
            print(f'[{response.status_code}] => {final_fuzz_str}')
            
    def start(self) -> None:
        self.detect_modes()
        words = self.wordlist.read().strip().split('\n')
        response = {}
        for word in words:
            statement = self.prepare_statement(word)
            thread = threading.Thread(target=self.make_request, args=(statement, response))
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
