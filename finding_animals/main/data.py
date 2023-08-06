import pandas as pd

# 유기동물 데이터를 불러오는 클래스
class AnimalData:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data_species = None
        self.data_haircolor = None
        self.data = None
        self.load_data()
    
    def load_data(self):
        self.data = pd.read_csv(self.data_path + "유기동물_데이터.csv")

        self.data_species = pd.read_csv(self.data_path + "unique/species.csv")
        self.data_species = self.data_species.dropna()
        self.data_species = self.data_species.sort_values(by=["species"])
        
        self.data_haircolor = pd.read_csv(self.data_path + "unique/hairColor.csv")
        self.data_haircolor = self.data_haircolor.dropna()
        self.data_haircolor = self.data_haircolor.sort_values(by=["hairColor"])

    def search(self, params):
        return