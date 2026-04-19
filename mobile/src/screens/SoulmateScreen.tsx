import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {analyzeSoulmate} from '../services/PythonBridge';

const SoulmateScreen = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [profileName, setProfileName] = useState('');

  const analyze = async () => {
    setLoading(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      const gender = (profile as any).gender || 'male';
      setProfileName(profile.name || 'Profile');
      const data = await analyzeSoulmate(JSON.stringify(chart), gender);
      setResult(data);
    } catch (error: any) {
      Alert.alert('Soulmate Analysis', error?.message || 'Unable to analyze. Please ensure an active profile exists.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💕</Text>
        <Text style={styles.title}>Your Soulmate Analysis</Text>
        <Text style={styles.subtitle}>Discover your ideal life partner based on 7th house and Venus/Mars</Text>
      </View>

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Reveal Your Soulmate</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.readyBanner}><Text style={styles.readyText}>✨ Your Soulmate Analysis is Ready!</Text></View>

          {result.physical && (
            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Physical Characteristics</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Height:</Text> {result.physical.description}</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Build:</Text> {result.physical.build}</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Complexion:</Text> {result.physical.complexion}</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Special Features:</Text> {result.physical.eyes}</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Overall Look:</Text> {result.physical.style}</Text>
            </View>
          )}

          {result.personality && (
            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Personality Traits</Text>
              {result.personality.positive_traits?.map((t: string, i: number) => <Text key={i} style={styles.listItem}>• {t}</Text>)}
              <Text style={styles.infoRow}><Text style={styles.label}>7th House Influence:</Text> {result.personality['7th_house_influence']}</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Emotional Nature:</Text> {result.personality.emotional_nature}</Text>
            </View>
          )}

          {result.timing && (
            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Meeting & Timing</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Period:</Text> {result.timing.period}</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>Place:</Text> {result.timing.place}</Text>
              <Text style={styles.infoRow}><Text style={styles.label}>How:</Text> {result.timing.how}</Text>
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
  title: {fontSize: 28, fontWeight: '700', color: THEME.text, textAlign: 'center'},
  subtitle: {fontSize: 12, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginVertical: 10, alignSelf: 'flex-start'},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 14},
  readyBanner: {backgroundColor: '#DCFCE7', borderRadius: 8, padding: 10, marginBottom: 10},
  readyText: {fontSize: 12, color: '#166534', fontWeight: '600'},
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  sectionTitle: {fontSize: 34, fontWeight: '700', color: THEME.text, marginBottom: 10},
  infoRow: {fontSize: 13, color: THEME.text, lineHeight: 22, backgroundColor: '#EEF2F7', borderRadius: 8, padding: 8, marginBottom: 6},
  label: {fontWeight: '700', color: '#1F4E79'},
  listItem: {fontSize: 13, color: THEME.text, lineHeight: 22},
});

export default SoulmateScreen;
