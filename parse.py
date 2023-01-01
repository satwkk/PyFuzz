from args import Arg
    
'''
Parses the arguments for FUZZ keyword
# TODO: We are iterating over all arguments, not neccessary.
'''
def parse_args(args: Arg) -> dict[Arg, int]:
    for arg_name in reversed(dir(args)):
        if not arg_name.startswith('__') and not arg_name == 'index':
            arg_value = getattr(args, arg_name)
            for i in range(0, len(arg_value)):
                if arg_value[i:i+4] == "FUZZ":
                    args.index = i
                    return (arg_name, args)
                    

def craft_headers(header_args: str):
    if len(header_args) == 0 or ',' not in header_args or ':' not in header_args:
        return ""

    key_val_pairs = {}
    headers = header_args.split(',')
    for header in headers:
        key, val = header.split(':')
        key_val_pairs[key.strip()] = val.strip()
    return key_val_pairs