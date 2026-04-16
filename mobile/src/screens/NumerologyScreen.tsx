/**
 * Numerology Screen
 */

import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import {THEME} from '../constants/theme';
import {calculateNumerology} from '../services/PythonBridge';

const NumerologyScreen = () => {
  const [name, setName] = useState('User');
  const [dateOfBirth, setDateOfBirth] = useState('1990-01-01');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const response: any = await calculateNumerology(name, dateOfBirth);
      if (response?.error) {
        Alert.alert('Numerology Error', response.error);
      }
      setData(response);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Failed to calculate numerology');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Numerology</Text>

      <View style={styles.card}>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="Full name" />
        <TextInput
          style={styles.input}
          value={dateOfBirth}
          onChangeText={setDateOfBirth}
          placeholder="Date of birth (YYYY-MM-DD)"
        />
        <TouchableOpacity style={styles.button} onPress={handleCalculate} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? 'Calculating...' : 'Calculate Numerology'}</Text>
        </TouchableOpacity>
      </View>

      {data ? (
        <View style={styles.card}>
          <Text style={styles.result}>Life Path: {data.life_path_number || data.lifePathNumber || '-'}</Text>
          <Text style={styles.result}>Destiny: {data.destiny_number || data.destinyNumber || '-'}</Text>
          <Text style={styles.result}>Soul: {data.soul_number || data.soulNumber || '-'}</Text>
          <Text style={styles.result}>Personality: {data.personality_number || data.personalityNumber || '-'}</Text>
          {data.interpretation ? (
            <Text style={styles.interpretation}>{typeof data.interpretation === 'string' ? data.interpretation : JSON.stringify(data.interpretation)}</Text>
          ) : null}
        </View>
      ) : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.background,
  },
  content: {
    padding: 16,
    paddingBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 12,
  },
  card: {
    backgroundColor: THEME.card,
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  input: {
    backgroundColor: '#fff',
    borderColor: '#E0E0E0',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginBottom: 8,
    color: THEME.text,
  },
  button: {
    backgroundColor: THEME.primary,
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  result: {
    color: THEME.text,
    marginBottom: 6,
    fontSize: 16,
    fontWeight: '600',
  },
  interpretation: {
    marginTop: 8,
    color: THEME.textLight,
    lineHeight: 20,
  },
});

export default NumerologyScreen;
