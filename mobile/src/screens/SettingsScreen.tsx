import React from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, Switch, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {useAppSettings} from '../contexts/AppSettingsContext';

const SettingsScreen = () => {
  const {
    language,
    chartStyle,
    ayanamsa,
    notifications,
    darkMode,
    setLanguage,
    setChartStyle,
    setAyanamsa,
    setNotifications,
    setDarkMode,
    saveSettings,
    t,
  } = useAppSettings();

  const LANGUAGES = ['English', 'Hindi', 'Marathi'] as const;
  const CHART_STYLES = ['North', 'South'] as const;
  const AYANAMSAS = ['Lahiri', 'Raman', 'Krishnamurti (KP)', 'Fagan-Bradley', 'True Chitra'];

  const onSave = async () => {
    await saveSettings();
    Alert.alert(t('settings'), t('saved'));
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>⚙️</Text>
        <Text style={styles.title}>{t('settings')}</Text>
        <Text style={styles.subtitle}>Customize your astrology experience</Text>
      </View>

      {/* Language */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🌐 {t('language')}</Text>
        <View style={styles.chipRow}>
          {LANGUAGES.map(lang => (
            <TouchableOpacity key={lang} style={[styles.chip, language === lang && styles.chipActive]} onPress={() => setLanguage(lang)}>
              <Text style={[styles.chipText, language === lang && styles.chipTextActive]}>{lang}</Text>
            </TouchableOpacity>
          ))}
        </View>
      </View>

      {/* Chart Style */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>📐 Chart Style</Text>
        <View style={styles.chipRow}>
          {CHART_STYLES.map(style => (
            <TouchableOpacity key={style} style={[styles.chip, chartStyle === style && styles.chipActive]} onPress={() => setChartStyle(style)}>
              <Text style={[styles.chipText, chartStyle === style && styles.chipTextActive]}>{style} Indian</Text>
            </TouchableOpacity>
          ))}
        </View>
        <Text style={styles.hint}>
          {chartStyle === 'North' ? 'Diamond/rhombus shaped chart (Uttar Shaili)' : 'Square grid chart (Dakshin Shaili)'}
        </Text>
      </View>

      {/* Ayanamsa */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🔭 Ayanamsa System</Text>
        {AYANAMSAS.map(a => (
          <TouchableOpacity key={a} style={[styles.radioRow, ayanamsa === a && styles.radioActive]} onPress={() => setAyanamsa(a)}>
            <View style={[styles.radio, ayanamsa === a && styles.radioFilled]} />
            <Text style={[styles.radioText, ayanamsa === a && styles.radioTextActive]}>{a}</Text>
          </TouchableOpacity>
        ))}
        {ayanamsa === 'Lahiri' && <Text style={styles.hint}>Recommended: Government of India standard (Chitrapaksha)</Text>}
      </View>

      {/* Notifications */}
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>🔔 Preferences</Text>
        <View style={styles.toggleRow}>
          <Text style={styles.toggleLabel}>Daily Horoscope Notifications</Text>
          <Switch value={notifications} onValueChange={setNotifications} trackColor={{true: THEME.primary}} />
        </View>
        <View style={styles.toggleRow}>
          <Text style={styles.toggleLabel}>Dark Mode (Coming Soon)</Text>
          <Switch value={darkMode} onValueChange={setDarkMode} disabled trackColor={{true: THEME.primary}} />
        </View>
      </View>

      <TouchableOpacity style={styles.button} onPress={onSave}>
        <Text style={styles.buttonText}>💾 {t('save_preferences')}</Text>
      </TouchableOpacity>

      <View style={styles.aboutCard}>
        <Text style={styles.aboutTitle}>About KundaliSaga</Text>
        <Text style={styles.aboutText}>Version 1.0.0 • Privacy-First Vedic Astrology{'\n'}All calculations done locally on your device.</Text>
      </View>
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
  section: {backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 16, elevation: 2},
  sectionTitle: {fontSize: 15, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  chipRow: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 8},
  chip: {borderRadius: 20, paddingHorizontal: 16, paddingVertical: 8, borderWidth: 1.5, borderColor: '#E5D5C5'},
  chipActive: {backgroundColor: THEME.primary, borderColor: THEME.primary},
  chipText: {fontSize: 14, color: THEME.text},
  chipTextActive: {color: '#fff', fontWeight: 'bold'},
  hint: {fontSize: 12, color: THEME.textLight, marginTop: 4},
  radioRow: {flexDirection: 'row', alignItems: 'center', padding: 10, borderRadius: 8, marginBottom: 4},
  radioActive: {backgroundColor: '#FFF8F0'},
  radio: {width: 18, height: 18, borderRadius: 9, borderWidth: 2, borderColor: THEME.textLight, marginRight: 12},
  radioFilled: {borderColor: THEME.primary, backgroundColor: THEME.primary},
  radioText: {fontSize: 14, color: THEME.text},
  radioTextActive: {color: THEME.primary, fontWeight: 'bold'},
  toggleRow: {flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingVertical: 8},
  toggleLabel: {fontSize: 14, color: THEME.text},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 20},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  aboutCard: {backgroundColor: '#fff', borderRadius: 12, padding: 16, alignItems: 'center', elevation: 1},
  aboutTitle: {fontSize: 14, fontWeight: 'bold', color: THEME.text, marginBottom: 4},
  aboutText: {fontSize: 12, color: THEME.textLight, textAlign: 'center', lineHeight: 18},
});

export default SettingsScreen;
