# Database Commands Reference

Complete guide for managing the PostgreSQL database for Cultural Context Analyzer.

## Initial Setup

### Create Database

```sql
-- Connect to PostgreSQL
psql -U postgres

-- Create database
CREATE DATABASE cultural_context_db;

-- List all databases (verify creation)
\l

-- Connect to the database
\c cultural_context_db

-- Exit
\q
```

## Viewing Data

### Connect to Database

```powershell
psql -U postgres -d cultural_context_db
```

### Basic Queries

```sql
-- View all analyses (summary)
SELECT id, language, LEFT(input_text, 50) as text_preview, created_at 
FROM analyses 
ORDER BY created_at DESC;

-- View specific analysis by ID
SELECT * FROM analyses WHERE id = 1;

-- View full text of an analysis
SELECT id, input_text, cultural_origin 
FROM analyses 
WHERE id = 1;

-- Count total analyses
SELECT COUNT(*) FROM analyses;

-- Count by language
SELECT language, COUNT(*) as count 
FROM analyses 
GROUP BY language 
ORDER BY count DESC;

-- Recent analyses (last 10)
SELECT id, LEFT(input_text, 40) as text, created_at 
FROM analyses 
ORDER BY created_at DESC 
LIMIT 10;

-- Search by text content
SELECT id, input_text, created_at 
FROM analyses 
WHERE input_text ILIKE '%ramayana%';

-- Analyses from specific date
SELECT id, input_text, created_at 
FROM analyses 
WHERE DATE(created_at) = '2024-01-01';

-- Analyses from last 7 days
SELECT id, LEFT(input_text, 50) as text, created_at 
FROM analyses 
WHERE created_at >= NOW() - INTERVAL '7 days';
```

## Data Management

### Delete Data

```sql
-- Delete specific analysis
DELETE FROM analyses WHERE id = 1;

-- Delete all analyses (careful!)
DELETE FROM analyses;

-- Delete old analyses (older than 30 days)
DELETE FROM analyses 
WHERE created_at < NOW() - INTERVAL '30 days';

-- Delete by language
DELETE FROM analyses WHERE language = 'en';
```

### Update Data

```sql
-- Update language
UPDATE analyses 
SET language = 'hi' 
WHERE id = 1;

-- Update text
UPDATE analyses 
SET input_text = 'Updated text' 
WHERE id = 1;
```

## Database Maintenance

### Backup Database

```powershell
# Full backup
pg_dump -U postgres cultural_context_db > backup.sql

# Backup with timestamp
pg_dump -U postgres cultural_context_db > backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').sql

# Backup specific table
pg_dump -U postgres -t analyses cultural_context_db > analyses_backup.sql

# Compressed backup
pg_dump -U postgres cultural_context_db | gzip > backup.sql.gz
```

### Restore Database

```powershell
# Restore from backup
psql -U postgres cultural_context_db < backup.sql

# Restore compressed backup
gunzip -c backup.sql.gz | psql -U postgres cultural_context_db

# Drop and recreate before restore
psql -U postgres -c "DROP DATABASE cultural_context_db;"
psql -U postgres -c "CREATE DATABASE cultural_context_db;"
psql -U postgres cultural_context_db < backup.sql
```

### Reset Database

```sql
-- Connect to database
\c cultural_context_db

-- Drop table
DROP TABLE analyses;

-- Recreate table (or restart backend to auto-create)
CREATE TABLE analyses (
    id SERIAL PRIMARY KEY,
    input_text TEXT NOT NULL,
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    cultural_origin TEXT NOT NULL,
    cross_cultural_connections TEXT NOT NULL,
    modern_analogy TEXT NOT NULL,
    visualization_description TEXT NOT NULL,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Advanced Queries

### Statistics

```sql
-- Average text length
SELECT AVG(LENGTH(input_text)) as avg_length 
FROM analyses;

-- Longest text
SELECT id, LENGTH(input_text) as length, LEFT(input_text, 50) as preview 
FROM analyses 
ORDER BY length DESC 
LIMIT 5;

-- Analyses per day
SELECT DATE(created_at) as date, COUNT(*) as count 
FROM analyses 
GROUP BY DATE(created_at) 
ORDER BY date DESC;

-- Most common languages
SELECT language, COUNT(*) as count 
FROM analyses 
GROUP BY language 
ORDER BY count DESC;
```

### Export Data

```sql
-- Export to CSV
\copy (SELECT * FROM analyses) TO 'analyses.csv' WITH CSV HEADER;

-- Export specific columns
\copy (SELECT id, input_text, language, created_at FROM analyses) TO 'analyses_summary.csv' WITH CSV HEADER;

-- Export filtered data
\copy (SELECT * FROM analyses WHERE language = 'en') TO 'english_analyses.csv' WITH CSV HEADER;
```

### Import Data

```sql
-- Import from CSV
\copy analyses(input_text, language, cultural_origin, cross_cultural_connections, modern_analogy, visualization_description) FROM 'data.csv' WITH CSV HEADER;
```

## Database Information

### Table Structure

```sql
-- View table structure
\d analyses

-- View all tables
\dt

-- View table size
SELECT pg_size_pretty(pg_total_relation_size('analyses')) as size;

-- View indexes
\di
```

### Database Information

```sql
-- Current database
SELECT current_database();

-- Database size
SELECT pg_size_pretty(pg_database_size('cultural_context_db')) as size;

-- Connection info
\conninfo

-- List all databases
\l

-- List all users
\du
```

## Performance Optimization

### Create Indexes

```sql
-- Index on language for faster filtering
CREATE INDEX idx_language ON analyses(language);

-- Index on created_at for faster date queries
CREATE INDEX idx_created_at ON analyses(created_at);

-- Text search index
CREATE INDEX idx_input_text ON analyses USING gin(to_tsvector('english', input_text));
```

### Analyze Table

```sql
-- Update statistics
ANALYZE analyses;

-- Vacuum table
VACUUM analyses;

-- Full vacuum
VACUUM FULL analyses;
```

## User Management

### Create Read-Only User

```sql
-- Create user
CREATE USER readonly_user WITH PASSWORD 'secure_password';

-- Grant connect
GRANT CONNECT ON DATABASE cultural_context_db TO readonly_user;

-- Grant select only
GRANT SELECT ON analyses TO readonly_user;
```

### Create Application User

```sql
-- Create user
CREATE USER app_user WITH PASSWORD 'secure_password';

-- Grant all privileges
GRANT ALL PRIVILEGES ON DATABASE cultural_context_db TO app_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO app_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO app_user;
```

## Troubleshooting

### Connection Issues

```powershell
# Check if PostgreSQL is running
Get-Service postgresql*

# Start PostgreSQL service
Start-Service postgresql-x64-XX

# Check port
netstat -an | findstr :5432
```

### Reset Password

```sql
-- As postgres user
ALTER USER postgres WITH PASSWORD 'new_password';
```

### Check Connections

```sql
-- View active connections
SELECT * FROM pg_stat_activity WHERE datname = 'cultural_context_db';

-- Kill connection
SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = 'cultural_context_db' AND pid <> pg_backend_pid();
```

## Useful psql Commands

```
\l              List all databases
\c dbname       Connect to database
\dt             List all tables
\d tablename    Describe table
\du             List users
\q              Quit
\?              Help
\h SQL_COMMAND  SQL command help
\timing         Toggle query timing
\x              Toggle expanded display
```

## Automation Scripts

### Daily Backup Script

Create `backup_daily.ps1`:

```powershell
$date = Get-Date -Format 'yyyyMMdd'
$backupFile = "backup_$date.sql"
pg_dump -U postgres cultural_context_db > $backupFile
Write-Host "Backup created: $backupFile"
```

### Cleanup Old Data Script

Create `cleanup_old.ps1`:

```powershell
psql -U postgres -d cultural_context_db -c "DELETE FROM analyses WHERE created_at < NOW() - INTERVAL '90 days';"
Write-Host "Old analyses deleted"
```

## Best Practices

1. **Regular Backups**: Backup daily or before major changes
2. **Monitor Size**: Check database size regularly
3. **Clean Old Data**: Remove old analyses periodically
4. **Use Indexes**: Create indexes for frequently queried columns
5. **Vacuum Regularly**: Run VACUUM to reclaim space
6. **Secure Passwords**: Use strong passwords for database users
7. **Limit Privileges**: Give users only necessary permissions
8. **Monitor Connections**: Check for idle connections

## Quick Reference

```sql
-- Most common operations
SELECT * FROM analyses ORDER BY created_at DESC LIMIT 10;  -- Recent
SELECT COUNT(*) FROM analyses;                              -- Count
DELETE FROM analyses WHERE id = 1;                          -- Delete
\copy analyses TO 'backup.csv' WITH CSV HEADER;            -- Export
```

---

For more information, see the [PostgreSQL Documentation](https://www.postgresql.org/docs/)
