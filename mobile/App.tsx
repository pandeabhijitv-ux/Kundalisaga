/**
 * KundaliSaga Mobile App
 * Main Application Entry Point
 */

import React, {useEffect, useState} from 'react';
import {
  StatusBar,
  StyleSheet,
  ActivityIndicator,
  View,
  Text,
} from 'react-native';
import {NavigationContainer} from '@react-navigation/native';
import {SafeAreaProvider} from 'react-native-safe-area-context';
import AppNavigator from './src/navigation/AppNavigator';
import {AuthProvider, useAuth} from './src/contexts/AuthContext';
import SplashScreen from './src/screens/SplashScreen';

// Theme colors matching your Streamlit app
export const THEME = {
  background: '#FFF5E6',
  primary: '#FF6B35',
  secondary: '#F9C74F',
  text: '#333333',
  textLight: '#666666',
  card: '#FFFFF0',
  success: '#4CAF50',
  warning: '#FF9800',
  error: '#F44336',
};

const AppContent = () => {
  const {isLoading} = useAuth();

  if (isLoading) {
    return <SplashScreen />;
  }

  return (
    <NavigationContainer>
      <AppNavigator />
    </NavigationContainer>
  );
};

const App = () => {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <StatusBar
          barStyle="dark-content"
          backgroundColor={THEME.background}
        />
        <AppContent />
      </AuthProvider>
    </SafeAreaProvider>
  );
};

export default App;
