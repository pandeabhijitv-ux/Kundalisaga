import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator} from 'react-native';
import {THEME} from '../constants/theme';

const SECTORS = [
  {icon: '💻', name: 'Technology & IT', desc: 'Software, AI, Data Science'},
  {icon: '💊', name: 'Medicine & Health', desc: 'Doctors, Healers, Wellness'},
  {icon: '⚖️', name: 'Law & Justice', desc: 'Legal, Judiciary, HR'},
  {icon: '🎨', name: 'Arts & Media', desc: 'Film, Music, Design'},
  {icon: '🏦', name: 'Finance & Banking', desc: 'Investment, CA, Stocks'},
  {icon: '🏗️', name: 'Real Estate', desc: 'Property, Construction'},
  {icon: '🌱', name: 'Agriculture', desc: 'Farming, Food, Nature'},
  {icon: '✈️', name: 'Travel & Tourism', desc: 'Aviation, Hospitality'},
];

const CareerScreen = () => {
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const analyze = () => {
    setAnalyzing(true);
    setTimeout(() => {
      setResult('Based on your birth chart, your 10th house lord and planetary positions suggest strong aptitude for Technology & Finance sectors. Mercury and Jupiter in favorable positions indicate success in intellectual and analytical roles.');
      setAnalyzing(false);
    }, 1500);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💼</Text>
        <Text style={styles.title}>Career & Business Analysis</Text>
        <Text style={styles.subtitle}>Discover ideal sectors based on your birth chart</Text>
      </View>

      <Text style={styles.sectionTitle}>Favorable Business Sectors</Text>
      <View style={styles.grid}>
        {SECTORS.map((s, i) => (
          <View key={i} style={styles.sectorCard}>
            <Text style={styles.sectorIcon}>{s.icon}</Text>
            <Text style={styles.sectorName}>{s.name}</Text>
            <Text style={styles.sectorDesc}>{s.desc}</Text>
          </View>
        ))}
      </View>

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={analyzing}>
        {analyzing ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>🔍 Analyze My Career Chart</Text>}
      </TouchableOpacity>

      {result && (
        <View style={styles.resultCard}>
          <Text style={styles.resultTitle}>📊 Career Analysis</Text>
          <Text style={styles.resultText}>{result}</Text>
        </View>
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
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  grid: {flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 20},
  sectorCard: {width: '47%', backgroundColor: '#fff', borderRadius: 12, padding: 12, alignItems: 'center', elevation: 2},
  sectorIcon: {fontSize: 28, marginBottom: 6},
  sectorName: {fontSize: 13, fontWeight: '600', color: THEME.primary, textAlign: 'center'},
  sectorDesc: {fontSize: 11, color: THEME.textLight, textAlign: 'center', marginTop: 2},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginVertical: 16},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  resultCard: {backgroundColor: '#fff', borderRadius: 12, padding: 16, elevation: 2, borderLeftWidth: 4, borderLeftColor: THEME.primary},
  resultTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.primary, marginBottom: 8},
  resultText: {fontSize: 14, color: THEME.text, lineHeight: 22},
});

export default CareerScreen;
