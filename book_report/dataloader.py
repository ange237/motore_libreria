# caricare il csv in un dataframe
import pandas as pd
#from app.config import CSV_PATH 

#funzione per caricare il CSV in un DataFrame e ritornare il DataFrame
def load_dataset():
    try:
      df = pd.read_csv("C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\motore_libreria\\book_report\\data\\dataset_progetto_pulito.csv")
      return df
      #print(df.head())  # Stampa le prime righe del DataFrame per verifica
    except Exception as e:
       print(f"ERRORE :{e}")  


#df =load_dataset()  # Chiamata alla funzione per caricare il dataset
#per stampare il numero di libri scriti da uno stesso authore

#print(df.groupby("author").count())  # Esempio di operazione sul DataFrame