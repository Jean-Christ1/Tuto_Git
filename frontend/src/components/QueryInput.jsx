/**
 * QueryInput Component
 *
 * Input component for natural language queries with suggestions
 * and query history.
 */

import React, { useState, useEffect } from 'react';
import {
  MagnifyingGlassIcon,
  SparklesIcon,
  ClockIcon,
  LightBulbIcon
} from '@heroicons/react/24/outline';

const QueryInput = ({ onSubmit, suggestions = [], loading = false }) => {
  const [query, setQuery] = useState('');
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [filteredSuggestions, setFilteredSuggestions] = useState([]);

  useEffect(() => {
    if (query.length > 2 && suggestions.length > 0) {
      const filtered = suggestions.filter(s =>
        s.query.toLowerCase().includes(query.toLowerCase())
      ).slice(0, 5);
      setFilteredSuggestions(filtered);
      setShowSuggestions(filtered.length > 0);
    } else {
      setShowSuggestions(false);
    }
  }, [query, suggestions]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !loading) {
      onSubmit(query.trim());
      setShowSuggestions(false);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion.query);
    setShowSuggestions(false);
    onSubmit(suggestion.query);
  };

  const exampleQueries = [
    "Show me all customers from the USA",
    "What are the top 10 best-selling artists?",
    "List all rock music tracks",
    "Show monthly revenue for 2023",
  ];

  return (
    <div className="card">
      <form onSubmit={handleSubmit} className="space-y-4">
        {/* Query Input */}
        <div className="relative">
          <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
            <SparklesIcon className="h-5 w-5 text-primary-500" />
          </div>

          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your data in plain English..."
            className="input-field pl-12 pr-24 py-4 text-lg"
            disabled={loading}
          />

          <button
            type="submit"
            disabled={!query.trim() || loading}
            className="absolute inset-y-0 right-2 m-2 px-6 bg-primary-600 text-white rounded-lg
                     hover:bg-primary-700 disabled:bg-gray-300 disabled:cursor-not-allowed
                     transition-colors duration-200 font-medium flex items-center gap-2"
          >
            {loading ? (
              <>
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <span>Processing</span>
              </>
            ) : (
              <>
                <MagnifyingGlassIcon className="w-5 h-5" />
                <span>Query</span>
              </>
            )}
          </button>
        </div>

        {/* Suggestions Dropdown */}
        {showSuggestions && (
          <div className="absolute z-10 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-80 overflow-y-auto">
            <div className="p-2">
              <div className="px-3 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                Suggestions
              </div>
              {filteredSuggestions.map((suggestion, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="w-full text-left px-3 py-2 hover:bg-gray-50 rounded-md
                           transition-colors duration-150 group"
                >
                  <div className="flex items-start gap-3">
                    <LightBulbIcon className="w-5 h-5 text-primary-500 mt-0.5 flex-shrink-0" />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium text-gray-900 group-hover:text-primary-600">
                        {suggestion.query}
                      </p>
                      <p className="text-xs text-gray-500 mt-1">
                        {suggestion.description}
                      </p>
                      <span className={`badge badge-${
                        suggestion.difficulty === 'easy' ? 'success' :
                        suggestion.difficulty === 'medium' ? 'warning' : 'error'
                      } mt-2`}>
                        {suggestion.category}
                      </span>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Example Queries */}
        {!query && !loading && (
          <div className="flex flex-wrap gap-2">
            <span className="text-sm text-gray-600 flex items-center gap-1">
              <ClockIcon className="w-4 h-4" />
              Try these:
            </span>
            {exampleQueries.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => setQuery(example)}
                className="text-sm px-3 py-1 bg-gray-100 text-gray-700 rounded-full
                         hover:bg-primary-50 hover:text-primary-700 transition-colors duration-200"
              >
                {example}
              </button>
            ))}
          </div>
        )}
      </form>

      {/* Quick Stats */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        <div className="text-center p-3 bg-gradient-to-br from-primary-50 to-primary-100 rounded-lg">
          <p className="text-2xl font-bold text-primary-700">11</p>
          <p className="text-xs text-primary-600">Tables</p>
        </div>
        <div className="text-center p-3 bg-gradient-to-br from-green-50 to-green-100 rounded-lg">
          <p className="text-2xl font-bold text-green-700">25K+</p>
          <p className="text-xs text-green-600">Records</p>
        </div>
        <div className="text-center p-3 bg-gradient-to-br from-purple-50 to-purple-100 rounded-lg">
          <p className="text-2xl font-bold text-purple-700">10</p>
          <p className="text-xs text-purple-600">Relationships</p>
        </div>
      </div>
    </div>
  );
};

export default QueryInput;
