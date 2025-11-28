#!/usr/bin/env python3
"""
Simple helper to create a PostgreSQL user and database.
Usage: python create_db.py
It reads the following environment variables (with defaults):
  SUPERUSER (default: postgres)
  SUPERPASS (password for superuser; required if server requires auth)
  DB_USER (default: internship_user)
  DB_PASS (default: Internship@2025)
  DB_NAME (default: internshipdb)
  HOST (default: localhost)
  PORT (default: 5432)

This script requires `psycopg2` or `psycopg2-binary` installed in your Python environment.
"""
import os
import sys
import psycopg2
from psycopg2 import sql

SUPERUSER = os.getenv("SUPERUSER", "postgres")
SUPERPASS = os.getenv("SUPERPASS", "")
DB_USER = os.getenv("DB_USER", "internship_user")
DB_PASS = os.getenv("DB_PASS", "Internship@2025")
DB_NAME = os.getenv("DB_NAME", "internshipdb")
HOST = os.getenv("HOST", "localhost")
PORT = int(os.getenv("PORT", 5432))

if not SUPERPASS:
    print("Note: SUPERPASS is empty. If your postgres instance requires a password, set SUPERPASS environment variable.")

conn = None
try:
    conn = psycopg2.connect(dbname="postgres", user=SUPERUSER, password=SUPERPASS or None, host=HOST, port=PORT)
    conn.autocommit = True
    cur = conn.cursor()

    # Create user if not exists
    try:
        cur.execute(sql.SQL("CREATE ROLE {} WITH LOGIN PASSWORD %s;").format(sql.Identifier(DB_USER)), [DB_PASS])
        print(f"Created user {DB_USER}")
    except psycopg2.errors.DuplicateObject:
        print(f"User {DB_USER} already exists; skipping creation")
        conn.rollback()

    # Create database if not exists and set owner
    try:
        cur.execute(sql.SQL("CREATE DATABASE {} OWNER {};").format(sql.Identifier(DB_NAME), sql.Identifier(DB_USER)))
        print(f"Created database {DB_NAME}")
    except psycopg2.errors.DuplicateDatabase:
        print(f"Database {DB_NAME} already exists; skipping creation")
        conn.rollback()

    cur.close()
except Exception as e:
    print("Failed to connect or execute SQL:", e)
    sys.exit(1)
finally:
    if conn:
        conn.close()

print("Done. You can now set DATABASE_URL to:")
print(f"postgresql://{DB_USER}:{DB_PASS}@{HOST}:{PORT}/{DB_NAME}")
