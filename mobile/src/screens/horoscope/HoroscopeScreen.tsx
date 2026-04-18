/**
 * Horoscope Screen
 * Birth chart calculation using Python bridge.
 */
import React, {useEffect, useState} from 'react';
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

type LocationOption = {
  label: string;
  latitude: string;
  longitude: string;
  timezone: string;
};

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

  useEffect(() => {
    if (preset === 'compatibility') {
      Alert.alert(
        'Compatibility Mode',
        'Start by calculating the first person chart. You can then compare with another profile from Profiles.'
      );
    }
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

  const buildPlaceLabel = (item: any) => {
    const address = item?.address || {};
    const locality =
      address.city ||
      address.town ||
      address.village ||
      address.hamlet ||
      address.suburb ||
      address.municipality;
    const subdistrict = address.subdistrict || address.county;
    const district = address.state_district || address.district;
    const state = address.state;
    const country = address.country;
    const parts = [locality, subdistrict, district, state, country].filter(Boolean);
    const deduped = Array.from(new Set(parts.map((p: string) => p.trim())));
    return deduped.length > 0 ? deduped.join(', ') : item.display_name || 'Unknown';
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
      const url = `https://nominatim.openstreetmap.org/search?format=jsonv2&addressdetails=1&limit=5&countrycodes=in&q=${encodeURIComponent(
        query,
      )}`;

      const res = await fetch(url, {
        headers: {
          Accept: 'application/json',
        },
      });

      if (!res.ok) {
        throw new Error('Location service not reachable');
      }

      const data = await res.json();
      if (!Array.isArray(data) || data.length === 0) {
        setStatusMessage('No matching location found. Try city + district.');
        return;
      }

      const options: LocationOption[] = data.map((item: any) => ({
        label: buildPlaceLabel(item),
        latitude: String(item.lat),
        longitude: String(item.lon),
        timezone: 'Asia/Kolkata',
      }));

      setLocationOptions(options);
      setStatusMessage(`Found ${options.length} location options.`);
    } catch (error: any) {
      setStatusMessage('Location search failed.');
      Alert.alert('Search Error', error?.message || 'Unable to search location');
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
    if (!Number.isFinite(lat) || !Number.isFinite(lon)) {
      Alert.alert('Invalid Coordinates', 'Latitude and Longitude must be valid numbers.');
      return;
    }

    if (lat < -90 || lat > 90 || lon < -180 || lon > 180) {
      Alert.alert('Invalid Coordinates', 'Latitude must be between -90 and 90, and Longitude between -180 and 180.');
      return;
    }

    setLoading(true);
    setStatusMessage('Calculating chart, please wait...');
    try {
      const result = await Promise.race([
        calculateChart({
        name,
        date,
        time,
        location,
        latitude: lat,
        longitude: lon,
        timezone,
      }),
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Calculation timed out. Please try again.')), 45000),
        ),
      ]);

      if (result?.error) {
        setStatusMessage('Calculation failed.');
        Alert.alert('Calculation Error', result.error);
        setChart(null);
        return;
      }

      setStatusMessage('Chart calculated successfully.');
      setChart(result);
    } catch (error: any) {
      setStatusMessage('Calculation failed.');
      Alert.alert('Error', error?.message || 'Failed to calculate chart');
    } finally {
      setLoading(false);
    }
  };

  const chartPlanets = Array.isArray(chart?.planets)
    ? chart.planets
    : Object.values(chart?.planets || {});

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Birth Chart Calculator</Text>

      <View style={styles.card}>
        <Text style={styles.stepTitle}>Step 1: Search Birth Location</Text>
        <TextInput
          style={styles.input}
          value={locationQuery}
          onChangeText={setLocationQuery}
          placeholder="Enter city / town / village"
        />
        <TouchableOpacity
          style={[styles.secondaryButton, searchingLocation && styles.buttonDisabled]}
          onPress={handleSearchLocation}
          disabled={searchingLocation}>
          {searchingLocation ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.buttonText}>Search Location</Text>
          )}
        </TouchableOpacity>

        {locationOptions.length > 0 ? (
          <View style={styles.locationList}>
            {locationOptions.map((option, index) => (
              <TouchableOpacity
                key={`${option.label}-${index}`}
                style={styles.locationItem}
                onPress={() => selectLocation(option)}>
                <Text style={styles.locationTitle}>{option.label}</Text>
                <Text style={styles.locationMeta}>
                  {Number(option.latitude).toFixed(4)}°, {Number(option.longitude).toFixed(4)}°
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        ) : null}

        <Text style={styles.stepTitle}>Step 2: Birth Details</Text>
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
              if (selectedDate) {
                setBirthDate(selectedDate);
              }
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
              if (selectedTime) {
                setBirthTime(selectedTime);
              }
            }}
          />
        ) : null}

        <TextInput style={styles.input} value={location} onChangeText={setLocation} placeholder="Location" />
        <TextInput style={styles.input} value={latitude} onChangeText={setLatitude} placeholder="Latitude" keyboardType="decimal-pad" />
        <TextInput style={styles.input} value={longitude} onChangeText={setLongitude} placeholder="Longitude" keyboardType="decimal-pad" />
        <TextInput style={styles.input} value={timezone} onChangeText={setTimezone} placeholder="Timezone" />

        <TouchableOpacity style={[styles.button, loading && styles.buttonDisabled]} onPress={handleCalculate} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? 'Calculating...' : 'Calculate Chart'}</Text>
        </TouchableOpacity>

        {statusMessage ? <Text style={styles.statusText}>{statusMessage}</Text> : null}
      </View>

      {chart ? (
        <View style={styles.card}>
          <Text style={styles.sectionTitle}>Chart Result</Text>
          <Text style={styles.row}>Ascendant: {chart?.ascendant?.sign || '-'} ({chart?.ascendant?.degree || 0})</Text>
          <Text style={styles.sectionTitle}>Planets</Text>
          {chartPlanets.slice(0, 12).map((planet: any, idx: number) => (
            <Text key={idx} style={styles.row}>
              {planet.name}: {planet.sign} ({planet.degree}) H{planet.house}
            </Text>
          ))}
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
  card: {
    backgroundColor: THEME.card,
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  stepTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 8,
    marginTop: 4,
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
  inputButton: {
    backgroundColor: '#fff',
    borderColor: '#E0E0E0',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 12,
    marginBottom: 8,
  },
  inputButtonText: {
    color: THEME.text,
  },
  button: {
    backgroundColor: THEME.primary,
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
    marginTop: 4,
  },
  secondaryButton: {
    backgroundColor: '#CC5B2A',
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
    marginBottom: 8,
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  buttonDisabled: {
    opacity: 0.7,
  },
  statusText: {
    marginTop: 10,
    color: THEME.textLight,
    textAlign: 'center',
  },
  locationList: {
    marginBottom: 8,
  },
  locationItem: {
    borderWidth: 1,
    borderColor: '#E0E0E0',
    backgroundColor: '#fff',
    borderRadius: 10,
    padding: 10,
    marginBottom: 6,
  },
  locationTitle: {
    color: THEME.text,
    fontWeight: '600',
  },
  locationMeta: {
    color: THEME.textLight,
    marginTop: 2,
    fontSize: 12,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 6,
    marginTop: 4,
  },
  row: {
    color: THEME.textLight,
    marginBottom: 4,
  },
});

export default HoroscopeScreen;
