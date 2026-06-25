import React, { useState, useEffect } from 'react';
import { api } from '../api/client';

export function FlakyWorkflows({ repo, days }) {
  const [flakyData, setFlakyData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;
    
    async function loadFlaky() {
      setLoading(true);
      try {
        const data = await api.getFlakyWorkflows(repo, days);
        if (isMounted) setFlakyData(data);
      } catch (err) {
        if (isMounted) setError(err.message);
      } finally {
        if (isMounted) setLoading(false);
      }
    }
    
    loadFlaky();
    return () => { isMounted = false; };
  }, [repo, days]);

  if (loading) {
    return (
      <div className="card h-full flex items-center justify-center min-h-[300px]">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="card h-full flex items-center justify-center min-h-[300px]">
        <p className="text-danger text-sm">Error loading flaky workflows: {error}</p>
      </div>
    );
  }

  if (!flakyData || flakyData.length === 0) {
    return (
      <div className="card h-full flex items-center justify-center min-h-[300px]">
        <p className="text-textMuted text-sm">No flaky workflows detected.</p>
      </div>
    );
  }

  return (
    <div className="card h-full flex flex-col">
      <h2 className="text-lg font-semibold mb-4 text-textMain">Top Flaky Workflows</h2>
      <p className="text-xs text-textMuted mb-4">Workflows that flip between success and failure frequently.</p>
      
      <div className="flex-1 overflow-y-auto">
        <ul className="space-y-4">
          {flakyData.map((item, index) => (
            <li key={index} className="flex justify-between items-center p-3 bg-background rounded-lg border border-border">
              <div className="flex flex-col">
                <span className="font-medium text-textMain">{item.workflow_name}</span>
                <span className="text-xs text-textMuted mt-1">{item.total_runs} total runs</span>
              </div>
              <div className="flex flex-col items-end">
                <span className="text-lg font-bold text-warning">{item.flakiness_score.toFixed(1)}</span>
                <span className="text-xs text-textMuted">flakiness score</span>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
