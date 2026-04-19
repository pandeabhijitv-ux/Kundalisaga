/**
 * Remedies Screen - Enhanced with Ayurvedic, Yoga, Muhurat & Color Therapy
 * Comprehensive remedy recommendations for all 9 planets + Rahu/Ketu
 */
import React, {useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import {THEME} from '../../constants/theme';
import {getRemedies} from '../../services/PythonBridge';
import {getActiveProfileWithChart} from '../../services/profileData';

type RemedyCategory = 'vedic' | 'ayurvedic' | 'yoga' | 'muhurat' | 'color';

const REMEDY_CATEGORIES: {label: string; value: RemedyCategory; icon: string}[] = [
  {label: '🕉️ Vedic', value: 'vedic', icon: '🕉️'},
  {label: '🌿 Ayurvedic', value: 'ayurvedic', icon: '🌿'},
  {label: '🧘 Yoga', value: 'yoga', icon: '🧘'},
  {label: '⏰ Muhurat', value: 'muhurat', icon: '⏰'},
  {label: '🌈 Colors', value: 'color', icon: '🌈'},
];

const RemediesScreen = () => {
  const [loading, setLoading] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<RemedyCategory>('vedic');
  const [remedyData, setRemedyData] = useState<any>(null);
  const [profileWithChart, setProfileWithChart] = useState<any>(null);

  React.useEffect(() => {
    loadProfile();
  }, []);

  const loadProfile = async () => {
    try {
      const data = await getActiveProfileWithChart();
      setProfileWithChart(data);
    } catch (err) {
      console.log('No active profile');
    }
  };

  const handleLoadRemedies = async () => {
    if (!profileWithChart?.chart) {
      Alert.alert('No Profile', 'Please create and select a profile first to get personalized remedies');
      return;
    }

    setLoading(true);
    try {
      const response = await getRemedies(profileWithChart.chart);
      if ((response as any)?.error) {
        Alert.alert('Remedy Error', (response as any).error);
      }
      setRemedyData(response);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Failed to load remedies');
    } finally {
      setLoading(false);
    }
  };

  const renderVedicRemedies = () => {
    if (!remedyData ||!remedyData.gemstones) return null;
    return (
      <View>
        <RemedySection title="💎 Gemstones" items={remedyData.gemstones} />
        <RemedySection title="📿 Mantras" items={remedyData.mantras} />
        <RemedySection title="🙏 Fasting & Charity" items={remedyData.fasting || []} />
        <RemedySection title="⚡ Daily Practices" items={remedyData.daily_practices || []} />
      </View>
    );
  };

  const renderAyurvedicRemedies = () => {
    if (!remedyData?.ayurvedic) return null;
    return (
      <View>
        <Text style={styles.categoryInfo}>🌿 Ayurvedic herbs and treatments to balance planetary energies</Text>
        {Object.entries(remedyData.ayurvedic).map((entry: any) => (
          <RemedyDetailsCard key={entry[0]} title={`${entry[0]} Treatments`} details={entry[1]} />
        ))}
      </View>
    );
  };

  const renderYogaRemedies = () => {
    if (!remedyData?.yoga) return null;
    return (
      <View>
        <Text style={styles.categoryInfo}>🧘 Yoga asanas and pranayama for planetary balance</Text>
        {Object.entries(remedyData.yoga).map((entry: any) => (
          <RemedyDetailsCard key={entry[0]} title={`${entry[0]} Yoga`} details={entry[1]} />
        ))}
      </View>
    );
  };

  const renderMuhuratRemedies = () => {
    if (!remedyData?.muhurat) return null;
    return (
      <View>
        <Text style={styles.categoryInfo}>⏰ Best auspicious timings to start remedies</Text>
        {Object.entries(remedyData.muhurat).map((entry: any) => (
          <RemedyDetailsCard key={entry[0]} title={`${entry[0]} Muhurat`} details={entry[1]} />
        ))}
      </View>
    );
  };

  const renderColorRemedies = () => {
    if (!remedyData?.color) return null;
    return (
      <View>
        <Text style={styles.categoryInfo}>🌈 Colors, gemstones, and objects to attract planetary energy</Text>
        {Object.entries(remedyData.color).map((entry: any) => (
          <RemedyDetailsCard key={entry[0]} title={`${entry[0]} Color Therapy`} details={entry[1]} />
        ))}
      </View>
    );
  };

  const getCategoryContent = () => {
    switch (selectedCategory) {
      case 'vedic': return renderVedicRemedies();
      case 'ayurvedic': return renderAyurvedicRemedies();
      case 'yoga': return renderYogaRemedies();
      case 'muhurat': return renderMuhuratRemedies();
      case 'color': return renderColorRemedies();
      default: return null;
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {/* Profile Context */}
      {profileWithChart ? (
        <View style={styles.profileBanner}>
          <Text style={styles.profileName}>👤 {profileWithChart.profile.name}</Text>
          <Text style={styles.profileDetails}>{profileWithChart.profile.date}</Text>
        </View>
      ) : (
        <View style={styles.warningBanner}>
          <Text style={styles.warningText}>⚠️ No profile selected for personalized remedies</Text>
        </View>
      )}

      <Text style={styles.title}>🔮 Personalized Astrological Remedies</Text>

      <View style={styles.card}>
        <Text style={styles.helper}>
          Explore 5 powerful remedy systems: Vedic mantras, Ayurvedic herbs, Yoga practices, Muhurat timings, and Color therapy—tailored to your birth chart.
        </Text>
        <TouchableOpacity 
          style={[styles.button, !profileWithChart?.chart && styles.buttonDisabled]} 
          onPress={handleLoadRemedies} 
          disabled={loading || !profileWithChart?.chart}>
          {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>✨ Load Personalized Remedies</Text>}
        </TouchableOpacity>
      </View>

      {remedyData && (
        <>
          {/* Category Selector */}
          <View style={styles.categorySelector}>
            {REMEDY_CATEGORIES.map(cat => (
              <TouchableOpacity
                key={cat.value}
                style={[styles.categoryTab, selectedCategory === cat.value && styles.categoryTabActive]}
                onPress={() => setSelectedCategory(cat.value)}>
                <Text style={[styles.categoryTabText, selectedCategory === cat.value && styles.categoryTabTextActive]}>
                  {cat.label}
                </Text>
              </TouchableOpacity>
            ))}
          </View>

          {/* Remedy Content */}
          <View style={styles.remedyContent}>
            {getCategoryContent()}
          </View>
        </>
      )}
    </ScrollView>
  );
};

const RemedySection = ({title, items}: {title: string; items: any[]}) => {
  if (!items || items.length === 0) return null;
  return (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {items.map((item, idx) => (
        <Text key={idx} style={styles.row}>
          • {typeof item === 'string' ? item : formatItem(item)}
        </Text>
      ))}
    </View>
  );
};

const RemedyDetailsCard = ({title, details}: {title: string; details: any[]}) => {
  if (!details || details.length === 0) return null;
  return (
    <View style={styles.detailsCard}>
      <Text style={styles.detailsTitle}>{title}</Text>
      {details.map((detail, idx) => (
        <View key={idx} style={styles.detailItem}>
          {Object.entries(detail).map(([key, value]: any) => (
            <Text key={key} style={styles.detailText}>
              <Text style={styles.detailLabel}>{formatLabel(key)}: </Text>
              {typeof value === 'string' ? value : JSON.stringify(value)}
            </Text>
          ))}
        </View>
      ))}
    </View>
  );
};

const formatLabel = (label: string): string => {
  return label.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
};

const formatItem = (item: any): string => {
  if (!item) return '';
  return item.name || item.mantra || item.day || item.description || item.remedy || JSON.stringify(item).substring(0, 50);
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
  profileBanner: {
    backgroundColor: '#E8F4F8',
    borderRadius: 10,
    padding: 12,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: THEME.primary,
  },
  profileName: {
    fontSize: 14,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 4,
  },
  profileDetails: {
    fontSize: 12,
    color: THEME.textLight,
  },
  warningBanner: {
    backgroundColor: '#FEE2E2',
    borderRadius: 10,
    padding: 12,
    marginBottom: 12,
    borderLeftWidth: 4,
    borderLeftColor: '#DC2626',
  },
  warningText: {
    fontSize: 12,
    color: '#991B1B',
    fontWeight: '500',
  },
  title: {
    fontSize: 22,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 12,
  },
  card: {
    backgroundColor: THEME.card,
    borderRadius: 12,
    padding: 14,
    marginBottom: 12,
  },
  helper: {
    fontSize: 12,
    color: THEME.textLight,
    lineHeight: 18,
    marginBottom: 12,
  },
  button: {
    backgroundColor: THEME.primary,
    borderRadius: 10,
    paddingVertical: 12,
    paddingHorizontal: 14,
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.5,
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
    fontSize: 14,
  },
  categorySelector: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 8,
    marginBottom: 16,
  },
  categoryTab: {
    borderWidth: 1,
    borderColor: THEME.primary,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 8,
    backgroundColor: '#fff',
  },
  categoryTabActive: {
    backgroundColor: THEME.primary,
  },
  categoryTabText: {
    fontSize: 12,
    color: THEME.primary,
    fontWeight: '600',
  },
  categoryTabTextActive: {
    color: '#fff',
  },
  remedyContent: {
    backgroundColor: THEME.card,
    borderRadius: 12,
    padding: 14,
  },
  categoryInfo: {
    fontSize: 12,
    color: THEME.textLight,
    fontStyle: 'italic',
    marginBottom: 12,
    paddingBottom: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#E0E0E0',
  },
  section: {
    marginBottom: 14,
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: THEME.primary,
    marginBottom: 8,
  },
  row: {
    fontSize: 12,
    color: THEME.text,
    lineHeight: 18,
    marginBottom: 6,
  },
  detailsCard: {
    backgroundColor: '#F9FAFB',
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    borderLeftWidth: 3,
    borderLeftColor: THEME.primary,
  },
  detailsTitle: {
    fontSize: 13,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 10,
  },
  detailItem: {
    marginBottom: 8,
  },
  detailText: {
    fontSize: 11,
    color: THEME.text,
    lineHeight: 16,
    marginBottom: 4,
  },
  detailLabel: {
    fontWeight: '600',
    color: THEME.primary,
  },
});

export default RemediesScreen;
