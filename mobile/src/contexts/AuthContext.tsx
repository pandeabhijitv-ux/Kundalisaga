/**
 * Auth Context Provider
 * Manages user authentication state across the app
 */

import React, {createContext, useState, useContext, useEffect} from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface User {
  id: string;
  name: string;
  email: string;
  phone?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isGuest: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  continueAsGuest: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGuest, setIsGuest] = useState(false);

  useEffect(() => {
    loadUser();
  }, []);

  const loadUser = async () => {
    try {
      const userData = await AsyncStorage.getItem('user');
      const guestMode = await AsyncStorage.getItem('guestMode');
      
      if (userData) {
        setUser(JSON.parse(userData));
      }
      
      if (guestMode === 'true') {
        setIsGuest(true);
      }
    } catch (error) {
      console.error('Error loading user:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const login = async (email: string, password: string) => {
    try {
      // TODO: Implement actual authentication with your Python backend
      // For now, mock implementation
      const mockUser = {
        id: '1',
        name: 'User',
        email: email,
      };
      
      await AsyncStorage.setItem('user', JSON.stringify(mockUser));
      await AsyncStorage.removeItem('guestMode');
      setUser(mockUser);
      setIsGuest(false);
    } catch (error) {
      throw new Error('Login failed');
    }
  };

  const register = async (name: string, email: string, password: string) => {
    try {
      // TODO: Implement actual registration
      const mockUser = {
        id: '1',
        name: name,
        email: email,
      };
      
      await AsyncStorage.setItem('user', JSON.stringify(mockUser));
      await AsyncStorage.removeItem('guestMode');
      setUser(mockUser);
      setIsGuest(false);
    } catch (error) {
      throw new Error('Registration failed');
    }
  };

  const logout = async () => {
    try {
      await AsyncStorage.removeItem('user');
      await AsyncStorage.removeItem('guestMode');
      setUser(null);
      setIsGuest(false);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  const continueAsGuest = () => {
    AsyncStorage.setItem('guestMode', 'true');
    setIsGuest(true);
  };

  return (
    <AuthContext.Provider
      value={{user, isLoading, isGuest, login, register, logout, continueAsGuest}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
