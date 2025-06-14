# TDS Virtual Teaching Assistant

A Flask-based virtual teaching assistant for data science courses, featuring AI-powered question answering and course material search.

## Features

- AI-powered question answering using OpenAI GPT
- Course material search and retrieval
- Image analysis support
- RESTful API endpoints
- Web interface for testing
- SQLite database for storing Q&A history

## Live Demo

Deploy this app to Vercel by clicking the button below:

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/your-username/tds-virtual-ta)

## Quick Deploy to Vercel

1. **Fork this repository** to your GitHub account
2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click "New Project"
   - Import your forked repository
   - Vercel will automatically detect the configuration
3. **Add Environment Variables** (Optional):
   - `OPENAI_API_KEY`: Your OpenAI API key for AI responses
   - `SESSION_SECRET`: Random string for session security
4. **Deploy**: Click "Deploy" and your app will be live!

## API Endpoints

- `POST /api/` - Submit questions for AI responses
- `GET /api/health` - Health check
- `GET /api/stats` - Usage statistics

## Local Development

```bash
# Clone the repository
git clone https://github.com/your-username/tds-virtual-ta.git
cd tds-virtual-ta

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

Visit `http://localhost:5000` to access the web interface.

## Environment Variables

- `DATABASE_URL`: Database connection string (optional, defaults to SQLite)
- `OPENAI_API_KEY`: OpenAI API key for AI responses (optional)
- `SESSION_SECRET`: Secret key for Flask sessions (optional)

## Tech Stack

- **Backend**: Flask, SQLAlchemy
- **Database**: SQLite (local), PostgreSQL (production)
- **AI**: OpenAI GPT-4
- **Deployment**: Vercel
- **Frontend**: HTML, CSS, JavaScript

## License

MIT License