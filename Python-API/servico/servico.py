import requests

class Servico:
    
    url = ""
    
    def procurar_pokemon(self, name):
        self.url = f"https://pokeapi.co/api/v2/pokemon/{name}"
        
        response = requests.get( self.url, json= )
        
        