# motore_libreria
progetto di un motore(API) che permette di ottenere report su un archivio di unna libreria(file csv).
fornisce diversi endpoint che permettono di ottenere un file pdf contenente un report completto sia su argomenti singoli(autore, editore,lingua di publicazione,paese di publicazione ecc.) che su tutta l'archivio.
il report è un file pdf che contiene informazioni testuali e grafici diversi per una spiegazione più in profondità.

# endpoints
1)report su un singolo autore ==> dato il nome di un autore, generare un report contenente: il numero totale di libri che ha scritto,prezzo medio dei libri,anno di publicazione piu  ricorrente
  gli editori con cui ha publicato i suoi libri, il suo libro piu recente,categorie principali dei suoi libri, il suo valore totale in euro,grafico di conteggio libri per anno e categoria

2)report di tutta l'archivio ==> generare un report contenente: numero totale di libri, prezzo medio,numero totale di autori ed editori, top 5 autori per numero di libri, top 5 editori , categoria piu presente, grafici:libri per anno ,libri per categoria, libri per autore,box plot dei prezzi medio per categoria o editore

3)report di un singolo editore ==> dato il nome di un editore, generare un report contenente: numero totale di libri pubblicati,prezzo medio dei libri, 5 autori principali(quali autori pubblicano di piu con questo editore), 5 categorie piu frequenti, grafico libri per anno e libri per autore

4)report di una singola categoria di libri ==> dato il nome di una categoria, generare un report contenente: numero di libri nella categoria,prezzo medio, anno piu frequente di pubblicazione,autori principali,editori piu frequenti, grafico libri per autore e/o per editore

# tecnologie
nel nostro progetto, useremmo :
-FASTAPI per creare il motore
-fpdf2 per la generazione dei report in formato pdf
-pandas, numpy e matplotlib per la gestione dati e generazione dei grafici

# struttura del progetto:
