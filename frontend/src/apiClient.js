const API_BASE_URL = '/api';

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!response.ok) {
    throw new Error(`Request failed with ${response.status}`);
  }
  return response.json();
}

export const api = {
  listSessions: () => request('/sessions'),
  createSession: (data) =>
    request('/sessions', { method: 'POST', body: JSON.stringify(data) }),
  listWorldEnvironments: () => request('/world-environments'),
  createWorldEnvironment: (data) =>
    request('/world-environments', {
      method: 'POST',
      body: JSON.stringify(data),
    }),
  listArchetypes: () => request('/archetypes'),
  createArchetype: (data) =>
    request('/archetypes', { method: 'POST', body: JSON.stringify(data) }),
  listSkills: () => request('/skills'),
  createSkill: (data) =>
    request('/skills', { method: 'POST', body: JSON.stringify(data) }),
};

export default api;
