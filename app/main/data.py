import pandas as pd
from .models import Animals, Species

PAGE_COUNT = 12
status_dict = {
    1: [1], # 공고중
    2: [2], # 입양가능
    3: [3,4,7,8,9,11,12], # 기타
    4: [5,6,10] # 종료
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
        query = query.filter(classification=int(params["classification"]))
        # 성별 구분
        if params["gender"] != 0:
            query = query.filter(gender=int(params["gender"]))
        # 지역 구분
        if params["gu"] != 0:
            query = query.filter(gu=int(params["gu"]))
        # 종 구분
        if params["species"] != 0:
            print(params["species"])
            query = query.filter(species=int(params["species"]))
        # 공고 상태
        if params["status"] != 0:
            query = query.filter(status__in=status_dict[int(params["status"])])

        # 날짜 최신순 정렬
        query = query.order_by("-rescue_date")
            
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
        return json, count, total_count

