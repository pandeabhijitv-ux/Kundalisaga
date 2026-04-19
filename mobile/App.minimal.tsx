/**
 * MINIMAL TEST APP - To identify crash cause
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
} from 'react-native';

const MinimalApp = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>🕉️ KundaliSaga Test</Text>
      <Text style={styles.subtitle}>If you see this, app loaded successfully!</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#FFF5E6',
  },
  text: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FF6B35',
    marginBottom: 20,
  },
  subtitle: {
    fontSize: 16,
    color: '#666666',
  },
});

export default MinimalApp;
