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
import AsyncStorage from '@react-native-async-storage/async-storage';
import {THEME} from '../../constants/theme';

interface Profile {
  id: string;
  name: string;
  date: string;
  time: string;
  location: string;
}

const STORAGE_KEY = 'kundali_profiles';

const ProfilesScreen = () => {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [name, setName] = useState('');
  const [date, setDate] = useState('1990-01-01');
  const [time, setTime] = useState('12:00');
  const [location, setLocation] = useState('Mumbai');

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      const raw = await AsyncStorage.getItem(STORAGE_KEY);
      if (raw) {
        setProfiles(JSON.parse(raw));
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to load profiles');
    }
  };

  const saveProfiles = async (nextProfiles: Profile[]) => {
    setProfiles(nextProfiles);
    await AsyncStorage.setItem(STORAGE_KEY, JSON.stringify(nextProfiles));
  };

  const addProfile = async () => {
    if (!name.trim()) {
      Alert.alert('Validation', 'Please enter profile name');
      return;
    }

    const newProfile: Profile = {
      id: `${Date.now()}`,
      name: name.trim(),
      date,
      time,
      location,
    };

    const next = [newProfile, ...profiles];
    await saveProfiles(next);
    setName('');
  };

  const deleteProfile = (id: string) => {
    Alert.alert('Delete Profile', 'Remove this saved profile?', [
      {text: 'Cancel', style: 'cancel'},
      {
        text: 'Delete',
        style: 'destructive',
        onPress: async () => {
          const next = profiles.filter(p => p.id !== id);
          await saveProfiles(next);
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
          placeholder="Name"
          value={name}
          onChangeText={setName}
        />
        <TextInput
          style={styles.input}
          placeholder="Date (YYYY-MM-DD)"
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
          placeholder="Location"
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
          <View style={styles.profileCard}>
            <View>
              <Text style={styles.profileName}>{item.name}</Text>
              <Text style={styles.profileMeta}>{item.date} | {item.time}</Text>
              <Text style={styles.profileMeta}>{item.location}</Text>
            </View>
            <TouchableOpacity onPress={() => deleteProfile(item.id)}>
              <Text style={styles.deleteText}>Delete</Text>
            </TouchableOpacity>
          </View>
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
  emptyText: {
    textAlign: 'center',
    color: THEME.textLight,
    marginTop: 12,
  },
});

export default ProfilesScreen;
