from site_parser.parser import Parser
from immo import Immobilie
import re

class ImmoweltParser(Parser):
    def __init__(self, stadt:str, max_price:int, radius=10):
        super().__init__()
        self.stadt = stadt
        self.max_price = max_price
        self.radius = radius
        self.website = f"https://www.immowelt.de/liste/{self.stadt}/haeuser/kaufen?d=true&r={self.radius}&sd=DESC&sf=TIMESTAMP&sp=1"
        
    def document_parser(self, document):
        articles = document.find_all('div', class_="EstateItem-1c115")
        items = []
        
        for n, article in enumerate(articles):
            price_string = document.find_all('div', class_="KeyFacts-efbce")[n].div.text
            immo_dict = {"id": article.a['id'],
                         "link": article.a['href'],
                         "title": article.h2.text,
                         "image_link": article.img['data-src']}
            try:
                immo_dict["price"]= int("".join(re.findall(r'\d+',price_string)))
            except:
                immo_dict["price"]= 42

            if immo_dict["id"] not in self.already_seen:
                items.append(Immobilie(immo_dict))
                self.already_seen.append(immo_dict["id"])
                
        return items