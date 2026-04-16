/**
 * Dasha Screen
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
import {getCurrentDasha} from '../services/PythonBridge';

const DashaScreen = () => {
  const [dateOfBirth, setDateOfBirth] = useState('1990-01-01');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const handleFetchDasha = async () => {
    setLoading(true);
    try {
      const response = await getCurrentDasha(dateOfBirth);
      if (response?.error) {
        Alert.alert('Dasha Error', response.error);
      }
      setData(response);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Failed to fetch dasha');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Current Dasha</Text>

      <View style={styles.card}>
        <TextInput
          style={styles.input}
          value={dateOfBirth}
          onChangeText={setDateOfBirth}
          placeholder="Date of birth (YYYY-MM-DD)"
        />
        <TouchableOpacity style={styles.button} onPress={handleFetchDasha} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? 'Loading...' : 'Get Current Dasha'}</Text>
        </TouchableOpacity>
      </View>

      {data ? (
        <View style={styles.card}>
          <Text style={styles.sectionTitle}>Mahadasha</Text>
          <Text style={styles.row}>Planet: {data?.mahadasha?.planet || '-'}</Text>
          <Text style={styles.row}>Start: {data?.mahadasha?.start_date || '-'}</Text>
          <Text style={styles.row}>End: {data?.mahadasha?.end_date || '-'}</Text>

          <Text style={styles.sectionTitle}>Antardasha</Text>
          <Text style={styles.row}>Planet: {data?.antardasha?.planet || '-'}</Text>
          <Text style={styles.row}>Start: {data?.antardasha?.start_date || '-'}</Text>
          <Text style={styles.row}>End: {data?.antardasha?.end_date || '-'}</Text>

          <Text style={styles.sectionTitle}>Interpretation</Text>
          <Text style={styles.interpretation}>{data?.interpretation || 'No interpretation available.'}</Text>
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
  sectionTitle: {
    marginTop: 8,
    marginBottom: 4,
    fontSize: 17,
    fontWeight: '700',
    color: THEME.text,
  },
  row: {
    color: THEME.textLight,
    marginBottom: 4,
  },
  interpretation: {
    color: THEME.textLight,
    lineHeight: 20,
  },
});

export default DashaScreen;
