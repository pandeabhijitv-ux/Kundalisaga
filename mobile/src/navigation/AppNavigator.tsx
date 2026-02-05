/**
 * App Navigator
 * Main navigation structure for the app
 */

import React from 'react';
import {createStackNavigator} from '@react-navigation/stack';
import {createBottomTabNavigator} from '@react-navigation/bottom-tabs';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import {THEME} from '../../App';
import {useAuth} from '../contexts/AuthContext';

// Import screens
import LoginScreen from '../screens/auth/LoginScreen';
import RegisterScreen from '../screens/auth/RegisterScreen';
import HomeScreen from '../screens/home/HomeScreen';
import ProfilesScreen from '../screens/profiles/ProfilesScreen';
import HoroscopeScreen from '../screens/horoscope/HoroscopeScreen';
import RemediesScreen from '../screens/remedies/RemediesScreen';
import AskQuestionScreen from '../screens/ask/AskQuestionScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

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
          tabBarIcon: ({color, size}) => (
            <Icon name="home" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Profiles"
        component={ProfilesScreen}
        options={{
          tabBarLabel: 'Profiles',
          tabBarIcon: ({color, size}) => (
            <Icon name="account-group" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Horoscope"
        component={HoroscopeScreen}
        options={{
          tabBarLabel: 'Horoscope',
          tabBarIcon: ({color, size}) => (
            <Icon name="zodiac-leo" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Ask"
        component={AskQuestionScreen}
        options={{
          tabBarLabel: 'Ask',
          tabBarIcon: ({color, size}) => (
            <Icon name="chat-question" size={size} color={color} />
          ),
        }}
      />
      <Tab.Screen
        name="Remedies"
        component={RemediesScreen}
        options={{
          tabBarLabel: 'Remedies',
          tabBarIcon: ({color, size}) => (
            <Icon name="meditation" size={size} color={color} />
          ),
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
        <Stack.Screen name="Main" component={MainTabs} />
      )}
    </Stack.Navigator>
  );
};

export default AppNavigator;
