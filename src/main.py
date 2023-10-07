import requests
from bs4 import BeautifulSoup

class Crawler:
    def request_data(self, url: str):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
    def extract_from_panini(self):
        raw_panini = self.request_data("https://panini.com.br/planet-manga?product_list_order=most_recent")
        mangas =  raw_panini.find_all('div', {'class': 'product-item-info'}) #Obtem os mangas

        print("******************** SITE PANINI ********************")
        for index, manga in enumerate(mangas):
            if manga:
                title = manga.find('a', {'class':'product-item-link'}) #Obtem o nome
                price = manga.find('span', {'class':'price'}) #Obtem o preço
                image = manga.find('img', {'class':'product-image-photo'}) #Obtem o link para a imagem
                
                if title and price and image: #Caso não consiga obter 1 das informações, o produto não é printado.
                    result = {
                        'title': title.text,
                        'price': price.text,
                        'image': image.attrs['srcset']
                    }
                    #Organiza o print do produto no terminal
                    print(f"#################### MANGA {index+1} ####################\n")
                    print(f"Titulo: {result['title']}")
                    print(f"Preço: {result['price']}")
                    print(f"Link para imagem: {result['image']}")
                    print("\n")
    
    def extract_from_mundos_infinitos(self):
        raw_mundos_infinitos = self.request_data("https://mundosinfinitos.com.br/geek/vitrines/mundo-manga.aspx")
        mangas =  raw_mundos_infinitos.find_all('div', {'class': 'box-produto'}) #Obtem os mangas

        print("******************** SITE MUNDOS INFINITOS ********************")
        for index, manga in enumerate(mangas):
            if manga:
                # A tag que tinha o nome do manga não estava bem definida, por isso tive que usar o atributo target, sendo que, primeiro eu filtro pela classe descrição 
                # para indicar que estou procurando o nome do mangá pois outros elementos utilizavam o atributo target.
                title = manga.find('div', {'class':'descricao'}).find('a', {'target':'_top'})
                price = manga.find('p', {'class':'preco-por'}) #Obtem o preço
                image = manga.find('img', {'class':'img-fluid'}) #Obtem o link para a imagem
                
                if title and price and image: #Caso não consiga obter 1 das informações, o produto não é printado.
                    result = {
                        'title': title.text,
                        'price': price.text,
                        'image': image.attrs['src']
                    }
                    #Organiza o print do produto no terminal
                    print(f"#################### MANGA {index+1} ####################\n")
                    print(f"Titulo: {result['title']}")
                    print(f"Preço: {result['price']}")
                    print(f"Link para imagem: {result['image']}")
                    print("\n")


if __name__ == "__main__":
    crawler = Crawler()
    crawler.extract_from_panini()
    crawler.extract_from_mundos_infinitos()