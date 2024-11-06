/* Interactions with the FastAPI backend */
import axios from 'axios';

interface CheckSessionIdResponse {
  found: boolean;
}

interface FreshSessionIdResponse {
  session_id: string;
}

const apiService = {
  sendQuery: async (query: string, sessionId: string) => axios.post('http://localhost:8000/query/', { user_input: query, session_id: sessionId }),
  checkSessionId: async (sessionId: string) => axios.get<CheckSessionIdResponse>('http://localhost:8000/check-session-id/', { params: { session_id: sessionId } }),
  freshSessionId:  async () => axios.post<FreshSessionIdResponse>('http://localhost:8000/fresh-session-id/')
};

export default apiService;
