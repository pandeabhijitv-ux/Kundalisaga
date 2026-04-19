import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {getGemstoneRecommendations} from '../services/PythonBridge';

const CONCERNS = [
  {key: 'general', label: 'General Life Analysis'},
  {key: 'career', label: 'Career & Profession'},
  {key: 'finance', label: 'Wealth & Finance'},
  {key: 'health', label: 'Health & Vitality'},
  {key: 'relationship', label: 'Love & Marriage'},
];

const GemstoneScreen = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [expanded, setExpanded] = useState<number | null>(null);
  const [concern, setConcern] = useState('general');
  const [profileName, setProfileName] = useState('');

  const analyze = async () => {
    setLoading(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      setProfileName(profile.name || 'Profile');
      const data = await getGemstoneRecommendations(JSON.stringify(chart), concern);
      setResult(data);
    } catch (error: any) {
      Alert.alert('Gemstone Analysis', error?.message || 'Unable to analyze. Please ensure an active profile exists.');
    } finally {
      setLoading(false);
    }
  };

  const allRecs = result ? [
    ...(result.primary_recommendations || []).map((r: any) => ({...r, tier: 'Primary'})),
    ...(result.secondary_recommendations || []).map((r: any) => ({...r, tier: 'Secondary'})),
    ...(result.supporting_recommendations || []).map((r: any) => ({...r, tier: 'Supporting'})),
  ] : [];

  const relevantPlanets = Array.from(new Set(allRecs.map((r: any) => r.planet).filter(Boolean)));

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💎</Text>
        <Text style={styles.title}>Gemstone Guide</Text>
        <Text style={styles.subtitle}>Get personalized gemstone recommendations based on your birth chart</Text>
      </View>

      <Text style={styles.fieldLabel}>Select your primary concern</Text>
      <View style={styles.concernRow}>
        {CONCERNS.map(c => (
          <TouchableOpacity key={c.key} style={[styles.concernChip, concern === c.key && styles.concernChipActive]} onPress={() => {setConcern(c.key); setResult(null);}}>
            <Text style={[styles.concernText, concern === c.key && styles.concernTextActive]}>{c.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Get Gemstone Recommendations</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.okBanner}><Text style={styles.okText}>✅ Analysis complete for {profileName}</Text></View>

          <View style={styles.metaCard}>
            <Text style={styles.metaLine}>Concern Category: {CONCERNS.find(c => c.key === concern)?.label}</Text>
            <Text style={styles.metaLine}>Relevant Planets: {relevantPlanets.length ? relevantPlanets.join(', ') : 'None identified'}</Text>
            <Text style={styles.metaLine}>Charts Analyzed: D1 (Rashi/Life)</Text>
          </View>

          {allRecs.length === 0 ? (
            <View style={styles.infoCard}><Text style={styles.infoText}>✅ No high-priority gemstones needed - your chart looks strong!</Text></View>
          ) : (
            allRecs.map((rec: any, i: number) => (
              <TouchableOpacity key={i} style={styles.gemCard} onPress={() => setExpanded(expanded === i ? null : i)}>
                <Text style={styles.gemName}>{rec.tier}: {rec.primary}</Text>
                <Text style={styles.planetName}>Planet: {rec.planet}  •  Priority: {rec.priority}</Text>
                <Text style={styles.benefits}>✨ {rec.benefits}</Text>
                {expanded === i && (
                  <View style={styles.details}>
                    {!!rec.alternative && <Text style={styles.detailRow}>Alternative: {rec.alternative}</Text>}
                    <Text style={styles.detailRow}>Weight: {rec.weight || '-'}</Text>
                    <Text style={styles.detailRow}>Metal: {rec.metal || '-'}</Text>
                    <Text style={styles.detailRow}>Finger: {rec.finger || '-'}</Text>
                    <Text style={styles.detailRow}>Day: {rec.day || '-'}</Text>
                    {!!rec.reason && <Text style={styles.detailNote}>{rec.reason}</Text>}
                  </View>
                )}
              </TouchableOpacity>
            ))
          )}

          {(result.general_guidelines || []).length > 0 && (
            <View style={styles.guidelinesCard}>
              <Text style={styles.sectionTitle}>Essential Gemstone Wearing Guidelines</Text>
              {result.general_guidelines.map((g: string, i: number) => <Text key={i} style={styles.guideline}>• {g}</Text>)}
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
  header: {alignItems: 'center', paddingVertical: 20, marginBottom: 8},
  icon: {fontSize: 44, marginBottom: 8},
  title: {fontSize: 22, fontWeight: 'bold', color: THEME.primary, textAlign: 'center'},
  subtitle: {fontSize: 13, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  fieldLabel: {fontSize: 13, color: THEME.textLight, marginBottom: 6},
  concernRow: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 14},
  concernChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 16, paddingHorizontal: 10, paddingVertical: 6},
  concernChipActive: {backgroundColor: THEME.primary},
  concernText: {fontSize: 12, color: THEME.primary},
  concernTextActive: {color: '#fff'},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginVertical: 10},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 14},
  okBanner: {backgroundColor: '#DCFCE7', borderRadius: 8, padding: 10, marginBottom: 10},
  okText: {fontSize: 12, color: '#166534', fontWeight: '600'},
  metaCard: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  metaLine: {fontSize: 13, color: THEME.text, lineHeight: 22},
  infoCard: {backgroundColor: '#E0F2FE', borderRadius: 10, padding: 12, marginBottom: 16},
  infoText: {fontSize: 13, color: '#0369A1', lineHeight: 18, fontWeight: '600'},
  gemCard: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  gemName: {fontSize: 16, fontWeight: 'bold', color: THEME.text},
  planetName: {fontSize: 12, color: THEME.textLight, marginTop: 2},
  benefits: {fontSize: 13, color: THEME.text, lineHeight: 18, marginTop: 6},
  details: {marginTop: 10, paddingTop: 10, borderTopWidth: 1, borderTopColor: 'rgba(0,0,0,0.1)'},
  detailRow: {fontSize: 13, color: THEME.text, marginBottom: 4},
  detailNote: {fontSize: 12, color: '#374151', fontStyle: 'italic', marginTop: 4},
  guidelinesCard: {backgroundColor: '#fff', borderRadius: 12, padding: 14, elevation: 2, marginBottom: 10},
  sectionTitle: {fontSize: 18, fontWeight: 'bold', color: THEME.text, marginBottom: 8},
  guideline: {fontSize: 13, color: THEME.text, lineHeight: 22},
});

export default GemstoneScreen;
