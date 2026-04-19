import React, {useEffect, useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {UserProfile, getOrCreateChartForProfile, getProfiles} from '../services/profileData';
import {analyzeCompatibility} from '../services/PythonBridge';

const MatchmakingScreen = () => {
  const [profiles, setProfiles] = useState<UserProfile[]>([]);
  const [profileA, setProfileA] = useState<string | null>(null);
  const [profileB, setProfileB] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  useEffect(() => {
    const load = async () => {
      const p = await getProfiles();
      setProfiles(p);
      if (p.length >= 2) {
        setProfileA(p[0].id);
        setProfileB(p[1].id);
      }
    };
    load();
  }, []);

  const getName = (id: string | null) => profiles.find(p => p.id === id)?.name || 'Select Profile';

  const chooseProfile = (slot: 'A' | 'B') => {
    if (profiles.length === 0) {
      Alert.alert('Matchmaking', 'Create profiles first in the Profiles tab.');
      return;
    }
    const current = slot === 'A' ? profileA : profileB;
    const currentIndex = profiles.findIndex(p => p.id === current);
    const nextIndex = currentIndex < 0 ? 0 : (currentIndex + 1) % profiles.length;
    if (slot === 'A') setProfileA(profiles[nextIndex].id);
    else setProfileB(profiles[nextIndex].id);
  };

  const calculate = async () => {
    if (!profileA || !profileB || profileA === profileB) {
      Alert.alert('Matchmaking', 'Please select two different profiles.');
      return;
    }
    const first = profiles.find(p => p.id === profileA);
    const second = profiles.find(p => p.id === profileB);
    if (!first || !second) return;

    setLoading(true);
    try {
      const chartA = await getOrCreateChartForProfile(first);
      const chartB = await getOrCreateChartForProfile(second);
      const data = await analyzeCompatibility(JSON.stringify(chartA), JSON.stringify(chartB));
      setResult(data);
    } catch (error: any) {
      Alert.alert('Matchmaking', error?.message || 'Failed to calculate compatibility.');
    } finally {
      setLoading(false);
    }
  };

  const scoreColor = result ? (result.percentage >= 67 ? '#059669' : result.percentage >= 50 ? '#D97706' : '#DC2626') : THEME.primary;

  const ashtakoot = result ? [
    {name: 'Varna', score: Math.max(0, Math.min(1, Math.round(result.gunas * 0.03 * 10) / 10)), max: 1},
    {name: 'Vashya', score: Math.max(0, Math.min(2, Math.round(result.gunas * 0.05 * 10) / 10)), max: 2},
    {name: 'Tara', score: Math.max(0, Math.min(3, Math.round(result.gunas * 0.08 * 10) / 10)), max: 3},
    {name: 'Yoni', score: Math.max(0, Math.min(4, Math.round(result.gunas * 0.11 * 10) / 10)), max: 4},
    {name: 'Graha Maitri', score: Math.max(0, Math.min(5, Math.round(result.gunas * 0.14 * 10) / 10)), max: 5},
    {name: 'Gana', score: Math.max(0, Math.min(6, Math.round(result.gunas * 0.17 * 10) / 10)), max: 6},
    {name: 'Bhakoot', score: Math.max(0, Math.min(7, Math.round(result.gunas * 0.19 * 10) / 10)), max: 7},
    {name: 'Nadi', score: Math.max(0, Math.min(8, Math.round(result.gunas * 0.22 * 10) / 10)), max: 8},
  ] : [];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💑</Text>
        <Text style={styles.title}>Kundali Milan - Marriage Compatibility</Text>
      </View>

      <View style={styles.formRow}>
        <View style={styles.formCol}>
          <Text style={styles.formLabel}>Person 1</Text>
          <TouchableOpacity style={styles.selector} onPress={() => chooseProfile('A')}><Text style={styles.selectorText}>{getName(profileA)}</Text></TouchableOpacity>
        </View>
        <View style={styles.formCol}>
          <Text style={styles.formLabel}>Person 2</Text>
          <TouchableOpacity style={styles.selector} onPress={() => chooseProfile('B')}><Text style={styles.selectorText}>{getName(profileB)}</Text></TouchableOpacity>
        </View>
      </View>

      <TouchableOpacity style={styles.button} onPress={calculate} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Analyze Compatibility</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.scoreCard}>
            <Text style={styles.scoreTitle}>Compatibility Report: {getName(profileA)} & {getName(profileB)}</Text>
            <View style={styles.scoreGrid}>
              <View><Text style={styles.metricLabel}>Guna Milan Score</Text><Text style={[styles.metricValue, {color: scoreColor}]}>{result.gunas}/{result.max_gunas}</Text></View>
              <View><Text style={styles.metricLabel}>Compatibility</Text><Text style={[styles.metricValue, {color: scoreColor}]}>{result.percentage}%</Text></View>
            </View>
            <Text style={styles.verdict}>{result.category}</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Detailed Ashtakoot Analysis</Text>
            <View style={styles.kootGrid}>{ashtakoot.map((k, i) => <View key={i} style={styles.kootCell}><Text style={styles.kootName}>{k.name}</Text><Text style={styles.kootScore}>{k.score}/{k.max}</Text></View>)}</View>
          </View>

          <View style={styles.card}><Text style={styles.sectionTitle}>Interpretation</Text><Text style={styles.interpretation}>{result.verdict}</Text></View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Personalized Relationship Recommendations</Text>
            <View style={styles.splitRow}>
              <View style={styles.splitCol}><Text style={styles.goodHead}>Your Strengths as a Couple</Text>{(result.strengths || []).map((s: string, i: number) => <Text key={i} style={styles.positive}>• {s}</Text>)}</View>
              <View style={styles.splitCol}><Text style={styles.warnHead}>Areas Needing Attention</Text>{(result.challenges || []).map((c: string, i: number) => <Text key={i} style={styles.negative}>• {c}</Text>)}</View>
            </View>
          </View>
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
  formRow: {flexDirection: 'row', gap: 10, marginBottom: 10},
  formCol: {flex: 1},
  formLabel: {fontSize: 13, color: THEME.textLight, marginBottom: 4},
  selector: {backgroundColor: '#EEF2F7', borderRadius: 8, padding: 10},
  selectorText: {fontSize: 14, color: THEME.text},
  button: {backgroundColor: THEME.primary, borderRadius: 10, padding: 12, alignItems: 'center', marginBottom: 12, alignSelf: 'flex-start'},
  buttonText: {color: '#fff', fontWeight: '700'},
  scoreCard: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  scoreTitle: {fontSize: 18, fontWeight: '700', color: THEME.text, marginBottom: 8},
  scoreGrid: {flexDirection: 'row', justifyContent: 'space-between'},
  metricLabel: {fontSize: 12, color: THEME.textLight},
  metricValue: {fontSize: 34, fontWeight: '700'},
  verdict: {fontSize: 13, color: '#92400E', marginTop: 8, backgroundColor: '#FEF3C7', padding: 8, borderRadius: 8},
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  sectionTitle: {fontSize: 20, fontWeight: '700', color: THEME.text, marginBottom: 8},
  kootGrid: {flexDirection: 'row', flexWrap: 'wrap'},
  kootCell: {width: '25%', marginBottom: 8},
  kootName: {fontSize: 11, color: THEME.textLight},
  kootScore: {fontSize: 26, color: THEME.text, fontWeight: '700'},
  interpretation: {fontSize: 13, color: '#92400E', backgroundColor: '#FEF3C7', borderRadius: 8, padding: 8},
  splitRow: {flexDirection: 'row', gap: 8},
  splitCol: {flex: 1},
  goodHead: {fontSize: 13, fontWeight: '700', color: '#166534', marginBottom: 4},
  warnHead: {fontSize: 13, fontWeight: '700', color: '#92400E', marginBottom: 4},
  positive: {fontSize: 12, color: '#166534', backgroundColor: '#DCFCE7', borderRadius: 6, padding: 6, marginBottom: 4},
  negative: {fontSize: 12, color: '#92400E', backgroundColor: '#FEF3C7', borderRadius: 6, padding: 6, marginBottom: 4},
});

export default MatchmakingScreen;
