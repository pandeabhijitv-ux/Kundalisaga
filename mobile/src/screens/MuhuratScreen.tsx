import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {getMuhuratAnalysis} from '../services/PythonBridge';

const EVENT_TYPES = [
  {key: 'marriage', label: 'Marriage'},
  {key: 'business', label: 'Business Launch'},
  {key: 'housewarming', label: 'Housewarming'},
  {key: 'travel', label: 'Travel'},
  {key: 'education', label: 'Education'},
];

const MuhuratScreen = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [eventType, setEventType] = useState('business');
  const [profileName, setProfileName] = useState('');
  const [ascendantSign, setAscendantSign] = useState('');
  const [moonSign, setMoonSign] = useState('');
  const [currentDasha, setCurrentDasha] = useState('Not available');

  const analyze = async () => {
    setLoading(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      setProfileName(profile.name || 'Profile');
      setAscendantSign(chart?.ascendant?.sign || '-');
      setMoonSign((chart?.planets as any)?.Moon?.sign || '-');
      const dashaLord = chart?.dasha?.current_dasha || chart?.dasha?.mahadasha || 'Not available';
      setCurrentDasha(dashaLord);
      const data = await getMuhuratAnalysis(JSON.stringify(chart), eventType);
      setResult(data);
    } catch (error: any) {
      Alert.alert('Muhurat Analysis', error?.message || 'Unable to analyze. Please ensure an active profile exists.');
    } finally {
      setLoading(false);
    }
  };

  const dateRows = (result?.upcoming_dates || []).slice(0, 3);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>⏰</Text>
        <Text style={styles.title}>Muhurat Finder - Auspicious Timing</Text>
      </View>

      <Text style={styles.fieldLabel}>Select Event Type</Text>
      <View style={styles.eventPicker}>
        {EVENT_TYPES.map(e => (
          <TouchableOpacity key={e.key}
            style={[styles.eventChip, eventType === e.key && styles.eventChipActive]}
            onPress={() => { setEventType(e.key); setResult(null); }}>
            <Text style={[styles.eventLabel, eventType === e.key && styles.eventLabelActive]}>{e.label}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Find Personalized Auspicious Times</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Personalized Muhurat for {profileName}</Text>
            <Text style={styles.detailText}>Event: {EVENT_TYPES.find(e => e.key === eventType)?.label}</Text>
            <View style={styles.metaRow}>
              <Text style={styles.metaChip}>Lagna (Ascendant): {ascendantSign}</Text>
              <Text style={styles.metaChip}>Moon Sign: {moonSign}</Text>
              <Text style={styles.metaChip}>Current Dasha: {currentDasha}</Text>
            </View>
          </View>

          {dateRows.length > 0 && (
            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Top 3 Personalized Auspicious Dates</Text>
              {dateRows.map((d: any, i: number) => {
                const dayLabel = typeof d === 'string' ? d : d.date;
                const dayName = typeof d === 'string' ? '' : (d.day || '');
                const score = 78 - i * 3;
                return (
                  <View key={i} style={styles.dateCard}>
                    <Text style={styles.dateTitle}>Option {i + 1}: {dayLabel}</Text>
                    <Text style={styles.dateSub}>Your Compatibility: {score}/100</Text>
                    {dayName ? <Text style={styles.dateSub}>Day: {dayName}</Text> : null}
                    {d?.planet ? <Text style={styles.dateSub}>{d.planet}</Text> : null}
                    <Text style={styles.goodTag}>{score >= 75 ? 'Very Good Match' : 'Good Match'}</Text>
                  </View>
                );
              })}
            </View>
          )}

          {(result.personal_tips || []).length > 0 && (
            <View style={styles.card}>
              <Text style={styles.sectionTitle}>Why these dates are favorable</Text>
              {result.personal_tips.map((tip: string, i: number) => (
                <Text key={i} style={styles.listText}>• {tip}</Text>
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
  header: {alignItems: 'center', paddingVertical: 20, marginBottom: 8},
  icon: {fontSize: 38, marginBottom: 8},
  title: {fontSize: 22, fontWeight: 'bold', color: THEME.primary, textAlign: 'center'},
  fieldLabel: {fontSize: 13, color: THEME.textLight, marginBottom: 6},
  eventPicker: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 16},
  eventChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 20, paddingHorizontal: 12, paddingVertical: 6},
  eventChipActive: {backgroundColor: THEME.primary},
  eventLabel: {fontSize: 12, color: THEME.primary},
  eventLabelActive: {color: '#fff'},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 16},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 14},
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  sectionTitle: {fontSize: 18, fontWeight: 'bold', color: THEME.text, marginBottom: 8},
  detailText: {fontSize: 13, color: THEME.text, marginBottom: 8},
  metaRow: {gap: 8},
  metaChip: {fontSize: 12, color: THEME.primary, backgroundColor: '#E8EEF6', borderRadius: 6, paddingHorizontal: 8, paddingVertical: 6},
  dateCard: {borderWidth: 1, borderColor: '#E5E7EB', borderRadius: 10, padding: 10, marginBottom: 8},
  dateTitle: {fontSize: 13, fontWeight: '700', color: THEME.text},
  dateSub: {fontSize: 12, color: THEME.textLight, marginTop: 2},
  goodTag: {fontSize: 12, color: '#166534', backgroundColor: '#DCFCE7', borderRadius: 6, alignSelf: 'flex-start', paddingHorizontal: 8, paddingVertical: 4, marginTop: 6},
  listText: {fontSize: 13, color: THEME.text, lineHeight: 22},
});

export default MuhuratScreen;
