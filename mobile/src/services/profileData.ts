import AsyncStorage from '@react-native-async-storage/async-storage';
import {calculateChart, ChartData} from './PythonBridge';

export interface UserProfile {
  id: string;
  name: string;
  email?: string;
  date: string;
  time: string;
  location: string;
  latitude?: number;
  longitude?: number;
  timezone?: string;
}

export const STORAGE_KEY_PROFILES = 'kundali_profiles';
export const STORAGE_KEY_ACTIVE_PROFILE = 'kundali_active_profile_id';
const CHART_CACHE_PREFIX = 'kundali_chart_cache_';

const DEFAULT_COORDS = {
  latitude: 19.076,
  longitude: 72.8777,
  timezone: 'Asia/Kolkata',
};

const normalizeProfile = (profile: UserProfile): UserProfile => ({
  ...profile,
  latitude: Number.isFinite(profile.latitude as number)
    ? Number(profile.latitude)
    : DEFAULT_COORDS.latitude,
  longitude: Number.isFinite(profile.longitude as number)
    ? Number(profile.longitude)
    : DEFAULT_COORDS.longitude,
  timezone: profile.timezone || DEFAULT_COORDS.timezone,
});

export const getProfiles = async (): Promise<UserProfile[]> => {
  const raw = await AsyncStorage.getItem(STORAGE_KEY_PROFILES);
  if (!raw) {
    return [];
  }
  const parsed = JSON.parse(raw);
  if (!Array.isArray(parsed)) {
    return [];
  }
  return parsed.map((p: UserProfile) => normalizeProfile(p));
};

export const saveProfiles = async (profiles: UserProfile[]): Promise<void> => {
  const normalized = profiles.map(normalizeProfile);
  await AsyncStorage.setItem(STORAGE_KEY_PROFILES, JSON.stringify(normalized));
};

export const setActiveProfileId = async (profileId: string): Promise<void> => {
  await AsyncStorage.setItem(STORAGE_KEY_ACTIVE_PROFILE, profileId);
};

export const getActiveProfileId = async (): Promise<string | null> => {
  return AsyncStorage.getItem(STORAGE_KEY_ACTIVE_PROFILE);
};

export const getActiveProfile = async (): Promise<UserProfile | null> => {
  const profiles = await getProfiles();
  if (profiles.length === 0) {
    return null;
  }

  const activeId = await getActiveProfileId();
  if (!activeId) {
    const first = profiles[0];
    await setActiveProfileId(first.id);
    return first;
  }

  const selected = profiles.find(p => p.id === activeId);
  if (selected) {
    return selected;
  }

  const fallback = profiles[0];
  await setActiveProfileId(fallback.id);
  return fallback;
};

const chartKey = (profileId: string) => `${CHART_CACHE_PREFIX}${profileId}`;

export const saveCachedChart = async (
  profileId: string,
  chart: ChartData,
): Promise<void> => {
  await AsyncStorage.setItem(chartKey(profileId), JSON.stringify(chart));
};

export const getCachedChart = async (
  profileId: string,
): Promise<ChartData | null> => {
  const raw = await AsyncStorage.getItem(chartKey(profileId));
  if (!raw) {
    return null;
  }
  return JSON.parse(raw);
};

export const getOrCreateChartForProfile = async (
  profile: UserProfile,
): Promise<ChartData> => {
  const normalized = normalizeProfile(profile);
  const cached = await getCachedChart(normalized.id);
  if (cached) {
    return cached;
  }

  const chart = await calculateChart({
    name: normalized.name,
    date: normalized.date,
    time: normalized.time,
    location: normalized.location,
    latitude: Number(normalized.latitude),
    longitude: Number(normalized.longitude),
    timezone: normalized.timezone || DEFAULT_COORDS.timezone,
  });

  if ((chart as any)?.error) {
    throw new Error((chart as any).error);
  }

  await saveCachedChart(normalized.id, chart);
  return chart;
};

export const getActiveProfileWithChart = async (): Promise<{
  profile: UserProfile;
  chart: ChartData;
}> => {
  const profile = await getActiveProfile();
  if (!profile) {
    throw new Error('No saved profile found. Please create a profile first.');
  }

  const chart = await getOrCreateChartForProfile(profile);
  return {profile, chart};
};
