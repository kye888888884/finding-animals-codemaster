import numpy as np
import pandas as pd
from .models import Animals, Species
from .apps import MainConfig

PAGE_COUNT = 12
status_dict = {
    1: [1], # 공고중
    2: [2], # 입양가능
    3: [3,4,7,8,9,11,12], # 기타
    4: [5,6,10] # 종료
}

def norm(mean,std,x):
    return (x - mean) / std

def calSimilarity(sub, limitVal, is_cat = False):
    mat = MainConfig.feature_cat if is_cat else MainConfig.feature_dog

    result = []
    
    for i in range(len(mat)):
        feaVal = np.array(mat.iloc[i])
        tmp = feaVal[:-2] - sub
        tmp = abs(tmp)
        cal = np.sum(tmp)
        mat["similarity"][i] = cal

    if is_cat:
        m=mat["similarity"].max()
        s=mat["similarity"].min()
    else:
        m=mat["similarity"].mean()
        s=mat["similarity"].std()
    
    # for i in range(len(mat)):
    #     mat["similarity"][i] = norm(m,s,mat["similarity"][i])
    #     if mat["similarity"][i] <= limitVal:
    #         result.append(mat["id"][i])
    
    df = pd.DataFrame(mat, columns=['id', 'similarity'])
    df = df.sort_values(by=['similarity'], axis=0)
    df = df.reset_index(drop=True)
    df = df[:12]
    result = df["id"].tolist()

    return result

# 유기동물 데이터를 불러오는 클래스
class AnimalData:
    def __init__(self, haircolors):
        self.haircolors = haircolors
        pass

    def search(self, params):
        is_cat = int(params["classification"]) == 2

        sim_query = Animals.objects.none()
        if params["on_sim"]:
            pred = params["pred"][1:-1].split(",") # [1:-1] : 괄호 제거
            pred = list(map(float, pred))
            pred = np.array(pred, dtype="float64")

            limitVal = 0.0 if is_cat else -3.0
            seq_list = calSimilarity(pred, limitVal, is_cat)[:12]
            
            # get queryset from seq_list by searching id
            for seq in seq_list:
                sim_query |= Animals.objects.filter(id=seq)
        # print(sim_query)

        sim_count = sim_query.count()

        # print(params)
        query = Animals.objects.all()
        # 대분류 (개, 고양이, 기타)
        query = query.filter(classification=int(params["classification"]))
        # 성별 구분
        if params["gender"] != 0:
            query = query.filter(gender=int(params["gender"]))
        # 지역 구분
        if params["gu"] != 0:
            query = query.filter(gu=int(params["gu"]))
        # 종 구분
        if params["species"] != 0:
            query = query.filter(species=int(params["species"]))
        # 공고 상태
        if params["status"] != 0:
            query = query.filter(status__in=status_dict[int(params["status"])])

        # 날짜 최신순 정렬
        query = query.order_by("-rescue_date")
        
        # 유사도 검색 결과와 합치기
        query = sim_query | query
        query = query.distinct() # 중복 제거
            
        # query 실행
        query_set = query.values()

        # 페이지네이션
        p = (int(params["page"]) - 1) * PAGE_COUNT
        total_count = query_set.count()
        query_set = query_set[p:p + PAGE_COUNT]
        count = query_set.count()
        
        # queryset to list
        query_set = list(query_set)
        df = pd.DataFrame(query_set, columns=['index', 'id', 'status', 'classification', 'species', 'is_mix', 'gender', 'age', 'weight', 'haircolor', 'filepath', 'gu', 'locate', 'rescue_date'])

        df["rescue_date"] = df["rescue_date"].astype(str)
        json = df.to_json(orient="records")
        return json, count, total_count, sim_count

