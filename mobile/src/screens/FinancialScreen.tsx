import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {getActiveProfileWithChart} from '../services/profileData';
import {analyzeFinancial} from '../services/PythonBridge';

const STRENGTH_COLOR = (s: number) => {
  if (s >= 80) return '#16A34A';
  if (s >= 65) return '#CA8A04';
  if (s >= 50) return '#2563EB';
  if (s >= 35) return '#D97706';
  return '#DC2626';
};

const STRENGTH_LABEL = (s: number) => {
  if (s >= 80) return 'Excellent';
  if (s >= 65) return 'Very Good';
  if (s >= 50) return 'Good';
  if (s >= 35) return 'Moderate';
  return 'Caution';
};

const DASHA_COLORS: Record<string, string> = {
  Jupiter: '#1D4ED8', Venus: '#BE185D', Mercury: '#0891B2',
  Sun: '#D97706', Moon: '#7C3AED', Mars: '#DC2626',
  Saturn: '#374151', Rahu: '#6366F1', Ketu: '#92400E',
};

const FinancialScreen = () => {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [tab, setTab] = useState<'market' | 'sector' | 'personalized'>('personalized');

  const analyze = async () => {
    setLoading(true);
    try {
      const {chart} = await getActiveProfileWithChart();
      const data = await analyzeFinancial(JSON.stringify(chart));
      setResult(data);
    } catch (error: any) {
      Alert.alert('Financial Analysis', error?.message || 'Unable to analyze. Please ensure an active profile exists.');
    } finally {
      setLoading(false);
    }
  };

  const market: any = result?.market && typeof result.market === 'object' ? result.market : null;
  const sectorList: any[] = Array.isArray(result?.sector) ? result.sector : [];
  const personalized: any = result?.personalized && typeof result.personalized === 'object' ? result.personalized : null;
  const personalRecs: any[] = Array.isArray(personalized?.recommendations) ? personalized.recommendations : [];
  const wealthHouses: any[] = Array.isArray(personalized?.wealth_house_analysis) ? personalized.wealth_house_analysis : [];

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>📈</Text>
        <Text style={styles.title}>Financial Outlook</Text>
        <Text style={styles.subtitle}>Planetary sector guidance based on your natal chart & Dasha period</Text>
      </View>

      <View style={styles.tabRow}>
        {(['market', 'sector', 'personalized'] as const).map(t => (
          <TouchableOpacity key={t} style={[styles.tab, tab === t && styles.tabActive]} onPress={() => setTab(t)}>
            <Text style={[styles.tabText, tab === t && styles.tabTextActive]}>
              {t === 'market' ? 'Dasha Period' : t === 'sector' ? 'Sectors' : 'My Analysis'}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      {!result && (
        <TouchableOpacity style={styles.button} onPress={analyze} disabled={loading}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>🔮 Generate Financial Analysis</Text>}
        </TouchableOpacity>
      )}

      {loading && <ActivityIndicator size="large" color={THEME.primary} style={{marginTop: 20}} />}

      {result && (
        <>
          <View style={styles.generatedBanner}>
            <Text style={styles.generatedText}>✅ Report Generated — {new Date().toISOString().slice(0, 10)}</Text>
          </View>

          {/* ── MARKET OVERVIEW TAB (Dasha Period) ─────────────────────── */}
          {tab === 'market' && market && (
            <>
              {/* Dasha header card */}
              <View style={[styles.dashaCard, {borderLeftColor: DASHA_COLORS[market.mahadasha] || THEME.primary}]}>
                <Text style={styles.dashaLabel}>Current Mahadasha</Text>
                <Text style={[styles.dashaName, {color: DASHA_COLORS[market.mahadasha] || THEME.primary}]}>
                  {market.mahadasha} Mahadasha
                </Text>
                {!!market.years_remaining && (
                  <Text style={styles.dashaRemaining}>⏳ {market.years_remaining} remaining (ends {market.dasha_end})</Text>
                )}
                <View style={[styles.sentimentPill, {backgroundColor: STRENGTH_COLOR(market.strength) + '22'}]}>
                  <Text style={[styles.sentimentText, {color: STRENGTH_COLOR(market.strength)}]}>
                    {market.sentiment}
                  </Text>
                </View>
              </View>

              {/* Strength meter */}
              <View style={styles.card}>
                <Text style={styles.cardLabel}>Dasha Financial Strength</Text>
                <View style={styles.meterBg}>
                  <View style={[styles.meterFill, {width: `${market.strength}%` as any, backgroundColor: STRENGTH_COLOR(market.strength)}]} />
                </View>
                <Text style={[styles.meterScore, {color: STRENGTH_COLOR(market.strength)}]}>
                  {market.strength}/100 — {STRENGTH_LABEL(market.strength)}
                </Text>
              </View>

              {/* Outlook */}
              <View style={styles.card}>
                <Text style={styles.cardLabel}>📊 Period Outlook</Text>
                <Text style={styles.bodyText}>{market.outlook}</Text>
              </View>

              {/* Favorable sectors */}
              {Array.isArray(market.favorable_sectors) && market.favorable_sectors.length > 0 && (
                <View style={styles.card}>
                  <Text style={styles.cardLabel}>✅ Sectors Favored This Dasha</Text>
                  {market.favorable_sectors.map((s: string, i: number) => (
                    <Text key={i} style={styles.bulletText}>• {s}</Text>
                  ))}
                </View>
              )}

              {/* Caution */}
              <View style={[styles.card, {borderLeftWidth: 4, borderLeftColor: '#F59E0B'}]}>
                <Text style={styles.cardLabel}>⚠️ Caution</Text>
                <Text style={styles.bodyText}>{market.caution}</Text>
              </View>

              {/* Investment tip */}
              <View style={[styles.card, {backgroundColor: '#EFF6FF', borderLeftWidth: 4, borderLeftColor: '#3B82F6'}]}>
                <Text style={styles.cardLabel}>💡 Investment Tip</Text>
                <Text style={styles.bodyText}>{market.investment_tip}</Text>
              </View>
            </>
          )}

          {/* ── SECTOR ANALYSIS TAB ─────────────────────────────────────── */}
          {tab === 'sector' && (
            <>
              <Text style={styles.sectionHeading}>Sector Rankings from Your Natal Chart</Text>
              <Text style={styles.sectionSubtitle}>
                Ranked by the strength of each sector's ruling planet in your birth chart. Strong house placement = stronger sector for you.
              </Text>
              {sectorList.slice(0, 10).map((item: any, i: number) => (
                <View key={i} style={styles.sectorCard}>
                  <View style={styles.sectorCardTop}>
                    <View style={styles.sectorRankBadge}>
                      <Text style={styles.sectorRankText}>#{i + 1}</Text>
                    </View>
                    <View style={{flex: 1}}>
                      <Text style={styles.sectorCardName}>{item.sector}</Text>
                      <Text style={styles.sectorCardPlanet}>
                        🪐 {item.ruling_planet} in {item.planet_sign} • House {item.planet_house}
                      </Text>
                    </View>
                    <View style={[styles.ratingPill, {backgroundColor: STRENGTH_COLOR(item.strength) + '22'}]}>
                      <Text style={[styles.ratingText, {color: STRENGTH_COLOR(item.strength)}]}>{item.rating}</Text>
                    </View>
                  </View>
                  <View style={styles.meterBg}>
                    <View style={[styles.meterFill, {width: `${item.strength}%` as any, backgroundColor: STRENGTH_COLOR(item.strength)}]} />
                  </View>
                  <Text style={styles.sectorReason}>{item.reason}</Text>
                  <Text style={styles.stocksText}>📌 {item.stocks}</Text>
                </View>
              ))}
            </>
          )}

          {/* ── PERSONALIZED TAB ─────────────────────────────────────────── */}
          {tab === 'personalized' && personalized && (
            <>
              {/* Summary */}
              {!!personalized.summary && (
                <View style={[styles.card, {backgroundColor: '#F0FDF4', borderLeftWidth: 4, borderLeftColor: '#22C55E'}]}>
                  <Text style={styles.cardLabel}>🌟 Your Financial Summary</Text>
                  <Text style={styles.bodyText}>{personalized.summary}</Text>
                </View>
              )}

              {/* Wealth House Analysis */}
              {wealthHouses.length > 0 && (
                <View style={styles.card}>
                  <Text style={styles.cardLabel}>🏠 Wealth House Analysis</Text>
                  <Text style={styles.sectorSubtitle}>Planets in your 2nd (Wealth), 5th (Speculation), 9th (Fortune) & 11th (Gains) houses</Text>
                  {wealthHouses.map((item: any, i: number) => (
                    <View key={i} style={styles.wealthRow}>
                      <Text style={styles.wealthPlanet}>{item.planet}</Text>
                      <Text style={styles.wealthHouse}>H{item.house} {item.house_name}</Text>
                      <Text style={styles.wealthSign}>{item.sign}</Text>
                      <View style={[styles.wealthStrBadge, {backgroundColor: STRENGTH_COLOR(item.strength) + '22'}]}>
                        <Text style={[styles.wealthStrText, {color: STRENGTH_COLOR(item.strength)}]}>{item.strength}</Text>
                      </View>
                    </View>
                  ))}
                </View>
              )}

              {/* Top Sector Opportunities */}
              <Text style={styles.sectionHeading}>Your Top Opportunities</Text>
              {personalRecs.map((rec: any, i: number) => (
                <View key={i} style={styles.sectorCard}>
                  <View style={styles.sectorCardTop}>
                    <View style={styles.sectorRankBadge}>
                      <Text style={styles.sectorRankText}>#{i + 1}</Text>
                    </View>
                    <View style={{flex: 1}}>
                      <Text style={styles.sectorCardName}>{rec.sector}</Text>
                      <Text style={styles.sectorCardPlanet}>
                        🪐 {rec.ruling_planet} in {rec.planet_sign} • House {rec.planet_house}
                      </Text>
                    </View>
                    <View style={[styles.ratingPill, {backgroundColor: STRENGTH_COLOR(rec.combined_strength) + '22'}]}>
                      <Text style={[styles.ratingText, {color: STRENGTH_COLOR(rec.combined_strength)}]}>{rec.rating}</Text>
                    </View>
                  </View>

                  <View style={styles.strengthRow}>
                    <View style={styles.strengthCol}>
                      <Text style={styles.strengthColLabel}>Natal</Text>
                      <Text style={styles.strengthColValue}>{rec.natal_strength}</Text>
                    </View>
                    {rec.dasha_boost > 0 && (
                      <View style={styles.strengthCol}>
                        <Text style={styles.strengthColLabel}>Dasha Boost</Text>
                        <Text style={[styles.strengthColValue, {color: '#16A34A'}]}>+{rec.dasha_boost}</Text>
                      </View>
                    )}
                    <View style={styles.strengthCol}>
                      <Text style={styles.strengthColLabel}>Combined</Text>
                      <Text style={[styles.strengthColValue, {color: STRENGTH_COLOR(rec.combined_strength)}]}>{rec.combined_strength}</Text>
                    </View>
                  </View>

                  <View style={[styles.adviceBox, rec.dasha_boost > 0 ? {backgroundColor: '#F0FDF4'} : {}]}>
                    <Text style={styles.adviceText}>{rec.advice}</Text>
                  </View>
                  <Text style={styles.stocksText}>📌 {rec.stocks}</Text>
                </View>
              ))}

              {personalRecs.length === 0 && (
                <View style={styles.card}>
                  <Text style={styles.bodyText}>No personalized recommendations available. Generate your report with an active profile.</Text>
                </View>
              )}
            </>
          )}

          <TouchableOpacity style={[styles.button, {backgroundColor: '#6B7280', marginTop: 12}]} onPress={() => setResult(null)}>
            <Text style={styles.buttonText}>🔄 Re-analyze</Text>
          </TouchableOpacity>
        </>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#FFF8F0'},
  content: {padding: 16, paddingBottom: 40},
  header: {alignItems: 'center', paddingVertical: 16, marginBottom: 8},
  icon: {fontSize: 40, marginBottom: 6},
  title: {fontSize: 22, fontWeight: 'bold', color: THEME.primary, textAlign: 'center'},
  subtitle: {fontSize: 12, color: THEME.textLight, textAlign: 'center', marginTop: 4, lineHeight: 18},
  generatedBanner: {backgroundColor: '#DCFCE7', borderRadius: 8, padding: 10, marginBottom: 12},
  generatedText: {fontSize: 12, color: '#166534', fontWeight: '600'},
  tabRow: {flexDirection: 'row', marginBottom: 14, backgroundColor: '#F3F4F6', borderRadius: 10, padding: 4},
  tab: {flex: 1, paddingVertical: 8, alignItems: 'center', borderRadius: 8},
  tabActive: {backgroundColor: THEME.primary},
  tabText: {fontSize: 12, color: THEME.textLight, fontWeight: '600'},
  tabTextActive: {color: '#fff'},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginVertical: 10},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  // Dasha card
  dashaCard: {backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 10, elevation: 2, borderLeftWidth: 5},
  dashaLabel: {fontSize: 11, color: THEME.textLight, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 4},
  dashaName: {fontSize: 26, fontWeight: '800', marginBottom: 6},
  dashaRemaining: {fontSize: 13, color: THEME.textLight, marginBottom: 10},
  sentimentPill: {borderRadius: 20, paddingHorizontal: 12, paddingVertical: 6, alignSelf: 'flex-start'},
  sentimentText: {fontSize: 14, fontWeight: '700'},
  // Generic card
  card: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  cardLabel: {fontSize: 13, fontWeight: '700', color: THEME.text, marginBottom: 8},
  bodyText: {fontSize: 14, color: THEME.text, lineHeight: 22},
  bulletText: {fontSize: 14, color: THEME.text, lineHeight: 24},
  // Meter
  meterBg: {height: 8, backgroundColor: '#E5E7EB', borderRadius: 4, marginVertical: 8, overflow: 'hidden'},
  meterFill: {height: 8, borderRadius: 4},
  meterScore: {fontSize: 13, fontWeight: '700'},
  // Section headings
  sectionHeading: {fontSize: 18, fontWeight: '700', color: THEME.text, marginVertical: 10},
  sectionSubtitle: {fontSize: 12, color: THEME.textLight, marginBottom: 12, lineHeight: 18},
  sectorSubtitle: {fontSize: 12, color: THEME.textLight, marginBottom: 10, lineHeight: 18},
  // Sector cards
  sectorCard: {backgroundColor: '#fff', borderRadius: 12, padding: 14, marginBottom: 10, elevation: 2},
  sectorCardTop: {flexDirection: 'row', alignItems: 'flex-start', marginBottom: 8, gap: 8},
  sectorRankBadge: {width: 28, height: 28, borderRadius: 14, backgroundColor: THEME.primary + '22', alignItems: 'center', justifyContent: 'center'},
  sectorRankText: {fontSize: 11, fontWeight: '700', color: THEME.primary},
  sectorCardName: {fontSize: 15, fontWeight: '700', color: THEME.text, flex: 1, flexWrap: 'wrap'},
  sectorCardPlanet: {fontSize: 12, color: THEME.textLight, marginTop: 2},
  ratingPill: {borderRadius: 12, paddingHorizontal: 10, paddingVertical: 4, alignSelf: 'flex-start'},
  ratingText: {fontSize: 11, fontWeight: '700'},
  sectorReason: {fontSize: 12, color: '#374151', lineHeight: 18, marginTop: 6},
  stocksText: {fontSize: 12, color: '#1D4ED8', marginTop: 6, lineHeight: 18},
  // Strength row in personalized
  strengthRow: {flexDirection: 'row', marginVertical: 8, borderTopWidth: 1, borderTopColor: '#F3F4F6', paddingTop: 8},
  strengthCol: {flex: 1, alignItems: 'center'},
  strengthColLabel: {fontSize: 11, color: THEME.textLight},
  strengthColValue: {fontSize: 22, fontWeight: '700', color: THEME.text},
  // Advice
  adviceBox: {backgroundColor: '#F1F5F9', borderRadius: 8, padding: 10, marginTop: 6},
  adviceText: {fontSize: 12, color: '#1e3a5f', lineHeight: 18},
  // Wealth house rows
  wealthRow: {flexDirection: 'row', alignItems: 'center', paddingVertical: 6, borderBottomWidth: 1, borderBottomColor: '#F3F4F6', gap: 8},
  wealthPlanet: {fontSize: 13, fontWeight: '700', color: THEME.text, width: 72},
  wealthHouse: {fontSize: 12, color: THEME.textLight, flex: 1},
  wealthSign: {fontSize: 12, color: THEME.text, width: 70},
  wealthStrBadge: {borderRadius: 12, paddingHorizontal: 10, paddingVertical: 4},
  wealthStrText: {fontSize: 12, fontWeight: '700'},
});

export default FinancialScreen;
