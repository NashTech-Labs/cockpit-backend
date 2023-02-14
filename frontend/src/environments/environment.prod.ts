export const environment = {
  production: true,
  api: {
    baseUrl: 'http://localhost:8000/',
    routes: {
      adminFetch: { endpoint: 'import-cluster', method: 'POST' },
    },
  },
};
