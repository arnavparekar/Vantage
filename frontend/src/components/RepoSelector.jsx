import React from 'react';

export function RepoSelector({ repos, selectedRepo, onRepoChange, days, onDaysChange }) {
  return (
    <div className="flex flex-col sm:flex-row justify-between items-center bg-surface border border-border rounded-xl p-4 mb-6 shadow-sm">
      <div className="flex items-center space-x-3 w-full sm:w-auto mb-4 sm:mb-0">
        <label htmlFor="repo-select" className="text-textMuted font-medium text-sm whitespace-nowrap">
          Repository:
        </label>
        <select
          id="repo-select"
          className="bg-background border border-border text-textMain text-sm rounded-lg focus:ring-primary focus:border-primary block w-full sm:w-64 p-2.5 transition-colors outline-none"
          value={selectedRepo || 'All Repos'}
          onChange={(e) => onRepoChange(e.target.value)}
        >
          <option value="All Repos">All Repositories</option>
          {repos.map((repo, i) => (
            <option key={i} value={repo}>{repo}</option>
          ))}
        </select>
      </div>

      <div className="flex items-center space-x-3 w-full sm:w-auto">
        <label htmlFor="days-select" className="text-textMuted font-medium text-sm whitespace-nowrap">
          Time Range:
        </label>
        <select
          id="days-select"
          className="bg-background border border-border text-textMain text-sm rounded-lg focus:ring-primary focus:border-primary block w-full sm:w-40 p-2.5 transition-colors outline-none"
          value={days}
          onChange={(e) => onDaysChange(Number(e.target.value))}
        >
          <option value={7}>Last 7 Days</option>
          <option value={14}>Last 14 Days</option>
          <option value={30}>Last 30 Days</option>
          <option value={90}>Last 90 Days</option>
        </select>
      </div>
    </div>
  );
}
