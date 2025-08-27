class Pokemon:
    
    id = ""
    name = ""
    types = []
    
    def __init__(self, poke_id = "", name = "", types = []):
        self.id = poke_id
        self.name = name
        self.types = types
        
    def __str__(self):
        return f"""
    \n-----------Pokemon------------\n
    Numero da Pokedex: {self.id}\n
    Nome: {self.name}\n
    Seu Tipo: {self.types}
    """
    
    