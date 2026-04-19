/**
 * Home Screen
 * Main dashboard with quick access to all features
 */

import React, {useEffect, useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Modal,
} from 'react-native';
import {THEME} from '../../constants/theme';
import {useAuth} from '../../contexts/AuthContext';
import {getCurrentDasha} from '../../services/PythonBridge';
import {getProfiles} from '../../services/profileData';

const EMOJI_ICONS: {[key: string]: string} = {
  'Get Remedies': '🕉️',
  'Ask Question': '❓',
  'Career': '💼',
  'Financial': '📊',
  'Gemstones': '💎',
  'Numerology': '🔢',
  'Matchmaking': '❤️',
  'Muhurat': '⏰',
  'Varshaphal': '📅',
  'Dasha Analysis': '🪐',
  'Name Guide': '✨',
  'Soulmate': '💑',
};

const ACTION_LABELS: {[key: string]: string} = {
  'Get Remedies': 'View',
  'Ask Question': 'Ask',
  'Career': 'Analyze',
  'Financial': 'View',
  'Gemstones': 'View',
  'Numerology': 'View',
  'Matchmaking': 'Check',
  'Muhurat': 'Find',
  'Varshaphal': 'View',
  'Dasha Analysis': 'Analyze',
  'Name Guide': 'Suggest',
  'Soulmate': 'Find',
};

const HomeScreen = ({navigation}: any) => {
  const {user, isGuest, logout} = useAuth();
  const [currentDasha, setCurrentDasha] = useState<any>(null);
  const [hasProfiles, setHasProfiles] = useState<boolean | null>(null); // null = loading
  const [showNoProfileModal, setShowNoProfileModal] = useState(false);

  useEffect(() => {
    checkProfiles();
    loadDashaInfo();
  }, []);

  // Re-check profiles when screen is focused
  useEffect(() => {
    const unsubscribe = navigation.addListener('focus', () => {
      checkProfiles();
    });
    return unsubscribe;
  }, [navigation]);

  const checkProfiles = async () => {
    try {
      const profiles = await getProfiles();
      setHasProfiles(profiles.length > 0);
    } catch {
      setHasProfiles(false);
    }
  };

  const loadDashaInfo = async () => {
    try {
      const dasha = await getCurrentDasha('1990-01-01');
      if (dasha) {
        setCurrentDasha(dasha);
      }
    } catch (error) {
      console.error('Error loading dasha:', error);
    }
  };

  const features = [
    {
      title: 'Ask Question',
      color: '#87CEEB',
      screen: 'Ask',
      description: 'Instant answers about career, wealth, relationships',
    },
    {
      title: 'Career',
      color: '#6A5ACD',
      screen: 'Career',
      description: 'Best career & profession from your chart',
    },
    {
      title: 'Financial',
      color: '#7B68EE',
      screen: 'Financial',
      description: 'Wealth timing & financial planetary transits',
    },
    {
      title: 'Gemstones',
      color: '#FF69B4',
      screen: 'Gemstone',
      description: 'Personalized recommendations from chart analysis',
    },
    {
      title: 'Numerology',
      color: '#90EE90',
      screen: 'Numerology',
      description: 'Life Path, Expression & Soul numbers',
    },
    {
      title: 'Matchmaking',
      color: '#FF6B35',
      screen: 'Matchmaking',
      description: 'Kundali Milan & compatibility analysis',
    },
    {
      title: 'Muhurat',
      color: '#F9C74F',
      screen: 'Muhurat',
      description: 'Auspicious timing for important events',
    },
    {
      title: 'Varshaphal',
      color: '#00CED1',
      screen: 'Varshaphal',
      description: 'Annual predictions & yearly forecast',
    },
    {
      title: 'Dasha Analysis',
      color: '#9370DB',
      screen: 'Dasha',
      description: 'Detailed planetary period predictions',
    },
    {
      title: 'Get Remedies',
      color: '#FF8FA3',
      screen: 'Remedies',
      description: 'Lal Kitab remedies & lifestyle changes',
    },
    {
      title: 'Name Guide',
      color: '#20B2AA',
      screen: 'NameRecommendation',
      description: 'Lucky names based on nakshatra',
    },
    {
      title: 'Soulmate',
      color: '#E75480',
      screen: 'Soulmate',
      description: 'Soulmate traits & relationship insights',
    },
  ];

  const handleFeaturePress = (feature: (typeof features)[0]) => {
    if (!hasProfiles) {
      setShowNoProfileModal(true);
      return;
    }
    navigation.navigate(feature.screen);
  };

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      {text: 'Cancel', style: 'cancel'},
      {text: 'Logout', onPress: logout},
    ]);
  };

  return (
    <ScrollView style={styles.container}>
      {/* No-profile gate modal */}
      <Modal
        visible={showNoProfileModal}
        transparent
        animationType="fade"
        onRequestClose={() => setShowNoProfileModal(false)}>
        <View style={styles.modalOverlay}>
          <View style={styles.modalBox}>
            <Text style={styles.modalEmoji}>👤</Text>
            <Text style={styles.modalTitle}>Profile Required</Text>
            <Text style={styles.modalMessage}>
              To use astrology services, please create your birth profile first.{'\n\n'}
              Add your name, date of birth, time and place so we can calculate your personalised chart.
            </Text>
            <TouchableOpacity
              style={styles.modalPrimaryBtn}
              onPress={() => {
                setShowNoProfileModal(false);
                navigation.navigate('Profiles');
              }}>
              <Text style={styles.modalPrimaryBtnText}>Create Profile →</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.modalSecondaryBtn}
              onPress={() => setShowNoProfileModal(false)}>
              <Text style={styles.modalSecondaryBtnText}>Maybe Later</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      <View style={styles.header}>
        <Text style={styles.mantra}>🕉️ ॐ गं गणपतये नमः 🕉️</Text>
        <Text style={styles.title}>KundaliSaga</Text>
        <Text style={styles.subtitle}>Vedic Astrology AI</Text>

        {isGuest ? (
          <View style={styles.guestBanner}>
            <Text style={styles.inlineEmoji}>ℹ️</Text>
            <Text style={styles.guestText}>Guest Mode - Limited Features</Text>
          </View>
        ) : (
          <View style={styles.userInfo}>
            <Text style={styles.inlineEmoji}>👤</Text>
            <Text style={styles.userName}>Welcome, {user?.name}!</Text>
          </View>
        )}
      </View>

      <View style={styles.content}>
        {/* Profile warning banner */}
        {hasProfiles === false && (
          <TouchableOpacity
            style={styles.profileBanner}
            onPress={() => navigation.navigate('Profiles')}>
            <Text style={styles.profileBannerIcon}>⚠️</Text>
            <View style={{flex: 1}}>
              <Text style={styles.profileBannerTitle}>No birth profile found</Text>
              <Text style={styles.profileBannerSub}>Tap here to create your profile and unlock all features</Text>
            </View>
            <Text style={styles.profileBannerArrow}>›</Text>
          </TouchableOpacity>
        )}

        <Text style={styles.sectionTitle}>Astrology Services</Text>
        <View style={styles.featuresGrid}>
          {features.map((feature, index) => (
            <TouchableOpacity
              key={index}
              style={[
                styles.featureCard,
                {backgroundColor: feature.color},
                !hasProfiles && styles.featureCardLocked,
              ]}
              onPress={() => handleFeaturePress(feature)}>
              {!hasProfiles && (
                <View style={styles.lockOverlay}>
                  <Text style={styles.lockIcon}>🔒</Text>
                </View>
              )}
              <Text style={styles.featureIconText}>{EMOJI_ICONS[feature.title] || '✨'}</Text>
              <Text style={styles.featureTitle}>{feature.title}</Text>
              <Text style={styles.featureDescriptionLight}>
                {feature.description}
              </Text>
              <View style={styles.actionBtn}>
                <Text style={styles.actionBtnText}>{ACTION_LABELS[feature.title] || 'View'}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {currentDasha && (
          <View style={styles.dashaCard}>
            <Text style={styles.dashaTitle}>Current Dasha</Text>
            <Text style={styles.dashaText}>
              Mahadasha: {currentDasha.mahadasha_name || currentDasha?.mahadasha?.planet || currentDasha.mahadasha}
            </Text>
            <Text style={styles.dashaText}>
              Antardasha: {currentDasha.antardasha_name || currentDasha?.antardasha?.planet || currentDasha.antardasha}
            </Text>
          </View>
        )}

        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.inlineEmoji}>🚪</Text>
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.background,
  },
  header: {
    padding: 20,
    alignItems: 'center',
    backgroundColor: THEME.card,
    borderBottomLeftRadius: 30,
    borderBottomRightRadius: 30,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  mantra: {fontSize: 20, color: THEME.primary, marginTop: 10},
  title: {fontSize: 28, fontWeight: 'bold', color: THEME.primary, marginTop: 10},
  subtitle: {fontSize: 14, color: THEME.textLight, marginTop: 5},
  inlineEmoji: {fontSize: 18},
  guestBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF3CD',
    padding: 10,
    borderRadius: 10,
    marginTop: 15,
  },
  guestText: {marginLeft: 10, color: THEME.warning, fontWeight: '600'},
  userInfo: {flexDirection: 'row', alignItems: 'center', marginTop: 15},
  userName: {marginLeft: 10, fontSize: 16, color: THEME.text, fontWeight: '600'},
  content: {padding: 20},
  sectionTitle: {fontSize: 20, fontWeight: 'bold', color: THEME.text, marginBottom: 15},
  // Profile banner
  profileBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF3CD',
    borderRadius: 12,
    padding: 14,
    marginBottom: 16,
    borderLeftWidth: 4,
    borderLeftColor: '#F59E0B',
  },
  profileBannerIcon: {fontSize: 22, marginRight: 10},
  profileBannerTitle: {fontSize: 14, fontWeight: '700', color: '#92400E'},
  profileBannerSub: {fontSize: 12, color: '#92400E', marginTop: 2},
  profileBannerArrow: {fontSize: 24, color: '#92400E', marginLeft: 8},
  // Features grid
  featuresGrid: {flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between'},
  featureCard: {
    width: '48%',
    padding: 15,
    borderRadius: 12,
    marginBottom: 15,
    minHeight: 140,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.15,
    shadowRadius: 4,
    elevation: 3,
    overflow: 'hidden',
  },
  featureCardLocked: {opacity: 0.55},
  lockOverlay: {
    position: 'absolute',
    top: 8,
    right: 8,
    zIndex: 10,
  },
  lockIcon: {fontSize: 16},
  featureIconText: {fontSize: 24},
  featureTitle: {fontSize: 15, fontWeight: 'bold', color: 'white', marginTop: 8},
  featureDescriptionLight: {
    fontSize: 11,
    color: 'rgba(255,255,255,0.85)',
    marginTop: 4,
    lineHeight: 15,
  },
  actionBtn: {
    marginTop: 10,
    backgroundColor: 'rgba(255,255,255,0.25)',
    borderRadius: 6,
    paddingVertical: 5,
    paddingHorizontal: 10,
    alignSelf: 'flex-start',
  },
  actionBtnText: {color: 'white', fontSize: 12, fontWeight: '600'},
  dashaCard: {
    backgroundColor: THEME.card,
    padding: 20,
    borderRadius: 15,
    marginTop: 20,
    borderLeftWidth: 4,
    borderLeftColor: THEME.primary,
  },
  dashaTitle: {fontSize: 18, fontWeight: 'bold', color: THEME.text, marginBottom: 10},
  dashaText: {fontSize: 14, color: THEME.textLight, marginTop: 5},
  logoutButton: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    padding: 15,
    marginTop: 30,
    borderRadius: 10,
    borderWidth: 1,
    borderColor: THEME.error,
  },
  logoutText: {marginLeft: 10, color: THEME.error, fontSize: 16, fontWeight: '600'},
  // Modal
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.55)',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  modalBox: {
    backgroundColor: '#fff',
    borderRadius: 20,
    padding: 28,
    alignItems: 'center',
    width: '100%',
    maxWidth: 360,
  },
  modalEmoji: {fontSize: 48, marginBottom: 12},
  modalTitle: {
    fontSize: 22,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 12,
    textAlign: 'center',
  },
  modalMessage: {
    fontSize: 14,
    color: THEME.textLight,
    textAlign: 'center',
    lineHeight: 22,
    marginBottom: 24,
  },
  modalPrimaryBtn: {
    backgroundColor: THEME.primary,
    borderRadius: 12,
    paddingVertical: 14,
    paddingHorizontal: 32,
    width: '100%',
    alignItems: 'center',
    marginBottom: 10,
  },
  modalPrimaryBtnText: {color: '#fff', fontWeight: '700', fontSize: 16},
  modalSecondaryBtn: {paddingVertical: 10},
  modalSecondaryBtnText: {color: THEME.textLight, fontSize: 14},
});

export default HomeScreen;

