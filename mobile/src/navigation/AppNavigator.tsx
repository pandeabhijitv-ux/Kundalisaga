/**
 * App Navigator
 * Main navigation structure for the app
 */

import React from 'react';
import {Text} from 'react-native';
import {createStackNavigator} from '@react-navigation/stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import {THEME} from '../constants/theme';
import {useAuth} from '../contexts/AuthContext';

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
  return (
    <Tab.Navigator
      screenOptions={{
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
      }}>
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarLabel: 'Home',
          tabBarIcon: ({size}) => <TabEmojiIcon routeName="Home" size={size} />,
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
        </>
      )}
    </Stack.Navigator>
  );
};

export default AppNavigator;
