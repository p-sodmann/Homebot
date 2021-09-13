from bs4 import BeautifulSoup
import requests


class Parser:
    def __init__(self):
        self.already_seen = []
    
    def document_parser(self, document):
        return []
    
    def __call__(self, callback):
        # recover context
        context = callback.job.context
        
        # tell the website who we are
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        
        # download website        
        page = requests.get(self.website, headers=headers)
        return_items = []
        
        # check if we got a result
        if page.status_code == 200:
            content = page.content
            
            document = BeautifulSoup(content, 'html.parser')
            items = self.document_parser(document)

            for item in items:
                if item.id not in context.user_data["already_seen"]:
                    context.user_data["already_seen"].append(item.id)
                    return_items.append(item)

        print(f"found {len(return_items)} items")

        return return_items