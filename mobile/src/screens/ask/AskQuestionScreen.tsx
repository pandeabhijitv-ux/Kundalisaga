/**
 * Ask Question Screen - Improved with Personalized Chart Analysis
 * Uses specialized chart analysis functions for accurate, personalized answers
 */
import React, {useEffect, useState} from 'react';
import {View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Alert, ActivityIndicator} from 'react-native';
import {THEME} from '../../constants/theme';
import {
  searchKnowledge,
  analyzeCareer,
  analyzeFinancial,
  getGemstoneRecommendations,
  getNameRecommendations,
  getMuhuratAnalysis,
  analyzeVarshaphal,
  analyzeSoulmate,
} from '../../services/PythonBridge';
import {getActiveProfileWithChart, UserProfile} from '../../services/profileData';

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

interface ProfileWithChart {
  profile: UserProfile;
  chart: any;
}

const AskQuestionScreen = ({route}: any) => {
  const preset = route?.params?.preset;
  const [selectedCategory, setSelectedCategory] = useState('career');
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState('');
  const [profileWithChart, setProfileWithChart] = useState<ProfileWithChart | null>(null);

  useEffect(() => {
    loadProfileAndPreset();
  }, [preset]);

  const loadProfileAndPreset = async () => {
    try {
      const data = await getActiveProfileWithChart();
      setProfileWithChart(data);
    } catch (err) {
      console.log('No active profile with chart:', err);
      setProfileWithChart(null);
    }
    const category = preset || 'career';
    setSelectedCategory(category);
    setQuery(PRESET_QUESTIONS[category] || PRESET_QUESTIONS.career);
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      Alert.alert('Validation', 'Please enter a question');
      return;
    }

    if (!profileWithChart?.chart) {
      Alert.alert('No Profile', 'Please create and select a profile first to get personalized answers');
      return;
    }

    setLoading(true);
    try {
      let result = '';
      const chartJson = JSON.stringify(profileWithChart.chart);

      switch (selectedCategory) {
        case 'career':
          const careerAnalysis = await analyzeCareer(chartJson);
          result = typeof careerAnalysis === 'string' ? careerAnalysis : JSON.stringify(careerAnalysis);
          break;

        case 'finance':
          const financialAnalysis = await analyzeFinancial(chartJson);
          result = typeof financialAnalysis === 'string' ? financialAnalysis : JSON.stringify(financialAnalysis);
          break;

        case 'gemstones':
          const gemsResult = await getGemstoneRecommendations(chartJson, query.trim());
          result = typeof gemsResult === 'string' ? gemsResult : JSON.stringify(gemsResult);
          break;

        case 'name':
          const nameResult = await getNameRecommendations(chartJson, 'male');
          result = typeof nameResult === 'string' ? nameResult : JSON.stringify(nameResult);
          break;

        case 'muhurat':
          const eventType = query.toLowerCase().includes('marriage') ? 'marriage' : 'other';
          const muhuratResult = await getMuhuratAnalysis(chartJson, eventType);
          result = typeof muhuratResult === 'string' ? muhuratResult : JSON.stringify(muhuratResult);
          break;

        case 'varshaphal':
          const varshaphalResult = await analyzeVarshaphal(chartJson);
          result = typeof varshaphalResult === 'string' ? varshaphalResult : JSON.stringify(varshaphalResult);
          break;

        case 'matchmaking':
          const soulResult = await analyzeSoulmate(chartJson, 'male');
          result = typeof soulResult === 'string' ? soulResult : JSON.stringify(soulResult);
          break;

        case 'knowledge':
        default:
          const response = await searchKnowledge(query.trim());
          result = response?.results?.[0]?.text || 'No clear answer found. Please refine your question.';
          break;
      }

      setAnswer(result);
    } catch (error: any) {
      console.error('Error:', error);
      Alert.alert('Error', error?.message || 'Failed to analyze your chart. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Profile Context Banner */}
      {profileWithChart ? (
        <View style={styles.profileBanner}>
          <Text style={styles.profileName}>👤 {profileWithChart.profile.name}</Text>
          <Text style={styles.profileDetails}>{profileWithChart.profile.date} • {profileWithChart.profile.location}</Text>
        </View>
      ) : (
        <View style={styles.warningBanner}>
          <Text style={styles.warningText}>⚠️ No profile selected. Create a profile first for personalized answers.</Text>
        </View>
      )}

      <View style={styles.powered}>
        <Text style={styles.poweredText}>💡 Powered by advanced chart analysis - Instant, accurate, personalized answers!</Text>
      </View>

      <Text style={styles.fieldLabel}>Choose a question category:</Text>
      <View style={styles.categoryRow}>
        {Object.keys(CATEGORY_LABELS).map(key => (
          <TouchableOpacity
            key={key}
            style={[styles.categoryChip, selectedCategory === key && styles.categoryChipActive]}
            onPress={() => {
              setSelectedCategory(key);
              setQuery(PRESET_QUESTIONS[key]);
            }}>
            <Text style={[styles.categoryText, selectedCategory === key && styles.categoryTextActive]}>
              {CATEGORY_LABELS[key]}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.fieldLabel}>Question:</Text>
      <TextInput
        style={styles.input}
        value={query}
        onChangeText={setQuery}
        multiline
        placeholder="Ask your question..."
        placeholderTextColor="#999"
      />

      <TouchableOpacity style={[styles.button, loading || !profileWithChart?.chart ? styles.buttonDisabled : {}]} onPress={handleSearch} disabled={loading || !profileWithChart?.chart}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>🔮 Get Personalized Answer</Text>}
      </TouchableOpacity>

      {answer ? (
        <View style={styles.answerCard}>
          <Text style={styles.answerTitle}>📘 Personalized Answer:</Text>
          <Text style={styles.answerText}>{answer}</Text>
          <View style={styles.answerMeta}>
            <Text style={styles.answerMetaText}>
              ✨ Based on {profileWithChart?.profile.name}'s birth chart • Category: {CATEGORY_LABELS[selectedCategory]}
            </Text>
          </View>
        </View>
      ) : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: THEME.background},
  content: {padding: 16, paddingBottom: 24},
  profileBanner: {backgroundColor: '#E8F4F8', borderRadius: 10, padding: 12, marginBottom: 12, borderLeftWidth: 4, borderLeftColor: THEME.primary},
  profileName: {fontSize: 15, fontWeight: '700', color: THEME.text, marginBottom: 4},
  profileDetails: {fontSize: 12, color: THEME.textLight},
  warningBanner: {backgroundColor: '#FEE2E2', borderRadius: 10, padding: 12, marginBottom: 12, borderLeftWidth: 4, borderLeftColor: '#DC2626'},
  warningText: {fontSize: 12, color: '#991B1B', fontWeight: '500'},
  powered: {backgroundColor: '#FEF3C7', borderRadius: 8, padding: 12, marginBottom: 12},
  poweredText: {fontSize: 12, color: '#92400E', fontWeight: '600'},
  fieldLabel: {fontSize: 13, color: THEME.textLight, marginBottom: 8, fontWeight: '600'},
  categoryRow: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 14},
  categoryChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 14, paddingHorizontal: 11, paddingVertical: 7, backgroundColor: '#fff'},
  categoryChipActive: {backgroundColor: THEME.primary},
  categoryText: {fontSize: 12, color: THEME.primary, fontWeight: '500'},
  categoryTextActive: {color: '#fff'},
  input: {backgroundColor: '#fff', borderColor: '#E0E0E0', borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 11, marginBottom: 12, minHeight: 90, textAlignVertical: 'top', color: THEME.text, fontSize: 13},
  button: {backgroundColor: THEME.primary, borderRadius: 10, paddingVertical: 13, paddingHorizontal: 16, alignItems: 'center', alignSelf: 'flex-start', marginBottom: 14},
  buttonDisabled: {opacity: 0.5},
  buttonText: {color: '#fff', fontWeight: '700', fontSize: 14},
  answerCard: {backgroundColor: THEME.card, borderRadius: 12, padding: 14, marginTop: 12, borderLeftWidth: 4, borderLeftColor: THEME.primary},
  answerTitle: {fontSize: 15, fontWeight: '700', color: THEME.text, marginBottom: 10},
  answerText: {fontSize: 13, color: THEME.text, lineHeight: 21, marginBottom: 10},
  answerMeta: {backgroundColor: '#ECFDF5', borderRadius: 8, padding: 10, marginTop: 8},
  answerMetaText: {fontSize: 11, color: '#065F46', fontWeight: '500'},
});

export default AskQuestionScreen;
