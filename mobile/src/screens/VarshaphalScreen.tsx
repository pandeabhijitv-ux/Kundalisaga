import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {analyzeVarshaphal} from '../services/PythonBridge';

const VarshaphalScreen = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [profileName, setProfileName] = useState('');
  const currentYear = new Date().getFullYear();

  const analyze = async () => {
    setLoading(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      setProfileName(profile.name || 'Profile');
      const data = await analyzeVarshaphal(JSON.stringify(chart));
      setResult(data);
    } catch (error: any) {
      Alert.alert('Varshaphal', error?.message || 'Unable to analyze. Please ensure an active profile exists.');
    } finally {
      setLoading(false);
    }
  };

  const overallRating = Math.max(45, Math.min(88, 60 + (result?.strong_planets?.length || 0) * 4 - (result?.weak_planets?.length || 0) * 2));
  const munthaHouse = ((currentYear + 3) % 12) + 1;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>🗓️</Text>
        <Text style={styles.title}>Varshaphal - Annual Predictions</Text>
        <Text style={styles.subtitle}>Comprehensive yearly forecast based on your chart</Text>
      </View>

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Generate Annual Predictions</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.card}>
            <Text style={styles.mainHeading}>Varshaphal {result.year || currentYear} - {profileName}</Text>
            <Text style={styles.muntha}>🌟 Muntha Position: House {munthaHouse}</Text>
            <Text style={styles.munthaNote}>The Muntha for your {result.year || currentYear} Varshaphal is in the {munthaHouse}th house, which is a key area of focus this year.</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Overall Year Outlook</Text>
            <View style={styles.metricRow}>
              <View><Text style={styles.metricLabel}>Overall Rating</Text><Text style={styles.metricValue}>{overallRating}/100</Text></View>
              <View><Text style={styles.metricLabel}>Best Months</Text><Text style={styles.metricValue}>Jan-Mar</Text></View>
              <View><Text style={styles.metricLabel}>Key Planet</Text><Text style={styles.metricValue}>{(result.strong_planets || [])[0] || 'Mercury'}</Text></View>
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Detailed Annual Forecast</Text>
            {(result.focus_areas || []).slice(0, 5).map((f: string, i: number) => {
              const score = 78 - i * 6;
              return (
                <View key={i} style={styles.forecastBlock}>
                  <Text style={styles.forecastTitle}>Area {i + 1} • Score: {score}/100</Text>
                  <View style={styles.bar}><View style={[styles.barFill, {width: `${score}%`}]} /></View>
                  <Text style={styles.forecastPoint}>• {f}</Text>
                </View>
              );
            })}
          </View>

          {(result.challenges || []).length > 0 && (
            <View style={[styles.card, {backgroundColor: '#FFFBEB'}]}>
              <Text style={styles.sectionTitle}>Challenges</Text>
              {(result.challenges || []).map((c: string, i: number) => <Text key={i} style={styles.challenge}>• {c}</Text>)}
            </View>
          )}

          {(result.remedies || []).length > 0 && (
            <View style={[styles.card, {backgroundColor: '#FCF8E8'}]}>
              <Text style={styles.sectionTitle}>Remedies</Text>
              {(result.remedies || []).map((r: string, i: number) => <Text key={i} style={styles.remedy}>• {r}</Text>)}
            </View>
          )}

          <TouchableOpacity style={[styles.button, {backgroundColor: THEME.textLight, marginTop: 8}]} onPress={() => setResult(null)}>
            <Text style={styles.buttonText}>Re-analyze</Text>
          </TouchableOpacity>
        </>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#FFF8F0'},
  content: {padding: 16, paddingBottom: 40},
  header: {alignItems: 'center', paddingVertical: 20, marginBottom: 8},
  icon: {fontSize: 42, marginBottom: 8},
  title: {fontSize: 22, fontWeight: '700', color: THEME.text, textAlign: 'center'},
  subtitle: {fontSize: 12, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  button: {backgroundColor: THEME.primary, borderRadius: 10, padding: 12, alignItems: 'center', marginBottom: 12, alignSelf: 'flex-start'},
  buttonText: {color: '#fff', fontWeight: '700'},
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  mainHeading: {fontSize: 34, fontWeight: '700', color: THEME.text, marginBottom: 8},
  muntha: {fontSize: 26, fontWeight: '700', color: THEME.text, marginBottom: 6},
  munthaNote: {fontSize: 12, color: '#1F4E79', backgroundColor: '#EEF2F7', borderRadius: 8, padding: 8},
  sectionTitle: {fontSize: 30, fontWeight: '700', color: THEME.text, marginBottom: 8},
  metricRow: {flexDirection: 'row', justifyContent: 'space-between'},
  metricLabel: {fontSize: 11, color: THEME.textLight},
  metricValue: {fontSize: 26, fontWeight: '700', color: THEME.text},
  forecastBlock: {marginBottom: 10},
  forecastTitle: {fontSize: 12, color: THEME.text, marginBottom: 4},
  bar: {height: 5, borderRadius: 3, backgroundColor: '#D9E3EF', marginBottom: 6},
  barFill: {height: 5, borderRadius: 3, backgroundColor: '#2D89E5'},
  forecastPoint: {fontSize: 13, color: THEME.text},
  challenge: {fontSize: 13, color: '#92400E', lineHeight: 22},
  remedy: {fontSize: 13, color: THEME.text, lineHeight: 22},
});

export default VarshaphalScreen;
