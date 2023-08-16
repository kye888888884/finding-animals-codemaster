import pandas as pd

PAGE_COUNT = 5
status_dict = {
    "1": "[1]", # 공고중
    "2": "[2]", # 입양가능
    "3": "[3,4,7,8,9,11,12]", # 기타
    "4": "[5,6,10]" # 종료
}

# 유기동물 데이터를 불러오는 클래스
class AnimalData:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = None
        self.load_data()
    
    def load_data(self):
        self.data = pd.read_csv(self.data_path + "animals_data.csv")

    def search(self, params):
        print(params)
        expr = f"classification == {params['classification']}"
        if params["gender"] != "0":
            expr += f" and gender == {params['gender']}"
        if params["gu"] != "0":
            expr += f" and gu == {params['gu']}"
        if params["species"] != "":
            expr += f" and species == '{params['species']}'"
        # if params["haircolor"] != "":
        #     expr += f" and hairColor == '{params['haircolor']}'"
        if params["status"] != "0":
            expr += f" and adoptionStatusCd in {status_dict[params['status']]}"
        
        df_q = self.data.query(expr)
        # rescueDate를 기준으로 내림차순 정렬
        df_q = df_q.sort_values(by=["rescueDate"], ascending=False)
        total_count = len(df_q)
        
        p = (int(params["page"]) - 1) * PAGE_COUNT
        df_q = df_q.iloc[p:p + PAGE_COUNT]
        count = len(df_q)
        
        result = df_q.to_json(orient="records")
        return result, count, total_count

