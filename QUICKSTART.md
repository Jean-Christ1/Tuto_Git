# Quick Start Guide

Get up and running with Natural Language to SQL in under 5 minutes!

## Prerequisites

Before you begin, ensure you have:

- ✅ Python 3.9 or higher
- ✅ Node.js 18 or higher
- ✅ OpenAI API key OR Anthropic API key
- ✅ Git (to clone the repository)

## Option 1: Docker (Recommended)

The fastest way to get started!

### Step 1: Get an API Key

**OpenAI:**
1. Visit https://platform.openai.com/api-keys
2. Create a new API key
3. Copy the key

**OR Anthropic:**
1. Visit https://console.anthropic.com/
2. Create an API key
3. Copy the key

### Step 2: Clone and Configure

```bash
# Clone the repository
git clone https://github.com/yourusername/natural-language-to-sql-accelerator.git
cd natural-language-to-sql-accelerator

# Create .env file
cat > backend/.env << EOF
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
EOF
```

### Step 3: Run with Docker

```bash
# Start all services
docker-compose up -d

# Check if services are running
docker-compose ps
```

### Step 4: Access the Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

That's it! 🎉

## Option 2: Manual Setup

If you prefer to run services individually:

### Step 1: Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Edit and add your API key

# Start backend server
uvicorn app.main:app --reload
```

Backend will be running at http://localhost:8000

### Step 2: Frontend Setup

Open a new terminal:

```bash
cd frontend

# Install dependencies
npm install

# Configure environment (optional)
cp .env.example .env

# Start frontend
npm start
```

Frontend will open at http://localhost:3000

## Your First Query

1. **Open the app** at http://localhost:3000

2. **Type a question** in the query box:
   ```
   Show me all customers from the USA
   ```

3. **Click "Query"** or press Enter

4. **View results** in table or chart format

## Example Queries to Try

### Basic Queries
```
Show all albums
List the top 10 artists
How many tracks are there?
```

### Analytics Queries
```
What are the total sales by country?
Show the top 10 best-selling tracks
What is the average invoice amount?
```

### Complex Queries
```
Which genres generate the most revenue?
Show customer purchase history with totals
List all tracks with their artists and albums
```

## Exploring the Database

The sample Chinook database includes:

- 🎵 **11 tables**: Artists, Albums, Tracks, Customers, Invoices, etc.
- 📊 **25,000+ records**: Real-world music store data
- 🔗 **10 relationships**: Foreign keys linking tables

Use the **Schema Explorer** on the right side to:
- Browse all tables
- View column details
- See relationships
- Click "View Data" for quick queries

## Visualization Types

Switch between different views:

- **📊 Table**: Traditional row/column display
- **📈 Bar Chart**: Compare values across categories
- **📉 Line Chart**: Show trends over time
- **🥧 Pie Chart**: Display proportions

## Exporting Results

Download your query results:

- **CSV**: Click "CSV" button
- **JSON**: Click "JSON" button

## Tips for Better Queries

✅ **DO:**
- Be specific: "Show top 10 customers by sales"
- Use table names: "List albums by AC/DC"
- Ask for totals: "What is the total revenue?"
- Specify limits: "Show first 20 tracks"

❌ **DON'T:**
- Be too vague: "Show me everything"
- Use complex SQL terms (unless you want to)
- Ask questions unrelated to the database

## Troubleshooting

### API Connection Error

```
Error: Network Error
```

**Solution:**
1. Check if backend is running: http://localhost:8000/health
2. Verify CORS settings in `backend/.env`
3. Check firewall settings

### Invalid API Key

```
Error: Authentication failed
```

**Solution:**
1. Verify your API key is correct
2. Check API key has sufficient credits
3. Ensure LLM_PROVIDER matches your key (openai or anthropic)

### Query Failed

```
Error: Query execution failed
```

**Solution:**
1. Check query syntax
2. Verify table names exist (use Schema Explorer)
3. Try a simpler query first

### Database Not Found

```
Error: Database connection failed
```

**Solution:**
1. Ensure `database/chinook.db` exists
2. Check DATABASE_URL in `.env`
3. Try re-downloading the database

## Next Steps

Now that you're up and running:

1. **Explore the Schema**: Click on tables in the Schema Explorer
2. **Try Suggestions**: Click on example queries
3. **View Query History**: Rerun previous queries
4. **Experiment**: Try different visualization types
5. **Export Data**: Download results for further analysis

## Configuration Options

### Backend Configuration

Edit `backend/.env`:

```env
# LLM Provider (openai or anthropic)
LLM_PROVIDER=openai

# API Keys
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here

# Query Settings
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT=30

# Database
DATABASE_URL=sqlite:///../database/chinook.db
```

### Frontend Configuration

Edit `frontend/.env`:

```env
# API URL
REACT_APP_API_URL=http://localhost:8000
```

## Performance Tips

- **Limit results**: Add "limit 100" to queries for faster response
- **Cache results**: Caching is enabled by default (5 min TTL)
- **Use filters**: Narrow down results with WHERE conditions
- **Avoid SELECT ***: Request only needed columns

## Using Different Databases

Want to use your own database?

1. **Place your database** in the `database/` folder
2. **Update DATABASE_URL** in `backend/.env`:
   ```env
   # SQLite
   DATABASE_URL=sqlite:///../database/your_database.db

   # PostgreSQL
   DATABASE_URL=postgresql://user:password@localhost/dbname

   # MySQL
   DATABASE_URL=mysql://user:password@localhost/dbname
   ```
3. **Restart the backend**

## API Documentation

Interactive API documentation is available at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

Try the API endpoints directly from the browser!

## Getting Help

- 📖 **Documentation**: See README.md for full documentation
- 🐛 **Issues**: Report bugs on GitHub Issues
- 💬 **Discussions**: Ask questions in GitHub Discussions
- 📧 **Contact**: Reach out to maintainers

## What's Next?

- [ ] Try all example queries
- [ ] Explore the database schema
- [ ] Export some results
- [ ] Try different visualization types
- [ ] Read the full documentation
- [ ] Customize the configuration
- [ ] Connect your own database

---

**Happy querying! 🚀**

For more details, see the [full README](README.md).
