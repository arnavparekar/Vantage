import React, { useState } from 'react';
import { RepoSelector } from './components/RepoSelector';
import { SummaryCards } from './components/SummaryCards';
import { BuildDurationChart } from './components/BuildDurationChart';
import { FailureRateChart } from './components/FailureRateChart';
import { FlakyWorkflows } from './components/FlakyWorkflows';
import { RecentRunsTable } from './components/RecentRunsTable';
import { useAnalytics } from './hooks/useAnalytics';

function App() {
  const [selectedRepo, setSelectedRepo] = useState('All Repos');
  const [days, setDays] = useState(30);

  const { 
    summary, 
    durationTrend, 
    failureRate, 
    recentRuns, 
    repos, 
    loading, 
    error 
  } = useAnalytics(selectedRepo === 'All Repos' ? null : selectedRepo, days);

  return (
    <div className="min-h-screen bg-background text-textMain p-4 sm:p-6 lg:p-8">
      <div className="max-w-7xl mx-auto space-y-6">
        
        {/* Header */}
        <header className="mb-8">
          <h1 className="text-3xl font-bold text-transparent bg-clip-text bg-gradient-to-r from-primary to-emerald-400">
            Vantage CI/CD Analytics
          </h1>
          <p className="text-textMuted mt-2">Actionable insights for your GitHub Actions workflows</p>
        </header>

        {/* Global Error Banner */}
        {error && (
          <div className="bg-danger/10 border border-danger/20 text-danger p-4 rounded-lg mb-6">
            <p className="font-semibold">Error loading data</p>
            <p className="text-sm mt-1">{error}</p>
          </div>
        )}

        {/* Filters */}
        <RepoSelector 
          repos={repos || []} 
          selectedRepo={selectedRepo} 
          onRepoChange={setSelectedRepo} 
          days={days} 
          onDaysChange={setDays} 
        />

        {/* Top Level Metrics */}
        <SummaryCards summary={summary} loading={loading} />

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
          <BuildDurationChart data={durationTrend} loading={loading} />
          <FailureRateChart data={failureRate} loading={loading} />
        </div>

        {/* Bottom Row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <RecentRunsTable runs={recentRuns} loading={loading} />
          </div>
          <div className="lg:col-span-1">
            <FlakyWorkflows repo={selectedRepo === 'All Repos' ? null : selectedRepo} days={days} />
          </div>
        </div>

      </div>
    </div>
  );
}

export default App;
