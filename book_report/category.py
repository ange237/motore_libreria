import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

"""4)report di una singola categoria di libri ==> dato il nome di una categoria, generare un report contenente: 
numero di libri nella categoria,prezzo medio, anno piu frequente di pubblicazione,autori principali,editori 
piu frequenti, grafico libri per autore e/o per editore"""

#numero di libri nella categoria
def get_num_libri_category(df,category):
    df_category = df[df["category"] == category]
    ##numero di libri nella categoria
    return (df_category["isbn"].count())

#prezzo medio della categoria
def get_avg_price_category(df,category):
    df_category = df[df["category"] == category]
    return round(df_category["price_in_euros"].mean())


#anno piu frequente di pubblicazione della categoria
def get_year_max_publication_category(df,category):
    df_category = df[df["category"] == category]
    df_anno = df_category.groupby("publication_year").count().sort_values(by = 'book_name', ascending = False)
    anno = (df_anno.index.tolist())[0]
    return anno


#lista dei 5 principali autori della categoria
def get_list_author_category(df,category):
    df_category = df[df["category"] == category]
    list_autore = df_category.groupby('author').count().sort_values(by = 'isbn', ascending = False).index.tolist()
    return list_autore[:5]



#lista dei 5 editori  piu frequenti della categoria
def get_list_publisher_category(df,category):
  df_category = df[df["category"] == category]
  list_editori = df_category.groupby('publisher').count().sort_values(by = 'isbn', ascending = False).index.tolist()
  return list_editori[:5]

# grafico numero di libri per i 5 autori principali di una categoria 
def graph_num_libri_author_category(df,category):
 df_category = df[df["category"] == category]
 df_category = df_category.groupby('author').size().sort_values(ascending=False).reset_index(name='num_libri')
 df_category = df_category.head(5)  # Prendi i primi 5 autori
 print(df_category)

 fig, ax = plt.subplots()
 sns.barplot(data=df_category, x="author", y="num_libri", ax=ax)
 ax.set_title(f"numero di libri per i 5 autori piu frequenti ddella categoria  {category}")
 ax.set_xlabel("autore/i")
 ax.set_ylabel("Numero di pubblicazioni")
 ax.grid(True)
 ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))#solo interi sull'asse y
 plt.xticks(rotation=15)
 #ritorna il grafico
 return fig



#grafico numero libri per i 5 editori principali di una categoria 
def graph_num_libri_publisher_category(df,category):
 df_category = df[df["category"] == category]
 df_category = df_category.groupby('publisher').size().sort_values(ascending=False).reset_index(name='num_libri')
 df_category = df_category.head(5)  # Prendi i primi 5 autori
 print(df_category)

 fig, ax = plt.subplots()
 sns.barplot(data=df_category, x="publisher", y="num_libri", ax=ax)
 ax.set_title(f"numero di libri per i 5 editori piu frequenti ddella categoria  {category}")
 ax.set_xlabel("editore/i")
 ax.set_ylabel("Numero di pubblicazioni")
 ax.grid(True)
 ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))#solo interi sull'asse y
 plt.xticks(rotation=15)
 #ritorna il grafico
 return fig