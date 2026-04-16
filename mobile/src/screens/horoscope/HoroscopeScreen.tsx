/**
 * Horoscope Screen
 * Birth chart calculation using Python bridge.
 */
import React, {useEffect, useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import {THEME} from '../../constants/theme';
import {calculateChart} from '../../services/PythonBridge';

const HoroscopeScreen = ({route}: any) => {
  const preset = route?.params?.preset;
  const [loading, setLoading] = useState(false);
  const [name, setName] = useState('User');
  const [date, setDate] = useState('1990-01-01');
  const [time, setTime] = useState('12:00');
  const [location, setLocation] = useState('Mumbai');
  const [latitude, setLatitude] = useState('19.0760');
  const [longitude, setLongitude] = useState('72.8777');
  const [timezone, setTimezone] = useState('Asia/Kolkata');
  const [chart, setChart] = useState<any>(null);

  useEffect(() => {
    if (preset === 'compatibility') {
      Alert.alert(
        'Compatibility Mode',
        'Start by calculating the first person chart. You can then compare with another profile from Profiles.'
      );
    }
  }, [preset]);

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const result = await calculateChart({
        name,
        date,
        time,
        location,
        latitude: Number(latitude),
        longitude: Number(longitude),
        timezone,
      });
      if (result?.error) {
        Alert.alert('Calculation Error', result.error);
      }
      setChart(result);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Failed to calculate chart');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Birth Chart Calculator</Text>

      <View style={styles.card}>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="Name" />
        <TextInput style={styles.input} value={date} onChangeText={setDate} placeholder="YYYY-MM-DD" />
        <TextInput style={styles.input} value={time} onChangeText={setTime} placeholder="HH:MM" />
        <TextInput style={styles.input} value={location} onChangeText={setLocation} placeholder="Location" />
        <TextInput style={styles.input} value={latitude} onChangeText={setLatitude} placeholder="Latitude" keyboardType="decimal-pad" />
        <TextInput style={styles.input} value={longitude} onChangeText={setLongitude} placeholder="Longitude" keyboardType="decimal-pad" />
        <TextInput style={styles.input} value={timezone} onChangeText={setTimezone} placeholder="Timezone" />

        <TouchableOpacity style={styles.button} onPress={handleCalculate} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? 'Calculating...' : 'Calculate Chart'}</Text>
        </TouchableOpacity>
      </View>

      {chart ? (
        <View style={styles.card}>
          <Text style={styles.sectionTitle}>Chart Result</Text>
          <Text style={styles.row}>Ascendant: {chart?.ascendant?.sign || '-'} ({chart?.ascendant?.degree || 0})</Text>
          <Text style={styles.sectionTitle}>Planets</Text>
          {(chart?.planets || []).slice(0, 12).map((planet: any, idx: number) => (
            <Text key={idx} style={styles.row}>
              {planet.name}: {planet.sign} ({planet.degree}) H{planet.house}
            </Text>
          ))}
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
    marginTop: 4,
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 6,
    marginTop: 4,
  },
  row: {
    color: THEME.textLight,
    marginBottom: 4,
  },
});

export default HoroscopeScreen;
