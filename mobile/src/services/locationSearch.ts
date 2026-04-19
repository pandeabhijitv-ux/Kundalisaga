export interface LocationOption {
  label: string;
  latitude: string;
  longitude: string;
  timezone: string;
}

const DEFAULT_TIMEZONE = 'Asia/Kolkata';

const fetchWithTimeout = async (url: string, timeoutMs = 10000): Promise<Response> => {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);
  try {
    return await fetch(url, {
      signal: controller.signal,
      headers: {
        Accept: 'application/json',
        'Accept-Language': 'en',
        'User-Agent': 'KundaliSaga/1.0',
      },
    });
  } finally {
    clearTimeout(timeoutId);
  }
};

const buildPlaceLabel = (item: any): string => {
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
  const uniqueParts = Array.from(new Set(parts.map((p: string) => p.trim())));
  return uniqueParts.length > 0 ? uniqueParts.join(', ') : item.display_name || 'Unknown';
};

const mapNominatimResults = (data: any[]): LocationOption[] =>
  data.map((item: any) => ({
    label: buildPlaceLabel(item),
    latitude: String(item.lat),
    longitude: String(item.lon),
    timezone: DEFAULT_TIMEZONE,
  }));

const mapMapsCoResults = (data: any[]): LocationOption[] =>
  data.map((item: any) => ({
    label: item.display_name || `${item.lat}, ${item.lon}`,
    latitude: String(item.lat),
    longitude: String(item.lon),
    timezone: DEFAULT_TIMEZONE,
  }));

const dedupeOptions = (options: LocationOption[]): LocationOption[] => {
  const seen = new Set<string>();
  return options.filter(opt => {
    const key = `${opt.label}|${opt.latitude}|${opt.longitude}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
};

export const searchLocations = async (query: string): Promise<LocationOption[]> => {
  const q = query.trim();
  if (q.length < 3) {
    throw new Error('Please enter at least 3 characters.');
  }

  const nominatimUrl = `https://nominatim.openstreetmap.org/search?format=jsonv2&addressdetails=1&limit=6&q=${encodeURIComponent(q)}`;
  const fallbackUrl = `https://geocode.maps.co/search?q=${encodeURIComponent(q)}`;

  let options: LocationOption[] = [];

  try {
    const res = await fetchWithTimeout(nominatimUrl);
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data)) {
        options = mapNominatimResults(data);
      }
    }
  } catch {
    // Try fallback service below.
  }

  if (options.length === 0) {
    const fallbackRes = await fetchWithTimeout(fallbackUrl);
    if (!fallbackRes.ok) {
      throw new Error('Location service not reachable. Please try again in a moment.');
    }
    const fallbackData = await fallbackRes.json();
    if (Array.isArray(fallbackData)) {
      options = mapMapsCoResults(fallbackData);
    }
  }

  const clean = dedupeOptions(options).filter(
    item => Number.isFinite(Number(item.latitude)) && Number.isFinite(Number(item.longitude)),
  );

  if (clean.length === 0) {
    throw new Error('No matching location found. Try city and state together.');
  }

  return clean.slice(0, 6);
};
