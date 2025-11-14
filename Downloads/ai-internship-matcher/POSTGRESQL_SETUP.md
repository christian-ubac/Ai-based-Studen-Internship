# PostgreSQL Database Setup for AI Internship Matcher

## Prerequisites
- PostgreSQL installed on your machine
- Access to PostgreSQL command line (psql)
- Administrator or appropriate permissions

---

## Step 1: Check PostgreSQL Installation

Open Command Prompt (cmd) or PowerShell and verify PostgreSQL is installed:

```powershell
psql --version
```

Expected output:
```
psql (PostgreSQL) 13.x (or higher)
```

If not found, download from: https://www.postgresql.org/download/

---

## Step 2: Connect to PostgreSQL Server

Open Command Prompt/PowerShell and connect to the default PostgreSQL server:

```powershell
psql -U postgres
```

You'll be prompted for the PostgreSQL password (set during installation).

Expected prompt:
```
postgres=#
```

---

## Step 3: Create Database

Once connected, create a new database for the internship matcher:

```sql
CREATE DATABASE internshipdb;
```

Expected output:
```
CREATE DATABASE
```

---

## Step 4: Create User (Optional but Recommended)

Create a dedicated user for your application:

```sql
CREATE USER internship_user WITH PASSWORD 'your_secure_password';
```

Example:
```sql
CREATE USER internship_user WITH PASSWORD 'Internship@2025';
```

---

## Step 5: Grant Permissions

Give the user permission to access the database:

```sql
ALTER ROLE internship_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE internshipdb TO internship_user;
```

---

## Step 6: Verify Database Creation

List all databases to confirm creation:

```sql
\l
```

You should see `internshipdb` in the list.

---

## Step 7: Exit PostgreSQL

Exit the psql prompt:

```sql
\q
```

You'll return to the Command Prompt.

---

## Step 8: Update Your .env File

Edit `backend/.env` with your database credentials:

**If using default postgres user:**
```
DATABASE_URL=postgresql://postgres:your_postgres_password@localhost:5432/internshipdb
```

**If using the new internship_user:**
```
DATABASE_URL=postgresql://internship_user:Internship@2025@localhost:5432/internshipdb
```

Example (for this guide):
```
DATABASE_URL=postgresql://internship_user:Internship@2025@localhost:5432/internshipdb
RAPID_API_KEY=61d2bbe17cmshf9c0f78736a491?p128608jsn0416f849ea82
RAPID_API_HOST=internships-api.p.rapidapi.com
JOBSCRAPER_RATE_LIMIT=1.0
```

---

## Step 9: Verify Connection (Optional)

Test your connection from Command Prompt:

```powershell
psql -U internship_user -d internshipdb -h localhost
```

Enter your password when prompted. If successful, you'll see:
```
internshipdb=>
```

Type `\q` to exit.

---

## Step 10: Initialize Database Tables

The application will automatically create tables when you start the backend. But you can manually initialize if needed:

Open Command Prompt and navigate to the backend:

```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\backend
```

Run the initialization:

```powershell
python -c "from app.db import engine; from app.models import Base; Base.metadata.create_all(bind=engine)"
```

Expected: No errors, tables created silently.

---

## Complete Command-by-Command Guide

Copy-paste this sequence in Command Prompt/PowerShell:

### Open PostgreSQL
```powershell
psql -U postgres
```
(Enter your postgres password when prompted)

### Inside psql, run these commands:
```sql
-- Create database
CREATE DATABASE internshipdb;

-- Create user
CREATE USER internship_user WITH PASSWORD 'Internship@2025';

-- Grant permissions
ALTER ROLE internship_user CREATEDB;
GRANT ALL PRIVILEGES ON DATABASE internshipdb TO internship_user;

-- Verify
\l

-- Exit
\q
```

---

## Verify Everything Works

### 1. Test PostgreSQL Connection
```powershell
psql -U internship_user -d internshipdb -h localhost
```

Should work without errors.

### 2. Start Backend
```powershell
cd C:\Users\ACER\Downloads\ai-internship-matcher\backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Look for:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

If you see table creation logs, the database is working!

### 3. Seed Sample Data (Optional)
```powershell
python scripts/seed_internships.py
```

This populates the database with sample internships.

---

## Troubleshooting

### "psql: command not found"
- PostgreSQL not in PATH
- **Solution:** Add PostgreSQL bin folder to PATH:
  1. Find PostgreSQL install path (default: `C:\Program Files\PostgreSQL\13\bin`)
  2. Add to system PATH environment variables
  3. Restart Command Prompt

### "password authentication failed"
- Wrong password
- **Solution:** 
  - Use the password you set during PostgreSQL installation
  - Or reset password (see below)

### "could not connect to server"
- PostgreSQL service not running
- **Solution:**
  ```powershell
  # Start PostgreSQL service (Windows)
  pg_ctl -D "C:\Program Files\PostgreSQL\13\data" start
  
  # Or use Services (services.msc) and start "postgresql-x64-13"
  ```

### "database internshipdb does not exist"
- Database not created
- **Solution:** Run the CREATE DATABASE command again

### Application can't connect to database
- Wrong DATABASE_URL in .env
- **Solution:** Double-check connection string format:
  ```
  postgresql://username:password@localhost:5432/internshipdb
  ```

---

## PostgreSQL Service Management

### Start PostgreSQL (Windows)
```powershell
pg_ctl -D "C:\Program Files\PostgreSQL\13\data" start
```

### Stop PostgreSQL
```powershell
pg_ctl -D "C:\Program Files\PostgreSQL\13\data" stop
```

### Check Status
```powershell
pg_ctl -D "C:\Program Files\PostgreSQL\13\data" status
```

Or use Services GUI:
```powershell
services.msc
```
Find `postgresql-x64-13` and manage from there.

---

## Quick Reference: Common psql Commands

Inside psql prompt:

| Command | Purpose |
|---------|---------|
| `\l` | List all databases |
| `\du` | List all users/roles |
| `\dt` | List all tables in current database |
| `\c database_name` | Connect to a database |
| `\q` | Exit psql |
| `\h` | Get help |
| `\d table_name` | Describe a table |

---

## Database Structure (Auto-Created)

Once the backend starts, these tables are created automatically:

```
internshipdb
├── students (id, name, email, program, gpa, protected_age)
├── resumes (id, student_id, filename, parsed_text, skills, outcomes, embedding, created_at)
├── internships (id, title, company_name, location, description, required_skills, posting_url, posted_date, is_active, source)
├── departments (id, name, program_focus, description, required_skills, embedding)
└── recommendations (id, student_id, department_id, score, reason, created_at)
```

---

## Final Checklist

- [ ] PostgreSQL installed and running
- [ ] Database `internshipdb` created
- [ ] User `internship_user` created (optional)
- [ ] Permissions granted
- [ ] `.env` file updated with correct DATABASE_URL
- [ ] Backend starts without connection errors
- [ ] Tables are created automatically
- [ ] (Optional) Sample data seeded

---

## Next Steps

Once database is set up:

1. **Start Backend:**
   ```powershell
   cd backend
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Start Frontend:**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Open Browser:**
   ```
   http://localhost:5173
   ```

4. **Upload Resume & See Recommendations!**

---

## Need Help?

- PostgreSQL docs: https://www.postgresql.org/docs/
- psql reference: https://www.postgresql.org/docs/current/app-psql.html
- Connection string format: https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING

Your AI Internship Matcher is ready! 🚀
