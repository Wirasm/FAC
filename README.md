# FastAPI Clerk Astro Starter Pack (FAC)

A full-stack starter template featuring FastAPI backend with Clerk authentication and Astro frontend.

## 📁 Project Structure

This repository is organized as a monorepo containing both backend and frontend code:

```
/
├── backend/           # FastAPI application with Clerk authentication
│   ├── auth/          # Authentication modules and dependencies
│   ├── core/          # Core configuration and middleware
│   ├── tests/         # Test suite for the API
│   └── main.py        # FastAPI application entry point
│
└── frontend/          # Astro frontend application
    ├── public/        # Static assets
    └── src/           # Source code
        ├── layouts/   # Layout components
        ├── pages/     # Page components
        └── components/# Reusable components
```

## 🚀 Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```
   cd backend
   ```

2. Create a virtual environment and install dependencies:
   ```
   uv sync
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Create a `.env` file based on the provided `.env.example` with your Clerk API keys.

4. Run the FastAPI server:
   ```
   uv run main.py
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```
   cd frontend
   ```

2. Install dependencies:
   ```
   pnpm install
   ```

3. Start the development server:
   ```
   pnpm dev
   ```

## 🧪 Testing

### Backend Tests

Run the backend tests from the backend directory:
```
cd backend
pytest
```

## 🔒 Authentication

This starter pack uses [Clerk](https://clerk.dev/) for authentication:

1. The backend verifies JWT tokens issued by Clerk
2. Protected routes require valid authentication
3. The frontend uses Clerk.js for user authentication flow

## 📦 Development

When developing, you'll typically want to run both the backend and frontend servers simultaneously:

1. Terminal 1 (Backend):
   ```
   cd backend
   source .venv/bin/activate
   uv run main.py
   ```

2. Terminal 2 (Frontend):
   ```
   cd frontend
   pnpm dev
   ```

## 📚 Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Clerk Documentation](https://clerk.dev/docs)
- [Astro Documentation](https://docs.astro.build)
