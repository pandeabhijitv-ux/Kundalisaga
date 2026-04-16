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
  'Birth Chart': '📜',
  Profiles: '👥',
  'Ask Question': '💬',
  Remedies: '🕉️',
  Numerology: '🔢',
  'Current Dasha': '🪐',
  'Knowledge Search': '📚',
  Compatibility: '❤️',
  'Career Guidance': '💼',
  'Financial Astrology': '💰',
  'Navagraha Mantras': '🎵',
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
      title: 'Birth Chart',
      color: '#FF6B35',
      screen: 'Horoscope',
      description: 'Calculate Vedic horoscope',
    },
    {
      title: 'Profiles',
      color: '#F9C74F',
      screen: 'Profiles',
      description: 'Manage family profiles',
    },
    {
      title: 'Ask Question',
      color: '#4ECDC4',
      screen: 'Ask',
      description: 'Get astrological insights',
    },
    {
      title: 'Remedies',
      color: '#95E1D3',
      screen: 'Remedies',
      description: 'Personalized solutions',
    },
    {
      title: 'Numerology',
      color: '#9C6ADE',
      screen: 'Numerology',
      description: 'Life path and destiny numbers',
    },
    {
      title: 'Current Dasha',
      color: '#5C7AEA',
      screen: 'Dasha',
      description: 'Mahadasha and antardasha',
    },
    {
      title: 'Knowledge Search',
      color: '#2A9D8F',
      screen: 'Ask',
      params: {preset: 'knowledge'},
      description: 'Search astrology knowledge base',
    },
    {
      title: 'Compatibility',
      color: '#E76F51',
      screen: 'Horoscope',
      params: {preset: 'compatibility'},
      description: 'Basic compatibility workflow',
    },
    {
      title: 'Career Guidance',
      color: '#457B9D',
      screen: 'Ask',
      params: {preset: 'career'},
      description: 'Career-focused question prompts',
    },
    {
      title: 'Financial Astrology',
      color: '#2B9348',
      screen: 'Ask',
      params: {preset: 'finance'},
      description: 'Money and timing insights',
    },
    {
      title: 'Navagraha Mantras',
      color: '#8D99AE',
      screen: 'Remedies',
      params: {preset: 'mantras'},
      description: 'Planetary mantra recommendations',
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
        <Text style={styles.sectionTitle}>Quick Access</Text>
        <View style={styles.featuresGrid}>
          {features.map((feature, index) => (
            <TouchableOpacity
              key={index}
              style={[styles.featureCard, {borderLeftColor: feature.color}]}
              onPress={() => navigation.navigate(feature.screen, feature.params)}>
              <View style={[styles.featureIconWrap, {backgroundColor: `${feature.color}20`}]}>
                <Text style={styles.featureIconText}>{EMOJI_ICONS[feature.title] || '✨'}</Text>
              </View>
              <Text style={styles.featureTitle}>{feature.title}</Text>
              <Text style={styles.featureDescription}>
                {feature.description}
              </Text>
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
    backgroundColor: THEME.card,
    padding: 15,
    borderRadius: 15,
    marginBottom: 15,
    alignItems: 'center',
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: {width: 0, height: 2},
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  featureTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    color: THEME.text,
    marginTop: 10,
    textAlign: 'center',
  },
  featureIconWrap: {
    width: 56,
    height: 56,
    borderRadius: 28,
    alignItems: 'center',
    justifyContent: 'center',
  },
  featureIconText: {
    fontSize: 30,
  },
  featureDescription: {
    fontSize: 12,
    color: THEME.textLight,
    marginTop: 5,
    textAlign: 'center',
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
