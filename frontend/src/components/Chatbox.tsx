import React, { useState, useEffect, useCallback } from 'react';
import { Box, TextField, IconButton, Typography, Paper, List, ListItem, ListItemText } from '@mui/material';
import SendIcon from '@mui/icons-material/Send';
import { useLocation, useNavigate } from 'react-router-dom';
import { client } from '../services/apiService';
import type { components } from '../services/api';
import { useNavigationContext } from '../navigation';

type Message = components['schemas']['ChatMessage'];

const Chatbox: React.FC = () => {
  const [loadingSession, setLoadingSession] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const {pathname} = useLocation();
  const navigate = useNavigate();
  const { addItem } = useNavigationContext();
  
  const sessionId = pathname === '/' ? '/' : pathname.split('/')[2] ?? '/';

  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);

  // Helper to update messages list
  const addMessage = useCallback((message: Message) => {
    setMessages((prev) => [...prev, message]);
  }, []);

  useEffect(() => {
    const initializeSession = async () => {
      if (sessionId === '/') {
        setMessages([]);
        setLoadingSession(false);
        return;
      }
      const response = await client.GET('/get-chat/', { params: { query: { session_id: sessionId }}});
      if (response.error) {
        setError('something went wrong');
      }
      const { data } = response;
      if (data) {
        setMessages(data.messages);
      } else {
        setError('the chat doesn\'t exist');
      }
      setLoadingSession(false);
    };

    initializeSession();
  }, [sessionId]);

  const sendMessage = async () => {
    if (!input.trim()) {return;}

    const userMessage: Message = { user_or_chatbot: 'user', message: input };
    addMessage(userMessage);
    setInput('');

    const response = await client.POST('/query/', { body: { user_input: input, session_id: sessionId }});
    if (response.error) {
      const errorMessage: Message = { user_or_chatbot: 'chatbot', message: 'Error: Unable to send message' };
      addMessage(errorMessage);
    }
    const { data } = response;
    if (data) {
      const botResponse: Message = { user_or_chatbot: 'chatbot', message: data.message };
      addMessage(botResponse);
      addItem({
        segment: `/chat/${data.id}`,
        title: data.id,
      }, 4);
      navigate(`/chat/${data.id}`, { replace: true });
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => { setInput(e.target.value); };
  const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {sendMessage();}
  };

  if (loadingSession) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Typography variant="h6">Loading session...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <Typography variant="h6" color="error">
          {error}
        </Typography>
      </Box>
    );
  }

  return (
    <Box
      height="100%"
      width="100%"
      p={3}
      display="flex"
      flexDirection="column"
      justifyContent="space-between"
      alignItems="center"
      bgcolor="#333"
    >
      <Paper
        style={{
          height: '100%',
          overflow: 'auto',
          width: '80%',
          padding: '10px',
          boxSizing: 'border-box',
        }}
        elevation={3}
      >
        <List>
          {messages.map((msg, index) => (
            <ListItem key={index} alignItems="flex-start">
              <ListItemText
                primary={
                  <Typography variant="body1" color={msg.user_or_chatbot === 'user' ? 'primary' : 'secondary'}>
                    {msg.user_or_chatbot}
                  </Typography>
                }
                secondary={<Typography variant="body2">{msg.message}</Typography>}
              />
            </ListItem>
          ))}
        </List>
      </Paper>
      <Box display="flex" width="80%" mt={2} alignItems="center">
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type a message"
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyPress}
        />
        <IconButton color="primary" onClick={sendMessage}>
          <SendIcon />
        </IconButton>
      </Box>
    </Box>
  );
};

export default Chatbox;
