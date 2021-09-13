from site_parser.parser import Parser
from immo import Immobilie
import re


class EbayParser(Parser):
    def __init__(self, plz:str, max_price:int, radius=10):
        super().__init__()
        self.plz = plz
        self.max_price = max_price
        self.radius = radius
        self.website = f"https://www.ebay-kleinanzeigen.de/s-haus-kaufen/{self.plz}/c208l7700r{self.radius}"
        
    def document_parser(self, document):
        # check if we already run this parser and have set a "has seen" object for this user/context
        articles = document.find_all("article")
        items = []
        
        for article in articles:
            price_string = article.find_all("p", class_ = "aditem-main--middle--price")[0].text
            immo_dict = {"id": article['data-adid'],
            "link": 'https://www.ebay-kleinanzeigen.de'+article['data-href'],
            "title": article.find_all("a", class_ = "ellipsis")[0].text}
            # try to parse the price
            try:
                immo_dict["price"]= int("".join(re.findall(r'\d+',price_string)))
            except:
                immo_dict["price"]= 42
            # get the image link
            if "data-imgsrc" in article.a.div.attrs:
                immo_dict["image_link"]= article.a.div['data-imgsrc']
            else:
                immo_dict["image_link"]= None
            
            items.append(Immobilie(immo_dict))
                                
        return items