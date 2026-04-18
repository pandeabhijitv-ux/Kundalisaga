import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator} from 'react-native';
import {THEME} from '../constants/theme';

const SOULMATE_TRAITS = [
  {trait: 'Physical Appearance', icon: '👁️'},
  {trait: 'Nature & Personality', icon: '💭'},
  {trait: 'Profession', icon: '💼'},
  {trait: 'Meeting Direction', icon: '🧭'},
  {trait: 'Marriage Timing', icon: '💍'},
  {trait: 'Compatibility Factors', icon: '💕'},
];

const SoulmateScreen = () => {
  const [loading, setLoading] = useState(false);
  const [revealed, setRevealed] = useState(false);

  const analyze = () => {
    setLoading(true);
    setTimeout(() => {
      setRevealed(true);
      setLoading(false);
    }, 2000);
  };

  const RESULTS: Record<string, string> = {
    'Physical Appearance': 'Attractive, medium height, expressive eyes, warm complexion',
    'Nature & Personality': 'Intelligent, caring, spiritual-minded, good communicator',
    'Profession': 'Likely in education, medicine, law or arts',
    'Meeting Direction': 'Most likely to meet in the East or through educational/professional circles',
    'Marriage Timing': 'Favorable periods: 2025-2027 (Jupiter transit favorable)',
    'Compatibility Factors': 'Fire or Earth signs most compatible with your chart',
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💕</Text>
        <Text style={styles.title}>Soulmate Analysis</Text>
        <Text style={styles.subtitle}>Discover your destined partner's traits from your Navamsa chart</Text>
      </View>

      <View style={styles.infoCard}>
        <Text style={styles.infoText}>🌟 Your 7th house, Navamsa chart, and Venus placement reveal the characteristics of your life partner.</Text>
      </View>

      {!revealed ? (
        <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
          {loading ? (
            <View style={styles.loadingRow}>
              <ActivityIndicator color="#fff" />
              <Text style={[styles.buttonText, {marginLeft: 8}]}>Reading your stars...</Text>
            </View>
          ) : (
            <Text style={styles.buttonText}>💫 Reveal My Soulmate Profile</Text>
          )}
        </TouchableOpacity>
      ) : (
        <>
          {SOULMATE_TRAITS.map((t, i) => (
            <View key={i} style={styles.traitCard}>
              <Text style={styles.traitIcon}>{t.icon}</Text>
              <View style={styles.traitInfo}>
                <Text style={styles.traitTitle}>{t.trait}</Text>
                <Text style={styles.traitValue}>{RESULTS[t.trait]}</Text>
              </View>
            </View>
          ))}
          <TouchableOpacity style={[styles.button, {marginTop: 12}]} onPress={() => setRevealed(false)}>
            <Text style={styles.buttonText}>🔄 Re-analyze</Text>
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
  infoCard: {backgroundColor: '#FCE4EC', borderRadius: 10, padding: 14, marginBottom: 20},
  infoText: {fontSize: 13, color: '#880E4F', lineHeight: 20},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 16, alignItems: 'center', marginBottom: 16},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  loadingRow: {flexDirection: 'row', alignItems: 'center'},
  traitCard: {flexDirection: 'row', backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2, alignItems: 'flex-start'},
  traitIcon: {fontSize: 28, marginRight: 12},
  traitInfo: {flex: 1},
  traitTitle: {fontSize: 14, fontWeight: 'bold', color: THEME.primary, marginBottom: 4},
  traitValue: {fontSize: 13, color: THEME.text, lineHeight: 20},
});

export default SoulmateScreen;
