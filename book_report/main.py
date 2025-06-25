# punto di partenza di  FastAPI (dove si trova gli endpoint)
from fastapi import FastAPI, Query, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
from io import BytesIO
from dataloader import load_dataset
from report_generator import *




app = FastAPI()
#logo_path = "C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\motore_libreria\\book_report\\static\\agm_solutions_2.png"
logo_path = "C:\\Users\\ange.kadjafomekon\\OneDrive - AGM Solutions\\Desktop\\motore_libreria\\book_report\\static\\agm_solutions.png"
# prima si carica il dataset
df = load_dataset()


@app.get("/")
def lire_racine():
    return {"message": "Bienvenue !"}

@app.get("/report/author")
def report_author(author: str):
    try:
        pdf_bytes = generate_author_report(df, author,logo_path)
        return StreamingResponse(BytesIO(pdf_bytes),
                                 media_type="application/pdf",
                                 headers={"Content-Disposition": f"attachment; filename=rapport_publisher_{author}.pdf"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))
    

@app.get("/report/publisher")
def report_publisher(publisher: str):
    try:
        pdf_bytes = generate_publisher_report(df, publisher,logo_path)
        return StreamingResponse(BytesIO(pdf_bytes),
                                 media_type="application/pdf",
                                 headers={"Content-Disposition": f"attachment; filename=rapport_publisher_{publisher}.pdf"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/report/category")
def report_category(category: str):
    try:
        pdf_bytes = generate_category_report(df, category, logo_path)
        return StreamingResponse(BytesIO(pdf_bytes),
                                 media_type="application/pdf",
                                 headers={"Content-Disposition": f"attachment; filename=rapport_categorie_{category}.pdf"})
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/report/full")
def report_full():
    pdf_bytes = generate_full_archive_report(df, logo_path)
    return StreamingResponse(BytesIO(pdf_bytes),
                             media_type="application/pdf",
                             headers={"Content-Disposition": "attachment; filename=rapport_complet.pdf"})




"""
# Charger le dataset une seule fois
DATA_PATH = "dataset/dataset_progetto_pulito.csv"
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    raise RuntimeError(f"⚠️ Dataset non trouvé à : {DATA_PATH}")

@router.get("/report/publisher/{publisher_name}")
def get_report_by_publisher(publisher_name: str):
    output_path = f"outputs/reports/publisher_{publisher_name}.pdf"
    if not generate_publisher_report(df, publisher_name, output_path):
        raise HTTPException(status_code=404, detail="Éditeur non trouvé dans le dataset.")
    return FileResponse(output_path, media_type="application/pdf", filename=os.path.basename(output_path))


@router.get("/report/category/{category_name}")
def get_report_by_category(category_name: str):
    output_path = f"outputs/reports/category_{category_name}.pdf"
    if not generate_category_report(df, category_name, output_path):
        raise HTTPException(status_code=404, detail="Catégorie non trouvée dans le dataset.")
    return FileResponse(output_path, media_type="application/pdf", filename=os.path.basename(output_path))


@router.get("/report/full")
def get_full_report():
    output_path = "outputs/reports/full_report.pdf"
    generate_full_archive_report(df, output_path)
    return FileResponse(output_path, media_type="application/pdf", filename=os.path.basename(output_path))"""