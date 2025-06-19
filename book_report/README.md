# motore_libreria
progetto di un motore(API) che permette di ottenere report su un archivio di unna libreria(file csv).
fornisce diversi endpoint che permettono di ottenere un file pdf contenente un report completto sia su argomenti singoli(autore, editore,lingua di publicazione,paese di publicazione ecc.) che su tutta l'archivio.
il report è un file pdf che contiene informazioni testuali e grafici diversi per una spiegazione più in profondità.

# endpoints
-report su un singolo autore ==> dato il nome di un autore, generare un report contenente: il numero di libri che ha scritto,
  gli editori con chi ha publicato i suoi libri, il suo libro piu recente,il numero di pagine totali che gha scritto, il suo valore totale in euro
-report di tutta l'archivio
-report di un singolo editore
-report di una singola categoria di libri

# tecnologie
nel nostro progetto, useremmo :
-FASTAPI per creare il motore
-fpdf2 per la generazione dei report in formato pdf
-pandas, numpy e matplotlib per la gestione dati e generazione dei grafici

# struttura del progetto:
