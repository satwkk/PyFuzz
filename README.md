# PyFuzz 
Pyfuzz is a content discovery tool written in python. It can fuzz hidden url endpoints and subdomains.
Note: Pyfuzz is in early dev stage 

# Examples

URL Endpoint fuzzing
```
python pyfuzz.py https://example.com/FUZZ wordlist.txt

python pyfuzz.py https://example.com/FUZZ.php wordlist.txt
```

Subdomain fuzzing
```
python pyfuzz.py https://example.com/ wordlist.txt "Host: FUZZ.example.com"
```

TODO: Implement optparse for arguments