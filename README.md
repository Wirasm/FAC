# FastAPI Clerk Astro Starter Pack (FAC)

A full-stack starter template featuring FastAPI backend with Clerk authentication and Astro frontend. This template includes a sample items catalog with authentication-protected endpoints.

## 📁 Project Structure

This repository is organized as a monorepo containing both backend and frontend code:

```
/
├── backend/                 # FastAPI application with Clerk authentication
│   ├── app/                 # Main application directory
│   │   ├── auth/            # Authentication modules and dependencies
│   │   ├── core/            # Core configuration and middleware
│   │   ├── item/            # Item-related modules (models, schemas, routes)
│   │   ├── database.py      # Database connection and session management
│   │   └── main.py          # FastAPI application entry point
│   ├── tests/               # Test suite for the API
│   └── seed_db.py           # Database seeding script
│
├── frontend/                # Astro frontend application
│   ├── public/              # Static assets
│   ├── src/                 # Source code
│   │   ├── components/      # Reusable components
│   │   ├── layouts/         # Layout components
│   │   ├── pages/           # Page components (including items catalog)
│   │   └── styles/          # CSS and Tailwind styles
│   └── astro.config.mjs     # Astro configuration
│
└── docker-compose.db.yml    # Docker Compose file for PostgreSQL database
```

## 🚀 Getting Started

### Database Setup

1. Start the PostgreSQL database using Docker:
   ```bash
   docker-compose -f docker-compose.db.yml up -d
   ```

2. Verify the database is running:
   ```bash
   docker ps
   ```

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. Create a `.env` file with your Clerk API keys:
   ```
   CLERK_SECRET_KEY=your_secret_key
   CLERK_PUBLISHABLE_KEY=your_publishable_key
   CLERK_FRONTEND_API_URL=https://your-clerk-instance.clerk.accounts.dev
   ```

4. Seed the database with sample items:
   ```bash
   uv run seed_db.py
   ```

5. Run the FastAPI server:
   ```bash
   uv run app/main.py
   ```

   The server will be available at http://127.0.0.1:8000

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   pnpm install
   ```

3. Start the development server:
   ```bash
   pnpm dev
   ```

   The Astro frontend will be available at http://localhost:3000

## 🔍 API Endpoints

### Public Endpoints

- `GET /api/items` - Get a list of all items
- `GET /api/items/{item_id}` - Get a specific item by ID

### Protected Endpoints (Require Authentication)

- `POST /api/items` - Create a new item
- `PUT /api/items/{item_id}` - Update an existing item
- `DELETE /api/items/{item_id}` - Delete an item

## 🧪 Testing

### Backend Tests

Run the backend tests from the backend directory:
```bash
cd backend
uv run pytest
```

## 🔒 Authentication

This starter pack uses [Clerk](https://clerk.dev/) for authentication:

1. The backend verifies JWT tokens issued by Clerk
2. Protected routes require valid authentication
3. The frontend uses Clerk.js for user authentication flow

To configure authentication:
1. Create an account at [Clerk](https://clerk.dev/)
2. Set up an application and get your API keys
3. Update the `.env` file with your keys
4. Configure the Clerk frontend settings in your Clerk dashboard

## 📦 Development Workflow

When developing, run both the backend and frontend servers simultaneously:

1. Terminal 1 (Database):
   ```bash
   docker-compose -f docker-compose.db.yml up
   ```

2. Terminal 2 (Backend):
   ```bash
   cd backend
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv run app/main.py
   ```

3. Terminal 3 (Frontend):
   ```bash
   cd frontend
   pnpm dev
   ```

## 📚 Documentation

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Clerk Documentation](https://clerk.dev/docs)
- [Astro Documentation](https://docs.astro.build)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
