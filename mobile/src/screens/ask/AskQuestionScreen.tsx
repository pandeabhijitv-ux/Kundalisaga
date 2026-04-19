/**
 * Ask Question Screen
 * PWA-like category + single answer layout.
 */
import React, {useEffect, useState} from 'react';
import {View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Alert, ActivityIndicator} from 'react-native';
import {THEME} from '../../constants/theme';
import {searchKnowledge} from '../../services/PythonBridge';
import {getActiveProfile, UserProfile} from '../../services/profileData';

const PRESET_QUESTIONS: {[key: string]: string} = {
  career: 'What does my birth chart indicate about my career and profession?',
  finance: 'What does my birth chart indicate about finance and investment?',
  knowledge: 'Explain the significance of my ascendant and moon sign.',
  gemstones: 'Which gemstones are recommended based on my chart?',
  matchmaking: 'How does my chart indicate marriage compatibility?',
  muhurat: 'Which timings are auspicious for important events?',
  varshaphal: 'What is my annual forecast for this year?',
  name: 'What names are auspicious based on my nakshatra?',
};

const CATEGORY_LABELS: {[key: string]: string} = {
  career: 'Career & Profession',
  finance: 'Financial Outlook',
  knowledge: 'Vedic Basics',
  gemstones: 'Gemstone Guide',
  matchmaking: 'Matchmaking',
  muhurat: 'Muhurat Finder',
  varshaphal: 'Varshaphal',
  name: 'Name Recommendation',
};

const AskQuestionScreen = ({route}: any) => {
  const preset = route?.params?.preset;
  const [selectedCategory, setSelectedCategory] = useState('career');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState('');
  const [profile, setProfile] = useState<UserProfile | null>(null);

  useEffect(() => {
    loadProfileAndPreset();
  }, [preset]);

  const loadProfileAndPreset = async () => {
    try {
      const activeProfile = await getActiveProfile();
      setProfile(activeProfile);
    } catch {
      setProfile(null);
    }
    const category = preset || 'career';
    setSelectedCategory(category);
    setQuery(PRESET_QUESTIONS[category] || PRESET_QUESTIONS.career);
  };

  const buildContextualQuery = () => {
    if (!profile) return query.trim();
    return `${query.trim()}\n\n[Birth Details: Name: ${profile.name}, Date: ${profile.date}, Time: ${profile.time}, Place: ${profile.location}]`;
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      Alert.alert('Validation', 'Please enter a question');
      return;
    }
    setLoading(true);
    try {
      const response = await searchKnowledge(buildContextualQuery());
      if (response?.error) Alert.alert('Search Error', response.error);
      const best = response?.results?.[0]?.text || 'No clear answer found. Please refine your question.';
      setAnswer(best);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Failed to search knowledge base');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.powered}><Text style={styles.poweredText}>💡 Powered by built-in Vedic astrology knowledge - Instant, accurate answers!</Text></View>

      <Text style={styles.fieldLabel}>Choose a question category:</Text>
      <View style={styles.categoryRow}>
        {Object.keys(CATEGORY_LABELS).map(key => (
          <TouchableOpacity key={key} style={[styles.categoryChip, selectedCategory === key && styles.categoryChipActive]} onPress={() => {setSelectedCategory(key); setQuery(PRESET_QUESTIONS[key]);}}>
            <Text style={[styles.categoryText, selectedCategory === key && styles.categoryTextActive]}>{CATEGORY_LABELS[key]}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.fieldLabel}>Question:</Text>
      <TextInput style={styles.input} value={query} onChangeText={setQuery} multiline />

      <TouchableOpacity style={styles.button} onPress={handleSearch} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Submit Question</Text>}
      </TouchableOpacity>

      {answer ? (
        <View style={styles.answerCard}>
          <Text style={styles.answerTitle}>📘 Answer:</Text>
          <Text style={styles.answerText}>{answer}</Text>
          <View style={styles.footerTag}><Text style={styles.footerTagText}>✅ Answer generated from built-in Vedic astrology knowledge</Text></View>
        </View>
      ) : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: THEME.background},
  content: {padding: 16, paddingBottom: 24},
  powered: {backgroundColor: '#FEF3C7', borderRadius: 8, padding: 10, marginBottom: 10},
  poweredText: {fontSize: 12, color: '#92400E', fontWeight: '600'},
  fieldLabel: {fontSize: 13, color: THEME.textLight, marginBottom: 6},
  categoryRow: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 10},
  categoryChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 14, paddingHorizontal: 10, paddingVertical: 6},
  categoryChipActive: {backgroundColor: THEME.primary},
  categoryText: {fontSize: 12, color: THEME.primary},
  categoryTextActive: {color: '#fff'},
  input: {backgroundColor: '#fff', borderColor: '#E0E0E0', borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 10, marginBottom: 8, minHeight: 86, textAlignVertical: 'top', color: THEME.text},
  button: {backgroundColor: THEME.primary, borderRadius: 10, paddingVertical: 12, alignItems: 'center', alignSelf: 'flex-start', paddingHorizontal: 14, marginBottom: 10},
  buttonText: {color: '#fff', fontWeight: '700'},
  answerCard: {backgroundColor: THEME.card, borderRadius: 12, padding: 12, marginTop: 10},
  answerTitle: {fontSize: 34, fontWeight: '700', color: THEME.text, marginBottom: 8},
  answerText: {fontSize: 13, color: THEME.text, lineHeight: 20},
  footerTag: {backgroundColor: '#DCFCE7', borderRadius: 8, padding: 10, marginTop: 10},
  footerTagText: {fontSize: 12, color: '#166534', fontWeight: '600'},
});

export default AskQuestionScreen;
