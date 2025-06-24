import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
#import dataloader
#contiene tutte le funzioni per il report di un editore( publisher)


#numero totale di libri pubblicati
def get_tot_book_publisher(df,publisher):
  df_pub = df[df["publisher"] == publisher]
  num_books = len(df_pub)
  return  num_books 

#prezzo medio dei libri
def get_med_price_publisher(df,publisher):
 df_pub = df[df["publisher"] == publisher]
 avg_price = df_pub["price_in_euros"].mean()
 return round(avg_price)



#i 5 autori principali(quali autori pubblicano di piu con questo editore)
def get_5_author_publisher(df,publisher):
 df_pub = df[df['publisher'] == publisher]
 df_pub = df_pub.groupby('author').count()
 df_sorted_autthor = df_pub.sort_values(by='book_name', ascending=False)
 df_sorted_autthor = df_sorted_autthor.head()
 list_autori = df_sorted_autthor.index.tolist()
 return list_autori

# lista delle 5 categorie piu frequenti
def get_5_category_publisher(df,publisher):
 df_pub = df[df['publisher'] == publisher]
 list_category = df_pub.groupby('category').count()
 list_category = list_category.sort_values(by='isbn', ascending=False)
 list_category = list_category.index.tolist()
 return list_category[:5]
   

#grafico numero di libri per gli ultimi dieci anni di pubblicazione
def get_graph_libri_anno_publisher(df,publisher):
 df_pub = df[df['publisher'] == publisher]

 df_cont = df_pub.groupby('publication_year').size().reset_index(name='num_libri')
 df_cont = df_cont.tail(10)
 print(df_cont)

 fig, ax = plt.subplots()
 sns.barplot(data=df_cont, x="publication_year", y="num_libri", ax=ax)
 ax.set_title(f"numero di libri per gli ultimi dieci anni di pubblicazione per {publisher}")
 ax.set_xlabel("anno/i")
 ax.set_ylabel("Numero di libri")
 ax.grid(True)

 #ritorna il grafico
 return fig



#grafico  a barre numero di libri per i 10 autori piu frequenti dell'editore
def get_graph_libri_autore_publisher(df,publisher):
 df_pub = df[df['publisher'] == publisher]
 df_cont = df_pub.groupby('author').size().reset_index(name='num_libri')
 df_cont = df_cont.sort_values(by='num_libri', ascending=False)
 df_cont = df_cont.head(10)
 #print(df_cont)

 fig, ax = plt.subplots()
 sns.barplot(data=df_cont, x="author", y="num_libri", ax=ax)
 ax.set_title(f"numero di libri per i 10 autori piu frequenti di {publisher}")
 ax.set_xlabel("autore/i")
 ax.set_ylabel("Numero di pubblicazioni")
 #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))  # solo interi sull'asse y
 ax.grid(True)
 plt.xticks(rotation=25)
 #ritorna il grafico
 return fig

#grafico  numero di libri per le 5 categorie  piu frequenti
def get_graph_libri_category_publisher(df,publisher):
 df_pub = df[df['publisher'] == publisher]
 df_cont = df_pub.groupby('category').size().reset_index(name='num_libri')
 df_cont = df_cont.sort_values(by='num_libri', ascending=False)
 df_cont = df_cont.head(5)
 #print(df_cont) 

 fig, ax = plt.subplots()
 sns.barplot(data=df_cont, x="category", y="num_libri", ax=ax)
 ax.set_title(f"numero di libri per le 5 categorie piu frequenti di {publisher}")
 ax.set_xlabel("categorie")
 ax.set_ylabel("Numero di pubblicazioni")
 ax.yaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))
 ax.grid(True)
 #ritorna il grafico
 return fig