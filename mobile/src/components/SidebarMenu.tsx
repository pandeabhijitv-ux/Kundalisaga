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
        <View style={styles.userSection}>
          <View style={styles.userCard}>
            <Text style={styles.userName}>{isGuest ? 'Guest' : user?.name || 'User'}</Text>
          </View>
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

        <View style={styles.footer}>
          <Text style={styles.footerIcon}>☂️</Text>
          <Text style={styles.footerBrand}>Krittika Apps</Text>
          <Text style={styles.footerTagline}>Sharp. Supreme. Protective.</Text>
          <Text style={styles.footerCopy}>© 2026 Krittika Apps</Text>
          <Text style={styles.footerLink}>Privacy Policy</Text>
        </View>
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
    padding: 16,
    paddingTop: 46,
    alignItems: 'flex-start',
  },
  userCard: {
    width: '100%',
    backgroundColor: '#E5F1D9',
    borderRadius: 10,
    paddingHorizontal: 14,
    paddingVertical: 12,
    marginBottom: 10,
  },
  userName: {
    fontSize: 16,
    fontWeight: '700',
    color: '#2E7D32',
  },
  userEmail: {
    fontSize: 12,
    color: THEME.primary,
    marginBottom: 10,
    marginLeft: 4,
    textDecorationLine: 'underline',
  },
  logoutBtn: {
    marginTop: 4,
    borderWidth: 1,
    borderColor: '#D7C7B2',
    backgroundColor: '#FFF',
    paddingHorizontal: 14,
    paddingVertical: 10,
    borderRadius: 8,
  },
  logoutBtnText: {
    color: '#8B4513',
    fontSize: 13,
    fontWeight: '600',
  },
  navHeading: {
    fontSize: 16,
    fontWeight: '700',
    color: '#222',
    paddingHorizontal: 16,
    paddingTop: 16,
    paddingBottom: 8,
  },
  navList: {
    flex: 1,
  },
  navItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
    paddingHorizontal: 16,
  },
  navItemActive: {
    backgroundColor: `${THEME.primary}15`,
    borderLeftWidth: 3,
    borderLeftColor: THEME.primary,
  },
  navIcon: {
    fontSize: 17,
    width: 30,
  },
  navLabel: {
    fontSize: 14,
    color: '#444',
    flex: 1,
  },
  navLabelActive: {
    color: THEME.primary,
    fontWeight: '600',
  },
  footer: {
    borderTopWidth: 1,
    borderTopColor: '#E5DCCF',
    paddingTop: 16,
    paddingBottom: 20,
    alignItems: 'center',
    paddingHorizontal: 16,
  },
  footerIcon: {
    fontSize: 26,
    marginBottom: 6,
    color: '#7B3FA0',
  },
  footerBrand: {
    fontSize: 22,
    fontWeight: '700',
    color: '#FF6B2C',
  },
  footerTagline: {
    fontSize: 12,
    color: '#6A5B4D',
    marginTop: 2,
  },
  footerCopy: {
    fontSize: 11,
    color: '#8A7E73',
    marginTop: 6,
  },
  footerLink: {
    fontSize: 11,
    color: '#E37B53',
    marginTop: 4,
  },
});

export default SidebarMenu;
