/**
 * App Navigator
 * Main navigation structure for the app
 */

import React, {useState} from 'react';
import {Text, TouchableOpacity} from 'react-native';
import {createStackNavigator} from '@react-navigation/stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {THEME} from '../constants/theme';
import {useAuth} from '../contexts/AuthContext';
import SidebarMenu from '../components/SidebarMenu';

// Import screens
import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';
import HomeScreen from '../screens/home/HomeScreen';
import ProfilesScreen from '../screens/profiles/ProfilesScreen';
import HoroscopeScreen from '../screens/horoscope/HoroscopeScreen';
import RemediesScreen from '../screens/remedies/RemediesScreen';
import AskQuestionScreen from '../screens/ask/AskQuestionScreen';
import NumerologyScreen from '../screens/NumerologyScreen';
import DashaScreen from '../screens/DashaScreen';
import GemstoneScreen from '../screens/GemstoneScreen';
import SettingsScreen from '../screens/SettingsScreen';
import StotrasScreen from '../screens/StotrasScreen';

const CareerScreen = require('../screens/CareerScreen').default;
const FinancialScreen = require('../screens/FinancialScreen').default;
const MatchmakingScreen = require('../screens/MatchmakingScreen').default;
const SoulmateScreen = require('../screens/SoulmateScreen').default;
const MuhuratScreen = require('../screens/MuhuratScreen').default;
const VarshaphalScreen = require('../screens/VarshaphalScreen').default;
const NameRecommendationScreen = require('../screens/NameRecommendationScreen').default;

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

const TAB_ICONS: {[key: string]: string} = {
  Home: '🏠',
  Profiles: '👨‍👩‍👧‍👦',
  Horoscope: '🪐',
  Ask: '💬',
  Remedies: '🕉️',
};

const TabEmojiIcon = ({routeName, size}: {routeName: string; size: number}) => (
  <Text style={{fontSize: size - 2}}>{TAB_ICONS[routeName] || '✨'}</Text>
);

const MainTabs = () => {
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [currentSidebarScreen, setCurrentSidebarScreen] = useState('Home');

  const HamburgerButton = ({routeName}: {routeName: string}) => (
    <TouchableOpacity
      onPress={() => {
        setCurrentSidebarScreen(routeName);
        setSidebarVisible(true);
      }}
      style={{paddingHorizontal: 14, paddingVertical: 8}}>
      <Text style={{fontSize: 20}}>☰</Text>
    </TouchableOpacity>
  );

  return (
    <>
      <Tab.Navigator
        screenOptions={({route}) => ({
          tabBarActiveTintColor: THEME.primary,
          tabBarInactiveTintColor: THEME.textLight,
          tabBarStyle: {
            backgroundColor: THEME.background,
            borderTopColor: '#E0E0E0',
          },
          headerStyle: {
            backgroundColor: THEME.background,
          },
          headerTintColor: THEME.primary,
          headerLeft: () => <HamburgerButton routeName={route.name} />,
        })}>
        <Tab.Screen
          name="Home"
          component={HomeScreen}
          options={{
            tabBarLabel: 'Home',
            tabBarIcon: ({size}) => <TabEmojiIcon routeName="Home" size={size} />,
            headerTitle: '🔮 KundaliSaga',
          }}
        />
        <Tab.Screen
          name="Profiles"
          component={ProfilesScreen}
          options={{
            tabBarLabel: 'Profiles',
            tabBarIcon: ({size}) => <TabEmojiIcon routeName="Profiles" size={size} />,
          }}
        />
        <Tab.Screen
          name="Horoscope"
          component={HoroscopeScreen}
          options={{
            tabBarLabel: 'Horoscope',
            tabBarIcon: ({size}) => <TabEmojiIcon routeName="Horoscope" size={size} />,
          }}
        />
        <Tab.Screen
          name="Ask"
          component={AskQuestionScreen}
          options={{
            tabBarLabel: 'Ask',
            tabBarIcon: ({size}) => <TabEmojiIcon routeName="Ask" size={size} />,
          }}
        />
        <Tab.Screen
          name="Remedies"
          component={RemediesScreen}
          options={{
            tabBarLabel: 'Remedies',
            tabBarIcon: ({size}) => <TabEmojiIcon routeName="Remedies" size={size} />,
          }}
        />
      </Tab.Navigator>
      <SidebarMenu
        visible={sidebarVisible}
        onClose={() => setSidebarVisible(false)}
        currentScreen={currentSidebarScreen}
      />
    </>
  );
};

const AppNavigator = () => {
  const {user, isGuest} = useAuth();
  const [sidebarVisible, setSidebarVisible] = useState(false);
  const [currentSidebarScreen, setCurrentSidebarScreen] = useState('Home');

  const openSidebar = (screenName: string) => {
    setCurrentSidebarScreen(screenName);
    setSidebarVisible(true);
  };

  const stackScreenOptions = (title: string, routeName: string) => ({
    headerShown: true,
    title,
    headerStyle: {backgroundColor: THEME.background},
    headerTintColor: THEME.primary,
    headerRight: () => (
      <TouchableOpacity
        onPress={() => openSidebar(routeName)}
        style={{paddingHorizontal: 14, paddingVertical: 8}}>
        <Text style={{fontSize: 20}}>☰</Text>
      </TouchableOpacity>
    ),
  });

  return (
    <>
      <Stack.Navigator
        screenOptions={{
          headerShown: false,
        }}>
        {!user && !isGuest ? (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        ) : (
          <>
            <Stack.Screen name="Main" component={MainTabs} />
            <Stack.Screen name="Numerology" component={NumerologyScreen} options={stackScreenOptions('Numerology', 'Numerology')} />
            <Stack.Screen name="Dasha" component={DashaScreen} options={stackScreenOptions('Current Dasha', 'Dasha')} />
            <Stack.Screen name="Career" component={CareerScreen} options={stackScreenOptions('Career Guidance', 'Career')} />
            <Stack.Screen name="Financial" component={FinancialScreen} options={stackScreenOptions('Financial Outlook', 'Financial')} />
            <Stack.Screen name="Gemstone" component={GemstoneScreen} options={stackScreenOptions('Gemstone Guide', 'Gemstone')} />
            <Stack.Screen name="Matchmaking" component={MatchmakingScreen} options={stackScreenOptions('Matchmaking', 'Matchmaking')} />
            <Stack.Screen name="Soulmate" component={SoulmateScreen} options={stackScreenOptions('Soulmate Analysis', 'Soulmate')} />
            <Stack.Screen name="Muhurat" component={MuhuratScreen} options={stackScreenOptions('Muhurat Finder', 'Muhurat')} />
            <Stack.Screen name="Varshaphal" component={VarshaphalScreen} options={stackScreenOptions('Varshaphal', 'Varshaphal')} />
            <Stack.Screen name="NameRecommendation" component={NameRecommendationScreen} options={stackScreenOptions('Name Recommendation', 'NameRecommendation')} />
            <Stack.Screen name="Settings" component={SettingsScreen} options={stackScreenOptions('Settings', 'Settings')} />
            <Stack.Screen name="Stotras" component={StotrasScreen} options={stackScreenOptions('Stotras & Prayers', 'Stotras')} />
          </>
        )}
      </Stack.Navigator>
      <SidebarMenu visible={sidebarVisible} onClose={() => setSidebarVisible(false)} currentScreen={currentSidebarScreen} />
    </>
  );
};

export default AppNavigator;
