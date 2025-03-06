-- This script runs automatically when the container starts for the first time

-- Create tables (optional - your FastAPI app can handle this too)
CREATE TABLE IF NOT EXISTS playrooms (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    image_url TEXT,
    clerk_user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample data (optional)
INSERT INTO playrooms (title, description, image_url, clerk_user_id)
VALUES 
('Sample Playroom', 'This is a sample playroom for testing', 'https://example.com/sample-image.jpg', 'user_2jkl3h4k5j6h7l8j9');