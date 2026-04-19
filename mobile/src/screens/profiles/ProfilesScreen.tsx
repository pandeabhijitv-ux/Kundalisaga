/**
 * Profiles Screen
 * Local profile manager for family birth records.
 */
import React, {useEffect, useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  FlatList,
  Alert,
} from 'react-native';
import {THEME} from '../../constants/theme';
import {LocationOption, searchLocations} from '../../services/locationSearch';
import {
  UserProfile,
  getActiveProfileId,
  getProfiles,
  saveProfiles,
  setActiveProfileId,
} from '../../services/profileData';

const ProfilesScreen = () => {
  const [profiles, setProfiles] = useState<UserProfile[]>([]);
  const [activeProfileId, setActiveProfile] = useState<string | null>(null);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [date, setDate] = useState('1990-01-01');
  const [time, setTime] = useState('12:00');
  const [location, setLocation] = useState('Mumbai');
  const [locationQuery, setLocationQuery] = useState('Mumbai');
  const [locationOptions, setLocationOptions] = useState<LocationOption[]>([]);
  const [searchingLocation, setSearchingLocation] = useState(false);
  const [latitude, setLatitude] = useState<number>(19.076);
  const [longitude, setLongitude] = useState<number>(72.8777);
  const [timezone, setTimezone] = useState('Asia/Kolkata');

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      const data = await getProfiles();
      const active = await getActiveProfileId();
      setProfiles(data);
      if (active) {
        setActiveProfile(active);
      } else if (data.length > 0) {
        await setActiveProfileId(data[0].id);
        setActiveProfile(data[0].id);
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to load profiles');
    }
  };

  const persistProfiles = async (nextProfiles: UserProfile[]) => {
    setProfiles(nextProfiles);
    await saveProfiles(nextProfiles);
  };

  const addProfile = async () => {
    if (!name.trim()) {
      Alert.alert('Validation', 'Please enter profile name');
      return;
    }
    if (!location.trim()) {
      Alert.alert('Validation', 'Please select a location before creating profile');
      return;
    }

    const newProfile: UserProfile = {
      id: `${Date.now()}`,
      name: name.trim(),
      email: email.trim() || undefined,
      date,
      time,
      location,
      latitude,
      longitude,
      timezone,
    };

    const next = [newProfile, ...profiles];
    await persistProfiles(next);
    if (!activeProfileId) {
      await setActiveProfileId(newProfile.id);
      setActiveProfile(newProfile.id);
    }
    setName('');
    setEmail('');
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
      const results = await searchLocations(query);
      setLocationOptions(results);
    } catch (error: any) {
      Alert.alert('Search Error', error?.message || 'Unable to search location right now');
    } finally {
      setSearchingLocation(false);
    }
  };

  const selectLocation = (option: LocationOption) => {
    setLocation(option.label);
    setLocationQuery(option.label);
    setLatitude(Number(option.latitude));
    setLongitude(Number(option.longitude));
    setTimezone(option.timezone || 'Asia/Kolkata');
    setLocationOptions([]);
  };

  const selectActiveProfile = async (id: string) => {
    await setActiveProfileId(id);
    setActiveProfile(id);
    Alert.alert('Active Profile Updated', 'This profile will be used for analytics and predictions.');
  };

  const deleteProfile = (id: string) => {
    Alert.alert('Delete Profile', 'Remove this saved profile?', [
      {text: 'Cancel', style: 'cancel'},
      {
        text: 'Delete',
        style: 'destructive',
        onPress: async () => {
          const next = profiles.filter(p => p.id !== id);
          await persistProfiles(next);
          if (activeProfileId === id) {
            const nextActive = next[0]?.id || null;
            if (nextActive) {
              await setActiveProfileId(nextActive);
            }
            setActiveProfile(nextActive);
          }
        },
      },
    ]);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Family Profiles</Text>

      <View style={styles.formCard}>
        <TextInput
          style={styles.input}
          placeholder="Full Name"
          value={name}
          onChangeText={setName}
        />
        <TextInput
          style={styles.input}
          placeholder="Email Address (optional)"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Date of Birth (YYYY-MM-DD)"
          value={date}
          onChangeText={setDate}
        />
        <TextInput
          style={styles.input}
          placeholder="Time (HH:MM)"
          value={time}
          onChangeText={setTime}
        />
        <TextInput
          style={styles.input}
          placeholder="Search city / town / village"
          value={locationQuery}
          onChangeText={setLocationQuery}
        />

        <TouchableOpacity style={[styles.searchButton, searchingLocation && styles.searchButtonDisabled]} onPress={handleSearchLocation} disabled={searchingLocation}>
          <Text style={styles.searchButtonText}>{searchingLocation ? 'Searching...' : 'Search Location'}</Text>
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

        <TextInput
          style={styles.input}
          placeholder="Selected Location"
          value={location}
          onChangeText={setLocation}
        />

        <TouchableOpacity style={styles.addButton} onPress={addProfile}>
          <Text style={styles.addButtonText}>Add Profile</Text>
        </TouchableOpacity>
      </View>

      <FlatList
        data={profiles}
        keyExtractor={item => item.id}
        contentContainerStyle={styles.listContent}
        ListEmptyComponent={
          <Text style={styles.emptyText}>No profiles saved yet.</Text>
        }
        renderItem={({item}) => (
          <TouchableOpacity
            style={[
              styles.profileCard,
              activeProfileId === item.id && styles.activeProfileCard,
            ]}
            onPress={() => selectActiveProfile(item.id)}>
            <View>
              <Text style={styles.profileName}>{item.name}</Text>
              {item.email ? <Text style={styles.profileMeta}>📧 {item.email}</Text> : null}
              <Text style={styles.profileMeta}>{item.date} | {item.time}</Text>
              <Text style={styles.profileMeta}>📍 {item.location}</Text>
              {activeProfileId === item.id ? (
                <Text style={styles.activeTag}>Active Profile</Text>
              ) : null}
            </View>
            <TouchableOpacity onPress={() => deleteProfile(item.id)}>
              <Text style={styles.deleteText}>Delete</Text>
            </TouchableOpacity>
          </TouchableOpacity>
        )}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.background,
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 12,
  },
  formCard: {
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
  addButton: {
    backgroundColor: THEME.primary,
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
  },
  searchButton: {
    backgroundColor: '#CC5B2A',
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
    marginBottom: 8,
  },
  searchButtonDisabled: {
    opacity: 0.7,
  },
  searchButtonText: {
    color: '#fff',
    fontWeight: '700',
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
  addButtonText: {
    color: '#fff',
    fontWeight: '700',
  },
  listContent: {
    paddingBottom: 20,
  },
  profileCard: {
    backgroundColor: THEME.card,
    borderRadius: 12,
    padding: 12,
    marginBottom: 8,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  activeProfileCard: {
    borderWidth: 1.5,
    borderColor: THEME.primary,
  },
  profileName: {
    fontSize: 16,
    fontWeight: '700',
    color: THEME.text,
  },
  profileMeta: {
    color: THEME.textLight,
    marginTop: 2,
  },
  deleteText: {
    color: THEME.error,
    fontWeight: '700',
  },
  activeTag: {
    marginTop: 6,
    color: THEME.primary,
    fontSize: 12,
    fontWeight: '700',
  },
  emptyText: {
    textAlign: 'center',
    color: THEME.textLight,
    marginTop: 12,
  },
});

export default ProfilesScreen;
