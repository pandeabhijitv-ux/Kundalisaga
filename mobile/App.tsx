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
import {AppSettingsProvider} from './src/contexts/AppSettingsContext';
import SplashScreen from './src/screens/SplashScreen';
import {THEME} from './src/constants/theme';

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
      <AppSettingsProvider>
        <AuthProvider>
          <StatusBar
            barStyle="dark-content"
            backgroundColor={THEME.background}
          />
          <AppContent />
        </AuthProvider>
      </AppSettingsProvider>
    </SafeAreaProvider>
  );
};

export default App;
