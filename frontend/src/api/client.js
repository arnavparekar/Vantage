const API_BASE_URL = '/api';

async function fetchJson(endpoint) {
  const response = await fetch(`${API_BASE_URL}${endpoint}`);
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(`API error: ${response.status} ${errorBody}`);
  }
  return response.json();
}

export const api = {
  getRepos: () => fetchJson('/repos'),
  
  getSummary: (repo, days = 30) => {
    const params = new URLSearchParams({ days });
    if (repo && repo !== 'All Repos') params.append('repo', repo);
    return fetchJson(`/summary?${params.toString()}`);
  },
  
  getRuns: (repo, branch, limit = 50, offset = 0) => {
    const params = new URLSearchParams({ limit, offset });
    if (repo && repo !== 'All Repos') params.append('repo', repo);
    if (branch) params.append('branch', branch);
    return fetchJson(`/runs?${params.toString()}`);
  },
  
  getDurationTrend: (repo, branch, days = 30) => {
    const params = new URLSearchParams({ days });
    if (repo && repo !== 'All Repos') params.append('repo', repo);
    if (branch) params.append('branch', branch);
    return fetchJson(`/duration-trend?${params.toString()}`);
  },
  
  getFailureRate: (repo, days = 30) => {
    const params = new URLSearchParams({ days });
    if (repo && repo !== 'All Repos') params.append('repo', repo);
    return fetchJson(`/failure-rate?${params.toString()}`);
  },
  
  getFlakyWorkflows: (repo, days = 30) => {
    const params = new URLSearchParams({ days });
    if (repo && repo !== 'All Repos') params.append('repo', repo);
    return fetchJson(`/flaky-workflows?${params.toString()}`);
  }
};
