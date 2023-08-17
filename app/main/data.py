import pandas as pd
from .models import Animals, Species

PAGE_COUNT = 5
status_dict = {
    "1": "[1]", # 공고중
    "2": "[2]", # 입양가능
    "3": "[3,4,7,8,9,11,12]", # 기타
    "4": "[5,6,10]" # 종료
}

# 유기동물 데이터를 불러오는 클래스
class AnimalData:
    def __init__(self, haircolors):
        self.haircolors = haircolors
        pass

    def search(self, params):
        print(params)
        query = Animals.objects.all()
        # 대분류 (개, 고양이, 기타)
        query = query.filter(classification=params["classification"])
        # expr = f"classification == {params['classification']}"
        # 성별 구분
        if params["gender"] != "0":
            query = query.filter(gender=params["gender"])
        #     expr += f" and gender == {params['gender']}"
        # 지역 구분
        # if params["gu"] != "0":
        #     expr += f" and gu == {params['gu']}"
        # 종 구분
        # if params["species"] != "":
        #     expr += f" and species == '{params['species']}'"
        # 공고 상태
        # if params["status"] != "0":
        #     expr += f" and adoptionStatusCd in {status_dict[params['status']]}"
        # 털색 구분

        # 날짜 최신순 정렬
        query = query.order_by("-rescue_date")
        
        # exprs_color = []
        # for i, (key, value) in enumerate(self.haircolors.items()):
        #     if params["haircolors"][i]:
        #         exprs_color.append(f"{key} == 1")
        # if len(exprs_color) > 0:
        #     expr += " and ("
        #     expr += " or ".join(exprs_color)
        #     expr += ")"
        # print(expr)
            
        # query 실행
        p = (int(params["page"]) - 1) * PAGE_COUNT
        query_set = query.values()
        total_count = query_set.count()
        query_set = query_set[p:p + PAGE_COUNT]
        count = query_set.count()
        
        # queryset to list
        query_set = list(query_set)
        # list to json
        df = pd.DataFrame(query_set)
        
        species = Species.objects.all().values()
        df_species = pd.DataFrame(species)
        df_species = df_species[["id", "name_kr"]]
        dict_species = df_species.set_index("id").to_dict()["name_kr"]
        df["species"] = df["species"].map(dict_species)
        df["rescue_date"] = df["rescue_date"].astype(str)
        json = df.to_json(orient="records")
        return json, count, total_count

