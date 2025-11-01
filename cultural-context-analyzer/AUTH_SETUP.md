# Authentication Setup Guide

This guide will help you set up user authentication for the Cultural Context Analyzer.

## Database Setup

**IMPORTANT:** You need to create a `users` table and update the `analyses` table in your Supabase database before the authentication will work.

### Quick Setup

1. Go to your Supabase Dashboard: https://supabase.com/dashboard
2. Select your project
3. Navigate to **SQL Editor** (left sidebar)
4. Click **New Query**
5. **First**, copy and paste the contents of `backend/setup_users_table.sql` and click **Run**
6. **Second**, copy and paste the contents of `backend/add_user_id_to_analyses.sql` and click **Run**

Alternatively, you can manually run this SQL:

```sql
-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id BIGSERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create index on email for faster lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Enable Row Level Security (optional, but recommended)
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Policy to allow insert for registration
CREATE POLICY "Allow insert for service role" ON users
    FOR INSERT WITH CHECK (true);

-- Policy to allow read access
CREATE POLICY "Users can read own data" ON users
    FOR SELECT USING (true);
```

## Installation

### Backend Dependencies

Install the new authentication dependencies:

```bash
cd backend
pip install -r requirements.txt
```

The new dependencies are:
- `bcrypt>=4.0.1` - For password hashing
- `python-jose[cryptography]>=3.3.0` - For JWT token generation and verification

### Frontend Dependencies

Install react-router-dom:

```bash
cd frontend
npm install
```

## API Endpoints

### Register User
- **POST** `/api/auth/register`
- **Body:**
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "1234567890",
    "password": "password123"
  }
  ```
- **Response:**
  ```json
  {
    "access_token": "eyJ...",
    "token_type": "bearer",
    "user": {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "1234567890",
      "created_at": "2024-01-01T00:00:00"
    }
  }
  ```

### Login
- **POST** `/api/auth/login`
- **Body:**
  ```json
  {
    "email": "john@example.com",
    "password": "password123"
  }
  ```
- **Response:** Same as register response

### Get Current User
- **GET** `/api/auth/me`
- **Headers:** `Authorization: Bearer <token>`
- **Response:** User object without password_hash

## Frontend Routes

- `/` - Main analyzer page (protected, requires login)
- `/login` - Login page
- `/register` - Registration page

## Security Notes

1. **JWT Secret Key**: The current SECRET_KEY in `main.py` is a placeholder. In production, set it as an environment variable:
   ```python
   SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production-use-env-variable")
   ```

2. **Password Requirements**: 
   - Minimum 6 characters
   - Stored as bcrypt hash (never plaintext)

3. **Token Expiration**: Currently set to 7 days. You can adjust `ACCESS_TOKEN_EXPIRE_MINUTES` in `main.py`.

## Testing

1. Start the backend:
   ```bash
   cd backend
   python main.py
   ```

2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```

3. Navigate to `http://localhost:5173/register` to create an account
4. After registration, you'll be automatically logged in
5. Navigate to `/login` to test login functionality

## Troubleshooting

### "Email already registered" error
- The email already exists in the database
- Try logging in instead or use a different email

### "Could not validate credentials" error
- Token may be expired or invalid
- Try logging in again

### Database connection errors
- Make sure your Supabase credentials are set in `.env`:
  ```
  SUPABASE_URL=your-supabase-url
  SUPABASE_ANON_KEY=your-anon-key
  ```

