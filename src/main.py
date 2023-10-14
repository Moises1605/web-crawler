import requests
from bs4 import BeautifulSoup
import schedule
from datetime import datetime
from database import Database
from dotenv import load_dotenv

class Crawler:

    def __init__(self) -> None:
        load_dotenv()
        self.db = Database()
    
    def request_data(self, url: str) -> BeautifulSoup:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup
    
    def format(self, price: str) -> float:
        print(price)
        return float(price.replace("R$", '').replace(",", "."))

    def extract_from_panini(self, page: int) -> None:
        raw_panini = self.request_data(f"https://panini.com.br/planet-manga?p={page}")
        mangas =  raw_panini.find_all('div', {'class': 'product-item-info'}) #Obtem os mangas
        for index, manga in enumerate(mangas):
            if manga:
                title = manga.find('a', {'class':'product-item-link'}) #Obtem o nome
                price = manga.find('span', {'class':'price'}) #Obtem o preço
                image = manga.find('img', {'class':'product-image-photo'}) #Obtem o link para a imagem
                
                if title and price and image: #Caso não consiga obter 1 das informações, o produto não é printado.
                    result = {
                        'title': title.text,
                        'price': self.format(price.text),
                        'image': image.attrs['srcset'],
                        'date': datetime.now()
                    }

                    result = self.db.insert(data=result) #Inserção no banco de dados
                    if(result):
                        print("Operação realizada com sucesso")
                    else:
                        print("Erro ao adicionar dado no banco de dados")
    
    def extract_from_mundos_infinitos(self, page: int) -> None:
        raw_mundos_infinitos = self.request_data(f"https://mundosinfinitos.com.br/geek/vitrines/mundo-manga.aspx?pg={page}")
        mangas =  raw_mundos_infinitos.find_all('div', {'class': 'box-produto'}) #Obtem os mangas
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
                        'price': self.format(price.text[0:price.text.index(',')+3]),
                        'image': image.attrs['src'],
                        'date': datetime.now()
                    }

                    result = self.db.insert(data=result) #Inserção no banco de dados
                    print(result)
                    if(result):
                        print("Operação realizada com sucesso")
                    else:
                        print("Erro ao adicionar dado no banco de dados")
    
    def execute(self, num_pages: int) -> None:
        for page in range(1, num_pages):
             self.extract_from_panini(page)
             self.extract_from_mundos_infinitos(page)

if __name__ == "__main__":
    crawler = Crawler()
    #crawler.extract_from_panini(2)
    #crawler.extract_from_mundos_infinitos(2)
    #Chama a função que realiza a busca no banco, indicando qpor qual tipo de valor será buscado (title, price, image) e o valor que será procurado. A bsuca é realiza como se fosse utilizando o ilike do sql.
    #crawler.db.search(target='title', value="Ayashimon")
    
    # Caso queira testar a parte de pesquisa, basta descomentar essa parte de cima, e comentar essa parte logo abaixo.
    def job() -> None:
        print("\n Execute job. Time: {}".format(str(datetime.now())))
        crawler.execute(1)
    schedule.every(1).minutes.do(job)
    while True:
        schedule.run_pending()