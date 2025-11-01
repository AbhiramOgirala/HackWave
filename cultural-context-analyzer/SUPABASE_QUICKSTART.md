# Supabase Quick Start Guide

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com) and sign up/login
2. Click **"New Project"**
3. Fill in:
   - **Name**: `cultural-context-analyzer`
   - **Database Password**: Create a strong password (**SAVE THIS!**)
   - **Region**: Choose closest to you
4. Click **"Create new project"** (takes ~2 minutes)

## Step 2: Get Your Credentials

Once your project is ready:

1. Go to **Project Settings** (⚙️ gear icon in sidebar)
2. Click **API** section
3. Copy these two values:

   ```
   Project URL: https://xxxxxxxxxxxxx.supabase.co
   anon public key: eyJhbGc...very-long-key...
   ```

## Step 3: Update Your `.env` File

Edit `backend/.env`:

```env
GEMINI_API_KEY='your-gemini-api-key'

# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=eyJhbGc...your-anon-key...
SUPABASE_DB_PASSWORD=your-database-password
```

Replace with your actual values from Step 2!

## Step 4: Run SQL Setup

1. In Supabase Dashboard, click **SQL Editor** (in left sidebar)
2. Click **"New query"**
3. Open the file `supabase_setup.sql` from this project
4. Copy ALL the SQL code
5. Paste it into the SQL Editor
6. Click **"Run"** (or press Ctrl+Enter)

You should see: ✅ Success messages

## Step 5: Verify Table Creation

1. Click **Table Editor** (in left sidebar)
2. You should see `analyses` table
3. Click on it to see the columns:
   - id
   - input_text
   - language
   - cultural_origin
   - cross_cultural_connections
   - modern_analogy
   - visualization_description
   - image_url
   - created_at

## Step 6: Run Your Application

```powershell
# Backend
cd backend
.\venv\Scripts\Activate.ps1
python main.py
```

Look for:
```
🔗 Connecting to Supabase database...
✅ Database initialized successfully
🚀 Cultural Context Analyzer API is running
```

## Step 7: Test It!

1. Start frontend: `cd frontend && npm run dev`
2. Open browser: `http://localhost:5173`
3. Analyze some text
4. Check Supabase Table Editor to see your data!

## Troubleshooting

### "Missing database configuration" Error

Make sure your `.env` has:
- `SUPABASE_URL` (starts with https://)
- `SUPABASE_DB_PASSWORD` (the password you created in Step 1)

### Cannot Connect to Database

1. Verify password is correct
2. Check Project URL has `https://` prefix
3. Ensure your Supabase project is active (green status)

### Table Not Found

Run the SQL setup again (Step 4)

## Useful SQL Queries

Run these in SQL Editor to manage your data:

### View All Analyses
```sql
SELECT * FROM analyses ORDER BY created_at DESC LIMIT 10;
```

### Count Total Records
```sql
SELECT COUNT(*) as total FROM analyses;
```

### Delete All Data
```sql
TRUNCATE TABLE analyses;
```

### Delete Specific Record
```sql
DELETE FROM analyses WHERE id = 1;
```

### View Recent Analyses by Language
```sql
SELECT language, COUNT(*) as count 
FROM analyses 
GROUP BY language;
```

## Database Backup

Supabase automatically backs up your database daily (free tier).

### Manual Backup:
1. Go to **Database** > **Backups**
2. Click **"Download backup"**

## Next Steps

- ✅ Your database is now cloud-hosted!
- View data in real-time in Table Editor
- Set up Row Level Security (RLS) for production
- Add more tables/features as needed

## Support

If you need help:
- [Supabase Docs](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)
- Check error messages in Supabase Dashboard > Logs
