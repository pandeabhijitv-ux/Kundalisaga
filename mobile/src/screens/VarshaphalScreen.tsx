import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert, Platform} from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import {THEME} from '../constants/theme';
import {useAppSettings} from '../contexts/AppSettingsContext';
import {getActiveProfileWithChart} from '../services/profileData';
import {analyzeVarshaphal} from '../services/PythonBridge';

const VarshaphalScreen = () => {
  const {t} = useAppSettings();
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [profileName, setProfileName] = useState('');
  const currentYear = new Date().getFullYear();
  const [selectedYear, setSelectedYear] = useState(currentYear);
  const [pickerDate, setPickerDate] = useState(new Date(currentYear, 0, 1));
  const [showYearPicker, setShowYearPicker] = useState(false);

  const openYearPicker = () => {
    setPickerDate(new Date(selectedYear, 0, 1));
    setShowYearPicker(true);
  };

  const handleYearChange = (event: any, picked?: Date) => {
    setShowYearPicker(false);
    if (event?.type === 'dismissed' || !picked) {
      return;
    }
    const year = picked.getFullYear();
    if (!Number.isFinite(year)) {
      return;
    }
    setPickerDate(new Date(year, 0, 1));
    setSelectedYear(year);
    setResult(null);
  };

  const analyze = async () => {
    setLoading(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      setProfileName(profile.name || t('profile_default'));
      const payload = JSON.stringify({...chart, _target_year: selectedYear});
      const data = await analyzeVarshaphal(payload);
      setResult(data);
    } catch (error: any) {
      Alert.alert(t('varshaphal_alert_title'), error?.message || t('varshaphal_alert_message'));
    } finally {
      setLoading(false);
    }
  };

  const overallRating = Math.max(45, Math.min(88, 60 + (result?.strong_planets?.length || 0) * 4 - (result?.weak_planets?.length || 0) * 2));
  const munthaHouse = ((currentYear + 3) % 12) + 1;
  const focusAreas = Array.isArray(result?.focus_areas)
    ? result.focus_areas
    : [];

  const formatFocusArea = (item: any) => {
    if (typeof item === 'string') return item;
    if (item && typeof item === 'object') {
      return item.prediction || item.theme || `Planet ${item.planet || '-'} in house ${item.house || '-'}`;
    }
    return String(item || '');
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>🗓️</Text>
        <Text style={styles.title}>{t('varshaphal_title')}</Text>
        <Text style={styles.subtitle}>{t('varshaphal_subtitle')}</Text>
      </View>

      <View style={styles.yearRow}>
        <Text style={styles.yearLabel}>Select Year</Text>
        <TouchableOpacity style={styles.yearButton} onPress={openYearPicker}>
          <Text style={styles.yearButtonText}>{selectedYear}</Text>
        </TouchableOpacity>
      </View>

      {showYearPicker ? (
        <DateTimePicker
          value={pickerDate}
          mode="date"
          display={Platform.OS === 'ios' ? 'spinner' : 'default'}
          onChange={handleYearChange}
        />
      ) : null}

      <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>{t('generate_annual_predictions')}</Text>}
      </TouchableOpacity>

      {result && (
        <>
          <View style={styles.card}>
            <Text style={styles.mainHeading}>Varshaphal {result.year || currentYear} - {profileName}</Text>
            <Text style={styles.muntha}>🌟 {t('muntha_position')}: {t('house')} {munthaHouse}</Text>
            <Text style={styles.munthaNote}>{t('muntha_note_prefix')} {result.year || currentYear} {t('muntha_note_suffix')} {munthaHouse}{t('muntha_note_suffix_2')}</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>{t('overall_year_outlook')}</Text>
            <View style={styles.metricRow}>
              <View><Text style={styles.metricLabel}>{t('overall_rating')}</Text><Text style={styles.metricValue}>{overallRating}/100</Text></View>
              <View><Text style={styles.metricLabel}>{t('best_months')}</Text><Text style={styles.metricValue}>Jan-Mar</Text></View>
              <View><Text style={styles.metricLabel}>{t('key_planet')}</Text><Text style={styles.metricValue}>{(result.strong_planets || [])[0] || 'Mercury'}</Text></View>
            </View>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>{t('detailed_annual_forecast')}</Text>
            {focusAreas.slice(0, 5).map((f: any, i: number) => {
              const score = 78 - i * 6;
              const text = formatFocusArea(f);
              return (
                <View key={i} style={styles.forecastBlock}>
                  <Text style={styles.forecastTitle}>{t('area')} {i + 1} • {t('score')}: {score}/100</Text>
                  <View style={styles.bar}><View style={[styles.barFill, {width: `${score}%`}]} /></View>
                  <Text style={styles.forecastPoint}>• {text}</Text>
                </View>
              );
            })}
          </View>

          {(result.challenges || []).length > 0 && (
            <View style={[styles.card, {backgroundColor: '#FFFBEB'}]}>
              <Text style={styles.sectionTitle}>{t('challenges')}</Text>
              {(result.challenges || []).map((c: string, i: number) => <Text key={i} style={styles.challenge}>• {c}</Text>)}
            </View>
          )}

          {(result.remedies || []).length > 0 && (
            <View style={[styles.card, {backgroundColor: '#FCF8E8'}]}>
              <Text style={styles.sectionTitle}>Remedies</Text>
              {(result.remedies || []).map((r: string, i: number) => <Text key={i} style={styles.remedy}>• {r}</Text>)}
            </View>
          )}

          <TouchableOpacity style={[styles.button, {backgroundColor: THEME.textLight, marginTop: 8}]} onPress={() => setResult(null)}>
            <Text style={styles.buttonText}>{t('reanalyze')}</Text>
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
  icon: {fontSize: 42, marginBottom: 8},
  title: {fontSize: 22, fontWeight: '700', color: THEME.text, textAlign: 'center'},
  subtitle: {fontSize: 12, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  yearRow: {flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 10},
  yearLabel: {fontSize: 13, color: THEME.textLight},
  yearButton: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 8, backgroundColor: '#fff'},
  yearButtonText: {fontSize: 14, color: THEME.text, fontWeight: '700'},
  button: {backgroundColor: THEME.primary, borderRadius: 10, padding: 12, alignItems: 'center', marginBottom: 12, alignSelf: 'flex-start'},
  buttonText: {color: '#fff', fontWeight: '700'},
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  mainHeading: {fontSize: 34, fontWeight: '700', color: THEME.text, marginBottom: 8},
  muntha: {fontSize: 26, fontWeight: '700', color: THEME.text, marginBottom: 6},
  munthaNote: {fontSize: 12, color: '#1F4E79', backgroundColor: '#EEF2F7', borderRadius: 8, padding: 8},
  sectionTitle: {fontSize: 30, fontWeight: '700', color: THEME.text, marginBottom: 8},
  metricRow: {flexDirection: 'row', justifyContent: 'space-between'},
  metricLabel: {fontSize: 11, color: THEME.textLight},
  metricValue: {fontSize: 26, fontWeight: '700', color: THEME.text},
  forecastBlock: {marginBottom: 10},
  forecastTitle: {fontSize: 12, color: THEME.text, marginBottom: 4},
  bar: {height: 5, borderRadius: 3, backgroundColor: '#D9E3EF', marginBottom: 6},
  barFill: {height: 5, borderRadius: 3, backgroundColor: '#2D89E5'},
  forecastPoint: {fontSize: 13, color: THEME.text},
  challenge: {fontSize: 13, color: '#92400E', lineHeight: 22},
  remedy: {fontSize: 13, color: THEME.text, lineHeight: 22},
});

export default VarshaphalScreen;
