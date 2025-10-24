# Natural Language to SQL - Accelerator

A modern, full-stack web platform that enables users to query databases using natural language and visualize results through interactive dashboards and charts.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![React](https://img.shields.io/badge/react-18.x-blue.svg)
![FastAPI](https://img.shields.io/badge/fastapi-0.104+-green.svg)

## 🚀 Features

- **Natural Language Queries**: Ask questions in plain English and get SQL results
- **Interactive Dashboard**: Modern, responsive UI built with React and Tailwind CSS
- **Real-time Visualizations**: Dynamic charts and graphs using Recharts
- **Query History**: Track and reuse previous queries
- **Schema Explorer**: Browse database structure and relationships
- **Smart Suggestions**: Get query suggestions based on your data
- **Export Capabilities**: Download results as CSV, JSON, or Excel
- **Multi-database Support**: Works with SQLite, PostgreSQL, MySQL

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## 🏗️ Architecture

```
┌─────────────────┐
│   React App     │  Modern UI with Tailwind CSS
│   (Frontend)    │  Recharts for visualizations
└────────┬────────┘
         │ REST API
┌────────▼────────┐
│   FastAPI       │  Backend API Server
│   (Backend)     │  Authentication & Routing
└────────┬────────┘
         │
┌────────▼────────┐
│  NL to SQL      │  LangChain + LLM
│  Engine         │  Query Generation
└────────┬────────┘
         │
┌────────▼────────┐
│   Database      │  SQLite/PostgreSQL/MySQL
│   (Chinook DB)  │  Sample Music Store Data
└─────────────────┘
```

## 🔧 Prerequisites

- **Python 3.9+**
- **Node.js 18+** and npm/yarn
- **OpenAI API Key** or **Anthropic API Key** (for NL to SQL)
- **Docker** (optional, for containerized deployment)

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/natural-language-to-sql-accelerator.git
cd natural-language-to-sql-accelerator
```

### 2. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
# or
yarn install
```

### 4. Database Setup

The Chinook database (SQLite) is included in the `database/` folder. It contains sample music store data with:
- 11 tables
- ~25,000 records
- Customers, invoices, tracks, artists, albums, and more

## 🚀 Quick Start

### Using Docker (Recommended)

```bash
docker-compose up --build
```

Access the application at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
cp .env.example .env
# Edit .env and add your API keys
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
# or
yarn start
```

## ⚙️ Configuration

Create a `.env` file in the `backend/` directory:

```env
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# LLM Provider (openai or anthropic)
LLM_PROVIDER=openai
OPENAI_API_KEY=your_openai_api_key_here
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Database
DATABASE_URL=sqlite:///./database/chinook.db

# Security
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# Query Settings
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT=30
```

## 💡 Usage

### Example Queries

Try these natural language queries:

1. **Simple Query**: "Show me all customers from the USA"
2. **Aggregation**: "What are the total sales by country?"
3. **Join Query**: "List the top 10 best-selling tracks with their artists"
4. **Time-based**: "Show monthly revenue for 2023"
5. **Complex**: "Which genres generate the most revenue per customer?"

### Dashboard Features

- **Query Input**: Type your question in natural language
- **Visualization Selector**: Choose from bar, line, pie, or table charts
- **Schema Browser**: Explore tables, columns, and relationships
- **Query History**: Review and rerun past queries
- **Export**: Download results in multiple formats

## 📚 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

- `POST /api/query` - Submit natural language query
- `GET /api/schema` - Get database schema information
- `GET /api/history` - Retrieve query history
- `POST /api/execute-sql` - Execute raw SQL (admin only)
- `GET /api/suggestions` - Get query suggestions

## 🛠️ Development

### Project Structure

```
natural-language-to-sql-accelerator/
├── backend/                  # Python FastAPI backend
│   ├── app/
│   │   ├── main.py          # Application entry point
│   │   ├── config.py        # Configuration management
│   │   ├── database.py      # Database connection
│   │   ├── models/          # Pydantic models
│   │   ├── routers/         # API route handlers
│   │   ├── services/        # Business logic
│   │   │   ├── nl_to_sql.py       # NL to SQL conversion
│   │   │   ├── query_executor.py  # Query execution
│   │   │   └── schema_analyzer.py # Schema analysis
│   │   └── utils/           # Utility functions
│   ├── tests/               # Backend tests
│   └── requirements.txt     # Python dependencies
├── frontend/                # React frontend
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── hooks/           # Custom React hooks
│   │   └── utils/           # Utility functions
│   └── package.json         # Node dependencies
├── database/                # Database files
│   └── chinook.db          # Sample SQLite database
└── docker-compose.yml       # Docker configuration
```

### Code Style

- **Python**: Black formatter, isort for imports, flake8 for linting
- **JavaScript**: ESLint + Prettier
- **Docstrings**: NumPy style for all Python functions
- **TypeScript**: Enabled for type safety in frontend

### Running Tests

**Backend:**
```bash
cd backend
pytest tests/ -v --cov=app
```

**Frontend:**
```bash
cd frontend
npm test
# or
yarn test
```

## 🐳 Deployment

### Docker Deployment

```bash
docker-compose up -d
```

### Cloud Deployment

#### AWS (Elastic Beanstalk)
```bash
eb init -p python-3.9 nl-to-sql-accelerator
eb create nl-to-sql-env
eb deploy
```

#### Heroku
```bash
heroku create your-app-name
git push heroku main
```

#### Digital Ocean / Azure / GCP
See `docs/deployment.md` for detailed instructions.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Chinook Database**: Sample database for music store scenarios
- **LangChain**: Framework for building LLM applications
- **FastAPI**: Modern Python web framework
- **React**: Frontend library
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Composable charting library

## 📞 Support

- **Documentation**: [Full documentation](docs/README.md)
- **Issues**: [GitHub Issues](https://github.com/yourusername/natural-language-to-sql-accelerator/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/natural-language-to-sql-accelerator/discussions)

## 🗺️ Roadmap

- [x] Basic NL to SQL conversion
- [x] Interactive dashboard
- [x] Chart visualizations
- [ ] Multi-user support with authentication
- [ ] Query optimization suggestions
- [ ] Advanced analytics and insights
- [ ] Custom database connections
- [ ] Mobile responsive design improvements
- [ ] AI-powered data insights
- [ ] Scheduled reports and alerts

---

**Built with ❤️ for data enthusiasts**
