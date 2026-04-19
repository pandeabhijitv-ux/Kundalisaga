/**
 * Dasha Screen
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
import {getCurrentDasha} from '../services/PythonBridge';
import {getActiveProfile} from '../services/profileData';

const PLANET_GUIDANCE: Record<string, {happening: string; doNow: string[]; avoid: string[]; remedies: string[]}> = {
  Sun: {
    happening: 'Leadership, visibility and responsibility are emphasized in this period.',
    doNow: ['Take ownership at work', 'Prioritize father/government-related matters', 'Focus on discipline and health routines'],
    avoid: ['Ego conflicts', 'Rushing authority decisions'],
    remedies: ['Offer water to Sun at sunrise', 'Recite Aditya Hridayam on Sundays'],
  },
  Moon: {
    happening: 'Emotions, family comfort and mental peace become the main life themes.',
    doNow: ['Protect sleep and emotional health', 'Spend grounding time with family', 'Take fewer but stable decisions'],
    avoid: ['Mood-driven decisions', 'Overthinking'],
    remedies: ['Chant Om Namah Shivaya on Mondays', 'Donate milk/rice to those in need'],
  },
  Mars: {
    happening: 'Energy, courage, competition and property actions become active.',
    doNow: ['Channel energy into focused goals', 'Exercise daily', 'Handle pending legal/property tasks'],
    avoid: ['Anger reactions', 'Risky driving or impulsive conflict'],
    remedies: ['Recite Hanuman Chalisa on Tuesdays', 'Donate red lentils'],
  },
  Mercury: {
    happening: 'Communication, learning, business and negotiation opportunities rise.',
    doNow: ['Improve skills and certifications', 'Network strategically', 'Audit business/document details'],
    avoid: ['Over-analysis paralysis', 'Loose communication'],
    remedies: ['Worship Ganesha on Wednesdays', 'Donate green items'],
  },
  Jupiter: {
    happening: 'Growth, wisdom, wealth planning and family blessings get highlighted.',
    doNow: ['Plan long-term finances', 'Seek mentors', 'Invest in learning and dharma'],
    avoid: ['Over-commitment', 'Overconfidence with money'],
    remedies: ['Donate yellow items on Thursdays', 'Chant Guru mantra or Vishnu stotra'],
  },
  Venus: {
    happening: 'Relationships, comforts, aesthetics and lifestyle upgrades come into focus.',
    doNow: ['Strengthen partnerships', 'Create financial boundaries around luxury', 'Support creative pursuits'],
    avoid: ['Over-spending', 'Escapist pleasure habits'],
    remedies: ['Offer prayers to Lakshmi on Fridays', 'Donate white sweets/clothes'],
  },
  Saturn: {
    happening: 'Karma, hard work, delays and maturity lessons dominate this period.',
    doNow: ['Follow strict routines', 'Clear long-pending obligations', 'Practice patience with consistency'],
    avoid: ['Taking shortcuts', 'Neglecting health/elder duties'],
    remedies: ['Light sesame oil diya on Saturdays', 'Serve elderly and laborers'],
  },
  Rahu: {
    happening: 'Ambition, sudden changes, foreign/technology themes and unconventional paths intensify.',
    doNow: ['Use innovation wisely', 'Verify facts before major commitments', 'Keep risk limits clear'],
    avoid: ['Speculative obsession', 'Confusing hype with real opportunity'],
    remedies: ['Durga prayers', 'Grounding meditation and charity'],
  },
  Ketu: {
    happening: 'Detachment, inner work, spirituality and karmic closure become strong themes.',
    doNow: ['Simplify priorities', 'Meditate regularly', 'Complete unfinished karmic duties'],
    avoid: ['Isolation from practical life', 'Neglecting material responsibilities'],
    remedies: ['Ganesha/Ketu mantra', 'Feed stray dogs and support spiritual causes'],
  },
};

const DashaScreen = ({navigation}: any) => {
  const {t} = useAppSettings();
  const [dateOfBirth, setDateOfBirth] = useState('1990-01-01');
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any>(null);
  const [profileName, setProfileName] = useState('');

  React.useEffect(() => {
    const prefill = async () => {
      try {
        const profile = await getActiveProfile();
        if (profile?.date) {
          setDateOfBirth(profile.date);
        }
        if (profile?.name) {
          setProfileName(profile.name);
        }
      } catch {
        // Keep manual fallback date.
      }
    };
    prefill();
  }, []);

  const handleFetchDasha = async () => {
    setLoading(true);
    try {
      const active = await getActiveProfile();
      const effectiveDob = active?.date || dateOfBirth;
      if (active?.name) {
        setProfileName(active.name);
      }
      if (active?.date) {
        setDateOfBirth(active.date);
      }

      const response = await getCurrentDasha(effectiveDob);
      if (response?.error) {
        Alert.alert(t('dasha_error'), response.error);
      }
      setData(response);
    } catch (error: any) {
      Alert.alert('Error', error?.message || t('failed_fetch_dasha'));
    } finally {
      setLoading(false);
    }
  };

  const mahaPlanet = data?.mahadasha?.planet || data?.mahadasha_name || '-';
  const antarPlanet = data?.antardasha?.planet || data?.antardasha_name || '-';
  const mahaGuide = PLANET_GUIDANCE[mahaPlanet] || null;
  const antarGuide = PLANET_GUIDANCE[antarPlanet] || null;

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>{t('detailed_dasha_analysis')}</Text>
      {!!profileName && <Text style={styles.profileNote}>{t('profile_label')}: {profileName}</Text>}

      <View style={styles.card}>
        <TextInput
          style={styles.input}
          value={dateOfBirth}
          onChangeText={setDateOfBirth}
          placeholder={t('dob_placeholder')}
        />
        <TouchableOpacity style={styles.button} onPress={handleFetchDasha} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? t('loading') : t('get_current_dasha')}</Text>
        </TouchableOpacity>
      </View>

      {data ? (
        <View style={styles.card}>
          <Text style={styles.sectionTitle}>{t('mahadasha')}</Text>
          <Text style={styles.row}>Planet: {mahaPlanet}</Text>
          <Text style={styles.row}>{t('start')}: {data?.mahadasha?.start_date || '-'}</Text>
          <Text style={styles.row}>{t('end')}: {data?.mahadasha?.end_date || '-'}</Text>
          {!!data?.mahadasha?.duration_years && <Text style={styles.row}>{t('duration')}: {data.mahadasha.duration_years} {t('years')}</Text>}

          <Text style={styles.sectionTitle}>{t('antardasha')}</Text>
          <Text style={styles.row}>Planet: {antarPlanet}</Text>
          <Text style={styles.row}>{t('start')}: {data?.antardasha?.start_date || '-'}</Text>
          <Text style={styles.row}>{t('end')}: {data?.antardasha?.end_date || '-'}</Text>

          <Text style={styles.sectionTitle}>{t('what_happening_now')}</Text>
          <Text style={styles.interpretation}>{mahaGuide?.happening || data?.interpretation || 'No interpretation available.'}</Text>

          {mahaGuide?.doNow?.length ? (
            <>
              <Text style={styles.sectionTitle}>{t('what_should_do')}</Text>
              {mahaGuide.doNow.map((line, idx) => <Text key={`do-${idx}`} style={styles.bullet}>• {line}</Text>)}
            </>
          ) : null}

          {mahaGuide?.avoid?.length ? (
            <>
              <Text style={styles.sectionTitle}>{t('what_to_avoid')}</Text>
              {mahaGuide.avoid.map((line, idx) => <Text key={`avoid-${idx}`} style={styles.bullet}>• {line}</Text>)}
            </>
          ) : null}

          <Text style={styles.sectionTitle}>{t('remedies_period')}</Text>
          {(mahaGuide?.remedies || []).map((line, idx) => <Text key={`rem-${idx}`} style={styles.bullet}>• {line}</Text>)}
          {antarGuide?.remedies?.slice(0, 1).map((line, idx) => (
            <Text key={`antar-rem-${idx}`} style={styles.bullet}>• {t('antardasha_support')}: {line}</Text>
          ))}

          <Text style={styles.tip}>{t('dasha_tip')}</Text>

          <View style={styles.ctaRow}>
            <TouchableOpacity style={styles.cta} onPress={() => navigation.navigate('Remedies')}>
              <Text style={styles.ctaText}>{t('go_to_remedies')}</Text>
            </TouchableOpacity>
            <TouchableOpacity style={styles.cta} onPress={() => navigation.navigate('Gemstone')}>
              <Text style={styles.ctaText}>{t('go_to_gemstone')}</Text>
            </TouchableOpacity>
          </View>
          <TouchableOpacity style={[styles.cta, {marginTop: 8}]} onPress={() => navigation.navigate('Stotras')}>
            <Text style={styles.ctaText}>{t('go_to_stotras')}</Text>
          </TouchableOpacity>
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
  sectionTitle: {
    marginTop: 8,
    marginBottom: 4,
    fontSize: 17,
    fontWeight: '700',
    color: THEME.text,
  },
  row: {
    color: THEME.textLight,
    marginBottom: 4,
  },
  interpretation: {
    color: THEME.textLight,
    lineHeight: 20,
  },
  bullet: {
    color: THEME.textLight,
    lineHeight: 20,
    marginBottom: 3,
  },
  tip: {
    marginTop: 10,
    color: '#1F4E79',
    backgroundColor: '#EEF2F7',
    borderRadius: 8,
    padding: 8,
    lineHeight: 18,
  },
  ctaRow: {
    flexDirection: 'row',
    gap: 8,
    marginTop: 10,
  },
  cta: {
    flex: 1,
    backgroundColor: THEME.primary,
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: 'center',
  },
  ctaText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 12,
  },
});

export default DashaScreen;
