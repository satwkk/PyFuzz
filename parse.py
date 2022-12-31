from args import Arg
    
'''
Parses the arguments for FUZZ keyword
# TODO: We are iterating over all arguments, not neccessary.
'''
def parse_args(args: Arg) -> dict[Arg, int]:
    result = {}
    # prepared_args = args
    for arg_name in reversed(dir(args)):
        # Filter for dunder/magic methods
        if not arg_name.startswith('__'):
            
            # Get the attribute value
            arg_value = getattr(args, arg_name)
            
            # Parse the arg for fuzz param
            for i in range(0, len(arg_value)):
                if arg_value[i:i+4] == "FUZZ":
                    args.set_fuzz_index(i)
                    return (arg_name, args)
                    # result[arg_name] = (arg_value, i)
                    # return result
                    # return (arg_name, arg_value, i)
                    