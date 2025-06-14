from app import app

# Vercel requires the app variable to be accessible at module level
# For local development, run with debug mode
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
