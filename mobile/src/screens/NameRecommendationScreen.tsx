import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {getNameRecommendations} from '../services/PythonBridge';

const NameRecommendationScreen = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [gender, setGender] = useState<'male' | 'female'>('male');
  const [purpose, setPurpose] = useState<'baby' | 'business' | 'personal'>('baby');
  const [profileName, setProfileName] = useState('');

  const analyze = async () => {
    setLoading(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      setProfileName(profile.name || 'Profile');
      const data = await getNameRecommendations(JSON.stringify(chart), gender);
      setResult(data);
    } catch (error: any) {
      Alert.alert('Name Recommendations', error?.message || 'Unable to analyze. Please ensure an active profile exists.');
    } finally {
      setLoading(false);
    }
  };

  const getNameText = (n: any) => (typeof n === 'string' ? n : n?.name || '-');
  const getMeaningText = (n: any) => (typeof n === 'string' ? 'Auspicious Vedic name based on nakshatra' : n?.meaning || 'Auspicious Vedic name');

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>✍️</Text>
        <Text style={styles.title}>Name Recommendation</Text>
        <Text style={styles.subtitle}>Basis of Nakshatra</Text>
      </View>

      <View style={styles.purposeRow}>
        <TouchableOpacity style={[styles.purposeChip, purpose === 'baby' && styles.purposeChipActive]} onPress={() => setPurpose('baby')}>
          <Text style={[styles.purposeLabel, purpose === 'baby' && styles.purposeLabelActive]}>Baby Name</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.purposeChip, purpose === 'business' && styles.purposeChipActive]} onPress={() => setPurpose('business')}>
          <Text style={[styles.purposeLabel, purpose === 'business' && styles.purposeLabelActive]}>Business Name</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.purposeChip, purpose === 'personal' && styles.purposeChipActive]} onPress={() => setPurpose('personal')}>
          <Text style={[styles.purposeLabel, purpose === 'personal' && styles.purposeLabelActive]}>Personal Rename</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.genderRow}>
        <TouchableOpacity style={[styles.genderChip, gender === 'male' && styles.genderActive]} onPress={() => {setGender('male'); setResult(null);}}>
          <Text style={[styles.genderLabel, gender === 'male' && styles.genderLabelActive]}>Male</Text>
        </TouchableOpacity>
        <TouchableOpacity style={[styles.genderChip, gender === 'female' && styles.genderActive]} onPress={() => {setGender('female'); setResult(null);}}>
          <Text style={[styles.genderLabel, gender === 'female' && styles.genderLabelActive]}>Female</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Generate Name Recommendations</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Name Recommendations for {profileName}</Text>
            <Text style={styles.detailRow}><Text style={styles.label}>Birth Nakshatra:</Text> {result.moon_nakshatra}</Text>
            <Text style={styles.detailRow}><Text style={styles.label}>Purpose:</Text> {purpose === 'baby' ? 'Baby Name' : purpose === 'business' ? 'Business Name' : 'Personal Rename'}</Text>
            <Text style={styles.detailRow}><Text style={styles.label}>Gender:</Text> {gender === 'male' ? 'Male' : 'Female'}</Text>
            <Text style={styles.detailRow}><Text style={styles.label}>Lucky Syllables:</Text> {(result.traditional_syllables || []).join(', ')}</Text>
          </View>

          {(result.name_suggestions || []).length > 0 && (
            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Recommended Names</Text>
              {(result.name_suggestions || []).slice(0, 5).map((n: any, i: number) => (
                <View key={i} style={styles.nameRow}>
                  <Text style={styles.nameText}>{i + 1}. {getNameText(n)}</Text>
                  <Text style={styles.nameMeaning}>Meaning: {getMeaningText(n)}</Text>
                  <Text style={styles.nameNote}>Syllable: {result.traditional_syllables?.[Math.min(i, (result.traditional_syllables?.length || 1) - 1)] || '-'}</Text>
                </View>
              ))}
            </View>
          )}

          {(result.additional_names || []).length > 0 && (
            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Additional Options</Text>
              <Text style={styles.chips}>{result.additional_names.join('  •  ')}</Text>
            </View>
          )}

          {(result.naming_guidance || []).length > 0 && (
            <View style={[styles.card, {backgroundColor: '#FCF8E8'}]}>
              <Text style={styles.sectionTitle}>Naming Guidance</Text>
              {result.naming_guidance.map((g: string, i: number) => (
                <Text key={i} style={styles.tip}>• {g}</Text>
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
  purposeRow: {flexDirection: 'row', gap: 8, marginBottom: 12, justifyContent: 'center', flexWrap: 'wrap'},
  purposeChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 20, paddingHorizontal: 12, paddingVertical: 6},
  purposeChipActive: {backgroundColor: THEME.primary},
  purposeLabel: {fontSize: 12, color: THEME.primary},
  purposeLabelActive: {color: '#fff'},
  genderRow: {flexDirection: 'row', gap: 12, marginBottom: 16, justifyContent: 'center'},
  genderChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 20, paddingHorizontal: 20, paddingVertical: 8},
  genderActive: {backgroundColor: THEME.primary},
  genderLabel: {fontSize: 14, color: THEME.primary, fontWeight: '600'},
  genderLabelActive: {color: '#fff'},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 16},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  sectionTitle: {fontSize: 15, fontWeight: 'bold', color: THEME.text, marginBottom: 8},
  detailRow: {fontSize: 13, color: THEME.text, lineHeight: 22},
  label: {fontWeight: '700', color: THEME.primary},
  nameRow: {marginBottom: 10, paddingBottom: 10, borderBottomWidth: 1, borderBottomColor: '#F3F4F6'},
  nameText: {fontSize: 18, fontWeight: 'bold', color: THEME.primary},
  nameMeaning: {fontSize: 13, color: THEME.text, marginTop: 2},
  nameNote: {fontSize: 12, color: THEME.textLight, fontStyle: 'italic', marginTop: 2},
  chips: {fontSize: 13, color: THEME.text, lineHeight: 22},
  tip: {fontSize: 13, color: THEME.text, lineHeight: 22},
});

export default NameRecommendationScreen;
