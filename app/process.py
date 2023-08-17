import pandas as pd
import sqlite3

def save_animals(df):
    # Connect to (create) database.
    database = "db.sqlite3"
    conn = sqlite3.connect(database)
    dtype={
        'id': 'AutoField', 
        'status': 'DecimalField', 
        'classification': 'DecimalField',
        'species': 'DecimalField', 
        'is_mix': 'BooleanField', 
        'gender': 'DecimalField', 
        'age': 'TextField', 
        'weight': 'DecimalField', 
        'haircolor': 'BinaryField', 
        'filepath': 'TextField', 
        'gu': 'DecimalField', 
        'locate': 'TextField',
    }
    df.to_sql(name='main_animals', con=conn, if_exists='replace', dtype=dtype)
    conn.close()

def save_species(df):
    # Connect to (create) database.
    database = "db.sqlite3"
    conn = sqlite3.connect(database)
    dtype={
        'id': 'AutoField', 
        'classification': 'DecimalField', 
        'name': 'TextField', 
        'name_kr': 'TextField', 
    }
    df.to_sql(name='main_species', con=conn, if_exists='replace', dtype=dtype)
    conn.close()

def clear_animals():
    # Connect to (create) database.
    database = "db.sqlite3"
    conn = sqlite3.connect(database)
    cur = conn.cursor()
    cur.execute("DELETE FROM main_animals")
    conn.commit()
    conn.close()

# Save to database.
df = pd.read_csv("main/data/animals_data.csv", encoding="utf-8-sig")
save_animals(df)
df = pd.read_csv("main/data/species_data.csv", encoding="utf-8-sig")
save_species(df)

# Clear database.
# clear_animals()