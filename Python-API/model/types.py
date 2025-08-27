from type import Type

class Types:
    slot = ""
    type = Type
    
    def __init__(self, slot, type):
        self.slot = slot
        self.type = type
    
    def __str__(self):
        return self.type