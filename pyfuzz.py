from banner import banner
from optparse import OptionParser
from config import DEFAULT_HEADERS
from fuzzer import get_fuzzer_factory

import parse

if __name__ == '__main__':
    print(banner)

    parser = OptionParser()
    parser.add_option("-u", "--url", dest="url", help="Url to fuzz")
    parser.add_option("-w", "--wordlist", dest="wordlist", help="Wordlist for bruteforcing")
    parser.add_option("-H", "--headers", dest="headers", help="Headers to provide for http/https request", )
    parser.add_option("-t", "--timeout", dest="timeout", help="Timeout for http/https request to complete")

    option, args = parser.parse_args()

    parsed_args = parse.parse_args(parser, option)
    
    fuzzer = get_fuzzer_factory(
        parsed_args=parsed_args, 
        args=parsed_args, 
        url=option.url, 
        headers=option.headers if option.headers else DEFAULT_HEADERS, 
        wordlist=option.wordlist, 
        timeout=int(option.timeout) if option.timeout else None
        )
    
    fuzzer.start()
    fuzzer.cleanup()
    
