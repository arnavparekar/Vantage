import React from 'react';

export function RecentRunsTable({ runs, loading }) {
  if (loading) {
    return (
      <div className="card mt-6 min-h-[300px] flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
      </div>
    );
  }

  if (!runs || runs.length === 0) {
    return (
      <div className="card mt-6">
        <h2 className="text-lg font-semibold mb-4 text-textMain">Recent Workflow Runs</h2>
        <p className="text-textMuted text-sm">No recent runs found for the selected criteria.</p>
      </div>
    );
  }

  return (
    <div className="card mt-6 overflow-hidden">
      <h2 className="text-lg font-semibold mb-4 text-textMain">Recent Workflow Runs</h2>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-sm text-textMuted">
          <thead className="text-xs uppercase bg-background text-textMain">
            <tr>
              <th scope="col" className="px-4 py-3 rounded-tl-lg">Workflow</th>
              <th scope="col" className="px-4 py-3">Repository</th>
              <th scope="col" className="px-4 py-3">Branch</th>
              <th scope="col" className="px-4 py-3">Status</th>
              <th scope="col" className="px-4 py-3">Duration</th>
              <th scope="col" className="px-4 py-3 rounded-tr-lg">Date</th>
            </tr>
          </thead>
          <tbody>
            {runs.map((run) => (
              <tr key={run.id} className="border-b border-border hover:bg-background/50 transition-colors">
                <td className="px-4 py-4 font-medium text-textMain">{run.name}</td>
                <td className="px-4 py-4">{run.repo}</td>
                <td className="px-4 py-4">
                  <span className="bg-surface border border-border px-2 py-1 rounded text-xs font-mono">{run.head_branch}</span>
                </td>
                <td className="px-4 py-4">
                  <span className={`badge ${
                    run.conclusion === 'success' ? 'badge-success' :
                    run.conclusion === 'failure' ? 'badge-danger' :
                    run.conclusion === 'cancelled' ? 'badge-warning' : 'badge-neutral'
                  }`}>
                    {run.conclusion || run.status}
                  </span>
                </td>
                <td className="px-4 py-4">
                  {run.duration_seconds ? `${Math.floor(run.duration_seconds / 60)}m ${run.duration_seconds % 60}s` : '-'}
                </td>
                <td className="px-4 py-4">
                  {new Date(run.started_at).toLocaleString(undefined, {
                    month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                  })}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
