/**
 * Header Component
 *
 * Main header component for the Natural Language to SQL dashboard.
 */

import React from 'react';
import { DatabaseIcon, SparklesIcon } from '@heroicons/react/24/outline';

const Header = () => {
  return (
    <header className="bg-white border-b border-gray-200 sticky top-0 z-50 shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Title */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center justify-center w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg shadow-md">
              <DatabaseIcon className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                Natural Language to SQL
                <SparklesIcon className="w-5 h-5 text-primary-500" />
              </h1>
              <p className="text-xs text-gray-500">Query your database in plain English</p>
            </div>
          </div>

          {/* Status Indicator */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-sm text-gray-600">Connected</span>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
