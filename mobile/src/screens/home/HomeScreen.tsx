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
} from 'react-native';
import {THEME} from '../../constants/theme';
import {useAuth} from '../../contexts/AuthContext';
import {getCurrentDasha} from '../../services/PythonBridge';

const EMOJI_ICONS: {[key: string]: string} = {
  'Get Remedies': '🕉️',
  'Ask Question': '❓',
  'Financial': '📊',
  'Gemstones': '💎',
  'Numerology': '🔢',
  'Matchmaking': '❤️',
  'Muhurat': '⏰',
  'Varshaphal': '📅',
  'Dasha Analysis': '🪐',
  'Name Guide': '✨',
};

const ACTION_LABELS: {[key: string]: string} = {
  'Get Remedies': 'View',
  'Ask Question': 'Ask',
  'Financial': 'View',
  'Gemstones': 'View',
  'Numerology': 'View',
  'Matchmaking': 'Check',
  'Muhurat': 'Find',
  'Varshaphal': 'View',
  'Dasha Analysis': 'Analyze',
  'Name Guide': 'Suggest',
};

const HomeScreen = ({navigation}: any) => {
  const {user, isGuest, logout} = useAuth();
  const [currentDasha, setCurrentDasha] = useState<any>(null);

  useEffect(() => {
    loadDashaInfo();
  }, []);

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
      title: 'Get Remedies',
      color: '#FF8FA3',
      screen: 'Remedies',
      description: 'Lal Kitab remedies & lifestyle changes',
    },
    {
      title: 'Ask Question',
      color: '#87CEEB',
      screen: 'Ask',
      description: 'Instant answers about career, wealth, relationships',
    },
    {
      title: 'Financial',
      color: '#7B68EE',
      screen: 'Ask',
      params: {preset: 'finance'},
      description: 'Market trends using planetary transits',
    },
    {
      title: 'Gemstones',
      color: '#FF69B4',
      screen: 'Ask',
      params: {preset: 'gemstones'},
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
      screen: 'Ask',
      params: {preset: 'matchmaking'},
      description: 'Kundali Milan & compatibility analysis',
    },
    {
      title: 'Muhurat',
      color: '#F9C74F',
      screen: 'Ask',
      params: {preset: 'muhurat'},
      description: 'Auspicious timing for important events',
    },
    {
      title: 'Varshaphal',
      color: '#00CED1',
      screen: 'Ask',
      params: {preset: 'varshaphal'},
      description: 'Annual predictions & yearly forecast',
    },
    {
      title: 'Dasha Analysis',
      color: '#9370DB',
      screen: 'Dasha',
      description: 'Detailed planetary period predictions',
    },
    {
      title: 'Name Guide',
      color: '#20B2AA',
      screen: 'Ask',
      params: {preset: 'name'},
      description: 'Lucky names based on numerology',
    },
  ];

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      {text: 'Cancel', style: 'cancel'},
      {text: 'Logout', onPress: logout},
    ]);
  };

  return (
    <ScrollView style={styles.container}>
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
        <Text style={styles.sectionTitle}>Welcome to KundaliSaga</Text>
        <View style={styles.featuresGrid}>
          {features.map((feature, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.featureCard, {backgroundColor: feature.color}]}
              onPress={() => navigation.navigate(feature.screen, feature.params)}>
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
  mantra: {
    fontSize: 20,
    color: THEME.primary,
    marginTop: 10,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: THEME.primary,
    marginTop: 10,
  },
  subtitle: {
    fontSize: 14,
    color: THEME.textLight,
    marginTop: 5,
  },
  inlineEmoji: {
    fontSize: 18,
  },
  guestBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF3CD',
    padding: 10,
    borderRadius: 10,
    marginTop: 15,
  },
  guestText: {
    marginLeft: 10,
    color: THEME.warning,
    fontWeight: '600',
  },
  userInfo: {
    flexDirection: 'row',
    alignItems: 'center',
    marginTop: 15,
  },
  userName: {
    marginLeft: 10,
    fontSize: 16,
    color: THEME.text,
    fontWeight: '600',
  },
  content: {
    padding: 20,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: THEME.text,
    marginBottom: 15,
  },
  featuresGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
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
  },
  featureTitle: {
    fontSize: 15,
    fontWeight: 'bold',
    color: 'white',
    marginTop: 8,
  },
  featureIconText: {
    fontSize: 24,
  },
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
  actionBtnText: {
    color: 'white',
    fontSize: 12,
    fontWeight: '600',
  },
  dashaCard: {
    backgroundColor: THEME.card,
    padding: 20,
    borderRadius: 15,
    marginTop: 20,
    borderLeftWidth: 4,
    borderLeftColor: THEME.primary,
  },
  dashaTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: THEME.text,
    marginBottom: 10,
  },
  dashaText: {
    fontSize: 14,
    color: THEME.textLight,
    marginTop: 5,
  },
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
  logoutText: {
    marginLeft: 10,
    color: THEME.error,
    fontSize: 16,
    fontWeight: '600',
  },
});

export default HomeScreen;
