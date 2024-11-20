import React, { createContext, useContext, useEffect, useState } from 'react';
import type { Navigation, NavigationItem } from '@toolpad/core/AppProvider';
import { client } from './services/apiService';

// Define types for Navigation and its elements


// Initial Navigation constant
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
];

// Create the context
const NavigationContext = createContext<{
  navigation: Navigation;
  addItem: (item: NavigationItem, index: number) => void;
    }>({
      navigation: NAVIGATION,
      // eslint-disable-next-line @typescript-eslint/no-empty-function
      addItem: () => {},
    });

// NavigationProvider component
export const NavigationProvider: React.FC<{ children: React.ReactNode }> = ({ children }: { children: React.ReactNode }) => {
  const [navigation, setNavigation] = useState<Navigation>([]);

  const loadChats = async () => {
    try {
      const { data } = await client.GET('/get-chats/');
      if (data) {
        const loadedItems = data.map((s: string) => ({
          segment: `chat/${s}`,
          title: s,
        }));

        setNavigation([...NAVIGATION, ...loadedItems]);
      }
    } catch (error) {
      // eslint-disable-next-line no-console
      console.error('Error loading chats:', error);
    }
  };

  // Load additional navigation items on the first render
  useEffect(() => {
    loadChats();
  }, []);

  // Function to add new items to the navigation
  const addItem = (item: NavigationItem, index: number) => {
    setNavigation((prev) => {
      const newNav = [...prev];
      newNav.splice(index, 0, item); // Insert the new item at the specified index
      return newNav;
    });
  };

  return (
    <NavigationContext.Provider value={{ navigation, addItem }}>
      {children}
    </NavigationContext.Provider>
  );
};

// Hook to use the NavigationContext
export const useNavigationContext = () => useContext(NavigationContext);
