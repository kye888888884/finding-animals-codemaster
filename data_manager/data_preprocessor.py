import pandas as pd
import numpy as np

load_path = './data/'
save_path = '../app/main/data/'
load_filename = 'animals_raw_data.csv'
save_filename = 'animals_data.csv'

color_dict = {
    'colorWhite': ['백'],
    'colorBlack': ['검', '흑'],
    'colorBrown': ['갈', '초코', '밤'],
    'colorYellow': ['노', '황'],
    'colorGray': ['회', '은'],
    'colorOther': ['녹', '록', '청', '파'],
}

def set_haircolor(df):
    for k in color_dict.keys():
        df[k] = 0

    for key, colors in color_dict.items():
        for color in colors:
            df.loc[df['hairColor'].notnull() & df['hairColor'].str.contains(color), key] = 1
    
    # hairColor열의 값을 colorWhite, colorBlack, colorBrown, colorYellow, colorGray, colorOther열의 이진 값으로 변경
    df['hairColor'] = 0
    for i, key in enumerate(color_dict):
        df['hairColor'] = df['hairColor'] + df[key] * (2 ** i)
    
    return df

def verify_species(df):
    verify_data = pd.read_csv(load_path + 'speciesMap.csv', encoding='utf-8-sig')
    # verify_data의 old열이 df의 species열에 포함되면 해당 값을 new열로 변경
    for i in range(len(verify_data)):
        df.loc[df['species'].notnull() & df['species'].str.contains(verify_data['old'][i]), 'species'] = df.loc[df['species'].notnull() & df['species'].str.contains(verify_data['old'][i]), 'species'].str.replace(verify_data['old'][i], verify_data['new'][i])
    return df

def split_mix(df): # Species열의 공백 제거, isMix열 추가
    # species열의 공백 제거
    df['species'] = df['species'].str.replace(' ', '')

    # 값이 0인 isMix열 추가
    df['isMix'] = 0

    # species열에 '믹스'가 포함될 경우 isMix열을 1로 변경
    df.loc[df['species'].notnull() & df['species'].str.contains('믹스'), 'isMix'] = 1
    # species열에서 '믹스'를 제거
    df['species'] = df['species'].str.replace(' 믹스', '')
    df['species'] = df['species'].str.replace('믹스', '')
    # species열이 ''와 같으면 믹스로
    df.loc[df['species'] == '', 'species'] = '믹스'

    return df

def get_species_id(df):
    species_names = pd.read_csv(load_path + 'speciesNames.csv', encoding='utf-8-sig')
    # species_names에서 name_kr열을 key로, id열을 value로 하는 딕셔너리 생성
    species_dict = dict(zip(species_names['name_kr'], species_names['id']))
    df['species'] = df['species'].map(species_dict)
    # species열의 값이 없으면 0으로 변경
    df.loc[df['species'].isnull(), 'species'] = 0
    # species열의 값을 정수형으로 변경
    df['species'] = df['species'].astype(int)
    return df

def modify_filepath(df):
    df['filePath'] = df['filePath'].str.replace('FileUpload/ANI/', '')
    return df

def remove_estimate_text(df):
    df['age'] = df['age'].str.replace('(추정)', '')
    df['weight'] = df['weight'].str.replace('(추정)', '')
    return df

def refine_weight(df):
    removes = ['kg', '(Kg)', 'Kg']
    for remove in removes:
        df['weight'] = df['weight'].str.replace(remove, '')
    return df

def modify_columns(df):
    columns = ['animalSeq', 'adoptionStatusCd', 'classification', 'species', 'isMix', 'gender', 'age', 'weight', 'hairColor', 'filePath', 'gu', 'foundPlace', 'rescueDate']
    df = df[columns]
    # animalSeq열의 이름을 id로 변경
    renames = {
        'animalSeq': 'id',
        'adoptionStatusCd': 'status',
        'isMix': 'is_mix',
        'hairColor': 'haircolor',
        'filePath': 'filepath',
        'foundPlace': 'locate',
        'rescueDate': 'rescue_date'
    }
    df.rename(columns=renames, inplace=True)
    return df

df = pd.read_csv(load_path + load_filename, encoding='utf-8-sig')
df = set_haircolor(df)
df = verify_species(df)
df = split_mix(df)
df = get_species_id(df)
df = modify_filepath(df)
df = remove_estimate_text(df)
df = refine_weight(df)
df = modify_columns(df)
df.to_csv(save_path + save_filename, encoding='utf-8-sig', index=False)
df.to_csv(load_path + save_filename, encoding='utf-8-sig', index=False)