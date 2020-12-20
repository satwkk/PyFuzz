#!/usr/bin/python3

# ====================================================================================================================================
# Author: v01d
# Description: This is a multithreaded directory bruteforcer and subdomain finder.
# Note: This doesn't make recursive dirbusting and is not production ready.
#     - I built it just for fun and for my project. If you want to contribute
#     - and improve the code then feel free to do that, i will be optimizing it 
#     - every now and then.
# Usage: python pyfuzz.py -u https://facebook.com/ -w wordlist.txt --type dir/domain
# ====================================================================================================================================

from termcolor import cprint
import threading
import requests
import optparse
import sys

''' 
All HTTP codes defined as global variables
We will iterate over all these codes to check
for response and print out desired output.
'''
SUCCESS_CODES = [i for i in range(200, 299)]
REDIRECT_CODES = [i for i in range(300, 399)]
ERROR_CODES = [i for i in range(400, 499)]
FORBIDDEN_CODES = [i for i in range(500, 599)]

''' 
Making a request to pages and checking for status codes.
Note: If you want to print error codes too comment out
the line where it prints it
'''
def make_request(url):
    try:
        response = requests.get(url)

        if response.status_code in SUCCESS_CODES:
            print(url + "\t\t==>\t" + str(response.status_code))

        if response.status_code in ERROR_CODES:
            pass

        if response.status_code in FORBIDDEN_CODES:
            print(url + "\t\t==>\t" + str(response.status_code))

        if response.status_code in REDIRECT_CODES:
            print(url + "\t\t==>\t" + str(response.status_code))

    except requests.ConnectionError:
        pass

if __name__ == "__main__":
    parser = optparse.OptionParser("[*] python pyfuzz.py -u https://facebook.com/ -w wordlist --type dir \n(Make sure to add the trailing '/' at the end of url")
    parser.add_option("-w", type="string", dest="wordlist", help="provide wordlist")
    parser.add_option("-u", type="string", dest="url", help="provide url")
    parser.add_option("-x", type="string", dest="ext", help="provide extension")
    parser.add_option("--type", type="string", dest="type", help="provide bruteforcing type")
    (options, args) = parser.parse_args()

    if (options.wordlist == None) & (options.url == None) & (options.ext == None):
        print(parser.usage)

    if (options.type == "dir"):
        url = options.url
        wordlist = options.wordlist

        with open(wordlist, "r") as wordList:
            for words in wordList.readlines():
                words = words.strip("\n")
                final_url = url + words
                #print(final_url)

                try:
                    t = threading.Thread(target=make_request, args=(final_url,))
                    t.daemon = True
                    t.start()
                except Exception as e:
                    pass

    if (options.type == "domain"):
        url = options.url
        wordlist = options.wordlist

        with open(wordlist, "r") as wordList:
            for words in wordList.readlines():
                words = words.strip("\n")

                if url.startswith("http"):
                    final_url = "http://" + words + "." + url.split("//")[1]
                if url.startswith("https"):
                    final_url = "https://" + words + "." + url.split("//")[1]

                try:
                    t = threading.Thread(target=make_request, args=(final_url,))
                    t.daemon = True
                    t.start()
                except Exception as e:
                    pass

'''
TODO: Add extension feature
'''