import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput, ActivityIndicator} from 'react-native';
import {THEME} from '../constants/theme';

const NAKSHATRA_LETTERS: Record<string, string[]> = {
  'Ashwini': ['Chu', 'Che', 'Cho', 'La'],
  'Bharani': ['Li', 'Lu', 'Le', 'Lo'],
  'Krittika': ['A', 'I', 'U', 'E'],
  'Rohini': ['O', 'Va', 'Vi', 'Vu'],
  'Mrigashira': ['Ve', 'Vo', 'Ka', 'Ki'],
  'Ardra': ['Ku', 'Gha', 'Na', 'Chha'],
  'Punarvasu': ['Ke', 'Ko', 'Ha', 'Hi'],
  'Pushya': ['Hu', 'He', 'Ho', 'Da'],
  'Ashlesha': ['Di', 'Du', 'De', 'Do'],
};

const SUGGESTIONS: Record<string, string[]> = {
  'Chu': ['Chandan', 'Chandra', 'Chulbul'],
  'La': ['Lalita', 'Laxmi', 'Lalit'],
  'A': ['Aarav', 'Anika', 'Arjun'],
  'O': ['Om', 'Omkar', 'Ojas'],
  'Ka': ['Karan', 'Kavita', 'Kartik'],
};

const NameRecommendationScreen = () => {
  const [birthStar, setBirthStar] = useState('');
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const calculate = () => {
    if (!birthStar.trim()) return;
    setLoading(true);
    setTimeout(() => {
      const nakshatra = birthStar.trim();
      const letters = NAKSHATRA_LETTERS[nakshatra] || ['A', 'Ka', 'Sa', 'Ma'];
      const suggestions = letters.flatMap(l => SUGGESTIONS[l] || [`${l}raj`, `${l}devi`, `${l}nanda`]);
      setResult({nakshatra, letters, suggestions: suggestions.slice(0, 8), luckyNumber: 5, luckyColor: 'Yellow'});
      setLoading(false);
    }, 1200);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>✨</Text>
        <Text style={styles.title}>Name Recommendation</Text>
        <Text style={styles.subtitle}>Find a lucky Vedic name based on birth nakshatra</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.label}>Enter Birth Nakshatra (e.g. Ashwini, Rohini)</Text>
        <TextInput
          style={styles.input}
          value={birthStar}
          onChangeText={setBirthStar}
          placeholder="Birth Nakshatra"
          placeholderTextColor={THEME.textLight}
        />
      </View>

      <TouchableOpacity style={styles.button} onPress={calculate} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>✨ Get Name Suggestions</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Recommended Starting Letters</Text>
            <View style={styles.letterRow}>
              {result.letters.map((l: string) => (
                <View key={l} style={styles.letterBadge}><Text style={styles.letterText}>{l}</Text></View>
              ))}
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Lucky Names for {result.nakshatra}</Text>
            <View style={styles.nameGrid}>
              {result.suggestions.map((name: string, i: number) => (
                <View key={i} style={styles.nameBadge}><Text style={styles.nameText}>{name}</Text></View>
              ))}
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Additional Recommendations</Text>
            <Text style={styles.detailRow}>🔢 Lucky Number: {result.luckyNumber}</Text>
            <Text style={styles.detailRow}>🎨 Lucky Color: {result.luckyColor}</Text>
          </View>
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
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 16, elevation: 2},
  label: {fontSize: 13, color: THEME.textLight, marginBottom: 8},
  input: {borderWidth: 1, borderColor: '#E5D5C5', borderRadius: 8, padding: 11, fontSize: 15, color: THEME.text},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 20},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  sectionTitle: {fontSize: 15, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  letterRow: {flexDirection: 'row', flexWrap: 'wrap', gap: 8},
  letterBadge: {backgroundColor: THEME.primary, borderRadius: 8, paddingHorizontal: 14, paddingVertical: 8},
  letterText: {color: '#fff', fontWeight: 'bold', fontSize: 16},
  nameGrid: {flexDirection: 'row', flexWrap: 'wrap', gap: 8},
  nameBadge: {backgroundColor: '#FFF8F0', borderRadius: 8, paddingHorizontal: 12, paddingVertical: 7, borderWidth: 1, borderColor: '#E5D5C5'},
  nameText: {color: THEME.text, fontSize: 14},
  detailRow: {fontSize: 14, color: THEME.text, marginBottom: 6},
});

export default NameRecommendationScreen;
