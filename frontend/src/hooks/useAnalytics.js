import { useState, useEffect } from 'react';
import { api } from '../api/client';

export function useAnalytics(repo, days = 30) {
  const [data, setData] = useState({
    summary: null,
    durationTrend: [],
    failureRate: [],
    recentRuns: [],
    repos: []
  });
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let isMounted = true;

    async function fetchData() {
      setLoading(true);
      setError(null);
      
      try {
        const [
          summary,
          durationTrend,
          failureRate,
          recentRuns,
          repos
        ] = await Promise.all([
          api.getSummary(repo, days),
          api.getDurationTrend(repo, null, days),
          api.getFailureRate(repo, days),
          api.getRuns(repo, null, 50, 0),
          api.getRepos()
        ]);

        if (isMounted) {
          setData({
            summary,
            durationTrend,
            failureRate,
            recentRuns,
            repos
          });
        }
      } catch (err) {
        if (isMounted) {
          setError(err.message);
        }
      } finally {
        if (isMounted) {
          setLoading(false);
        }
      }
    }

    fetchData();

    return () => {
      isMounted = false;
    };
  }, [repo, days]);

  return { ...data, loading, error };
}
