"""Verify DB connection and basic readiness.

Run this from the backend folder with the venv active:

    . .venv\Scripts\Activate.ps1
    python .\scripts\verify_db_connection.py

The script prints the DB URL (partially masked), number of tables and whether pgvector is installed.
"""
from app.config import settings
from app.db import engine, SessionLocal
from sqlalchemy import text

def mask_url(url: str) -> str:
    if not url:
        return "<empty>"
    # naive mask: hide password portion
    try:
        if "@" in url and ":" in url.split("@")[0]:
            pre, rest = url.split("@", 1)
            userpass = pre.split("//",1)[1]
            if ":" in userpass:
                user, pwd = userpass.split(":",1)
                return url.replace(f"{user}:{pwd}@", f"{user}:***@")
    except Exception:
        pass
    return url


def main():
    print("Using DATABASE_URL:", mask_url(settings.DATABASE_URL))
    # test engine connect
    try:
        with engine.connect() as conn:
            print("Connected to database. Engine dialect:", engine.dialect.name)
            # count tables in public schema
            res = conn.execute(text("SELECT count(*) FROM information_schema.tables WHERE table_schema='public';"))
            cnt = res.scalar()
            print(f"Public tables: {cnt}")
            # check pgvector extension
            try:
                res = conn.execute(text("SELECT extname FROM pg_extension WHERE extname='vector';"))
                has_vector = res.scalar() is not None
            except Exception:
                has_vector = False
            print("pgvector installed:", has_vector)
    except Exception as e:
        print("Failed to connect to DB:", e)

    # try opening a Session
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        print("SessionLocal test OK")
        db.close()
    except Exception as e:
        print("SessionLocal failed:", e)

if __name__ == '__main__':
    main()
