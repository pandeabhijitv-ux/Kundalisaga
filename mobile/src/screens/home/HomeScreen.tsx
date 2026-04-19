/**
 * Home Screen
 * Main dashboard with quick access to all features
 */

import React, {useEffect, useState} from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
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
import {useAppSettings} from '../../contexts/AppSettingsContext';
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
  'Stotras & Prayers': '🙏',
  'Name Guide': '✨',
  'Soulmate': '💑',
};

const MENU_TIP_SEEN_KEY = 'home_menu_tip_seen';

const HomeScreen = ({navigation}: any) => {
  const {user, isGuest, logout} = useAuth();
  const {t} = useAppSettings();
  const [currentDasha, setCurrentDasha] = useState<any>(null);
  const [hasProfiles, setHasProfiles] = useState<boolean | null>(null); // null = loading
  const [showNoProfileModal, setShowNoProfileModal] = useState(false);
  const [showMenuTip, setShowMenuTip] = useState(false);

  useEffect(() => {
    checkProfiles();
    loadDashaInfo();
    loadMenuTipPreference();
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

  const loadMenuTipPreference = async () => {
    try {
      const seen = await AsyncStorage.getItem(MENU_TIP_SEEN_KEY);
      setShowMenuTip(seen !== '1');
    } catch {
      setShowMenuTip(true);
    }
  };

  const dismissMenuTip = async () => {
    setShowMenuTip(false);
    try {
      await AsyncStorage.setItem(MENU_TIP_SEEN_KEY, '1');
    } catch {
      // No-op: tip can reappear if storage is unavailable.
    }
  };

  const features = [
    {
      title: t('ask_question'),
      color: '#87CEEB',
      screen: 'Ask',
      description: t('feature_ask_question_desc'),
      iconKey: 'Ask Question',
      actionText: t('action_ask'),
    },
    {
      title: t('career_guidance'),
      color: '#6A5ACD',
      screen: 'Career',
      description: t('feature_career_desc'),
      iconKey: 'Career',
      actionText: t('action_analyze'),
    },
    {
      title: t('financial_outlook'),
      color: '#7B68EE',
      screen: 'Financial',
      description: t('feature_financial_desc'),
      iconKey: 'Financial',
      actionText: t('action_view'),
    },
    {
      title: t('gemstone_guide'),
      color: '#FF69B4',
      screen: 'Gemstone',
      description: t('feature_gemstone_desc'),
      iconKey: 'Gemstones',
      actionText: t('action_view'),
    },
    {
      title: t('numerology'),
      color: '#90EE90',
      screen: 'Numerology',
      description: t('feature_numerology_desc'),
      iconKey: 'Numerology',
      actionText: t('action_view'),
    },
    {
      title: t('matchmaking'),
      color: '#FF6B35',
      screen: 'Matchmaking',
      description: t('feature_matchmaking_desc'),
      iconKey: 'Matchmaking',
      actionText: t('action_check'),
    },
    {
      title: t('muhurat_finder'),
      color: '#F9C74F',
      screen: 'Muhurat',
      description: t('feature_muhurat_desc'),
      iconKey: 'Muhurat',
      actionText: t('action_find'),
    },
    {
      title: t('varshaphal'),
      color: '#00CED1',
      screen: 'Varshaphal',
      description: t('feature_varshaphal_desc'),
      iconKey: 'Varshaphal',
      actionText: t('action_view'),
    },
    {
      title: t('dasha_analysis'),
      color: '#9370DB',
      screen: 'Dasha',
      description: t('feature_dasha_desc'),
      iconKey: 'Dasha Analysis',
      actionText: t('action_analyze'),
    },
    {
      title: t('stotras_prayers'),
      color: '#4DB6AC',
      screen: 'Stotras',
      description: t('feature_stotras_desc'),
      iconKey: 'Stotras & Prayers',
      actionText: t('action_open'),
    },
    {
      title: t('remedies'),
      color: '#FF8FA3',
      screen: 'Remedies',
      description: t('feature_remedies_desc'),
      iconKey: 'Get Remedies',
      actionText: t('action_view'),
    },
    {
      title: t('name_recommendation'),
      color: '#20B2AA',
      screen: 'NameRecommendation',
      description: t('feature_name_guide_desc'),
      iconKey: 'Name Guide',
      actionText: t('action_suggest'),
    },
    {
      title: t('soulmate_analysis'),
      color: '#E75480',
      screen: 'Soulmate',
      description: t('feature_soulmate_desc'),
      iconKey: 'Soulmate',
      actionText: t('action_find'),
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
    Alert.alert(t('logout'), t('confirm_logout'), [
      {text: t('cancel'), style: 'cancel'},
      {text: t('logout'), onPress: logout},
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
            <Text style={styles.modalTitle}>{t('profile_required')}</Text>
            <Text style={styles.modalMessage}>
              {t('create_profile_first')}{'\n\n'}
              {t('add_birth_details')}
            </Text>
            <TouchableOpacity
              style={styles.modalPrimaryBtn}
              onPress={() => {
                setShowNoProfileModal(false);
                navigation.navigate('Profiles');
              }}>
              <Text style={styles.modalPrimaryBtnText}>{t('create_profile')} →</Text>
            </TouchableOpacity>
            <TouchableOpacity
              style={styles.modalSecondaryBtn}
              onPress={() => setShowNoProfileModal(false)}>
              <Text style={styles.modalSecondaryBtnText}>{t('maybe_later')}</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>

      <View style={styles.header}>
        <Text style={styles.mantra}>🕉️ ॐ गं गणपतये नमः 🕉️</Text>
        <Text style={styles.title}>KundaliSaga</Text>
        <Text style={styles.subtitle}>{t('vedic_astrology_ai')}</Text>

        {isGuest ? (
          <View style={styles.guestBanner}>
            <Text style={styles.inlineEmoji}>ℹ️</Text>
            <Text style={styles.guestText}>{t('guest_mode_limited')}</Text>
          </View>
        ) : (
          <View style={styles.userInfo}>
            <Text style={styles.inlineEmoji}>👤</Text>
            <Text style={styles.userName}>{t('welcome_user')}, {user?.name}!</Text>
          </View>
        )}
      </View>

      <View style={styles.content}>
        {showMenuTip && (
          <View style={styles.menuTipCard}>
            <Text style={styles.menuTipIcon}>☰</Text>
            <View style={styles.menuTipTextWrap}>
              <Text style={styles.menuTipTitle}>{t('menu_tip_title')}</Text>
              <Text style={styles.menuTipBody}>{t('menu_tip_body')}</Text>
            </View>
            <TouchableOpacity onPress={dismissMenuTip} style={styles.menuTipBtn}>
              <Text style={styles.menuTipBtnText}>{t('menu_tip_dismiss')}</Text>
            </TouchableOpacity>
          </View>
        )}

        {/* Profile warning banner */}
        {hasProfiles === false && (
          <TouchableOpacity
            style={styles.profileBanner}
            onPress={() => navigation.navigate('Profiles')}>
            <Text style={styles.profileBannerIcon}>⚠️</Text>
            <View style={{flex: 1}}>
              <Text style={styles.profileBannerTitle}>{t('no_birth_profile_found')}</Text>
              <Text style={styles.profileBannerSub}>{t('create_profile_unlock_features')}</Text>
            </View>
            <Text style={styles.profileBannerArrow}>›</Text>
          </TouchableOpacity>
        )}

        <Text style={styles.sectionTitle}>{t('astrology_services')}</Text>
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
              <Text style={styles.featureIconText}>{EMOJI_ICONS[feature.iconKey] || '✨'}</Text>
              <Text style={styles.featureTitle}>{feature.title}</Text>
              <Text style={styles.featureDescriptionLight}>
                {feature.description}
              </Text>
              <View style={styles.actionBtn}>
                <Text style={styles.actionBtnText}>{feature.actionText || t('action_view')}</Text>
              </View>
            </TouchableOpacity>
          ))}
        </View>

        {currentDasha && (
          <View style={styles.dashaCard}>
            <Text style={styles.dashaTitle}>{t('current_dasha')}</Text>
            <Text style={styles.dashaText}>
              {t('mahadasha')}: {currentDasha.mahadasha_name || currentDasha?.mahadasha?.planet || currentDasha.mahadasha}
            </Text>
            <Text style={styles.dashaText}>
              {t('antardasha')}: {currentDasha.antardasha_name || currentDasha?.antardasha?.planet || currentDasha.antardasha}
            </Text>
          </View>
        )}

        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Text style={styles.inlineEmoji}>🚪</Text>
          <Text style={styles.logoutText}>{t('logout')}</Text>
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
  menuTipCard: {
    backgroundColor: '#EEF6FF',
    borderRadius: 12,
    padding: 12,
    marginBottom: 14,
    borderLeftWidth: 4,
    borderLeftColor: '#1D4ED8',
  },
  menuTipIcon: {
    fontSize: 22,
    marginBottom: 4,
  },
  menuTipTextWrap: {
    marginBottom: 8,
  },
  menuTipTitle: {
    fontSize: 14,
    fontWeight: '700',
    color: '#1E3A8A',
    marginBottom: 4,
  },
  menuTipBody: {
    fontSize: 12,
    color: '#1E3A8A',
    lineHeight: 18,
  },
  menuTipBtn: {
    alignSelf: 'flex-start',
    backgroundColor: '#1D4ED8',
    paddingHorizontal: 10,
    paddingVertical: 6,
    borderRadius: 8,
  },
  menuTipBtnText: {
    color: '#fff',
    fontSize: 12,
    fontWeight: '600',
  },
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

