import React, {useMemo, useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {analyzeFinancial} from '../services/PythonBridge';
import {getFinancialInsight} from '../services/astrologyInsights';

const RATING_STARS: Record<string, string> = {
  Excellent: '⭐⭐⭐⭐⭐',
  Good: '⭐⭐⭐⭐',
  Moderate: '⭐⭐⭐',
  Weak: '⭐⭐',
  Poor: '⭐',
};

const FinancialScreen = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [tab, setTab] = useState<'market' | 'sector' | 'personalized'>('personalized');
  const [profileName, setProfileName] = useState('');
  const [chartData, setChartData] = useState<any>(null);

  const topSectors = useMemo(() => {
    const raw = result?.market?.top_sectors;
    if (!Array.isArray(raw)) return [];
    return raw;
  }, [result]);

  const weakSectors = useMemo(() => {
    const raw = result?.market?.weak_sectors;
    if (!Array.isArray(raw)) return [];
    return raw;
  }, [result]);

  const analyze = async () => {
    setLoading(true);
    try {
      const {profile, chart} = await getActiveProfileWithChart();
      setProfileName(profile.name || 'Profile');
      setChartData(chart);
      const data = await analyzeFinancial(JSON.stringify(chart));
      setResult(data);
    } catch (error: any) {
      Alert.alert('Financial Analysis', error?.message || 'Unable to analyze. Please ensure an active profile exists.');
    } finally {
      setLoading(false);
    }
  };

  const personalRecs: any[] = Array.isArray(result?.personalized?.recommendations)
    ? result.personalized.recommendations
    : Array.isArray(result?.personalized?.sector_recommendations)
      ? result.personalized.sector_recommendations
      : Array.isArray(result?.recommendations)
        ? result.recommendations
        : [];
  const market: any = result?.market && typeof result.market === 'object' ? result.market : {};
  const localInsight = useMemo(() => {
    if (!chartData) return null;
    try {
      return getFinancialInsight(chartData);
    } catch {
      return null;
    }
  }, [chartData]);

  const fallbackPersonalRecs = useMemo(() => {
    const rows = Array.isArray(localInsight?.planetRows) ? localInsight!.planetRows : [];
    return rows.slice(0, 5).map((row: any, idx: number) => ({
      sector: row?.role || `Financial Theme ${idx + 1}`,
      rating: idx <= 1 ? 'Good' : 'Moderate',
      natal_strength: Math.max(40, 70 - idx * 6),
      transit_strength: Math.max(35, 60 - idx * 5),
      total_strength: Math.max(75, 130 - idx * 11),
      advice: row?.effect || 'Follow disciplined allocation and risk-managed timing.',
    }));
  }, [localInsight]);

  const effectivePersonalRecs = personalRecs.length > 0 ? personalRecs : fallbackPersonalRecs;
  const marketSentimentRaw = String(market.market_sentiment || 'Neutral');
  const isLiveUnavailable = /connect to internet|live transit unavailable|ephemeris not available/i.test(marketSentimentRaw);
  const marketSentiment = isLiveUnavailable
    ? (localInsight?.outlook || 'Live transit feed unavailable. Showing chart-based guidance.')
    : marketSentimentRaw;
  const fallbackTop = effectivePersonalRecs
    .slice()
    .sort((a: any, b: any) => (Number(b?.total_strength || 0) - Number(a?.total_strength || 0)))
    .slice(0, 3)
    .map((r: any) => ({sector: r.sector, rating: r.rating}));

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>📈</Text>
        <Text style={styles.title}>Financial Outlook</Text>
        <Text style={styles.subtitle}>Sector guidance based on your chart and current planetary transits</Text>
      </View>

      <View style={styles.premiumBanner}><Text style={styles.premiumText}>⭐ Premium Feature - Advanced financial astrology analysis</Text></View>

      <View style={styles.tabRow}>
        <TouchableOpacity style={[styles.tab, tab === 'market' && styles.tabActive]} onPress={() => setTab('market')}><Text style={[styles.tabText, tab === 'market' && styles.tabTextActive]}>Market Overview</Text></TouchableOpacity>
        <TouchableOpacity style={[styles.tab, tab === 'sector' && styles.tabActive]} onPress={() => setTab('sector')}><Text style={[styles.tabText, tab === 'sector' && styles.tabTextActive]}>Sector Analysis</Text></TouchableOpacity>
        <TouchableOpacity style={[styles.tab, tab === 'personalized' && styles.tabActive]} onPress={() => setTab('personalized')}><Text style={[styles.tabText, tab === 'personalized' && styles.tabTextActive]}>Personalized</Text></TouchableOpacity>
      </View>

      {!result && (
        <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>Get Personalized Report</Text>}
        </TouchableOpacity>
      )}

      {result && (
        <>
          <View style={styles.generatedBanner}><Text style={styles.generatedText}>✅ Report Generated - {new Date().toISOString().slice(0, 10)}</Text></View>

          {tab === 'personalized' && (
            <>
              <Text style={styles.sectionHeading}>Your Top Sector Opportunities</Text>
              {effectivePersonalRecs.map((rec: any, i: number) => (
                <View key={i} style={styles.card}>
                  <View style={styles.cardHeader}><Text style={styles.sectorName}>{RATING_STARS[rec.rating] || '⭐⭐⭐'} {rec.rating} - {rec.sector}</Text></View>
                  <View style={styles.metricRow}>
                    <View style={styles.metricCol}><Text style={styles.metricLabel}>Natal Strength</Text><Text style={styles.metricValue}>{rec.natal_strength ?? '-'}</Text></View>
                    <View style={styles.metricCol}><Text style={styles.metricLabel}>Transit Strength</Text><Text style={styles.metricValue}>{rec.transit_strength ?? '-'}</Text></View>
                    <View style={styles.metricCol}><Text style={styles.metricLabel}>Total Score</Text><Text style={styles.metricValue}>{rec.total_strength ?? '-'}</Text></View>
                  </View>
                  <View style={styles.adviceBox}><Text style={styles.advice}>💡 Sector Guidance: {rec.advice}</Text></View>
                </View>
              ))}

              {effectivePersonalRecs.length === 0 && (
                <View style={styles.card}>
                  <Text style={styles.sectionTitle}>No personalized sector data available</Text>
                  <Text style={styles.listItem}>Try again after selecting an active profile with a valid birth chart.</Text>
                </View>
              )}
            </>
          )}

          {tab === 'sector' && (
            <>
              <View style={styles.card}>
                <Text style={styles.sectionTitle}>Sector Ranking (Personalized)</Text>
                {effectivePersonalRecs.map((rec: any, i: number) => (
                  <Text key={i} style={styles.listItem}>{i + 1}. {rec.sector}  •  {rec.total_strength}/200</Text>
                ))}
                {effectivePersonalRecs.length === 0 && (
                  <Text style={styles.listItem}>No personalized ranking yet. Generate your report first.</Text>
                )}
              </View>

              {topSectors.length > 0 && (
                <View style={styles.card}>
                  <Text style={styles.sectionTitle}>Top Performing Sectors (Transit)</Text>
                  {topSectors.map((item: any, i: number) => {
                    const sector = typeof item === 'string' ? item : item?.sector;
                    const rating = typeof item === 'string' ? '' : item?.rating;
                    const prediction = typeof item === 'string' ? '' : item?.prediction;
                    return (
                      <View key={`top-${i}`} style={styles.sectorBlock}>
                        <Text style={styles.listItem}>• {sector}{rating ? ` - ${rating}` : ''}</Text>
                        {!!prediction && <Text style={styles.sectorMeta}>{prediction}</Text>}
                      </View>
                    );
                  })}
                </View>
              )}

              {weakSectors.length > 0 && (
                <View style={styles.card}>
                  <Text style={styles.sectionTitle}>Sectors To Avoid (Transit)</Text>
                  {weakSectors.map((item: any, i: number) => {
                    const sector = typeof item === 'string' ? item : item?.sector;
                    const rating = typeof item === 'string' ? '' : item?.rating;
                    return <Text key={`weak-${i}`} style={styles.listItem}>• {sector}{rating ? ` - ${rating}` : ''}</Text>;
                  })}
                </View>
              )}
            </>
          )}

          {tab === 'market' && (
            <>
              <View style={styles.card}>
                <Text style={styles.sectionTitle}>Overall Market Sentiment</Text>
                <Text style={styles.sentimentBig}>{marketSentiment}</Text>
                <Text style={styles.strengthLabel}>Overall Strength: {market.overall_strength || 'N/A'}</Text>
              </View>
              {isLiveUnavailable && effectivePersonalRecs.length > 0 && (
                <View style={styles.card}>
                  <Text style={styles.sectionTitle}>Local Personalized Snapshot</Text>
                  <Text style={styles.listItem}>Profile: {profileName || 'Active profile'}</Text>
                  {effectivePersonalRecs.slice(0, 3).map((rec: any, i: number) => (
                    <Text key={`local-${i}`} style={styles.listItem}>• {rec.sector} - {rec.rating} ({rec.total_strength}/200)</Text>
                  ))}
                </View>
              )}
              {(market.top_sectors?.length > 0 || fallbackTop.length > 0) && (
                <View style={styles.card}>
                  <Text style={styles.sectionTitle}>Top Sectors</Text>
                  {(market.top_sectors?.length > 0 ? market.top_sectors : fallbackTop).map((s: any, i: number) => {
                    const sector = typeof s === 'string' ? s : s?.sector;
                    const rating = typeof s === 'string' ? '' : s?.rating;
                    return <Text key={i} style={styles.listItem}>• {sector}{rating ? ` - ${rating}` : ''}</Text>;
                  })}
                </View>
              )}
            </>
          )}

          <TouchableOpacity style={[styles.button, {backgroundColor: THEME.textLight, marginTop: 8}]} onPress={() => setResult(null)}>
            <Text style={styles.buttonText}>Re-analyze</Text>
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
  title: {fontSize: 22, fontWeight: 'bold', color: THEME.primary, textAlign: 'center'},
  subtitle: {fontSize: 13, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  premiumBanner: {backgroundColor: '#FDEBCF', borderRadius: 8, padding: 10, marginBottom: 10},
  premiumText: {fontSize: 12, color: '#8A4B00', fontWeight: '600'},
  generatedBanner: {backgroundColor: '#DCFCE7', borderRadius: 8, padding: 10, marginBottom: 12},
  generatedText: {fontSize: 12, color: '#166534', fontWeight: '600'},
  tabRow: {flexDirection: 'row', marginBottom: 14, backgroundColor: '#F3F4F6', borderRadius: 10, padding: 4},
  tab: {flex: 1, padding: 8, alignItems: 'center', borderRadius: 8},
  tabActive: {backgroundColor: THEME.primary},
  tabText: {fontSize: 12, color: THEME.textLight, fontWeight: '600'},
  tabTextActive: {color: '#fff'},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginVertical: 10},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 14},
  sectionHeading: {fontSize: 30, fontWeight: '700', color: THEME.text, marginBottom: 10},
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  cardHeader: {marginBottom: 8},
  sectorName: {fontSize: 14, fontWeight: '700', color: THEME.text},
  metricRow: {flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8},
  metricCol: {flex: 1},
  metricLabel: {fontSize: 12, color: THEME.textLight},
  metricValue: {fontSize: 34, color: THEME.text, fontWeight: '700'},
  adviceBox: {backgroundColor: '#EEF2F7', borderRadius: 8, padding: 10},
  advice: {fontSize: 12, color: '#1F4E79', fontWeight: '600'},
  sectorBlock: {marginBottom: 8},
  sectorMeta: {fontSize: 12, color: THEME.textLight, marginLeft: 12, marginTop: 2},
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 8},
  sentimentBig: {fontSize: 24, fontWeight: 'bold', color: THEME.primary, textAlign: 'center', paddingVertical: 8},
  strengthLabel: {fontSize: 13, color: THEME.textLight, textAlign: 'center'},
  listItem: {fontSize: 13, color: THEME.text, lineHeight: 22},
});

export default FinancialScreen;
