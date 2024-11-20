// Frontend/src/App.js
import React from 'react';
import { createTheme } from '@mui/material/styles';
import { AppProvider } from '@toolpad/core/react-router-dom';
import type { Navigation } from '@toolpad/core/AppProvider';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import { Outlet } from 'react-router-dom';
import logo from './travelassistant.png';

const NAVIGATION: Navigation = [
  {
    kind: 'header',
    title: 'Admin',
  },
  {
    segment: 'admin',
    title: 'Admin',
  },
  {
    kind: 'header',
    title: 'Main items',
  },
  {
    segment: '',
    title: 'New',
  },
  {
    segment: 'chat/123124',
    title: 'test',
  },
  {
    segment: 'chat/12315324',
    title: 'test 2 ',
  },
  {
    segment: 'chat/12323124',
    title: 'test 3',
  },
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
  <AppProvider
    branding={{
      logo: <img src={logo} />,
      title: 'Travel Assistant',
    }}
    theme={darkTheme}
    navigation={NAVIGATION}>
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  </AppProvider>
);

export default App;
