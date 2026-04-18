import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput, ActivityIndicator} from 'react-native';
import {THEME} from '../constants/theme';

const COMPATIBILITY_POINTS = [
  {aspect: 'Varna (Character)', max: 1, desc: 'Spiritual compatibility'},
  {aspect: 'Vashya (Control)', max: 2, desc: 'Mutual influence'},
  {aspect: 'Tara (Star)', max: 3, desc: 'Birth star compatibility'},
  {aspect: 'Yoni (Nature)', max: 4, desc: 'Biological compatibility'},
  {aspect: 'Graha Maitri (Friendship)', max: 5, desc: 'Intellectual compatibility'},
  {aspect: 'Gana (Category)', max: 6, desc: 'Temperament compatibility'},
  {aspect: 'Bhakoot (Love)', max: 7, desc: 'Emotional compatibility'},
  {aspect: 'Nadi (Health)', max: 8, desc: 'Genetic compatibility'},
];

const MatchmakingScreen = () => {
  const [gender1, setGender1] = useState('Male');
  const [name1, setName1] = useState('');
  const [name2, setName2] = useState('');
  const [loading, setLoading] = useState(false);
  const [score, setScore] = useState<number | null>(null);

  const calculate = () => {
    setLoading(true);
    setTimeout(() => {
      setScore(28); // Sample score
      setLoading(false);
    }, 1500);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💑</Text>
        <Text style={styles.title}>Kundali Milan</Text>
        <Text style={styles.subtitle}>Marriage compatibility analysis (Ashta Koota)</Text>
      </View>

      <View style={styles.formCard}>
        <Text style={styles.formLabel}>Groom's Name</Text>
        <TextInput style={styles.input} placeholder="Enter groom's name" value={name1} onChangeText={setName1} />

        <Text style={styles.formLabel}>Bride's Name</Text>
        <TextInput style={styles.input} placeholder="Enter bride's name" value={name2} onChangeText={setName2} />

        <TouchableOpacity style={styles.button} onPress={calculate} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>💕 Calculate Compatibility</Text>}
        </TouchableOpacity>
      </View>

      {score !== null && (
        <View style={styles.scoreCard}>
          <Text style={styles.scoreTitle}>Compatibility Score</Text>
          <Text style={[styles.score, {color: score >= 24 ? '#059669' : score >= 18 ? '#D97706' : '#DC2626'}]}>{score}/36</Text>
          <Text style={styles.scoreLabel}>{score >= 24 ? '✅ Excellent Match' : score >= 18 ? '⚠️ Average Match' : '❌ Below Average'}</Text>
        </View>
      )}

      <Text style={styles.sectionTitle}>Ashta Koota (8 Aspects)</Text>
      {COMPATIBILITY_POINTS.map((k, i) => (
        <View key={i} style={styles.kootaRow}>
          <View style={styles.kootaLeft}>
            <Text style={styles.kootaName}>{k.aspect}</Text>
            <Text style={styles.kootaDesc}>{k.desc}</Text>
          </View>
          <Text style={styles.kootaMax}>/{k.max}</Text>
        </View>
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
  formCard: {backgroundColor: '#fff', borderRadius: 14, padding: 16, marginBottom: 20, elevation: 2},
  formLabel: {fontSize: 14, color: THEME.text, fontWeight: '600', marginBottom: 6},
  input: {borderWidth: 1, borderColor: '#E0E0E0', borderRadius: 8, padding: 10, fontSize: 14, marginBottom: 14, color: THEME.text},
  button: {backgroundColor: THEME.primary, borderRadius: 10, padding: 14, alignItems: 'center'},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  scoreCard: {backgroundColor: '#fff', borderRadius: 14, padding: 20, alignItems: 'center', marginBottom: 20, elevation: 3},
  scoreTitle: {fontSize: 16, color: THEME.text, fontWeight: '600', marginBottom: 8},
  score: {fontSize: 48, fontWeight: 'bold'},
  scoreLabel: {fontSize: 16, marginTop: 6, fontWeight: '600'},
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  kootaRow: {flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderRadius: 10, padding: 12, marginBottom: 8, elevation: 1},
  kootaLeft: {flex: 1},
  kootaName: {fontSize: 14, fontWeight: '600', color: THEME.text},
  kootaDesc: {fontSize: 12, color: THEME.textLight, marginTop: 2},
  kootaMax: {fontSize: 16, fontWeight: 'bold', color: THEME.primary},
});

export default MatchmakingScreen;
