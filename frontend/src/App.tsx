// Frontend/src/App.js
import React from 'react';
import { createTheme } from '@mui/material/styles';
import { AppProvider } from '@toolpad/core/react-router-dom';
import type { Navigation } from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import Chatbox from './components/Chatbox';

const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Main items',
  },
  {
    segment: '',
    title: 'New',
  },
  {
    segment: 'test',
    title: 'test',
  },
  {
    segment: 'test2',
    title: 'test 2 ',
  },
  {
    segment: 'test3',
    title: 'test 3',
  }
];

const darkTheme = createTheme({
  cssVariables: {
    colorSchemeSelector: 'data-toolpad-color-scheme',
  },
  palette: {
    mode: 'dark',
  },
});

const App = () => (
  <AppProvider theme={darkTheme} navigation={NAVIGATION}>
    <DashboardLayout>
      <Chatbox />
    </DashboardLayout>
  </AppProvider>
);

export default App;
