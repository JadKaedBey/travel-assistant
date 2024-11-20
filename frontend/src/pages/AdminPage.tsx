// Src/pages/AdminPage.js

import React from 'react';
import PinForm from '../components/PinForm';
import PinnedItems from '../components/PinnedItems';

export const AdminPage = () => (
  <div className="container mx-auto p-4">
    <h1 className="text-2xl font-bold mb-4">Admin Console</h1>
    <PinForm onRefresh={() => { window.location.reload(); }} />
    <PinnedItems isAdmin={true} />
  </div>
);
