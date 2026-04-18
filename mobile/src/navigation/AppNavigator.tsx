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
import CareerScreen from '../screens/CareerScreen';
import FinancialScreen from '../screens/FinancialScreen';
import GemstoneScreen from '../screens/GemstoneScreen';
import MatchmakingScreen from '../screens/MatchmakingScreen';
import SoulmateScreen from '../screens/SoulmateScreen';
import MuhuratScreen from '../screens/MuhuratScreen';
import VarshaphalScreen from '../screens/VarshaphalScreen';
import NameRecommendationScreen from '../screens/NameRecommendationScreen';
import BuyCreditsScreen from '../screens/BuyCreditsScreen';
import SettingsScreen from '../screens/SettingsScreen';
import StotrasScreen from '../screens/StotrasScreen';

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

  const HamburgerButton = ({navigation}: any) => (
    <TouchableOpacity
      onPress={() => setSidebarVisible(true)}
      style={{paddingHorizontal: 14, paddingVertical: 8}}>
      <Text style={{fontSize: 20}}>☰</Text>
    </TouchableOpacity>
  );

  return (
    <>
      <Tab.Navigator
        screenOptions={({navigation}) => ({
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
          headerLeft: () => <HamburgerButton navigation={navigation} />,
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
        currentScreen="Home"
      />
    </>
  );
};

const AppNavigator = () => {
  const {user, isGuest} = useAuth();

  return (
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
          <Stack.Screen
            name="Numerology"
            component={NumerologyScreen}
            options={{headerShown: true, title: 'Numerology'}}
          />
          <Stack.Screen
            name="Dasha"
            component={DashaScreen}
            options={{headerShown: true, title: 'Current Dasha'}}
          />
          <Stack.Screen name="Career" component={CareerScreen} options={{headerShown: true, title: 'Career Guidance'}} />
          <Stack.Screen name="Financial" component={FinancialScreen} options={{headerShown: true, title: 'Financial Outlook'}} />
          <Stack.Screen name="Gemstone" component={GemstoneScreen} options={{headerShown: true, title: 'Gemstone Guide'}} />
          <Stack.Screen name="Matchmaking" component={MatchmakingScreen} options={{headerShown: true, title: 'Matchmaking'}} />
          <Stack.Screen name="Soulmate" component={SoulmateScreen} options={{headerShown: true, title: 'Soulmate Analysis'}} />
          <Stack.Screen name="Muhurat" component={MuhuratScreen} options={{headerShown: true, title: 'Muhurat Finder'}} />
          <Stack.Screen name="Varshaphal" component={VarshaphalScreen} options={{headerShown: true, title: 'Varshaphal'}} />
          <Stack.Screen name="NameRecommendation" component={NameRecommendationScreen} options={{headerShown: true, title: 'Name Recommendation'}} />
          <Stack.Screen name="BuyCredits" component={BuyCreditsScreen} options={{headerShown: true, title: 'Buy Credits'}} />
          <Stack.Screen name="Settings" component={SettingsScreen} options={{headerShown: true, title: 'Settings'}} />
          <Stack.Screen name="Stotras" component={StotrasScreen} options={{headerShown: true, title: 'Stotras & Prayers'}} />
        </>
      )}
    </Stack.Navigator>
  );
};

export default AppNavigator;
