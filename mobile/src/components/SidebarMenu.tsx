/**
 * Sidebar Menu - matches PWA navigation sidebar
 * Pure React Native implementation, no external nav libraries needed
 */

import React, {useRef, useEffect} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Modal,
  Animated,
  Dimensions,
  TouchableWithoutFeedback,
} from 'react-native';
import {useNavigation} from '@react-navigation/native';
import {THEME} from '../constants/theme';
import {useAuth} from '../contexts/AuthContext';

const {width: SCREEN_WIDTH} = Dimensions.get('window');
const SIDEBAR_WIDTH = SCREEN_WIDTH * 0.78;

interface NavItem {
  label: string;
  icon: string;
  screen: string;
  params?: object;
}

const NAV_ITEMS: NavItem[] = [
  {label: 'Home', icon: '🏠', screen: 'Home'},
  {label: 'User Profiles', icon: '👤', screen: 'Profiles'},
  {label: 'Horoscope', icon: '🪐', screen: 'Horoscope'},
  {label: 'Ask Question', icon: '💬', screen: 'Ask'},
  {label: 'Remedies', icon: '🕉️', screen: 'Remedies'},
  {label: 'Career Guidance', icon: '💼', screen: 'Career'},
  {label: 'Financial Outlook', icon: '📊', screen: 'Financial'},
  {label: 'Gemstone Guide', icon: '💎', screen: 'Gemstone'},
  {label: 'Numerology', icon: '🔢', screen: 'Numerology'},
  {label: 'Matchmaking', icon: '💑', screen: 'Matchmaking'},
  {label: 'Soulmate Analysis', icon: '💕', screen: 'Soulmate'},
  {label: 'Muhurat Finder', icon: '⏰', screen: 'Muhurat'},
  {label: 'Varshaphal', icon: '📅', screen: 'Varshaphal'},
  {label: 'Dasha Analysis', icon: '🪐', screen: 'Dasha'},
  {label: 'Name Recommendation', icon: '✨', screen: 'NameRecommendation'},
  {label: 'Buy Credits', icon: '💳', screen: 'BuyCredits'},
  {label: 'Settings', icon: '⚙️', screen: 'Settings'},
  {label: 'Stotras & Prayers', icon: '🙏', screen: 'Stotras'},
];

interface Props {
  visible: boolean;
  onClose: () => void;
  currentScreen?: string;
}

const SidebarMenu = ({visible, onClose, currentScreen}: Props) => {
  const {user, isGuest, logout} = useAuth();
  const navigation = useNavigation<any>();
  const slideAnim = useRef(new Animated.Value(-SIDEBAR_WIDTH)).current;

  useEffect(() => {
    if (visible) {
      Animated.timing(slideAnim, {
        toValue: 0,
        duration: 250,
        useNativeDriver: true,
      }).start();
    } else {
      Animated.timing(slideAnim, {
        toValue: -SIDEBAR_WIDTH,
        duration: 200,
        useNativeDriver: true,
      }).start();
    }
  }, [visible, slideAnim]);

  const handleNavigate = (item: NavItem) => {
    onClose();
    setTimeout(() => {
      navigation.navigate(item.screen, item.params);
    }, 200);
  };

  const handleLogout = () => {
    onClose();
    setTimeout(() => logout(), 200);
  };

  return (
    <Modal
      visible={visible}
      transparent
      animationType="none"
      onRequestClose={onClose}>
      <TouchableWithoutFeedback onPress={onClose}>
        <View style={styles.overlay} />
      </TouchableWithoutFeedback>

      <Animated.View
        style={[styles.sidebar, {transform: [{translateX: slideAnim}]}]}>
        {/* User info */}
        <View style={styles.userSection}>
          <View style={styles.avatarCircle}>
            <Text style={styles.avatarText}>👤</Text>
          </View>
          <Text style={styles.userName}>
            {isGuest ? 'Guest' : user?.name || 'User'}
          </Text>
          {!isGuest && user?.email && (
            <Text style={styles.userEmail}>{user.email}</Text>
          )}
          {!isGuest && (
            <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
              <Text style={styles.logoutBtnText}>🚪 Logout</Text>
            </TouchableOpacity>
          )}
        </View>

        <Text style={styles.navHeading}>Navigation</Text>

        <ScrollView style={styles.navList} showsVerticalScrollIndicator={false}>
          {NAV_ITEMS.map((item, index) => {
            const isActive = currentScreen === item.screen && !item.params;
            return (
              <TouchableOpacity
                key={index}
                style={[styles.navItem, isActive && styles.navItemActive]}
                onPress={() => handleNavigate(item)}>
                <Text style={styles.navIcon}>{item.icon}</Text>
                <Text style={[styles.navLabel, isActive && styles.navLabelActive]}>
                  {item.label}
                </Text>
              </TouchableOpacity>
            );
          })}
        </ScrollView>
      </Animated.View>
    </Modal>
  );
};

const styles = StyleSheet.create({
  overlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0,0,0,0.4)',
  },
  sidebar: {
    position: 'absolute',
    top: 0,
    left: 0,
    bottom: 0,
    width: SIDEBAR_WIDTH,
    backgroundColor: '#FFF8F0',
    shadowColor: '#000',
    shadowOffset: {width: 4, height: 0},
    shadowOpacity: 0.15,
    shadowRadius: 8,
    elevation: 10,
  },
  userSection: {
    backgroundColor: '#E8F5E9',
    padding: 20,
    paddingTop: 50,
    alignItems: 'flex-start',
  },
  avatarCircle: {
    width: 48,
    height: 48,
    borderRadius: 24,
    backgroundColor: '#C8E6C9',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 8,
  },
  avatarText: {
    fontSize: 24,
  },
  userName: {
    fontSize: 16,
    fontWeight: '600',
    color: '#333',
    marginBottom: 2,
  },
  userEmail: {
    fontSize: 12,
    color: THEME.primary,
    marginBottom: 8,
  },
  logoutBtn: {
    marginTop: 4,
    backgroundColor: '#8B4513',
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 6,
  },
  logoutBtnText: {
    color: 'white',
    fontSize: 13,
  },
  navHeading: {
    fontSize: 14,
    fontWeight: '700',
    color: '#555',
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 8,
    textTransform: 'uppercase',
    letterSpacing: 1,
  },
  navList: {
    flex: 1,
  },
  navItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    paddingHorizontal: 16,
  },
  navItemActive: {
    backgroundColor: `${THEME.primary}15`,
  },
  navIcon: {
    fontSize: 18,
    width: 30,
  },
  navLabel: {
    fontSize: 15,
    color: '#444',
    flex: 1,
  },
  navLabelActive: {
    color: THEME.primary,
    fontWeight: '600',
  },
});

export default SidebarMenu;
