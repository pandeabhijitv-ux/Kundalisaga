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

interface RegisteredUser extends User {
  password: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isGuest: boolean;
  login: (email: string, password: string) => Promise<void>;
  loginWithOtp: (email: string) => Promise<void>;
  register: (name: string, email: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  continueAsGuest: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);
const STORAGE_KEY_USER = 'user';
const STORAGE_KEY_GUEST = 'guestMode';
const STORAGE_KEY_REGISTERED_USERS = 'registeredUsers';

export const AuthProvider: React.FC<{children: React.ReactNode}> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isGuest, setIsGuest] = useState(false);

  useEffect(() => {
    loadUser();
  }, []);

  const loadRegisteredUsers = async (): Promise<RegisteredUser[]> => {
    const raw = await AsyncStorage.getItem(STORAGE_KEY_REGISTERED_USERS);
    if (!raw) return [];
    try {
      const parsed = JSON.parse(raw);
      if (!Array.isArray(parsed)) return [];
      return parsed;
    } catch {
      return [];
    }
  };

  const saveRegisteredUsers = async (users: RegisteredUser[]) => {
    await AsyncStorage.setItem(STORAGE_KEY_REGISTERED_USERS, JSON.stringify(users));
  };

  const persistLoggedInUser = async (nextUser: User) => {
    await AsyncStorage.setItem(STORAGE_KEY_USER, JSON.stringify(nextUser));
    await AsyncStorage.removeItem(STORAGE_KEY_GUEST);
    setUser(nextUser);
    setIsGuest(false);
  };

  const loadUser = async () => {
    try {
      const userData = await AsyncStorage.getItem(STORAGE_KEY_USER);
      const guestMode = await AsyncStorage.getItem(STORAGE_KEY_GUEST);
      
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
    const normalizedEmail = email.trim().toLowerCase();
    const normalizedPassword = password.trim();
    if (!normalizedEmail || !normalizedPassword) {
      throw new Error('Please enter email and password');
    }

    const users = await loadRegisteredUsers();
    const found = users.find(u => u.email.toLowerCase() === normalizedEmail);
    if (!found) {
      throw new Error('No registered user found for this email. Please register first.');
    }
    if (found.password !== normalizedPassword) {
      throw new Error('Invalid email or password');
    }

    await persistLoggedInUser({id: found.id, name: found.name, email: found.email, phone: found.phone});
  };

  const loginWithOtp = async (email: string) => {
    const normalizedEmail = email.trim().toLowerCase();
    if (!normalizedEmail) {
      throw new Error('Please enter email');
    }

    const users = await loadRegisteredUsers();
    const found = users.find(u => u.email.toLowerCase() === normalizedEmail);
    if (!found) {
      throw new Error('No registered user found for this email. Please register first.');
    }

    await persistLoggedInUser({id: found.id, name: found.name, email: found.email, phone: found.phone});
  };

  const register = async (name: string, email: string, password: string) => {
    const trimmedName = name.trim();
    const normalizedEmail = email.trim().toLowerCase();
    const normalizedPassword = password.trim();

    if (!trimmedName || !normalizedEmail || !normalizedPassword) {
      throw new Error('Name, email and password are required');
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(normalizedEmail)) {
      throw new Error('Please enter a valid email address');
    }
    if (normalizedPassword.length < 6) {
      throw new Error('Password must be at least 6 characters');
    }

    const users = await loadRegisteredUsers();
    if (users.some(u => u.email.toLowerCase() === normalizedEmail)) {
      throw new Error('Email is already registered. Please login instead.');
    }

    const newUser: RegisteredUser = {
      id: `${Date.now()}`,
      name: trimmedName,
      email: normalizedEmail,
      password: normalizedPassword,
    };

    await saveRegisteredUsers([newUser, ...users]);
    await persistLoggedInUser({id: newUser.id, name: newUser.name, email: newUser.email});
  };

  const logout = async () => {
    try {
      await AsyncStorage.removeItem(STORAGE_KEY_USER);
      await AsyncStorage.removeItem(STORAGE_KEY_GUEST);
      setUser(null);
      setIsGuest(false);
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  const continueAsGuest = () => {
    AsyncStorage.setItem(STORAGE_KEY_GUEST, 'true');
    setIsGuest(true);
  };

  return (
    <AuthContext.Provider
      value={{user, isLoading, isGuest, login, loginWithOtp, register, logout, continueAsGuest}}>
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
