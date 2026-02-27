import axios from "axios";

const api = axios.create({
  // backend runs on port 8000; frontend on 3000
  baseURL: "http://localhost:8000",
  timeout: 5000,
});

export const getConnections = () => api.get("/connections").then((r) => r.data);
export const getAlerts = () => api.get("/alerts").then((r) => r.data);
// The backend stores bandwidth summary under /bandwidth_summary
export const getBandwidth = () => api.get("/bandwidth_summary").then((r) => r.data);

export default api;
