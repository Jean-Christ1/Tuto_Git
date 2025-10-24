/**
 * API Service Module
 *
 * This module provides functions to interact with the backend API
 * for natural language to SQL conversion and database querying.
 */

import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for adding auth tokens or other headers
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for handling errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server responded with error
      console.error('API Error:', error.response.data);
    } else if (error.request) {
      // Request made but no response
      console.error('Network Error:', error.request);
    } else {
      // Something else happened
      console.error('Error:', error.message);
    }
    return Promise.reject(error);
  }
);

/**
 * Query API endpoints
 */
export const queryAPI = {
  /**
   * Execute a natural language query
   *
   * @param {string} query - Natural language query
   * @param {string} visualizationType - Preferred visualization type
   * @param {number} maxResults - Maximum number of results
   * @returns {Promise} Query results
   */
  executeNaturalLanguage: async (query, visualizationType = 'table', maxResults = 100) => {
    const response = await api.post('/api/query/nl', {
      query,
      visualization_type: visualizationType,
      max_results: maxResults,
    });
    return response.data;
  },

  /**
   * Execute a SQL query directly
   *
   * @param {string} sqlQuery - SQL query to execute
   * @param {number} maxResults - Maximum number of results
   * @returns {Promise} Query results
   */
  executeSQL: async (sqlQuery, maxResults = 100) => {
    const response = await api.post('/api/query/sql', {
      sql_query: sqlQuery,
      max_results: maxResults,
    });
    return response.data;
  },

  /**
   * Get explanation of a SQL query
   *
   * @param {string} sqlQuery - SQL query to explain
   * @returns {Promise} Query explanation
   */
  explainQuery: async (sqlQuery) => {
    const response = await api.post('/api/query/explain', null, {
      params: { sql_query: sqlQuery },
    });
    return response.data;
  },

  /**
   * Export query results as CSV
   *
   * @param {string} query - Natural language query
   * @returns {Promise} CSV data
   */
  exportCSV: async (query) => {
    const response = await api.post('/api/query/export/csv', {
      natural_language_query: query,
    }, {
      responseType: 'blob',
    });
    return response.data;
  },

  /**
   * Export query results as JSON
   *
   * @param {string} query - Natural language query
   * @returns {Promise} JSON data
   */
  exportJSON: async (query) => {
    const response = await api.post('/api/query/export/json', {
      natural_language_query: query,
    });
    return response.data;
  },
};

/**
 * Schema API endpoints
 */
export const schemaAPI = {
  /**
   * Get complete database schema
   *
   * @returns {Promise} Database schema
   */
  getSchema: async () => {
    const response = await api.get('/api/schema');
    return response.data;
  },

  /**
   * Get list of all tables
   *
   * @returns {Promise} List of table names
   */
  getTables: async () => {
    const response = await api.get('/api/schema/tables');
    return response.data;
  },

  /**
   * Get schema for a specific table
   *
   * @param {string} tableName - Name of the table
   * @returns {Promise} Table schema
   */
  getTableSchema: async (tableName) => {
    const response = await api.get(`/api/schema/tables/${tableName}`);
    return response.data;
  },

  /**
   * Get related tables for a specific table
   *
   * @param {string} tableName - Name of the table
   * @returns {Promise} Related tables
   */
  getRelatedTables: async (tableName) => {
    const response = await api.get(`/api/schema/tables/${tableName}/related`);
    return response.data;
  },

  /**
   * Get statistics for a specific table
   *
   * @param {string} tableName - Name of the table
   * @returns {Promise} Table statistics
   */
  getTableStatistics: async (tableName) => {
    const response = await api.get(`/api/schema/tables/${tableName}/statistics`);
    return response.data;
  },

  /**
   * Get query suggestions
   *
   * @returns {Promise} List of suggested queries
   */
  getSuggestions: async () => {
    const response = await api.get('/api/schema/suggestions');
    return response.data;
  },

  /**
   * Search schema for columns
   *
   * @param {string} searchTerm - Search term
   * @returns {Promise} Search results
   */
  searchSchema: async (searchTerm) => {
    const response = await api.get('/api/schema/search', {
      params: { q: searchTerm },
    });
    return response.data;
  },

  /**
   * Get Entity Relationship Diagram data
   *
   * @returns {Promise} ERD data
   */
  getERD: async () => {
    const response = await api.get('/api/schema/erd');
    return response.data;
  },

  /**
   * Get all relationships
   *
   * @returns {Promise} List of relationships
   */
  getRelationships: async () => {
    const response = await api.get('/api/schema/relationships');
    return response.data;
  },
};

/**
 * Health check
 *
 * @returns {Promise} Health status
 */
export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
