from optparse import Values, OptionParser
from typing import List
    
'''
Parses the arguments for FUZZ keyword
'''
def parse_args(parser: OptionParser, options: Values) -> dict[str, tuple[str, int]]:
    available_args = [x.dest for x in parser._get_all_options()[1:]]
    result = {}

    for arg_name in reversed(dir(options)):
        if arg_name in available_args:
            arg_value = getattr(options, arg_name)
            if arg_value:
                for i in range(0, len(arg_value)):
                    if arg_value[i:i+4] == "FUZZ":
                        result[arg_name] = (arg_value, i)
                        return result

def craft_headers(header_args: str):
    key_val_pairs = {}
    headers = header_args.split(',')
    for header in headers:
        key, val = header.split(':')
        key_val_pairs[key.strip()] = val.strip()
    return key_val_pairs