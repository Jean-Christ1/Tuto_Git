# Natural Language to SQL - Frontend

Modern React dashboard for querying databases using natural language.

## Features

- **Natural Language Input**: Type questions in plain English
- **Multiple Visualizations**: Table, bar chart, line chart, and pie chart views
- **Schema Explorer**: Browse database structure and relationships
- **Query Suggestions**: Smart suggestions based on database schema
- **Export Options**: Download results as CSV or JSON
- **Query History**: Track and rerun previous queries
- **Responsive Design**: Works on desktop, tablet, and mobile

## Technology Stack

- **React 18**: Modern React with hooks
- **Tailwind CSS**: Utility-first CSS framework
- **Recharts**: Composable charting library
- **Axios**: HTTP client for API requests
- **Heroicons**: Beautiful hand-crafted SVG icons
- **React Hot Toast**: Notifications

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on http://localhost:8000

### Installation

```bash
# Install dependencies
npm install
# or
yarn install
```

### Configuration

Create a `.env` file in the frontend directory:

```env
REACT_APP_API_URL=http://localhost:8000
```

### Development

```bash
# Start development server
npm start
# or
yarn start
```

The application will open at http://localhost:3000

### Build for Production

```bash
# Create production build
npm run build
# or
yarn build
```

The optimized build will be in the `build/` directory.

## Project Structure

```
frontend/
├── public/
│   └── index.html              # HTML template
├── src/
│   ├── components/             # React components
│   │   ├── Header.jsx         # Header component
│   │   ├── QueryInput.jsx     # Query input with suggestions
│   │   ├── ResultsVisualization.jsx  # Results display
│   │   └── SchemaExplorer.jsx # Database schema explorer
│   ├── services/              # API services
│   │   └── api.js            # API client
│   ├── App.jsx               # Main app component
│   ├── index.js              # Entry point
│   └── index.css             # Global styles
├── package.json              # Dependencies
├── tailwind.config.js        # Tailwind configuration
└── README.md                 # This file
```

## Available Scripts

- `npm start` - Start development server
- `npm build` - Create production build
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (irreversible)

## Usage

### Basic Query

1. Type a question in plain English
2. Click "Query" or press Enter
3. View results in table or chart format

### Example Queries

- "Show me all customers from the USA"
- "What are the top 10 best-selling artists?"
- "List all rock music tracks"
- "Show monthly revenue for 2023"

### Schema Explorer

- Browse all tables and columns
- View relationships between tables
- Click "View Data" to query a table
- Expand tables to see detailed column information

### Visualizations

- **Table**: Traditional row/column view
- **Bar Chart**: Compare values across categories
- **Line Chart**: Show trends over time
- **Pie Chart**: Display proportions and percentages

### Export Results

- Click "CSV" to download as comma-separated values
- Click "JSON" to download as JSON format

## Customization

### Styling

The application uses Tailwind CSS. Customize colors and theme in `tailwind.config.js`:

```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      },
    },
  },
}
```

### API Configuration

Update the API base URL in `.env`:

```env
REACT_APP_API_URL=https://your-api-domain.com
```

## Troubleshooting

### API Connection Issues

If you see connection errors:

1. Ensure backend is running on the correct port
2. Check CORS settings in backend
3. Verify `REACT_APP_API_URL` in `.env`

### Build Issues

If build fails:

```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
npm run build
```

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Performance

- Lazy loading for large result sets
- Optimized bundle size with code splitting
- Efficient re-rendering with React hooks

## Contributing

Contributions welcome! Please see the main project README for guidelines.

## License

MIT License - see LICENSE file for details.
