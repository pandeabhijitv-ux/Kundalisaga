import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator} from 'react-native';
import {THEME} from '../constants/theme';

const PLANETS = [
  {planet: 'Jupiter', role: 'Wealth & Expansion', effect: '📈 Bull phase for investments', color: '#F59E0B'},
  {planet: 'Saturn', role: 'Discipline & Delays', effect: '⚠️ Caution in real estate', color: '#6B7280'},
  {planet: 'Venus', role: 'Luxury & Markets', effect: '✨ Favorable for commodities', color: '#EC4899'},
  {planet: 'Mercury', role: 'Trade & Commerce', effect: '💹 Good for short-term trades', color: '#10B981'},
  {planet: 'Mars', role: 'Energy & Risk', effect: '🔥 High volatility period', color: '#EF4444'},
];

const FinancialScreen = () => {
  const [loading, setLoading] = useState(false);
  const [expanded, setExpanded] = useState<number | null>(null);

  const analyze = () => {
    setLoading(true);
    setTimeout(() => setLoading(false), 1200);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>📈</Text>
        <Text style={styles.title}>Financial Astrology</Text>
        <Text style={styles.subtitle}>Market outlook based on planetary transits</Text>
      </View>

      <View style={styles.overviewCard}>
        <Text style={styles.overviewTitle}>🌟 Current Outlook</Text>
        <Text style={styles.overviewText}>Jupiter in Taurus creates favorable conditions for long-term investments. Saturn retrograde suggests caution in speculative markets until August.</Text>
      </View>

      <Text style={styles.sectionTitle}>Planetary Financial Influences</Text>
      {PLANETS.map((p, i) => (
        <TouchableOpacity key={i} style={styles.planetCard} onPress={() => setExpanded(expanded === i ? null : i)}>
          <View style={[styles.colorBar, {backgroundColor: p.color}]} />
          <View style={styles.planetInfo}>
            <Text style={styles.planetName}>{p.planet}</Text>
            <Text style={styles.planetRole}>{p.role}</Text>
            <Text style={styles.planetEffect}>{p.effect}</Text>
          </View>
          <Text style={styles.chevron}>{expanded === i ? '▲' : '▼'}</Text>
        </TouchableOpacity>
      ))}

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>📊 Get Personal Financial Forecast</Text>}
      </TouchableOpacity>

      <View style={styles.disclaimer}>
        <Text style={styles.disclaimerText}>⚠️ Astrological analysis is for guidance only. Consult a financial advisor for investment decisions.</Text>
      </View>
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
  overviewCard: {backgroundColor: '#E8F5E9', borderRadius: 12, padding: 16, marginBottom: 20, borderLeftWidth: 4, borderLeftColor: '#4CAF50'},
  overviewTitle: {fontSize: 16, fontWeight: 'bold', color: '#2E7D32', marginBottom: 6},
  overviewText: {fontSize: 14, color: '#388E3C', lineHeight: 20},
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  planetCard: {flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  colorBar: {width: 4, height: 50, borderRadius: 2, marginRight: 12},
  planetInfo: {flex: 1},
  planetName: {fontSize: 16, fontWeight: 'bold', color: THEME.text},
  planetRole: {fontSize: 12, color: THEME.textLight, marginTop: 2},
  planetEffect: {fontSize: 13, color: THEME.primary, marginTop: 4},
  chevron: {fontSize: 14, color: THEME.textLight},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginVertical: 16},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  disclaimer: {backgroundColor: '#FFF3CD', borderRadius: 8, padding: 12},
  disclaimerText: {fontSize: 12, color: '#856404', lineHeight: 18},
});

export default FinancialScreen;
