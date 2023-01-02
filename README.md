# PyFuzz 
Pyfuzz is a content discovery tool written in python. It can fuzz hidden url endpoints and subdomains.
Note: Pyfuzz is in early dev stage 

# Examples

URL Endpoint fuzzing
```
python pyfuzz.py -u https://example.com/FUZZ -w wordlist.txt

python pyfuzz.py -u https://example.com/FUZZ.php -w wordlist.txt
```

Subdomain fuzzing / Multiple headers
```
python pyfuzz.py -u https://example.com/ -w wordlist.txt -H "Host: FUZZ.example.com"

python pyfuzz.py -u https://example.com/ -w wordlist.txt -H "Host: FUZZ.example.com, User-Agent: Leet hacker zone"
```

Timeout for HTTP/HTTP requests
```
python pyfuzz.py -u https://example.com/ -w wordlist.txt -H "Host: FUZZ.example.com, User-Agent: Leet hacker zone" --timeout 5
```

TODO: Implement filtering by word, size and lines and proxy