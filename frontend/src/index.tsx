import React from 'react';
import { createRoot } from 'react-dom/client';
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import App from './App';
import Chatbox from './components/Chatbox';
import { AdminPage } from './pages/AdminPage';

const domNode = document.getElementById('root')!;
const root = createRoot(domNode);

const router = createBrowserRouter([
  {
    Component: App,
    children: [
      {
        path: '/',
        Component: Chatbox,
      },
      {
        path: 'chat/:id',
        Component: Chatbox,
      },
      {
        path: 'admin',
        Component: AdminPage
      }
    ]
  }
]);

root.render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>
);
