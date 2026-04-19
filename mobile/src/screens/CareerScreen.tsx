import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {analyzeCareer} from '../services/PythonBridge';

const STRENGTH_STAR: Record<string, string> = {
  Excellent: '⭐⭐⭐⭐⭐', 'Very Good': '⭐⭐⭐⭐', Good: '⭐⭐⭐', Average: '⭐⭐', Weak: '⭐',
};

const CareerScreen = () => {
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [profileName, setProfileName] = useState('');

  const analyze = async () => {
    setAnalyzing(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      setProfileName(profile.name);
      const data = await analyzeCareer(JSON.stringify(chart));
      setResult(data);
    } catch (error: any) {
      Alert.alert('Career Analysis', error?.message || 'Unable to analyze career. Please ensure an active profile exists.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💼</Text>
        <Text style={styles.title}>Career Guidance</Text>
        <Text style={styles.subtitle}>Real Vedic analysis using planetary strengths from your birth chart</Text>
      </View>

      {!result && (
        <TouchableOpacity style={styles.button} onPress={analyze} disabled={analyzing}>
          {analyzing ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Analyze Career (Active Profile)</Text>}
        </TouchableOpacity>
      )}

      {result && (
        <>
          <Text style={styles.sectionTitle}>Career Analysis for {profileName}</Text>
          {result.success && result.recommendations?.map((rec: any, i: number) => (
            <View key={i} style={[styles.resultCard, i === 0 && styles.topCard]}>
              <View style={styles.recHeader}>
                <Text style={styles.rankBadge}>#{rec.rank || i + 1}</Text>
                <View style={{flex: 1}}>
                  <Text style={styles.sectorName}>{rec.sector}</Text>
                  <Text style={styles.stars}>{STRENGTH_STAR[rec.strength] || '⭐⭐⭐'} {rec.strength}</Text>
                </View>
                <Text style={styles.score}>{rec.score}/{rec.max_score}</Text>
              </View>
              <Text style={styles.advice}>{rec.advice}</Text>
              {rec.factors?.length > 0 && (
                <Text style={styles.factors}>✦ {rec.factors.slice(0, 2).join('  ✦ ')}</Text>
              )}
            </View>
          ))}
          {(!result.success || !result.recommendations?.length) && (
            <View style={styles.resultCard}>
              <Text style={styles.advice}>{result.error || 'No recommendations generated. Ensure birth data is complete.'}</Text>
            </View>
          )}
          {result.planetary_strengths && (
            <View style={styles.planetsCard}>
              <Text style={styles.sectionTitle}>Planetary Strengths</Text>
              {Object.entries(result.planetary_strengths).slice(0, 9).map(([planet, strength]: [string, any]) => (
                <View key={planet} style={styles.planetItem}>
                  <View style={styles.planetRow}>
                    <Text style={styles.planetName}>{planet}</Text>
                    <Text style={styles.planetScore}>{strength}%</Text>
                  </View>
                  <View style={styles.bar}><View style={[styles.barFill, {width: `${Math.min(strength, 100)}%` as any}]} /></View>
                </View>
              ))}
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
  header: {alignItems: 'center', paddingVertical: 20, marginBottom: 16},
  icon: {fontSize: 48, marginBottom: 8},
  title: {fontSize: 22, fontWeight: 'bold', color: THEME.primary, textAlign: 'center'},
  subtitle: {fontSize: 14, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginVertical: 16},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  resultCard: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  topCard: {borderLeftWidth: 4, borderLeftColor: THEME.primary},
  recHeader: {flexDirection: 'row', alignItems: 'center', marginBottom: 8, gap: 8},
  rankBadge: {backgroundColor: THEME.primary, color: '#fff', fontWeight: 'bold', width: 28, height: 28, borderRadius: 14, textAlign: 'center', lineHeight: 28, fontSize: 13},
  sectorName: {fontSize: 15, fontWeight: 'bold', color: THEME.text},
  stars: {fontSize: 12, color: THEME.textLight, marginTop: 2},
  score: {fontSize: 16, fontWeight: 'bold', color: THEME.primary},
  advice: {fontSize: 13, color: THEME.text, lineHeight: 18, marginBottom: 6},
  factors: {fontSize: 12, color: THEME.textLight},
  planetsCard: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  planetItem: {marginBottom: 8},
  planetRow: {flexDirection: 'row', justifyContent: 'space-between', marginBottom: 3},
  planetName: {fontSize: 13, color: THEME.text},
  planetScore: {fontSize: 13, color: THEME.primary, fontWeight: '600'},
  bar: {height: 6, backgroundColor: '#E5E7EB', borderRadius: 3},
  barFill: {height: 6, backgroundColor: THEME.primary, borderRadius: 3},
});

export default CareerScreen;
