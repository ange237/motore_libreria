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
    if "author" not in df or "price_in_euros" not in df or "publication_date" not in df:
        raise ValueError("DataFrame must contain 'author', 'price_in_euros', and 'publication_date' columns.")
    df_author = df[df["author"] == author]
    pdf = PDFReport(title=sanitize_text(f"Rapport pour l'auteur: {author}"), logo_path=logo_path)
    pdf.add_page()
    if df_author.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'auteur '{author}'.")
    else:
        num_books = len(df_author) # nombre de livres écrits par l'auteur
        avg_price = df_author["price_in_euros"].mean()# prix moyen des livres de l'auteur
        # Ajout des informations dans le PDF
        pdf.add_text(f"L’auteur {author} a écrit {num_books} livres dans la base de données.")# nombre de livres
        pdf.add_text(f"Prix moyen des livres : {avg_price:.2f} €")# prix moyen des livres

        # Graphique : répartition des livres par année de publication   
        # Création du graphique
        # Utilisation de seaborn pour créer un graphique de comptage
        fig, ax = plt.subplots() # Crée une figure et un axe
        sns.countplot(data=df_author, x="publication_date", ax=ax)# Crée un graphique de comptage des livres par année
        plt.xticks(rotation=45)# Rotation des étiquettes de l'axe x pour une meilleure lisibilité
        plt.title("Livres par année")# Titre du graphique
        # Ajout du graphique au PDF
        pdf.add_image_plot(fig)# Ajoute le graphique au PDF
        plt.close(fig)# Ferme la figure pour libérer la mémoire
    return pdf.output(dest='S')# # Retourne le PDF en bytes

'--------------------------------------------------------------------------------------------------------------'

def generate_publisher_report(df: pd.DataFrame, publisher: str, logo_path: str ) -> bytes:
    """Generate a PDF report for a single publisher."""
    if "publisher" not in df or "price_in_euros" not in df or "publication_date" not in df:
        raise ValueError("DataFrame must contain 'publisher', 'price_in_euros', and 'publication_date' columns.")
    df_pub = df[df["publisher"] == publisher]
    pdf = PDFReport(title=sanitize_text(f"Rapport pour l’éditeur: {publisher}"), logo_path=logo_path)
    pdf.add_page()
    if df_pub.empty:
        pdf.add_text(f"Aucun livre trouvé pour l'éditeur '{publisher}'.")
    else:
        num_books = len(df_pub)
        avg_price = df_pub["price_in_euros"].mean()
        pdf.add_text(f"L’éditeur {publisher} a publié {num_books} livres.")
        #pdf.ln(5)  # Ajoute un espace entre les lignes
        pdf.add_text(f"Prix moyen : {avg_price:.2f} EUR")
        fig, ax = plt.subplots()
        sns.countplot(data=df_pub, x="publication_date", ax=ax)
        plt.xticks(rotation=45)
        plt.title("Livres par année")
        pdf.add_image_plot(fig)
        plt.close(fig)
    return pdf.output(dest='S')


'-------------------------------------------------------------------------------------------------------------------'


def generate_category_report(df: pd.DataFrame, category: str, logo_path: str) -> bytes:
    """Generate a PDF report for a single category."""
    if "category" not in df or "price_in_euros" not in df or "publication_date" not in df:
        raise ValueError("DataFrame must contain 'category', 'price_in_euros', and 'publication_date' columns.")
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


'---------------------------------------------------------------------------------------------------------------------------'


def generate_full_archive_report(df: pd.DataFrame, logo_path: str) -> bytes:
    """Generate a PDF report for the full archive."""
    if "price_in_euros" not in df or "author" not in df or "publication_date" not in df:
        raise ValueError("DataFrame must contain 'author', 'price_in_euros', and 'publication_date' columns.")
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
    return pdf.output(dest='S')