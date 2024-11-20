// Frontend/src/App.js
import React from 'react';
import { createTheme } from '@mui/material/styles';
import { AppProvider } from '@toolpad/core/react-router-dom';
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import { Outlet } from 'react-router-dom';
import logo from './travelassistant.png';
import { useNavigationContext } from './navigation';

const darkTheme = createTheme({
  cssVariables: {
    colorSchemeSelector: 'data-toolpad-color-scheme',
  },
  palette: {
    mode: 'dark',
  },
});

const App = () => {
  const {navigation} = useNavigationContext();

  return <AppProvider
    branding={{
      logo: <img src={logo} />,
      title: 'Travel Assistant',
    }}
    theme={darkTheme}
    navigation={navigation}>
    <DashboardLayout>
      <Outlet />
    </DashboardLayout>
  </AppProvider>;
};

export default App;
