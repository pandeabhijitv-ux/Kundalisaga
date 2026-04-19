/**
 * Numerology Screen
 */

import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import {THEME} from '../constants/theme';
import {useAppSettings} from '../contexts/AppSettingsContext';
import {calculateNumerology} from '../services/PythonBridge';
import {getActiveProfile} from '../services/profileData';

const asText = (value: any): string => {
  if (value == null) return '';
  if (Array.isArray(value)) return value.join(', ');
  if (typeof value === 'object') return '';
  return String(value);
};

const NumerologyScreen = () => {
  const {t} = useAppSettings();
  const [name, setName] = useState('User');
  const [dateOfBirth, setDateOfBirth] = useState('1990-01-01');
  const [profileName, setProfileName] = useState('');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);

  React.useEffect(() => {
    const loadActive = async () => {
      try {
        const profile = await getActiveProfile();
        if (profile?.name) {
          setName(profile.name);
          setProfileName(profile.name);
        }
        if (profile?.date) {
          setDateOfBirth(profile.date);
        }
      } catch {
        // Keep defaults if no active profile.
      }
    };
    loadActive();
  }, []);

  const handleCalculate = async () => {
    setLoading(true);
    try {
      const response: any = await calculateNumerology(name, dateOfBirth);
      if (response?.error) {
        Alert.alert(t('numerology_error'), response.error);
      }
      setData(response);
    } catch (error: any) {
      Alert.alert('Error', error?.message || t('failed_calculate_numerology'));
    } finally {
      setLoading(false);
    }
  };

  const interpretation = data?.interpretation && typeof data.interpretation === 'object'
    ? data.interpretation
    : null;

  const traits = Array.isArray(interpretation?.traits)
    ? interpretation.traits
    : [];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{t('numerology_title')}</Text>
      {!!profileName && <Text style={styles.profileNote}>{t('profile_label')}: {profileName}</Text>}

      <View style={styles.card}>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder={t('full_name')} />
        <TextInput
          style={styles.input}
          value={dateOfBirth}
          onChangeText={setDateOfBirth}
          placeholder={t('dob_placeholder')}
        />
        <TouchableOpacity style={styles.button} onPress={handleCalculate} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? t('calculating') : t('calculate_numerology')}</Text>
        </TouchableOpacity>
      </View>

      {data ? (
        <View style={styles.card}>
          <Text style={styles.result}>{t('life_path')}: {data.life_path_number || data.lifePathNumber || '-'}</Text>
          <Text style={styles.result}>{t('destiny')}: {data.destiny_number || data.destinyNumber || '-'}</Text>
          <Text style={styles.result}>{t('soul')}: {data.soul_number || data.soulNumber || '-'}</Text>
          <Text style={styles.result}>{t('personality')}: {data.personality_number || data.personalityNumber || '-'}</Text>
          <Text style={styles.sectionTitle}>{t('numerology_insights')}</Text>
          {!!asText(interpretation?.title) && (
            <Text style={styles.interpretation}><Text style={styles.label}>{t('archetype')}:</Text> {asText(interpretation?.title)}</Text>
          )}
          {!!asText(interpretation?.life_path) && (
            <Text style={styles.interpretation}><Text style={styles.label}>{t('life_path_strengths')}:</Text> {asText(interpretation?.life_path)}</Text>
          )}
          {!!asText(interpretation?.destiny) && (
            <Text style={styles.interpretation}><Text style={styles.label}>{t('destiny_talent')}:</Text> {asText(interpretation?.destiny)}</Text>
          )}
          {traits.length > 0 && (
            <Text style={styles.interpretation}><Text style={styles.label}>{t('core_traits')}:</Text> {traits.join(', ')}</Text>
          )}
          {!!asText(interpretation?.challenges) && (
            <Text style={styles.interpretation}><Text style={styles.label}>{t('growth_areas')}:</Text> {asText(interpretation?.challenges)}</Text>
          )}

          <Text style={styles.sectionTitle}>{t('useful_numbers')}</Text>
          <Text style={styles.interpretation}><Text style={styles.label}>{t('birthday_number')}:</Text> {data.birthday_number ?? '-'}</Text>
          <Text style={styles.interpretation}><Text style={styles.label}>{t('personal_year')}:</Text> {data.personal_year_number ?? '-'}</Text>
          <Text style={styles.interpretation}><Text style={styles.label}>{t('maturity_number')}:</Text> {data.maturity_number ?? '-'}</Text>

          {Array.isArray(data.master_numbers) && data.master_numbers.length > 0 && (
            <Text style={styles.interpretation}><Text style={styles.label}>{t('master_numbers')}:</Text> {data.master_numbers.join(', ')}</Text>
          )}
          {Array.isArray(data.karmic_debts) && data.karmic_debts.length > 0 && (
            <Text style={styles.interpretation}><Text style={styles.label}>{t('karmic_lessons')}:</Text> {data.karmic_debts.join(', ')}</Text>
          )}
        </View>
      ) : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.background,
  },
  content: {
    padding: 16,
    paddingBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 12,
  },
  profileNote: {
    color: THEME.textLight,
    marginBottom: 10,
  },
  card: {
    backgroundColor: THEME.card,
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  input: {
    backgroundColor: '#fff',
    borderColor: '#E0E0E0',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginBottom: 8,
    color: THEME.text,
  },
  button: {
    backgroundColor: THEME.primary,
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  result: {
    color: THEME.text,
    marginBottom: 6,
    fontSize: 16,
    fontWeight: '600',
  },
  sectionTitle: {
    marginTop: 10,
    marginBottom: 6,
    color: THEME.text,
    fontWeight: '700',
    fontSize: 16,
  },
  label: {
    color: THEME.text,
    fontWeight: '700',
  },
  interpretation: {
    color: THEME.textLight,
    lineHeight: 20,
    marginBottom: 6,
  },
});

export default NumerologyScreen;
