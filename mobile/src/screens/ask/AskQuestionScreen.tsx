/**
 * Ask Question Screen - Placeholder
 */
import React from 'react';
import {View, Text, StyleSheet} from 'react-native';
import {THEME} from '../../../App';

const AskQuestionScreen = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.text}>Ask Question Screen - Coming Soon</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: THEME.background},
  text: {fontSize: 18, color: THEME.text},
});

export default AskQuestionScreen;
