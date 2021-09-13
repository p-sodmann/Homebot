class Immobilie:
    def __init__(self, content:dict):
        self.id = content["id"]
        self.link = content["link"]
        self.title = content["title"]
        self.image_link = content["image_link"]
        self.price = content["price"]      
        
        
    def __str__(self):
        return f"<a href='{self.link}'>{self.title}: "+ str(self.price)+' €</a>'
    
    def __repr__(self):
        return self.__str__()