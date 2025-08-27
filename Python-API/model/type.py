class Type:
    url = ""
    name = ""
    
    def __init__(self, url, name):
        self.url = url
        self.name = name
        
    def __str__(self):
        return self.name