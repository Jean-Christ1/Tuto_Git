/**
 * ResultsVisualization Component
 *
 * Component to display query results with multiple visualization options
 * including table, bar chart, line chart, and pie chart.
 */

import React, { useState } from 'react';
import {
  TableCellsIcon,
  ChartBarIcon,
  ChartPieIcon,
  ArrowDownTrayIcon,
  CodeBracketIcon,
} from '@heroicons/react/24/outline';
import {
  BarChart,
  Bar,
  LineChart,
  Line,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

const ResultsVisualization = ({ result, query, sqlQuery }) => {
  const [viewMode, setViewMode] = useState(result?.suggested_visualization || 'table');
  const [showSQL, setShowSQL] = useState(false);

  if (!result || !result.result) {
    return null;
  }

  const { columns, rows, row_count, execution_time_ms } = result.result;

  // Prepare data for charts
  const prepareChartData = () => {
    if (rows.length === 0) return [];

    return rows.map(row => {
      const obj = {};
      columns.forEach((col, idx) => {
        obj[col] = row[idx];
      });
      return obj;
    });
  };

  const chartData = prepareChartData();

  // Colors for charts
  const COLORS = [
    '#0ea5e9', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981',
    '#6366f1', '#14b8a6', '#f97316', '#06b6d4', '#84cc16'
  ];

  // Export functions
  const handleExportCSV = () => {
    const csvContent = [
      columns.join(','),
      ...rows.map(row => row.map(cell =>
        typeof cell === 'string' && cell.includes(',') ? `"${cell}"` : cell
      ).join(','))
    ].join('\n');

    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'query_results.csv';
    a.click();
  };

  const handleExportJSON = () => {
    const jsonData = chartData;
    const blob = new Blob([JSON.stringify(jsonData, null, 2)], { type: 'application/json' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'query_results.json';
    a.click();
  };

  return (
    <div className="card space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-gray-200 pb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">Query Results</h3>
          <p className="text-sm text-gray-500 mt-1">
            {row_count} rows • {execution_time_ms}ms
          </p>
        </div>

        {/* View Mode Selector */}
        <div className="flex items-center gap-2">
          <div className="flex bg-gray-100 rounded-lg p-1">
            <button
              onClick={() => setViewMode('table')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'table'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="Table View"
            >
              <TableCellsIcon className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('bar')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'bar'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="Bar Chart"
            >
              <ChartBarIcon className="w-5 h-5" />
            </button>
            <button
              onClick={() => setViewMode('line')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'line'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="Line Chart"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z" />
              </svg>
            </button>
            <button
              onClick={() => setViewMode('pie')}
              className={`p-2 rounded-md transition-colors ${
                viewMode === 'pie'
                  ? 'bg-white text-primary-600 shadow-sm'
                  : 'text-gray-600 hover:text-gray-900'
              }`}
              title="Pie Chart"
            >
              <ChartPieIcon className="w-5 h-5" />
            </button>
          </div>

          {/* Export Buttons */}
          <button
            onClick={handleExportCSV}
            className="btn-outline flex items-center gap-2 text-sm"
          >
            <ArrowDownTrayIcon className="w-4 h-4" />
            CSV
          </button>
          <button
            onClick={handleExportJSON}
            className="btn-outline flex items-center gap-2 text-sm"
          >
            <ArrowDownTrayIcon className="w-4 h-4" />
            JSON
          </button>
        </div>
      </div>

      {/* SQL Query Display */}
      <div className="space-y-2">
        <button
          onClick={() => setShowSQL(!showSQL)}
          className="flex items-center gap-2 text-sm text-gray-600 hover:text-primary-600 transition-colors"
        >
          <CodeBracketIcon className="w-4 h-4" />
          {showSQL ? 'Hide' : 'Show'} Generated SQL
        </button>

        {showSQL && sqlQuery && (
          <div className="code-block">
            <code>{sqlQuery}</code>
          </div>
        )}
      </div>

      {/* Visualization */}
      <div className="mt-4">
        {viewMode === 'table' && (
          <div className="overflow-x-auto border border-gray-200 rounded-lg">
            <table className="data-table">
              <thead>
                <tr>
                  {columns.map((col, idx) => (
                    <th key={idx}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {rows.map((row, rowIdx) => (
                  <tr key={rowIdx}>
                    {row.map((cell, cellIdx) => (
                      <td key={cellIdx}>
                        {cell === null ? (
                          <span className="text-gray-400 italic">null</span>
                        ) : typeof cell === 'number' ? (
                          cell.toLocaleString()
                        ) : (
                          cell
                        )}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {viewMode === 'bar' && chartData.length > 0 && (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={chartData.slice(0, 20)}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={columns[0]} angle={-45} textAnchor="end" height={100} />
              <YAxis />
              <Tooltip />
              <Legend />
              {columns.slice(1).map((col, idx) => (
                <Bar key={col} dataKey={col} fill={COLORS[idx % COLORS.length]} />
              ))}
            </BarChart>
          </ResponsiveContainer>
        )}

        {viewMode === 'line' && chartData.length > 0 && (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={columns[0]} />
              <YAxis />
              <Tooltip />
              <Legend />
              {columns.slice(1).map((col, idx) => (
                <Line
                  key={col}
                  type="monotone"
                  dataKey={col}
                  stroke={COLORS[idx % COLORS.length]}
                  strokeWidth={2}
                />
              ))}
            </LineChart>
          </ResponsiveContainer>
        )}

        {viewMode === 'pie' && chartData.length > 0 && columns.length === 2 && (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={chartData.slice(0, 10)}
                dataKey={columns[1]}
                nameKey={columns[0]}
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {chartData.slice(0, 10).map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        )}
      </div>

      {/* Query Info */}
      {query && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-700">
            <span className="font-semibold">Natural Language Query:</span> {query}
          </p>
        </div>
      )}
    </div>
  );
};

export default ResultsVisualization;
