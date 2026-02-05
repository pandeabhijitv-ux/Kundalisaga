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
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {THEME} from '../../../App';
import {useAuth} from '../../contexts/AuthContext';
import {getCurrentDasha} from '../../services/PythonBridge';

const HomeScreen = ({navigation}: any) => {
  const {user, isGuest, logout} = useAuth();
  const [currentDasha, setCurrentDasha] = useState<any>(null);

  useEffect(() => {
    loadDashaInfo();
  }, []);

  const loadDashaInfo = async () => {
    try {
      // Example: Load current dasha for logged in user
      if (user) {
        // const dasha = await getCurrentDasha('1990-01-01');
        // setCurrentDasha(dasha);
      }
    } catch (error) {
      console.error('Error loading dasha:', error);
    }
  };

  const features = [
    {
      title: 'Birth Chart',
      icon: 'chart-donut',
      color: '#FF6B35',
      screen: 'Horoscope',
      description: 'Calculate Vedic horoscope',
    },
    {
      title: 'Profiles',
      icon: 'account-group',
      color: '#F9C74F',
      screen: 'Profiles',
      description: 'Manage family profiles',
    },
    {
      title: 'Ask Question',
      icon: 'chat-question',
      color: '#4ECDC4',
      screen: 'Ask',
      description: 'Get astrological insights',
    },
    {
      title: 'Remedies',
      icon: 'meditation',
      color: '#95E1D3',
      screen: 'Remedies',
      description: 'Personalized solutions',
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
            <Icon name="information" size={20} color={THEME.warning} />
            <Text style={styles.guestText}>Guest Mode - Limited Features</Text>
          </View>
        ) : (
          <View style={styles.userInfo}>
            <Icon name="account-circle" size={24} color={THEME.primary} />
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
              onPress={() => navigation.navigate(feature.screen)}>
              <Icon name={feature.icon} size={40} color={feature.color} />
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
              Mahadasha: {currentDasha.mahadasha}
            </Text>
            <Text style={styles.dashaText}>
              Antardasha: {currentDasha.antardasha}
            </Text>
          </View>
        )}

        <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
          <Icon name="logout" size={20} color={THEME.error} />
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
