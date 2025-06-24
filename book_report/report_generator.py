# Génération des rapports PDF avec FPDF2

# app/services/report_generator.py

"""from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from io import BytesIO
import unicodedata




def sanitize_text(text: str) -> str:
    # remplace les guillemets spéciaux et accents
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # normalise pour enlever les accents
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

class PDFReport(FPDF):
    def __init__(self, title, logo_path, format='A3', auto=True):
        super().__init__()
        self.title = title
        self.logo_path = logo_path
        self.set_auto_page_break(auto=True, margin=30)

    def header(self):
        # Logo
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)
        # Titre
        self.set_font('Arial', 'B', 11)
        self.multi_cell(self.w - 2 * self.l_margin, 10, self.title, border=False, align='C')
        self.ln(10)

    def footer(self):
        # Numéro de page
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(self.w - 2 * self.l_margin, 10, f'Page {self.page_no()}', align='C')

    def add_text(self, text):
        self.set_font("Arial", size=11)
        clean_text = sanitize_text(text)
        self.multi_cell(self.w - 2 * self.l_margin, 10, clean_text)

    def add_image_plot(self, fig):
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        self.image(buffer, w=180)
        buffer.close()


# genera il report per un singolo autore
#la funzione riceve un DataFrame, le nom de l'auteur et le chemin du logo
def generate_author_report(df: pd.DataFrame, author: str, logo_path: str = "C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\motore_libreria\\book_report\\static\\agm_solutions_2.png") -> bytes:
    # Filtrage des livres de l'auteur
    df_author = df[df["author"] == author]

    # Création du PDF
    pdf = PDFReport(title= sanitize_text(f"Rapport pour l'auteur: {author}"), logo_path=logo_path)
    pdf.add_page()

    if df_author.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'auteur '{author}'.")
    else:
        # Infos générales
        num_books = len(df_author)
        avg_price = df_author["price_in_euros"].mean()

        pdf.add_text(f"L’auteur {author} a écrit {num_books} livres dans la base de données.")
        pdf.add_text(f"Prix moyen des livres : {avg_price:.2f} €")

        # Graphique : répartition par année
        fig, ax = plt.subplots()
        sns.countplot(data=df_author, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S')  # Retourne un PDF en bytes


#genera il report per un singolo editore
def generate_publisher_report(df: pd.DataFrame, publisher: str, logo_path: str = "C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\motore_libreria\\book_report\\static\\agm_solutions_2.png") -> bytes:
    df_pub = df[df["publisher"] == publisher]
    pdf = PDFReport(title= sanitize_text(f"Rapport pour l’éditeur: {publisher}"), logo_path=logo_path)
    pdf.add_page()

    if df_pub.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'éditeur '{publisher}'.")
    else:
        num_books = len(df_pub)
        avg_price = df_pub["price_in_euros"].mean()

        pdf.add_text(f"L’éditeur {publisher} a publié {num_books} livres.")
        pdf.add_text(f"Prix moyen : {avg_price:.2f} EUR")

        fig, ax = plt.subplots()
        sns.countplot(data=df_pub, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S')

#genera il report per una singola categoria di libri
def generate_category_report(df: pd.DataFrame, category: str, logo_path: str = "C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\motore_libreria\\book_report\\static\\agm_solutions_2.png") -> bytes:
    df_cat = df[df["category"] == category]
    pdf = PDFReport(title=sanitize_text(f"Rapport pour la catégorie: {category}"), logo_path=logo_path)
    pdf.add_page()

    if df_cat.empty:
        pdf.add_text(f"Aucun livre trouvé pour la catégorie '{category}'.")
    else:
        num_books = len(df_cat)
        avg_price = df_cat["price_in_euros"].mean()

        pdf.add_text(f"La catégorie {category} contient {num_books} livres.")
        pdf.add_text(f"Prix moyen : {avg_price:.2f} €")

        fig, ax = plt.subplots()
        sns.countplot(data=df_cat, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S')

#genera il report completto dell'archivio
def generate_full_archive_report(df: pd.DataFrame, logo_path: str = "C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\motore_libreria\\book_report\\static\\agm_solutions_2.png") -> bytes:
    pdf = PDFReport(title=sanitize_text("Rapport complet de l’archive"), logo_path=logo_path)
    pdf.add_page()

    num_books = len(df)
    avg_price = df["price_in_euros"].mean()
    num_authors = df["author"].nunique()

    pdf.add_text(f"L’archive contient {num_books} livres.")
    pdf.add_text(f"Prix moyen : {avg_price:.2f} €")
    pdf.add_text(f"Nombre total d’auteurs : {num_authors}")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x="publication_date", ax=ax)
    plt.xticks(rotation=45)
    plt.title("Répartition des livres par année de publication")
    pdf.add_image_plot(fig)
    plt.close(fig)

    return pdf.output(dest='S')"""

"""from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from io import BytesIO
import unicodedata

# Fonction de nettoyage du texte
def sanitize_text(text: str) -> str:
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

class PDFReport(FPDF):
    def __init__(self, title, logo_path):
        super().__init__()
        self.title = sanitize_text(title)
        self.logo_path = logo_path
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)
        self.set_font('Arial', 'B', 16)
        self.multi_cell(0, 10, self.title, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.multi_cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_text(self, text):
        self.set_font("Arial", size=12)
        try:
            clean_text = sanitize_text(text)
            if len(clean_text) > 1000:
                clean_text = clean_text[:1000] + "..."
            self.multi_cell(0, 10, clean_text)
        except Exception as e:
            self.multi_cell(0, 10, f"[Texte invalide: {str(e)}]")

    def add_image_plot(self, fig):
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        self.image(buffer, w=180)
        buffer.close()

# ---------- Rapports ----------

def generate_author_report(df: pd.DataFrame, author: str, logo_path: str) -> bytes:
    df_author = df[df["author"] == author]
    pdf = PDFReport(title=f"Rapport pour l'auteur: {author}", logo_path=logo_path)
    pdf.add_page()

    if df_author.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'auteur '{author}'.")
    else:
        num_books = len(df_author)
        avg_price = df_author["price_in_euros"].mean()

        pdf.add_text(f"L'auteur {author} a écrit {num_books} livres.")
        pdf.add_text(f"Prix moyen des livres : {avg_price:.2f} €")

        fig, ax = plt.subplots()
        sns.countplot(data=df_author, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S').encode('latin1')

def generate_publisher_report(df: pd.DataFrame, publisher: str, logo_path: str) -> bytes:
    df_pub = df[df["publisher"] == publisher]
    pdf = PDFReport(title=f"Rapport pour l'éditeur: {publisher}", logo_path=logo_path)
    pdf.add_page()

    if df_pub.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'éditeur '{publisher}'.")
    else:
        num_books = len(df_pub)
        avg_price = df_pub["price_in_euros"].mean()

        pdf.add_text(f"L'éditeur {publisher} a publié {num_books} livres.")
        pdf.add_text(f"Prix moyen : {avg_price:.2f} €")

        fig, ax = plt.subplots()
        sns.countplot(data=df_pub, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S').encode('latin1')

def generate_category_report(df: pd.DataFrame, category: str, logo_path: str) -> bytes:
    df_cat = df[df["category"] == category]
    pdf = PDFReport(title=f"Rapport pour la catégorie: {category}", logo_path=logo_path)
    pdf.add_page()

    if df_cat.empty:
        pdf.add_text(f"Aucun livre trouvé pour la catégorie '{category}'.")
    else:
        num_books = len(df_cat)
        avg_price = df_cat["price_in_euros"].mean()

        pdf.add_text(f"La catégorie {category} contient {num_books} livres.")
        pdf.add_text(f"Prix moyen : {avg_price:.2f} €")

        fig, ax = plt.subplots()
        sns.countplot(data=df_cat, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S').encode('latin1')

def generate_full_archive_report(df: pd.DataFrame, logo_path: str) -> bytes:
    pdf = PDFReport(title="Rapport complet de l'archive", logo_path=logo_path)
    pdf.add_page()

    num_books = len(df)
    avg_price = df["price_in_euros"].mean()
    num_authors = df["author"].nunique()

    pdf.add_text(f"L'archive contient {num_books} livres.")
    pdf.add_text(f"Prix moyen : {avg_price:.2f} €")
    pdf.add_text(f"Nombre total d'auteurs : {num_authors}")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x="publication_date", ax=ax)
    plt.xticks(rotation=45)
    plt.title("Répartition des livres par année de publication")
    pdf.add_image_plot(fig)
    plt.close(fig)

    return pdf.output(dest='S').encode('latin1')"""

"""from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from io import BytesIO



class PDFReport(FPDF):
    def __init__(self, title, logo_path, unicode=True):
        super().__init__()
        self.title = title
        self.logo_path = logo_path
        self.unicode = unicode
        self.set_auto_page_break(auto=True, margin=15)
        if self.unicode:
            self.add_font("DejaVu", fname="DejaVuSans.ttf", uni=True)


    def header(self):
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)
        self.set_font('DejaVu' if self.unicode else 'Arial', 'B', 16)
        self.cell(0, 10, self.title, border=False, ln=True, align='C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('DejaVu' if self.unicode else 'Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', align='C')

    def add_text(self, text):
        self.set_font("DejaVu" if self.unicode else "Arial", size=12)
        self.multi_cell(0, 10, text)

    def add_image_plot(self, fig):
        buffer = BytesIO()
        fig.savefig(buffer, format='png')
        buffer.seek(0)
        self.image(buffer, w=180)
        buffer.close()

def generate_author_report(df: pd.DataFrame, author: str, logo_path: str = "", use_unicode=True) -> bytes:
    df_author = df[df["author"] == author]
    pdf = PDFReport(title=f"Rapport pour l'auteur: {author}", logo_path=logo_path, unicode=use_unicode)
    pdf.add_page()

    if df_author.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'auteur '{author}'.")
    else:
        num_books = len(df_author)
        avg_price = df_author["price_in_euros"].mean()
        pdf.add_text(f"L'auteur {author} a écrit {num_books} livres dans la base de données.")
        pdf.add_text(f"Prix moyen des livres : {avg_price:.2f} EUR")
        fig, ax = plt.subplots()
        sns.countplot(data=df_author, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S').encode('utf-8' if use_unicode else 'latin1')

def generate_publisher_report(df: pd.DataFrame, publisher: str, logo_path: str = "", use_unicode=True) -> bytes:
    df_pub = df[df["publisher"] == publisher]
    pdf = PDFReport(title=f"Rapport pour l'éditeur: {publisher}", logo_path=logo_path, unicode=use_unicode)
    pdf.add_page()

    if df_pub.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'éditeur '{publisher}'.")
    else:
        num_books = len(df_pub)
        avg_price = df_pub["price_in_euros"].mean()
        pdf.add_text(f"L'éditeur {publisher} a publié {num_books} livres.")
        pdf.add_text(f"Prix moyen : {avg_price:.2f} EUR")
        fig, ax = plt.subplots()
        sns.countplot(data=df_pub, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S').encode('utf-8' if use_unicode else 'latin1')

def generate_category_report(df: pd.DataFrame, category: str, logo_path: str = "", use_unicode=True) -> bytes:
    df_cat = df[df["category"] == category]
    pdf = PDFReport(title=f"Rapport pour la catégorie: {category}", logo_path=logo_path, unicode=use_unicode)
    pdf.add_page()

    if df_cat.empty:
        pdf.add_text(f"Aucun livre trouvé pour la catégorie '{category}'.")
    else:
        num_books = len(df_cat)
        avg_price = df_cat["price_in_euros"].mean()
        pdf.add_text(f"La catégorie {category} contient {num_books} livres.")
        pdf.add_text(f"Prix moyen : {avg_price:.2f} EUR")
        fig, ax = plt.subplots()
        sns.countplot(data=df_cat, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)

    return pdf.output(dest='S').encode('utf-8' if use_unicode else 'latin1')

def generate_full_archive_report(df: pd.DataFrame, logo_path: str = "", use_unicode=True) -> bytes:
    pdf = PDFReport(title="Rapport complet de l'archive", logo_path=logo_path, unicode=use_unicode)
    pdf.add_page()

    num_books = len(df)
    avg_price = df["price_in_euros"].mean()
    num_authors = df["author"].nunique()
    pdf.add_text(f"L'archive contient {num_books} livres.")
    pdf.add_text(f"Prix moyen : {avg_price:.2f} EUR")
    pdf.add_text(f"Nombre total d'auteurs : {num_authors}")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.countplot(data=df, x="publication_date", ax=ax)
    plt.xticks(rotation=45)
    plt.title("Répartition des livres par année de publication")
    pdf.add_image_plot(fig)
    plt.close(fig)

    return pdf.output(dest='S').encode('utf-8' if use_unicode else 'latin1')"""


from fpdf import FPDF
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from io import BytesIO
import unicodedata
from author import *
from publisher import *
from category import *
from archive import *

def sanitize_text(text: str) -> str:
    """Replace special quotes and accents, normalize to ASCII."""
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    return text

class PDFReport(FPDF):
    # Custom PDF report class inheriting from FPDF
    def __init__(self, title, logo_path, format='A3', auto=True):
        super().__init__(format=format)
        self.title = title
        self.logo_path = logo_path
        self.set_auto_page_break(auto=auto, margin=30)

    # Custom header method
    def header(self):
        # Logo
        if self.logo_path and os.path.exists(self.logo_path):
            self.image(self.logo_path, 10, 8, 33)
        # Title
        self.set_font('Arial', 'B', 12)
        self.multi_cell(self.w - 2 * self.l_margin, 10, self.title, border=False, align='C')
        self.ln(10) # Add a line break after the title

    # Custom footer method
    def footer(self):
        # Page number
        self.set_y(-15)
        self.set_font('Arial', 'I', 10)
        self.multi_cell(self.w - 2 * self.l_margin, 10, f'Page {self.page_no()}', align='C')

    # Method to add text to the PDF
    def add_text(self, text):
        self.set_font("Arial", size=12)
        clean_text = sanitize_text(text)
        self.multi_cell(self.w - 2 * self.l_margin, 9, clean_text, ln=True)

        

    
    # Method to add in grasetto text to the PDF
    def add_text_grasetto(self, text):
        self.set_font("Arial", "B", 14)
        clean_text = sanitize_text(text)
        self.multi_cell(self.w - 2 * self.l_margin, 9, clean_text,ln=True) 
        

    # Method to add an image plot to the PDF
    def add_image_plot(self, fig):
        buffer = BytesIO()
        fig.savefig(buffer, format='png', bbox_inches='tight')
        buffer.seek(0)
        # Use almost the full width of the page
        self.image(buffer, x=self.l_margin, w=self.w - 2 * self.l_margin)
        buffer.close()

"================================================================================================================"


def generate_author_report(df: pd.DataFrame, author: str, logo_path: str ) -> bytes:
    """Generate a PDF report for a single author."""
    if "author" not in df or "price_in_euros" not in df or "publication_year" not in df:
        raise ValueError("DataFrame must contain 'author', 'price_in_euros', and 'publication_year' columns.")
    df_author = df[df["author"] == author]
    pdf = PDFReport(title=sanitize_text(f"REPORT DELL'AUTORE : {author}"), logo_path=logo_path)
    pdf.add_page()
    if df_author.empty:
        pdf.add_text(f"NESSUN AUTORE TROVATO CON NOME  '{author}'.")
    else:
        #informationi generali sull'autore
        num_books = get_tot_book_author(df,author) # numero di libri scritti dall'autore
        avg_price = med_price_author(df,author)#prezzo medio dei libri dell'autore
        libro_recente = get_recent_book_author(df,author) # libro piu recente dell'autore
        anno_piu_ricorente = get_year_max_publication(df,author)# anno di pubblicazione piu ricorrente
        editori = get_list_publisher_author(df,author)# lista degli editori con cui ha pubblicato
        lista_categorie = get_list_category_author(df,author) # lista delle categorie principali dell'autore
        totale_valore = get_value_author(df,author) # il suo valore totale in euro
        graph_libri_anno_author_ =  graph_libri_anno_author(df,author)# # grafico a barra/linee di conteggio numero di libri per gli ultimi 5 anni di pubblicazione
        graph_libri_categoria_author_ = graph_libri_categoria_author(df,author) # grafico a barre di conteggio libri per categoria

        # si aggiungono le informazioni al PDF
        pdf.add_text_grasetto(f"NUMERO DI LIBRI  PRESENTI NELL'ARCHIVIO :  ")# numero di libri scritti dall'autore
        pdf.add_text(f"{num_books} ")# numero di libri scritti dall'autore
    
       
        
        pdf.add_text_grasetto(f"PREZZO MEDIO DI UN LIBRO :")# prezzo medio dei libri dell'autore
        pdf.add_text(f"{avg_price:.2f} euros ")

        pdf.add_text_grasetto(f"ANNO IN CUI HA PUIBBLICATO PIU LIBRI :")# anno di pubblicazione piu ricorrente
        pdf.add_text(f"{anno_piu_ricorente}  ")

        pdf.add_text_grasetto(f"ULTIMO LIBRO SCRITTO :")# libro piu recente dell'autore
        pdf.add_text(f"{libro_recente} ")

        pdf.add_text_grasetto(f"VALORE TOTALE DELL'AUTORE:")# il suo valore totale in euro")
        pdf.add_text(f"{totale_valore} euros")

        pdf.add_text_grasetto(f"EDITORI CON CUI HA PUBBLICATO LIBRI:")
        for idx, elemento in enumerate(editori, 1):
          pdf.add_text(f"   {idx}.  {elemento} ")

        pdf.add_text_grasetto(f"CATEGORIE PRINCIPALI DELL'UTORE:")
        for idx, elemento in enumerate(lista_categorie, 1):
          pdf.add_text(f"   {idx}.  {elemento} ")
        
        #GRAFICI
        """fig, ax = plt.subplots() # Crée une figure et un axe
        sns.countplot(data=df_author, x="publication_year", ax=ax)# Crée un graphique de comptage des livres par année
        plt.xticks(rotation=45)# Rotation des étiquettes de l'axe x pour une meilleure lisibilité
        plt.title("Livres par année")# Titre du graphique"""
        #grafico a barra/linee  di conteggio numero di libri per gli  ultimi 5 anni di pubblicazione
        #pdf.add_text(f"questo grafico mostra la produttività dell'autore negli ultimi anni piu recenti.")
        #fig = graph_libri_anno_author(df,author)
        # Ajout du graphique au PDF
        pdf.add_image_plot(graph_libri_anno_author_ )# Ajoute le graphique au PDF
        plt.close(graph_libri_anno_author_)
        #pdf.add_text(f"questo grafico mostra la distribuzione dei libri per categoria dell'autore.")

        pdf.add_image_plot(graph_libri_categoria_author_ )
        plt.close(graph_libri_categoria_author_)# Ferme la figure pour libérer la mémoire
    return pdf.output(dest='S')# # Retourne le PDF en bytes

'------------------------------------------------------------------------------------------------------------------------------------------------------'

def generate_publisher_report(df: pd.DataFrame, publisher: str, logo_path: str ) -> bytes:
    """Generate a PDF report for a single publisher."""
    if "publisher" not in df or "price_in_euros" not in df or "publication_year" not in df:
        raise ValueError("DataFrame must contain 'publisher', 'price_in_euros', and 'publication_year' columns.")
    
    df_pub = df[df["publisher"] == publisher]# # Filtre les livres de l'éditeur spécifié

    # Creazione del PDF
    pdf = PDFReport(title=sanitize_text(f"REPORT PER L'EDITORE: {publisher}"), logo_path=logo_path)
    pdf.add_page()
    if df_pub.empty:
        pdf.add_text(f"NESSUN EDITORE TROVATO PER '{publisher}'.")
    else:
        #si aggiunge le informazioni dell'editore
        num_books = get_tot_book_publisher(df,publisher)# numero totale di libri pubblicati
        avg_price = get_med_price_publisher(df,publisher) # prezzo medio dei libri
        autori = get_5_author_publisher(df,publisher) # i 5 autori principali dell'editore
        categorie = get_5_category_publisher(df,publisher) # lista delle 5 categorie piu frequenti dell'editore

        #grafici
        grapget_graph_libri_anno_publisher_ = get_graph_libri_anno_publisher(df,publisher) # grafico numero di libri per gli ultimi dieci anni di pubblicazione 
        get_graph_libri_autore_publisher_ = get_graph_libri_autore_publisher(df,publisher) # grafico a barre numero di libri per i 10 autori piu frequenti dell'editore
        get_graph_libri_category_publisher_ = get_graph_libri_category_publisher(df,publisher) # grafico a barre numero di libri per le 10 categorie piu frequenti dell'editore

        pdf.add_text_grasetto(f"NUMERO DI LIBRI PUBBLICATI DALL'EDITORE :")# numero totale di libri pubblicati
        pdf.add_text(f"{num_books} ")

        pdf.add_text_grasetto(f"PREZZO MEDIO DI UN LIBRO:")# numero totale di libri pubblicati
        pdf.add_text(f"{avg_price} ")

        pdf.add_text_grasetto(f"I 5 AUTORI PRINCIPALI:")# i 5 autori principali dell'editore
        for idx, elemento in enumerate(autori, 1):
          pdf.add_text(f"   {idx}.  {elemento} ")

        pdf.add_text_grasetto(f"LE 5 CATEGORIE PRINCIPALI:")# I 5 Editori principali
        for idx, elemento in enumerate(categorie, 1):
          pdf.add_text(f"   {idx}.  {elemento} ")  

        pdf.add_image_plot(grapget_graph_libri_anno_publisher_ )# Ajoute le graphique au PDF
        plt.close(grapget_graph_libri_anno_publisher_)  # Ferme la figure pour libérer la mémoire

        pdf.add_image_plot(get_graph_libri_autore_publisher_ )# Ajoute le graphique au PDF
        plt.close(get_graph_libri_autore_publisher_)


        pdf.add_image_plot(get_graph_libri_category_publisher_ )# Ajoute le graphique au PDF
        plt.close(get_graph_libri_category_publisher_)  

        
        #pdf.ln(5)  # Ajoute un espace entre les lignes
    return pdf.output(dest='S')


'-------------------------------------------------------------------------------------------------------------------'


def generate_category_report(df: pd.DataFrame, category: str, logo_path: str) -> bytes:
    """Generate a PDF report for a single category."""
    if "category" not in df or "price_in_euros" not in df or "publication_year" not in df:
        raise ValueError("DataFrame must contain 'category', 'price_in_euros', and 'publication_year' columns.")
    df_cat = df[df["category"] == category]
    pdf = PDFReport(title=sanitize_text(f"REPORT PER LA CATEGORIA : {category}"), logo_path=logo_path)
    pdf.add_page()
    if df_cat.empty:
        pdf.add_text(f"NESSUNA CATEGORIA TROVATA PER '{category}'.")
    else:
        num_books = get_num_libri_category(df,category) # numero totale di libri nella categoria
        avg_price = get_avg_price_category(df,category) # prezzo medio dei libri nella categoria
        anno_publicazione_max = get_year_max_publication_category(df,category) # anno di pubblicazione piu ricorrente nella categoria
        autori =get_list_author_category(df,category) # lista degli autori che hanno pubblicato nella categoria
        editori = get_list_publisher_category(df,category) # lista degli editori che hanno pubblicato nella categoria
        
        # grafici
        graph_num_libri_author_category_ = graph_num_libri_author_category(df,category) # grafico a barre numero di libri per i 10 autori piu frequenti nella categoria
        graph_num_libri_publisher_category_ = graph_num_libri_publisher_category(df,category) # grafico a barre numero di libri per i 10 editori piu frequenti nella categoria
        
        pdf.add_text_grasetto(f"NUMERO DI LIBRI PUBBLICATI DELLA CATEGORIA :")# numero totale di libri pubblicati
        pdf.add_text(f"{num_books} ")

        pdf.add_text_grasetto(f"PREZZO MEDIO DI UN LIBRO :")# prezzo medio dei libri nella categoria
        pdf.add_text(f"{avg_price} ")

        pdf.add_text_grasetto(f"ANNO IN CUI SONO STATI PUBBLICATI PIU LIBRI :")# anno di pubblicazione piu ricorrente nella categoria
        pdf.add_text(f"{anno_publicazione_max} ")

        pdf.add_text_grasetto(f"I 5 AUTORI PRINCIPALI :")# lista degli autori che hanno pubblicato nella categoria
        for idx, elemento in enumerate(autori, 1):
          pdf.add_text(f"   {idx}.  {elemento} ")

        pdf.add_text_grasetto(f"I 5 EDITORI PRINCIPALI :")# lista degli editori che hanno pubblicato nella categoria
        for idx, elemento in enumerate(editori, 1):
          pdf.add_text(f"   {idx}.  {elemento} ")  

        pdf.add_image_plot(graph_num_libri_author_category_  )# Ajoute le graphique au PDF
        plt.close(graph_num_libri_author_category_ )

        pdf.add_image_plot(graph_num_libri_publisher_category_ )# Ajoute le graphique au PDF
        plt.close(graph_num_libri_publisher_category_)  

    return pdf.output(dest='S')


'---------------------------------------------------------------------------------------------------------------------------'


def generate_full_archive_report(df: pd.DataFrame, logo_path: str) -> bytes:
    """Generate a PDF report for the full archive."""
    if "price_in_euros" not in df or "author" not in df or "publication_year" not in df:
        raise ValueError("DataFrame must contain 'author', 'price_in_euros', and 'publication_year' columns.")
    pdf = PDFReport(title=sanitize_text("REPORT COMPLETO DELL'ARCHIVIO"), logo_path=logo_path)
    pdf.add_page()
    num_books = get_tot_book_archive(df) # numero totale di libri nell'archivio
    avg_price = get_avg_price_archive(df) # prezzo medio dei libri nell'archivio
    num_authors = get_num_author_archive(df) # numero totale di autori nell'archivio
    num_editori = get_num_publisher_archive(df) # numero totale di editori nell'archivio
    autori = get_list_5_most_author_archive(df) # lista dei 5 autori piu frequenti nell'archivio
    editori = get_list_5_most_publisher_archive(df) # lista dei 5 editori piu frequenti nell'archivio
    categorie = get_list_5_most_category_archive(df) # lista delle 5 categorie piu frequenti nell'archivio

    # grafici
    graph_libri_anno_archive_ = graph_libri_anno_archive(df) # grafico a barre numero di libri per gli ultimi 10 anni di pubblicazione
    graph_libri_category_archive_ = graph_libri_category_archive(df) # grafico a barre numero di libri per le 10 categorie piu frequenti nell'archivio
    graph_libri_author_archive_ = graph_libri_author_archive(df) # grafico a barre numero di libri per i 10 autori piu frequenti nell'archivio
    graph_avg_prezzi_categoria_archive_ = graph_avg_prezzi_categoria_archive(df) # grafico a barre prezzo medio per le 10 categorie piu frequenti nell'archivio

    pdf.add_text_grasetto(f"NUMERO DI LIBRI TOTALI PRESENTI NELL'ARCHIVIO :")# numero totale di libri pubblicati
    pdf.add_text(f"{num_books} ")
    
    pdf.add_text_grasetto(f"PREZZO MEDIO DI UN LIBRO :")# prezzo medio dei libri nell'archivio
    pdf.add_text(f"{avg_price} ")
    
    pdf.add_text_grasetto(f"NUMERO TOTALE DI AUTORI PRESENTI NELL'ARCHIVIO :")# numero totale di autori nell'archivio
    pdf.add_text(f"{num_authors} ")

    pdf.add_text_grasetto(f"NUMERO TOTALE DI EDITORI PRESENTI NELL'ARCHIVIO :")# numero totale di editori nell'archivio
    pdf.add_text(f"{num_editori} ")

    pdf.add_text_grasetto(f"LISTA DEI 5 AUTORI PIU PRESENTI NELL'ARCHIVIO :")# lista dei 5 autori piu frequenti nell'archivio
    for idx, elemento in enumerate(autori, 1):
        pdf.add_text(f"   {idx}.  {elemento} ")

    pdf.add_text_grasetto(f"LISTA DEI 5 EDITORI PIU PRESENTI NELL'ARCHIVIO :")# lista dei 5 editori piu frequenti nell'archivio
    for idx, elemento in enumerate(editori, 1):
        pdf.add_text(f"   {idx}.  {elemento} ")    

    pdf.add_text_grasetto(f"LISTA DELLE 5 CATEGORIE PIU PRESENTI NELL'ARCHIVIO :")# lista delle 5 categorie piu frequenti nell'archivio
    for idx, elemento in enumerate(categorie, 1):
        pdf.add_text(f"   {idx}.  {elemento} ")    

    pdf.add_image_plot(graph_libri_anno_archive_  )# Ajoute le graphique au PDF
    plt.close(graph_libri_anno_archive_ )    

    pdf.add_image_plot(graph_libri_category_archive_  )# Ajoute le graphique au PDF
    plt.close(graph_libri_category_archive_ )

    pdf.add_image_plot(graph_libri_author_archive_ )# Ajoute le graphique au PDF
    plt.close(graph_libri_author_archive_)

    pdf.add_image_plot(graph_avg_prezzi_categoria_archive_  )# Ajoute le graphique au PDF
    plt.close(graph_avg_prezzi_categoria_archive_ )


    return pdf.output(dest='S')