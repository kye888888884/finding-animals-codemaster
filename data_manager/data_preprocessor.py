import pandas as pd
import numpy as np

base_path = './data/'
save_path = '../app/main/data/'
filename = 'animals_data.csv'

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
    
    return df

def split_mix(df):
    # 값이 0인 isMix열 추가
    df['isMix'] = 0

    # species열에 '믹스'가 포함될 경우 isMix열을 1로 변경
    df.loc[df['species'].notnull() & df['species'].str.contains('믹스'), 'isMix'] = 1
    # species열에서 '믹스'를 제거
    df['species'] = df['species'].str.replace(' 믹스', '')
    df['species'] = df['species'].str.replace('믹스', '')

    return df

def modify_filepath(df):
    df['filePath'] = df['filePath'].str.replace('FileUpload/ANI/', '')
    return df

df = pd.read_csv(base_path + 'animals_data.csv')
df = set_haircolor(df)
df = split_mix(df)
df = modify_filepath(df)
df.to_csv(save_path + 'animals_data.csv', encoding='utf-8-sig')