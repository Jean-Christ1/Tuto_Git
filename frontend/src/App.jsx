/**
 * Main App Component
 *
 * Root component for the Natural Language to SQL application.
 */

import React, { useState, useEffect } from 'react';
import toast, { Toaster } from 'react-hot-toast';
import Header from './components/Header';
import QueryInput from './components/QueryInput';
import ResultsVisualization from './components/ResultsVisualization';
import SchemaExplorer from './components/SchemaExplorer';
import { queryAPI, schemaAPI } from './services/api';
import {
  ChartBarIcon,
  ExclamationTriangleIcon,
} from '@heroicons/react/24/outline';

function App() {
  const [queryResult, setQueryResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [currentQuery, setCurrentQuery] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [queryHistory, setQueryHistory] = useState([]);

  useEffect(() => {
    loadSuggestions();
  }, []);

  const loadSuggestions = async () => {
    try {
      const response = await schemaAPI.getSuggestions();
      if (response.success) {
        setSuggestions(response.suggestions);
      }
    } catch (error) {
      console.error('Failed to load suggestions:', error);
    }
  };

  const handleQuerySubmit = async (query) => {
    setLoading(true);
    setCurrentQuery(query);
    setQueryResult(null);

    try {
      const result = await queryAPI.executeNaturalLanguage(query);

      if (result.success) {
        setQueryResult(result);

        // Add to history
        setQueryHistory(prev => [
          {
            query,
            sql: result.generated_sql,
            timestamp: new Date(),
            rowCount: result.result.row_count,
          },
          ...prev.slice(0, 9) // Keep last 10
        ]);

        toast.success(
          `Query executed successfully! ${result.result.row_count} rows returned in ${result.result.execution_time_ms}ms`,
          {
            duration: 3000,
            icon: '✅',
          }
        );
      } else {
        toast.error(result.error || 'Query execution failed');
      }
    } catch (error) {
      console.error('Query error:', error);
      const errorMessage = error.response?.data?.detail || error.message || 'An error occurred';
      toast.error(`Query failed: ${errorMessage}`, {
        duration: 5000,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleTableSelect = (tableName, action) => {
    let query = '';
    if (action === 'Show all') {
      query = `Show all ${tableName}`;
    } else if (action === 'Count records') {
      query = `How many records are in ${tableName}?`;
    }
    handleQuerySubmit(query);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-indigo-50">
      <Toaster position="top-right" />

      {/* Header */}
      <Header />

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Hero Section */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-primary-500 to-primary-600 rounded-2xl shadow-lg mb-4">
            <ChartBarIcon className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            Ask Questions About Your Data
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Transform natural language into powerful SQL queries and visualize your data instantly
          </p>
        </div>

        {/* Query Input Section */}
        <div className="mb-8">
          <QueryInput
            onSubmit={handleQuerySubmit}
            suggestions={suggestions}
            loading={loading}
          />
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Results Section (2 columns) */}
          <div className="lg:col-span-2 space-y-6">
            {/* Loading State */}
            {loading && (
              <div className="card">
                <div className="flex flex-col items-center justify-center py-12">
                  <div className="loading-dots text-primary-600 text-2xl mb-4">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                  <p className="text-gray-600">Analyzing your query and fetching results...</p>
                </div>
              </div>
            )}

            {/* Results */}
            {!loading && queryResult && (
              <ResultsVisualization
                result={queryResult}
                query={currentQuery}
                sqlQuery={queryResult.generated_sql}
              />
            )}

            {/* Empty State */}
            {!loading && !queryResult && (
              <div className="card">
                <div className="flex flex-col items-center justify-center py-12 text-center">
                  <div className="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mb-4">
                    <ChartBarIcon className="w-8 h-8 text-gray-400" />
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    No Results Yet
                  </h3>
                  <p className="text-gray-600 max-w-md">
                    Enter a question above to query your database. Try asking about customers,
                    sales, or any other data in your database.
                  </p>
                </div>
              </div>
            )}

            {/* Query History */}
            {queryHistory.length > 0 && (
              <div className="card">
                <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Queries</h3>
                <div className="space-y-2">
                  {queryHistory.map((item, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleQuerySubmit(item.query)}
                      className="w-full text-left p-3 bg-gray-50 hover:bg-gray-100 rounded-lg transition-colors group"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-medium text-gray-900 group-hover:text-primary-600 truncate">
                            {item.query}
                          </p>
                          <p className="text-xs text-gray-500 mt-1 font-mono truncate">
                            {item.sql}
                          </p>
                        </div>
                        <span className="badge badge-primary ml-2">
                          {item.rowCount} rows
                        </span>
                      </div>
                      <p className="text-xs text-gray-400 mt-1">
                        {new Date(item.timestamp).toLocaleTimeString()}
                      </p>
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Schema Explorer (1 column) */}
          <div className="lg:col-span-1">
            <SchemaExplorer onTableSelect={handleTableSelect} />

            {/* Tips Card */}
            <div className="card mt-6 bg-gradient-to-br from-yellow-50 to-orange-50 border-yellow-200">
              <div className="flex items-start gap-3">
                <ExclamationTriangleIcon className="w-5 h-5 text-yellow-600 flex-shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">Query Tips</h4>
                  <ul className="text-sm text-gray-700 space-y-1">
                    <li>• Be specific about what you want to see</li>
                    <li>• Use table names from the schema</li>
                    <li>• Try "top 10" or "limit 5" for large datasets</li>
                    <li>• Ask for aggregations like "total" or "average"</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-gray-200 text-center">
          <p className="text-sm text-gray-600">
            Natural Language to SQL Accelerator • Powered by LangChain & FastAPI
          </p>
          <p className="text-xs text-gray-500 mt-2">
            Sample data from Chinook Database • 11 tables • 25,000+ records
          </p>
        </footer>
      </main>
    </div>
  );
}

export default App;
