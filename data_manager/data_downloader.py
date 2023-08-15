import requests
import key # Service key

import json
import xmltodict

import pandas as pd
import numpy as np

url = 'http://apis.data.go.kr/6300000/animalDaejeonService/animalDaejeonList'
PAGE_NUM = 100
classes = [
    "adoptionStatusCd",
    "age",
    "animalSeq",
    "classification",
    "fileNm",
    "filePath",
    "foundPlace",
    "gender",
    "gu",
    "hairColor",
    "hitCnt",
    "memo",
    "modDtTm",
    "regDtTm",
    "regId",
    "rescueDate",
    "species",
    "weight",
];

def response_to_dict(response) -> dict:
    jsonString = response.content.decode('utf-8')
    jsonString = json.dumps(xmltodict.parse(jsonString), indent=4)
    jsonObj = json.loads(jsonString)
    return jsonObj

def get_response_dict(page: int) -> dict:
    response = requests.get(url, params={'serviceKey' : key.SERVICE_KEY, 'pageNo' : page, 'numOfRows' : PAGE_NUM})
    data = response_to_dict(response)
    return data

def get_count():
    data = get_response_dict(1)
    total_count = data['ServiceResult']['msgHeader']['totalCount']
    total_page = data['ServiceResult']['msgHeader']['totalPage']
    return int(total_count), int(total_page)

def get_animal_list(page):
    data = get_response_dict(page)
    li = data["ServiceResult"]["MsgBody"]["items"]
    return li

def get_dataframe():
    df = pd.DataFrame(columns=classes)
    count, page = get_count()
    for i in range(1, page+1):
        animal_list = get_animal_list(i)
        for animal in animal_list:
            li = []
            for c in classes:
                try:
                    li.append(animal[c])
                except:
                    li.append(None)
            df.loc[len(df)] = li
            print(f"{i}/{page}", end='\r')
    return df

# csv 저장
df = get_dataframe()
df.to_csv('./data/animals_data.csv', index=False, encoding='utf-8-sig')