
class Arg:
    def __init__(self, **kwargs):
        self.url = kwargs.get('url')
        self.headers = kwargs.get('headers')
        self.wordlist = kwargs.get('wordlist')
        self.index = 0
    
    def __str__(self):
        return f'{self.url} : {self.headers} : {self.wordlist} : {self.index}'
    