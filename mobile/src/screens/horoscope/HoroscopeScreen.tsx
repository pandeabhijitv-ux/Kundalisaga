/**
 * Horoscope Screen
 * Birth chart calculation and North Indian chart rendering (D1 + divisional tabs).
 */
import React, {useEffect, useMemo, useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
  Keyboard,
  ActivityIndicator,
} from 'react-native';
import DateTimePicker from '@react-native-community/datetimepicker';
import {THEME} from '../../constants/theme';
import {calculateChart} from '../../services/PythonBridge';
import {getActiveProfile, saveCachedChart} from '../../services/profileData';
import {LocationOption, searchLocations} from '../../services/locationSearch';
import NorthIndianChart from '../../components/NorthIndianChart';

const DIVISIONS: Array<'D1' | 'D2' | 'D3' | 'D7' | 'D9' | 'D10'> = ['D1', 'D2', 'D3', 'D7', 'D9', 'D10'];

const HoroscopeScreen = ({route}: any) => {
  const preset = route?.params?.preset;
  const [loading, setLoading] = useState(false);
  const [searchingLocation, setSearchingLocation] = useState(false);
  const [name, setName] = useState('User');
  const [birthDate, setBirthDate] = useState(new Date('1990-01-01T00:00:00'));
  const [birthTime, setBirthTime] = useState(new Date('1990-01-01T12:00:00'));
  const [showDatePicker, setShowDatePicker] = useState(false);
  const [showTimePicker, setShowTimePicker] = useState(false);
  const [location, setLocation] = useState('Mumbai');
  const [locationQuery, setLocationQuery] = useState('Mumbai');
  const [locationOptions, setLocationOptions] = useState<LocationOption[]>([]);
  const [latitude, setLatitude] = useState('19.0760');
  const [longitude, setLongitude] = useState('72.8777');
  const [timezone, setTimezone] = useState('Asia/Kolkata');
  const [chart, setChart] = useState<any>(null);
  const [statusMessage, setStatusMessage] = useState('');
  const [selectedDivision, setSelectedDivision] = useState<'D1' | 'D2' | 'D3' | 'D7' | 'D9' | 'D10'>('D1');

  useEffect(() => {
    if (preset === 'compatibility') {
      Alert.alert(
        'Compatibility Mode',
        'Start by calculating the first person chart. You can then compare with another profile from Profiles.'
      );
    }

    const prefillFromActiveProfile = async () => {
      try {
        const active = await getActiveProfile();
        if (!active) return;
        setName(active.name || 'User');
        setLocation(active.location || 'Mumbai');
        setLocationQuery(active.location || 'Mumbai');
        setLatitude(String(active.latitude ?? 19.076));
        setLongitude(String(active.longitude ?? 72.8777));
        setTimezone(active.timezone || 'Asia/Kolkata');

        if (active.date) {
          const d = new Date(`${active.date}T00:00:00`);
          if (!Number.isNaN(d.getTime())) setBirthDate(d);
        }
        if (active.time) {
          const [h, m] = active.time.split(':').map(x => Number(x));
          const t = new Date('1990-01-01T00:00:00');
          t.setHours(Number.isFinite(h) ? h : 12);
          t.setMinutes(Number.isFinite(m) ? m : 0);
          setBirthTime(t);
        }
      } catch (error) {
        console.warn('Unable to prefill active profile', error);
      }
    };

    prefillFromActiveProfile();
  }, [preset]);

  const formatDate = (value: Date) => {
    const y = value.getFullYear();
    const m = `${value.getMonth() + 1}`.padStart(2, '0');
    const d = `${value.getDate()}`.padStart(2, '0');
    return `${y}-${m}-${d}`;
  };

  const formatTime = (value: Date) => {
    const h = `${value.getHours()}`.padStart(2, '0');
    const m = `${value.getMinutes()}`.padStart(2, '0');
    return `${h}:${m}`;
  };

  const handleSearchLocation = async () => {
    const query = locationQuery.trim();
    if (query.length < 3) {
      Alert.alert('Location Search', 'Please enter at least 3 characters.');
      return;
    }

    setSearchingLocation(true);
    setLocationOptions([]);
    try {
      const options = await searchLocations(query);

      setLocationOptions(options);
      setStatusMessage(`Found ${options.length} location options.`);
    } catch (error: any) {
      setStatusMessage('Location search failed. You can still enter coordinates manually.');
      Alert.alert('Search Error', error?.message || 'Unable to search location right now');
    } finally {
      setSearchingLocation(false);
    }
  };

  const selectLocation = (option: LocationOption) => {
    setLocation(option.label);
    setLocationQuery(option.label);
    setLatitude(option.latitude);
    setLongitude(option.longitude);
    setTimezone(option.timezone);
    setLocationOptions([]);
    setStatusMessage('Location selected.');
  };

  const handleCalculate = async () => {
    Keyboard.dismiss();
    const date = formatDate(birthDate);
    const time = formatTime(birthTime);
    const lat = Number(latitude);
    const lon = Number(longitude);

    if (!name.trim()) {
      Alert.alert('Missing Name', 'Please enter name before calculating chart.');
      return;
    }
    if (!date.trim() || !time.trim()) {
      Alert.alert('Missing Birth Details', 'Please enter birth date and birth time.');
      return;
    }
    if (!Number.isFinite(lat) || !Number.isFinite(lon) || lat < -90 || lat > 90 || lon < -180 || lon > 180) {
      Alert.alert('Invalid Coordinates', 'Latitude must be -90..90 and Longitude must be -180..180.');
      return;
    }

    setLoading(true);
    setStatusMessage('Calculating your personalized birth chart...');
    try {
      const result = await Promise.race([
        calculateChart({name, date, time, location, latitude: lat, longitude: lon, timezone}),
        new Promise((_, reject) => setTimeout(() => reject(new Error('Calculation timed out. Please try again.')), 45000)),
      ]);

      if ((result as any)?.error) {
        setStatusMessage('Calculation failed.');
        Alert.alert('Calculation Error', (result as any).error);
        setChart(null);
        return;
      }

      setStatusMessage('Birth chart calculated!');
      setChart(result);
      setSelectedDivision('D1');

      try {
        const active = await getActiveProfile();
        if (active) await saveCachedChart(active.id, result as any);
      } catch (error) {
        console.warn('Failed to cache chart result', error);
      }
    } catch (error: any) {
      setStatusMessage('Calculation failed.');
      Alert.alert('Error', error?.message || 'Failed to calculate chart');
    } finally {
      setLoading(false);
    }
  };

  const planetsMap = useMemo(() => {
    if (!chart) return {} as Record<string, any>;
    if (chart.planets && !Array.isArray(chart.planets)) return chart.planets;
    const list = chart.planets_list || (Array.isArray(chart.planets) ? chart.planets : []);
    const out: Record<string, any> = {};
    list.forEach((p: any) => {
      if (p?.name) out[p.name] = p;
    });
    return out;
  }, [chart]);

  const planetsList = useMemo(() => {
    if (!chart) return [] as any[];
    if (Array.isArray(chart.planets_list)) return chart.planets_list;
    if (Array.isArray(chart.planets)) return chart.planets;
    return Object.values(planetsMap || {}).filter((p: any) => p?.name && p.name !== 'Ascendant');
  }, [chart, planetsMap]);

  const personality = useMemo(() => {
    if (!chart) return {strengths: [] as string[], growth: [] as string[], yogas: [] as string[]};
    const strengths: string[] = [];
    const growth: string[] = [];
    const yogas: string[] = [];

    const sun = planetsMap.Sun;
    const moon = planetsMap.Moon;
    const mercury = planetsMap.Mercury;
    const venus = planetsMap.Venus;
    const mars = planetsMap.Mars;

    if (sun && [1, 9, 10].includes(Number(sun.house))) {
      strengths.push(`Strong leadership qualities and natural confidence (Sun in ${sun.house}th house).`);
    }
    if (venus && [1, 5, 7, 11].includes(Number(venus.house))) {
      strengths.push(`Refined tastes and social grace (Venus in ${venus.house}th house).`);
    }
    if (mars && [3, 6, 11].includes(Number(mars.house))) {
      strengths.push(`Courage and determination to achieve goals (Mars in ${mars.house}th house).`);
    }
    if (!strengths.length) {
      strengths.push('Balanced temperament with potential for steady growth and recognition.');
    }

    if (moon && [8, 12].includes(Number(moon.house))) {
      growth.push(`Tendency to overthink and experience emotional fluctuations (Moon in ${moon.house}th house).`);
    }
    growth.push('Challenges are opportunities for growth. Your journey is uniquely yours.');

    if (sun && mercury && sun.sign === mercury.sign) {
      yogas.push('Budhaditya Yoga (sharp intellect and communication power).');
    }
    if (!yogas.length) {
      yogas.push('No major yoga prominently identified in this quick mobile view.');
    }

    return {strengths, growth, yogas};
  }, [chart, planetsMap]);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>🔮 Horoscope</Text>
      <View style={styles.tipBanner}>
        <Text style={styles.tipText}>💡 Tip: After viewing your chart, visit the Remedies page for personalized solutions.</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.stepTitle}>Select Birth Location</Text>
        <TextInput style={styles.input} value={locationQuery} onChangeText={setLocationQuery} placeholder="Enter city / town / village" />
        <TouchableOpacity style={[styles.secondaryButton, searchingLocation && styles.buttonDisabled]} onPress={handleSearchLocation} disabled={searchingLocation}>
          {searchingLocation ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Search Location</Text>}
        </TouchableOpacity>

        {locationOptions.length > 0 ? (
          <View style={styles.locationList}>
            {locationOptions.map((option, index) => (
              <TouchableOpacity key={`${option.label}-${index}`} style={styles.locationItem} onPress={() => selectLocation(option)}>
                <Text style={styles.locationTitle}>{option.label}</Text>
                <Text style={styles.locationMeta}>{Number(option.latitude).toFixed(4)}°, {Number(option.longitude).toFixed(4)}°</Text>
              </TouchableOpacity>
            ))}
          </View>
        ) : null}

        <Text style={styles.stepTitle}>Birth Details</Text>
        <TextInput style={styles.input} value={name} onChangeText={setName} placeholder="Name" />

        <TouchableOpacity style={styles.inputButton} onPress={() => setShowDatePicker(true)}>
          <Text style={styles.inputButtonText}>{formatDate(birthDate)}</Text>
        </TouchableOpacity>
        <TouchableOpacity style={styles.inputButton} onPress={() => setShowTimePicker(true)}>
          <Text style={styles.inputButtonText}>{formatTime(birthTime)}</Text>
        </TouchableOpacity>

        {showDatePicker ? (
          <DateTimePicker
            value={birthDate}
            mode="date"
            maximumDate={new Date()}
            minimumDate={new Date('1800-01-01T00:00:00')}
            onChange={(_, selectedDate) => {
              setShowDatePicker(false);
              if (selectedDate) setBirthDate(selectedDate);
            }}
          />
        ) : null}

        {showTimePicker ? (
          <DateTimePicker
            value={birthTime}
            mode="time"
            is24Hour
            onChange={(_, selectedTime) => {
              setShowTimePicker(false);
              if (selectedTime) setBirthTime(selectedTime);
            }}
          />
        ) : null}

        <TextInput style={styles.input} value={location} onChangeText={setLocation} placeholder="Location" />
        <TextInput style={styles.input} value={latitude} onChangeText={setLatitude} placeholder="Latitude" keyboardType="decimal-pad" />
        <TextInput style={styles.input} value={longitude} onChangeText={setLongitude} placeholder="Longitude" keyboardType="decimal-pad" />
        <TextInput style={styles.input} value={timezone} onChangeText={setTimezone} placeholder="Timezone" />

        <TouchableOpacity style={[styles.button, loading && styles.buttonDisabled]} onPress={handleCalculate} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? 'Calculating...' : 'Create Birth Chart'}</Text>
        </TouchableOpacity>

        {statusMessage ? <Text style={styles.statusText}>{statusMessage}</Text> : null}
      </View>

      {chart ? (
        <>
          <View style={styles.okBanner}><Text style={styles.okText}>✅ Birth chart calculated!</Text></View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>✨ Your Personality Insights</Text>
            <Text style={styles.subheading}>🌟 Your Strengths:</Text>
            {personality.strengths.map((s, i) => <Text key={`s-${i}`} style={styles.bullet}>• {s}</Text>)}
            <Text style={[styles.subheading, {marginTop: 12}]}>🎯 Areas for Growth:</Text>
            {personality.growth.map((g, i) => <Text key={`g-${i}`} style={styles.bullet}>• {g}</Text>)}
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>🧘 Special Yogas in Your Chart</Text>
            {personality.yogas.map((y, i) => <Text key={`y-${i}`} style={styles.yogaLine}>• {y}</Text>)}
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>📊 Birth Chart (Rashi Chakra)</Text>
            <NorthIndianChart chart={chart} division="D1" />
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Ascendant</Text>
            <Text style={styles.bullet}>{chart?.ascendant?.sign || '-'} - {(chart?.ascendant?.degree || 0).toFixed ? chart.ascendant.degree.toFixed(2) : chart?.ascendant?.degree}</Text>
            <Text style={styles.bullet}>Nakshatra: {chart?.ascendant?.nakshatra || 'Unknown'} (Pada {chart?.ascendant?.nakshatra_pada || 1})</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>Planetary Positions</Text>
            <View style={styles.tableHeader}>
              <Text style={[styles.th, {flex: 1.2}]}>Planet</Text>
              <Text style={styles.th}>Sign</Text>
              <Text style={styles.th}>Degree</Text>
              <Text style={styles.th}>House</Text>
              <Text style={[styles.th, {flex: 1.4}]}>Nakshatra</Text>
            </View>
            {planetsList.map((p: any, i: number) => (
              <View key={`${p.name}-${i}`} style={styles.tr}>
                <Text style={[styles.td, {flex: 1.2}]}>{p.name}</Text>
                <Text style={styles.td}>{p.sign}</Text>
                <Text style={styles.td}>{Number(p.degree || 0).toFixed(2)}°</Text>
                <Text style={styles.td}>{p.house || '-'}</Text>
                <Text style={[styles.td, {flex: 1.4}]}>{p.nakshatra || '-'}</Text>
              </View>
            ))}
          </View>

          <View style={styles.card}>
            <Text style={styles.sectionTitle}>📉 Divisional Charts (Vargas)</Text>
            <View style={styles.divisionTabs}>
              {DIVISIONS.map(div => (
                <TouchableOpacity key={div} style={[styles.divChip, selectedDivision === div && styles.divChipActive]} onPress={() => setSelectedDivision(div)}>
                  <Text style={[styles.divChipText, selectedDivision === div && styles.divChipTextActive]}>{div}</Text>
                </TouchableOpacity>
              ))}
            </View>
            <NorthIndianChart chart={chart} division={selectedDivision} />
          </View>
        </>
      ) : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: THEME.background},
  content: {padding: 16, paddingBottom: 24},
  title: {fontSize: 34, fontWeight: '700', color: THEME.text, marginBottom: 10},
  tipBanner: {backgroundColor: '#EEF2F7', borderRadius: 8, padding: 10, marginBottom: 10},
  tipText: {fontSize: 12, color: '#1F4E79', fontWeight: '600'},
  okBanner: {backgroundColor: '#DCFCE7', borderRadius: 8, padding: 10, marginBottom: 10},
  okText: {fontSize: 12, color: '#166534', fontWeight: '600'},
  card: {backgroundColor: THEME.card, borderRadius: 12, padding: 12, marginBottom: 12},
  stepTitle: {fontSize: 14, fontWeight: '700', color: THEME.text, marginBottom: 8, marginTop: 4},
  input: {backgroundColor: '#fff', borderColor: '#E0E0E0', borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 10, marginBottom: 8, color: THEME.text},
  inputButton: {backgroundColor: '#fff', borderColor: '#E0E0E0', borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 12, marginBottom: 8},
  inputButtonText: {color: THEME.text},
  button: {backgroundColor: THEME.primary, borderRadius: 10, paddingVertical: 12, alignItems: 'center', marginTop: 4},
  secondaryButton: {backgroundColor: '#CC5B2A', borderRadius: 10, paddingVertical: 12, alignItems: 'center', marginBottom: 8},
  buttonText: {color: '#fff', fontWeight: '700'},
  buttonDisabled: {opacity: 0.7},
  statusText: {marginTop: 10, color: THEME.textLight, textAlign: 'center'},
  locationList: {marginBottom: 8},
  locationItem: {borderWidth: 1, borderColor: '#E0E0E0', backgroundColor: '#fff', borderRadius: 10, padding: 10, marginBottom: 6},
  locationTitle: {color: THEME.text, fontWeight: '600'},
  locationMeta: {color: THEME.textLight, marginTop: 2, fontSize: 12},
  sectionTitle: {fontSize: 32, fontWeight: '700', color: THEME.text, marginBottom: 8},
  subheading: {fontSize: 14, fontWeight: '700', color: THEME.text, marginBottom: 6},
  bullet: {color: THEME.textLight, marginBottom: 5, lineHeight: 20},
  yogaLine: {color: '#1F4E79', backgroundColor: '#EEF2F7', borderRadius: 8, padding: 8, marginBottom: 6, fontWeight: '600'},
  tableHeader: {flexDirection: 'row', borderBottomWidth: 1, borderBottomColor: '#D9D9D9', paddingBottom: 6, marginBottom: 4},
  th: {flex: 1, fontSize: 11, fontWeight: '700', color: '#5A5A5A'},
  tr: {flexDirection: 'row', borderBottomWidth: 1, borderBottomColor: '#EFEFEF', paddingVertical: 6},
  td: {flex: 1, fontSize: 12, color: THEME.text},
  divisionTabs: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 10},
  divChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 14, paddingHorizontal: 10, paddingVertical: 6},
  divChipActive: {backgroundColor: THEME.primary},
  divChipText: {fontSize: 12, color: THEME.primary, fontWeight: '600'},
  divChipTextActive: {color: '#fff'},
});

export default HoroscopeScreen;
