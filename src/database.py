from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

class Database:
    def __init__(self) -> None:
        load_dotenv()
        self.mangas = self.connect()
    
    
    def connect(self):
        client = MongoClient(os.getenv('DB_URI'))
        collection = client['curso_crawler']
        return collection.mangas
    
    def insert(self, data: dict):
        try:
            filter = {'title': data['title']}
            result = self.mangas.find_one(filter, sort=[('date', -1)])
            if result is None or (result['price'] > data['price'] or result['price'] < data['price']):
                self.mangas.insert_one(data)
        except:
            return None
        return data
    
    def search(self, target, value):
        if target not in ['title', 'price', 'image']: #Validação para que o ususário insira campos válidos.
            print("Campo de busca inválido.\n")
            return
        result = list(self.mangas.find({target:{ '$regex': f"{value}"}}))
        if result is None:
            print("Não foi possivel encontrar o dado especificado.\n")
        else:
            print("Dado encontrado com sucesso.\n")
            print(result)


if __name__ == "__main__":
    db = Database()
    data = {"title": "Kemono Jihen - Incidentes Sobrenaturais Vol. 15", "price": "R$36,90", "image": "https://d14d9vp3wdof84.cloudfront.net/image/589816272436/image_h0cn0nu2ch69v850798c244f1n/-S300-FWEBP"}
    db.insert(data)