import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator} from 'react-native';
import {THEME} from '../constants/theme';

const ACTIVITIES = [
  {name: 'Marriage / Vivah', icon: '💍'},
  {name: 'Griha Pravesh (Housewarming)', icon: '🏠'},
  {name: 'Business Inauguration', icon: '🏢'},
  {name: 'Vehicle Purchase', icon: '🚗'},
  {name: 'Travel / Journey', icon: '✈️'},
  {name: 'Medical Procedure', icon: '🏥'},
  {name: 'Education / Vidyarambha', icon: '📚'},
  {name: 'Investment & Finance', icon: '💰'},
];

const MuhuratScreen = () => {
  const [selected, setSelected] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const findMuhurat = () => {
    if (selected === null) return;
    setLoading(true);
    setTimeout(() => {
      setResult({
        activity: ACTIVITIES[selected].name,
        dates: [
          {date: 'May 12, 2026 (Monday)', time: '7:30 AM - 9:00 AM', nakshatra: 'Rohini', quality: '⭐⭐⭐⭐⭐ Excellent'},
          {date: 'May 15, 2026 (Thursday)', time: '10:00 AM - 12:00 PM', nakshatra: 'Punarvasu', quality: '⭐⭐⭐⭐ Very Good'},
          {date: 'May 19, 2026 (Monday)', time: '6:00 AM - 7:30 AM', nakshatra: 'Hasta', quality: '⭐⭐⭐⭐ Very Good'},
        ],
      });
      setLoading(false);
    }, 1500);
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>⏰</Text>
        <Text style={styles.title}>Muhurat Finder</Text>
        <Text style={styles.subtitle}>Find auspicious timing for important life events</Text>
      </View>

      <Text style={styles.sectionTitle}>Select Activity</Text>
      <View style={styles.grid}>
        {ACTIVITIES.map((a, i) => (
          <TouchableOpacity
            key={i}
            style={[styles.activityCard, selected === i && styles.activitySelected]}
            onPress={() => setSelected(i)}>
            <Text style={styles.activityIcon}>{a.icon}</Text>
            <Text style={[styles.activityName, selected === i && styles.activityNameSelected]}>{a.name}</Text>
          </TouchableOpacity>
        ))}
      </View>

      <TouchableOpacity
        style={[styles.button, selected === null && styles.buttonDisabled]}
        onPress={findMuhurat}
        disabled={loading || selected === null}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>🔍 Find Auspicious Time</Text>}
      </TouchableOpacity>

      {result && (
        <View style={styles.resultsCard}>
          <Text style={styles.resultsTitle}>🌟 Muhurat for {result.activity}</Text>
          {result.dates.map((d: any, i: number) => (
            <View key={i} style={styles.muhuratRow}>
              <Text style={styles.muhuratDate}>📅 {d.date}</Text>
              <Text style={styles.muhuratTime}>🕐 {d.time}</Text>
              <Text style={styles.muhuratNakshatra}>⭐ Nakshatra: {d.nakshatra}</Text>
              <Text style={styles.muhuratQuality}>{d.quality}</Text>
            </View>
          ))}
        </View>
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
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  grid: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 20},
  activityCard: {width: '47%', backgroundColor: '#fff', borderRadius: 10, padding: 12, alignItems: 'center', borderWidth: 2, borderColor: '#E0E0E0'},
  activitySelected: {borderColor: THEME.primary, backgroundColor: '#FFF3E0'},
  activityIcon: {fontSize: 26, marginBottom: 6},
  activityName: {fontSize: 12, textAlign: 'center', color: THEME.text, fontWeight: '500'},
  activityNameSelected: {color: THEME.primary, fontWeight: 'bold'},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 20},
  buttonDisabled: {backgroundColor: '#CCC'},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  resultsCard: {backgroundColor: '#fff', borderRadius: 12, padding: 16, elevation: 2},
  resultsTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.primary, marginBottom: 14},
  muhuratRow: {backgroundColor: '#FFF8F0', borderRadius: 10, padding: 12, marginBottom: 10},
  muhuratDate: {fontSize: 14, fontWeight: '600', color: THEME.text, marginBottom: 4},
  muhuratTime: {fontSize: 13, color: THEME.text, marginBottom: 4},
  muhuratNakshatra: {fontSize: 13, color: THEME.text, marginBottom: 4},
  muhuratQuality: {fontSize: 13, color: '#D97706', fontWeight: '600'},
});

export default MuhuratScreen;
