/* Interactions with the FastAPI backend */
import axios from 'axios';

const apiService = {
  sendQuery: async (query: string, sessionId: string) => axios.post('http://localhost:8000/query/', { user_input: query, session_id: sessionId }),
  checkSessionId: async (sessionId: string) => axios.get('http://localhost:8000/check-session-id/', { params: { session_id: sessionId } }),
  freshSessionId: async () => axios.post('http://localhost:8000/fresh-session-id/')
};

export default apiService;
