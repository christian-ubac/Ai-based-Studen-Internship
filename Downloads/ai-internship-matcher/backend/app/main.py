from fastapi import FastAPI
from .db import engine
from . import models
from .api import uploads, recommendations, scraper, frontend_api
from .crud import list_students
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Internship Matcher (pilot)")
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(uploads.router)
app.include_router(recommendations.router)
app.include_router(scraper.router)
app.include_router(frontend_api.router)

@app.get("/api/students")
def get_students():
    from .db import SessionLocal
    db = SessionLocal()
    try:
        return [ {"id":s.id, "name":s.name, "program":s.program} for s in list_students(db) ]
    finally:
        db.close()
