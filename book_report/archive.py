import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
"""2)report di tutta l'archivio ==> generare un report contenente: numero totale di libri, prezzo medio,
numero totale di autori ed editori, top 5 autori per numero di libri, top 5 editori , categoria piu presente, 
grafici:libri per anno ,libri per categoria, libri per autore,box plot dei prezzi medio per categoria o editore"""


# numero totale di libri dell'archivio
def get_tot_book_archive(df):
    return len(df)


#prezzo medio di un libro dell'archivio
def get_avg_price_archive(df):
   avg_price = df['price_in_euros'].mean()
   return round(avg_price)

#numero totale di autori 
def get_num_author_archive(df):
    num_autore = df['author'].tolist()
    return len(set(num_autore)) # uso det per rimuovere i duplicati.

#numero totale di  editori
def get_num_publisher_archive(df):
    num_editori = df['publisher'].tolist()
    return len(set(num_editori))

#lista dei  5 autori per numero di libri
def get_list_5_most_author_archive(df):
    list_autori = df.groupby('author').count().sort_values(by = 'isbn', ascending = False).index.tolist()
    return list_autori[:5]

#lista dei  5 editori per numero di libri
def get_list_5_most_publisher_archive(df):
    list_editori = df.groupby('publisher').count().sort_values(by = 'isbn', ascending = False).index.tolist()
    return list_editori[:5]

#lista delle  5 categorie per numero di libri
def get_list_5_most_category_archive(df):
    list_category = df.groupby('category').count().sort_values(by = 'isbn', ascending = False).index.tolist()
    return (list_category[:5])


#grafico libri per gli ultimi 5 anni
def graph_libri_anno_archive(df):
 df = df.groupby('publication_year').size().sort_values(ascending=False).reset_index(name='num_libri')
 df = df.head(5)  # Prendi i primi 5 anni piu recenti
 #print(df)

 fig, ax = plt.subplots()
 sns.barplot(data=df, x="publication_year", y="num_libri", ax=ax)
 ax.set_title(f"numero di libri per i gli ultimi 5 anni")
 ax.set_xlabel("anni")
 ax.set_ylabel("Numero di libri")
 ax.grid(True)
 ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))#solo interi sull'asse y
 #ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
 #plt.xticks(rotation=15)
 #ritorna il grafico
 return fig

#grafico a torta che rappresenta il percentuale di ogni categoria nell'archivio
def graph_libri_category_archive(df):
 """df['category'].value_counts().plot.pie(autopct='%1.0f%%')
 plt.ylabel('')
 plt.title('Distribuzione per categoria')
 plt.show()"""
 """sns.histplot(data=df, x='category', bins=10, kde=False)
 plt.title('Istogramma')
 plt.xlabel('Valore')
 plt.ylabel('Frequenza')
 plt.show()"""
 fig, ax = plt.subplots()
 df['category'].value_counts().plot.pie(autopct='%1.0f%%', ax=ax)
 ax.set_ylabel('')
 ax.set_title('Distribuzione per categoria')
 return fig  # restituisce la figura

#grafico a barre numero di libri per autore(i 5 autori piu presente nell'archivio)
def graph_libri_author_archive(df):
 df = df.groupby('author').size().sort_values(ascending=False).reset_index(name='num_libri')
 df = df.head(5)  # Prendi i primi 5 autori
 #print(df)

 fig, ax = plt.subplots()
 sns.barplot(data=df, x="author", y="num_libri", ax=ax)
 ax.set_title(f"numero di libri per i 5 editori piu presenti nell'archivio")
 ax.set_xlabel("autori")
 ax.set_ylabel("Numero di libri pubblicati")
 ax.grid(True)
 ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))#solo interi sull'asse y
 plt.xticks(rotation=15)
 #ritorna il grafico
 return fig

#grafico a barre  box plot dei prezzi medio per categoria 
def graph_avg_prezzi_categoria_archive(df):
 fig, ax = plt.subplots(figsize=(8, 4))
 sns.barplot(data=df, x='category', y='price_in_euros', estimator='mean', ax=ax)
 ax.set_title('Prezzo medio per categoria')
 ax.set_xlabel('Categoria')
 ax.set_ylabel('Prezzo medio')
 plt.xticks(rotation=45)
 plt.tight_layout()
 return fig



#grafico a barra del valore totale in euro di ogni categoria



#grafico a barra del valore totale in euro dei  5 autori con valoe piu alto


#grafico a linee che rappresenta l'evoluzione del numero di libri publicati ogni anno
