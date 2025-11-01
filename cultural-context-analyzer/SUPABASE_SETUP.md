# Supabase Setup Guide

## Overview
This project now uses Supabase as the database backend. Supabase provides a PostgreSQL database with additional features like real-time subscriptions, authentication, and storage.

## Setup Steps

### 1. Create a Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Fill in:
   - **Project Name**: cultural-context-analyzer (or your choice)
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to your location
5. Click "Create new project" (takes ~2 minutes to provision)

### 2. Get Your Database Credentials

Once your project is ready:

#### Option A: Connection String (Recommended)
1. Go to **Project Settings** (gear icon) → **Database**
2. Scroll to **Connection string** section
3. Select **URI** tab
4. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxxxxxxxxxxxx.supabase.co:5432/postgres
   ```

#### Option B: Individual Parameters
From the same Database settings page, note:
- **Host**: `db.xxxxxxxxxxxxx.supabase.co`
- **Database name**: `postgres`
- **Port**: `5432`
- **User**: `postgres`
- **Password**: The password you created

### 3. Get Your API Keys (Optional - for future features)

1. Go to **Project Settings** → **API**
2. Copy:
   - **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
   - **anon/public key**: For client-side access
   - **service_role key**: For server-side admin access (keep secret!)

### 4. Update Your `.env` File

Edit `backend/.env` with your actual Supabase credentials:

```env
GEMINI_API_KEY='your-gemini-api-key'

# Supabase Configuration
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_KEY=your-service-role-key-here

# Supabase Database Connection
SUPABASE_DB_HOST=db.xxxxxxxxxxxxx.supabase.co
SUPABASE_DB_PORT=5432
SUPABASE_DB_NAME=postgres
SUPABASE_DB_USER=postgres
SUPABASE_DB_PASSWORD=your-database-password-here
```

### 5. Run the Application

The application will automatically create the `analyses` table on first run:

```bash
cd backend
python main.py
```

Look for: `✅ Database initialized successfully`

## Verify Database Setup

### Via Supabase Dashboard
1. Go to **Table Editor** in your Supabase project
2. You should see the `analyses` table after running the app
3. Click on it to view the schema

### Table Schema
The `analyses` table has the following columns:
- `id` (integer, primary key)
- `input_text` (text)
- `language` (varchar)
- `cultural_origin` (text)
- `cross_cultural_connections` (text)
- `modern_analogy` (text)
- `visualization_description` (text)
- `image_url` (text)
- `created_at` (timestamp)

## Benefits of Supabase

✅ **Managed Database**: No need to run PostgreSQL locally
✅ **Auto Backups**: Daily backups included
✅ **Dashboard**: Visual table editor and SQL editor
✅ **Scalable**: Easy to upgrade resources
✅ **Real-time**: Can add real-time features later
✅ **Free Tier**: 500MB database, 2GB bandwidth/month

## Troubleshooting

### Connection Issues
- Verify your database password is correct
- Check that your IP is allowed (Supabase allows all IPs by default)
- Ensure the host format is `db.xxxxxxxxxxxxx.supabase.co`

### SSL/TLS Errors
Supabase requires SSL. If you get SSL errors, you can add `?sslmode=require` to your connection string.

### View Logs
Check the Supabase Dashboard → **Logs** → **Postgres Logs** for database errors

### Direct SQL Access
Use the **SQL Editor** in Supabase Dashboard to run queries:
```sql
SELECT * FROM analyses ORDER BY created_at DESC LIMIT 10;
```

## Migration from Local PostgreSQL

If you have existing data from local PostgreSQL:

1. Export from local database:
   ```bash
   pg_dump -U postgres -d postgres -t analyses > analyses_backup.sql
   ```

2. Import to Supabase using the SQL Editor in dashboard:
   - Paste the SQL content
   - Run the query

## Next Steps

- ✅ Database is now cloud-hosted on Supabase
- Consider adding Row Level Security (RLS) policies
- Explore Supabase's real-time features
- Add Supabase Storage for image uploads
- Implement Supabase Auth for user authentication

## Resources

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Python Client](https://supabase.com/docs/reference/python/introduction)
- [PostgreSQL Connection](https://supabase.com/docs/guides/database/connecting-to-postgres)
