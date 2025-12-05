import axios from 'axios';
const API_BASE = process.env.REACT_APP_API_BASE || 'http://127.0.0.1:8000/api';
export function analyze(query){ return axios.post(`${API_BASE}/analyze/`, {query}).then(r=>r.data); }
export function compare(query){ return axios.post(`${API_BASE}/compare/`, {query}).then(r=>r.data); }
export function upload(file){ const fd=new FormData(); fd.append('file',file); return axios.post(`${API_BASE}/upload/`, fd, {headers:{'Content-Type':'multipart/form-data'}}).then(r=>r.data); }
export function download(area){ return axios.post(`${API_BASE}/download/`, {area}, {responseType:'blob'}).then(r=>r.data); }
