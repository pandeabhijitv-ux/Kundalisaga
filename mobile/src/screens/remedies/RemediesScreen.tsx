/**
 * Remedies Screen
 * Fetches remedy recommendations from Python bridge.
 */
import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import {THEME} from '../../constants/theme';
import {getRemedies} from '../../services/PythonBridge';

const RemediesScreen = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  const handleLoadRemedies = async () => {
    setLoading(true);
    try {
      const response = await getRemedies({planets: [], houses: [], ascendant: {}, dasha: {}} as any);
      if ((response as any)?.error) {
        Alert.alert('Remedy Error', (response as any).error);
      }
      setData(response);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Failed to load remedies');
    } finally {
      setLoading(false);
    }
  };

  const renderSection = (title: string, items: any[]) => {
    if (!items || items.length === 0) {
      return null;
    }

    return (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>{title}</Text>
        {items.map((item, idx) => (
          <Text key={idx} style={styles.row}>
            • {typeof item === 'string' ? item : item.name || item.mantra || item.day || JSON.stringify(item)}
          </Text>
        ))}
      </View>
    );
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Astrological Remedies</Text>

      <View style={styles.card}>
        <Text style={styles.helper}>
          Generate personalized remedy suggestions such as gemstones, mantras, fasting, and charity.
        </Text>
        <TouchableOpacity style={styles.button} onPress={handleLoadRemedies} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? 'Loading...' : 'Generate Remedies'}</Text>
        </TouchableOpacity>
      </View>

      {data ? (
        <View style={styles.card}>
          {renderSection('Gemstones', data.gemstones)}
          {renderSection('Mantras', data.mantras)}
          {renderSection('Fasting', data.fasting)}
          {renderSection('Charity', data.charity)}
          {renderSection('Daily Practices', data.daily_practices)}
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
  helper: {
    color: THEME.textLight,
    marginBottom: 10,
    lineHeight: 20,
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
  section: {
    marginBottom: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 6,
  },
  row: {
    color: THEME.textLight,
    marginBottom: 4,
    lineHeight: 20,
  },
});

export default RemediesScreen;
