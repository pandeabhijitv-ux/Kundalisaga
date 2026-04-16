/**
 * Splash Screen
 * Displayed while app is initializing
 */

import React from 'react';
import {View, Text, ActivityIndicator, StyleSheet, Image} from 'react-native';
import {THEME} from '../constants/theme';

const SplashScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.mantra}>🕉️ ॐ गं गणपतये नमः 🕉️</Text>
      <Text style={styles.title}>KundaliSaga</Text>
      <Text style={styles.subtitle}>Vedic Astrology AI</Text>
      <ActivityIndicator
        size="large"
        color={THEME.primary}
        style={styles.loader}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: THEME.background,
  },
  mantra: {
    fontSize: 24,
    color: THEME.primary,
    marginBottom: 20,
  },
  title: {
    fontSize: 36,
    fontWeight: 'bold',
    color: THEME.primary,
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 18,
    color: THEME.textLight,
    marginBottom: 40,
  },
  loader: {
    marginTop: 20,
  },
});

export default SplashScreen;
