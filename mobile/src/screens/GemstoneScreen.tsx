import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView} from 'react-native';
import {THEME} from '../constants/theme';

const GEMS = [
  {gem: 'Ruby', planet: 'Sun', color: '#DC2626', bg: '#FEE2E2', benefits: 'Leadership, confidence, vitality', finger: 'Ring finger', wearing: 'Sunday morning'},
  {gem: 'Pearl', planet: 'Moon', color: '#9CA3AF', bg: '#F3F4F6', benefits: 'Peace, intuition, emotional balance', finger: 'Little finger', wearing: 'Monday morning'},
  {gem: 'Red Coral', planet: 'Mars', color: '#EA580C', bg: '#FFEDD5', benefits: 'Courage, energy, protection', finger: 'Ring finger', wearing: 'Tuesday morning'},
  {gem: 'Emerald', planet: 'Mercury', color: '#059669', bg: '#D1FAE5', benefits: 'Intelligence, communication, business', finger: 'Little finger', wearing: 'Wednesday morning'},
  {gem: 'Yellow Sapphire', planet: 'Jupiter', color: '#D97706', bg: '#FEF3C7', benefits: 'Wisdom, wealth, spirituality', finger: 'Index finger', wearing: 'Thursday morning'},
  {gem: 'Diamond', planet: 'Venus', color: '#7C3AED', bg: '#EDE9FE', benefits: 'Love, luxury, creativity', finger: 'Middle finger', wearing: 'Friday morning'},
  {gem: 'Blue Sapphire', planet: 'Saturn', color: '#1D4ED8', bg: '#DBEAFE', benefits: 'Discipline, career success', finger: 'Middle finger', wearing: 'Saturday morning'},
];

const GemstoneScreen = () => {
  const [selected, setSelected] = useState<number | null>(null);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💎</Text>
        <Text style={styles.title}>Gemstone Guide</Text>
        <Text style={styles.subtitle}>Personalized gemstone recommendations by planetary ruler</Text>
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.infoText}>💡 Tap any gemstone to see detailed wearing instructions. Always consult a Jyotishi before wearing a gemstone.</Text>
      </View>

      {GEMS.map((g, i) => (
        <TouchableOpacity key={i} style={[styles.gemCard, {backgroundColor: g.bg}]} onPress={() => setSelected(selected === i ? null : i)}>
          <View style={styles.gemHeader}>
            <View style={[styles.gemDot, {backgroundColor: g.color}]} />
            <View style={styles.gemInfo}>
              <Text style={styles.gemName}>{g.gem}</Text>
              <Text style={styles.planetName}>Planet: {g.planet}</Text>
            </View>
            <Text style={styles.chevron}>{selected === i ? '▲' : '▼'}</Text>
          </View>
          <Text style={styles.benefits}>✨ {g.benefits}</Text>
          {selected === i && (
            <View style={styles.details}>
              <Text style={styles.detailRow}>👆 Finger: {g.finger}</Text>
              <Text style={styles.detailRow}>🌅 Best time: {g.wearing}</Text>
              <Text style={styles.detailNote}>Wear in gold/silver ring, weight: 3-7 carats recommended</Text>
            </View>
          )}
        </TouchableOpacity>
      ))}
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
  infoCard: {backgroundColor: '#E0F2FE', borderRadius: 10, padding: 12, marginBottom: 16},
  infoText: {fontSize: 13, color: '#0369A1', lineHeight: 18},
  gemCard: {borderRadius: 12, padding: 14, marginBottom: 10},
  gemHeader: {flexDirection: 'row', alignItems: 'center', marginBottom: 6},
  gemDot: {width: 14, height: 14, borderRadius: 7, marginRight: 10},
  gemInfo: {flex: 1},
  gemName: {fontSize: 16, fontWeight: 'bold', color: THEME.text},
  planetName: {fontSize: 12, color: THEME.textLight},
  chevron: {fontSize: 14, color: THEME.textLight},
  benefits: {fontSize: 13, color: THEME.text, lineHeight: 18},
  details: {marginTop: 10, paddingTop: 10, borderTopWidth: 1, borderTopColor: 'rgba(0,0,0,0.1)'},
  detailRow: {fontSize: 13, color: THEME.text, marginBottom: 4},
  detailNote: {fontSize: 12, color: THEME.textLight, fontStyle: 'italic', marginTop: 4},
});

export default GemstoneScreen;
