/**
 * SchemaExplorer Component
 *
 * Component to explore database schema with tables, columns, and relationships.
 */

import React, { useState, useEffect } from 'react';
import {
  TableCellsIcon,
  KeyIcon,
  LinkIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  MagnifyingGlassIcon,
} from '@heroicons/react/24/outline';
import { schemaAPI } from '../services/api';

const SchemaExplorer = ({ onTableSelect }) => {
  const [schema, setSchema] = useState(null);
  const [loading, setLoading] = useState(true);
  const [expandedTables, setExpandedTables] = useState(new Set());
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadSchema();
  }, []);

  const loadSchema = async () => {
    try {
      setLoading(true);
      const response = await schemaAPI.getSchema();
      if (response.success) {
        setSchema(response.schema);
      }
    } catch (error) {
      console.error('Failed to load schema:', error);
    } finally {
      setLoading(false);
    }
  };

  const toggleTable = (tableName) => {
    const newExpanded = new Set(expandedTables);
    if (newExpanded.has(tableName)) {
      newExpanded.delete(tableName);
    } else {
      newExpanded.add(tableName);
    }
    setExpandedTables(newExpanded);
  };

  const filteredTables = schema?.tables?.filter(table =>
    table.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    table.columns.some(col => col.name.toLowerCase().includes(searchTerm.toLowerCase()))
  ) || [];

  if (loading) {
    return (
      <div className="card">
        <div className="flex items-center justify-center py-8">
          <div className="loading-dots text-primary-600">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
          <TableCellsIcon className="w-5 h-5 text-primary-600" />
          Database Schema
        </h3>
        <span className="badge badge-primary">
          {schema?.table_count || 0} Tables
        </span>
      </div>

      {/* Search */}
      <div className="relative mb-4">
        <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
        <input
          type="text"
          placeholder="Search tables or columns..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="input-field pl-10 text-sm"
        />
      </div>

      {/* Tables List */}
      <div className="space-y-2 max-h-[600px] overflow-y-auto">
        {filteredTables.map((table) => (
          <div key={table.name} className="border border-gray-200 rounded-lg overflow-hidden">
            {/* Table Header */}
            <button
              onClick={() => toggleTable(table.name)}
              className="w-full flex items-center justify-between p-3 bg-gray-50 hover:bg-gray-100 transition-colors"
            >
              <div className="flex items-center gap-2">
                {expandedTables.has(table.name) ? (
                  <ChevronDownIcon className="w-4 h-4 text-gray-500" />
                ) : (
                  <ChevronRightIcon className="w-4 h-4 text-gray-500" />
                )}
                <TableCellsIcon className="w-4 h-4 text-primary-600" />
                <span className="font-medium text-gray-900">{table.name}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-500">
                  {table.columns?.length || 0} columns
                </span>
                {table.row_count !== null && (
                  <span className="badge badge-primary text-xs">
                    {table.row_count?.toLocaleString()} rows
                  </span>
                )}
              </div>
            </button>

            {/* Table Details */}
            {expandedTables.has(table.name) && (
              <div className="p-3 bg-white border-t border-gray-200">
                {/* Description */}
                {table.description && (
                  <p className="text-sm text-gray-600 mb-3">{table.description}</p>
                )}

                {/* Columns */}
                <div className="space-y-1">
                  {table.columns?.map((column) => (
                    <div
                      key={column.name}
                      className="flex items-center justify-between p-2 hover:bg-gray-50 rounded text-sm"
                    >
                      <div className="flex items-center gap-2 flex-1">
                        <span className="font-mono text-gray-900">{column.name}</span>
                        <span className="text-xs text-gray-500 font-mono">
                          {column.type}
                        </span>
                        {column.primary_key && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-yellow-100 text-yellow-800 rounded text-xs">
                            <KeyIcon className="w-3 h-3" />
                            PK
                          </span>
                        )}
                        {column.foreign_key && (
                          <span className="inline-flex items-center gap-1 px-2 py-0.5 bg-blue-100 text-blue-800 rounded text-xs">
                            <LinkIcon className="w-3 h-3" />
                            FK → {column.foreign_key.table}
                          </span>
                        )}
                        {!column.nullable && (
                          <span className="text-xs text-red-600">NOT NULL</span>
                        )}
                      </div>
                    </div>
                  ))}
                </div>

                {/* Foreign Keys */}
                {table.foreign_keys && table.foreign_keys.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200">
                    <p className="text-xs font-semibold text-gray-700 mb-2">
                      Relationships
                    </p>
                    <div className="space-y-1">
                      {table.foreign_keys.map((fk, idx) => (
                        <div key={idx} className="text-xs text-gray-600 flex items-center gap-1">
                          <LinkIcon className="w-3 h-3 text-primary-500" />
                          {fk.constrained_columns?.join(', ')} →{' '}
                          {fk.referred_table}.{fk.referred_columns?.join(', ')}
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="mt-3 pt-3 border-t border-gray-200 flex gap-2">
                  <button
                    onClick={() => onTableSelect && onTableSelect(table.name, 'Show all')}
                    className="text-xs btn-outline py-1 px-3"
                  >
                    View Data
                  </button>
                  <button
                    onClick={() => onTableSelect && onTableSelect(table.name, 'Count records')}
                    className="text-xs btn-outline py-1 px-3"
                  >
                    Count Rows
                  </button>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Summary */}
      {schema && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-2 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-primary-600">
                {schema.relationships?.length || 0}
              </p>
              <p className="text-xs text-gray-600">Relationships</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-green-600">
                {schema.tables?.reduce((sum, t) => sum + (t.columns?.length || 0), 0) || 0}
              </p>
              <p className="text-xs text-gray-600">Total Columns</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SchemaExplorer;
