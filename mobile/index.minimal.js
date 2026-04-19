/**
 * @format
 */

import {AppRegistry} from 'react-native';
import MinimalApp from './App.minimal'; // TESTING: Use minimal app

// Register with the same name as in MainActivity.java getMainComponentName()
AppRegistry.registerComponent('KundaliSaga', () => MinimalApp);
