import React from 'react';

export function SummaryCards({ summary, loading }) {
  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="card animate-pulse h-28 bg-surface border-border"></div>
        ))}
      </div>
    );
  }

  if (!summary) return null;

  const cards = [
    { label: 'Total Runs', value: summary.total_runs, color: 'text-primary' },
    { label: 'Success Rate', value: `${summary.success_rate.toFixed(1)}%`, color: summary.success_rate > 90 ? 'text-success' : 'text-warning' },
    { label: 'Avg Duration', value: `${Math.round(summary.avg_duration_seconds / 60)}m ${Math.round(summary.avg_duration_seconds % 60)}s`, color: 'text-textMain' },
    { label: 'MTTR', value: summary.mttr_seconds ? `${Math.round(summary.mttr_seconds / 60)}m` : 'N/A', color: 'text-textMuted' }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      {cards.map((card, i) => (
        <div key={i} className="card flex flex-col justify-center">
          <h3 className="text-sm font-semibold text-textMuted uppercase tracking-wider mb-1">{card.label}</h3>
          <p className={`text-3xl font-bold ${card.color}`}>{card.value}</p>
        </div>
      ))}
    </div>
  );
}
