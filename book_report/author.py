import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
"""1)report su un singolo autore ==> dato il nome di un autore, generare un report contenente: 
il numero totale di libri che ha scritto,prezzo medio dei libri,anno di publicazione piu  ricorrente,
gli editori con cui ha publicato i suoi libri, il suo libro piu recente,categorie principali dei suoi libri,
il suo valore totale in euro,grafico di conteggio libri per anno e categoria"""


#numero totale di libri che ha scritto l'autore
def get_tot_book_author(df,author):
    df_author = df[df["author"] == author]
    num_books = len(df_author) 
    return num_books


#prezzo medio dei libri scritti dall'autore
def med_price_author(df,author):
    df_author = df[df["author"] == author]
    avg_price = df_author["price_in_euros"].mean()
    return avg_price


#anno di publicazione piu  ricorrente per l'autore 
def get_year_max_publication(df,author):
    df_author = df[df["author"] == author]
    df_anno = df_author.groupby('publication_year').count().sort_values(by ='isbn', ascending = False)
    return ((df_anno.index.tolist())[0])


#lista degli editori con cui ha publicato i suoi libri
def get_list_publisher_author(df,author):
    df_author = df[df["author"] == author]
    return df_author.groupby('publisher').count().index.tolist()



# libro piu recente dell'autore
def get_recent_book_author(df,author):
    df_author = df[df["author"] == author]
    libro = df_author.sort_values(by = 'publication_year', ascending = False)
    return ((libro['book_name'].tolist())[0])

#lista categorie principali dei  dell'autore
def get_list_category_author(df,author):
    df_author = df[df["author"] == author]
    return df_author.groupby('category').count().sort_values(by ='isbn', ascending = False).index.tolist()
    


#il suo valore totale in euro(totale prezzo dei suoi libri)
def get_value_author(df,author):
    df_author = df[df["author"] == author]
    value = df_author['price_in_euros'].sum()
    return round(value)


#grafico a barra/linee  di conteggio numero di libri per gli  ultimi 5 anni di pubblicazione
def graph_libri_anno_author(df,author):
    df_author = df[df["author"] == author]
    df_cont = df_author.groupby('publication_year').size().reset_index(name='num_libri')
    df_cont = df_cont.tail(5)  # Prendi gli ultimi 5 anni

    fig, ax = plt.subplots()
    sns.lineplot(data=df_cont, x="publication_year", y="num_libri", marker="o", ax=ax)
    ax.set_title(f"Pubblicazioni di {author} negli ultimi 5 anni")
    ax.set_xlabel("Anno di pubblicazione")
    ax.set_ylabel("Numero di pubblicazioni")
    ax.grid(True)
    plt.xticks(rotation=25)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d'))

    return fig

#grafico di conteggio libri  per categoria per l'autore
def graph_libri_categoria_author(df,author):
    df_author = df[df["author"] == author]
    df_cont = df_author.groupby('category').size().reset_index(name='num_libri')
    print(df_cont)

    fig, ax = plt.subplots()
    sns.barplot(data=df_cont, x="category", y="num_libri", ax=ax)
    ax.set_title(f"numero di libri per categoria  di {author} ")
    ax.set_xlabel("categoria")
    ax.set_ylabel("Numero di pubblicazioni")
    plt.xticks(rotation=25)
    ax.grid(True)
    

    return fig
