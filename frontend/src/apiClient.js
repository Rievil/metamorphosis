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
  getSessions: () => request('/sessions'),
  getWorld: () => request('/world'),
  getPlayers: () => request('/players'),
  getArchetypes: () => request('/archetypes'),
};

export default api;
