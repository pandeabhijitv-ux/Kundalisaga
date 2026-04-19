/**
 * Python Bridge for React Native
 * This module provides the interface to call Python functions from JavaScript
 */

import {NativeModules} from 'react-native';

const {PythonBridge} = NativeModules;

// Check if PythonBridge native module is available
const isPythonBridgeAvailable = !!PythonBridge;

if (!isPythonBridgeAvailable) {
  console.warn('⚠️ PythonBridge native module not available. Python features will be disabled.');
}

export interface BirthDetails {
  name: string;
  date: string;
  time: string;
  location: string;
  latitude: number;
  longitude: number;
  timezone: string;
}

export interface ChartData {
  planets: any[];
  houses: any[];
  ascendant: any;
  dasha: any;
}

export interface RemedyData {
  gemstones: string[];
  mantras: string[];
  fasting: string[];
  charity: string[];
}

export interface NumerologyData {
  lifePathNumber: number;
  destinyNumber: number;
  soulNumber: number;
  personalityNumber: number;
  interpretation: string;
}

/**
 * Calculate Vedic Birth Chart
 */
export const calculateChart = async (
  birthDetails: BirthDetails,
): Promise<ChartData> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    const result = await PythonBridge.calculateChart(birthDetails);
    return result;
  } catch (error) {
    console.error('Error calculating chart:', error);
    throw error;
  }
};

/**
 * Get Astrological Remedies
 */
export const getRemedies = async (chartData: ChartData): Promise<RemedyData> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    const result = await PythonBridge.getRemedies(chartData);
    return result;
  } catch (error) {
    console.error('Error getting remedies:', error);
    throw error;
  }
};

/**
 * Calculate Numerology
 */
export const calculateNumerology = async (
  name: string,
  dateOfBirth: string,
): Promise<NumerologyData> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    const result = await PythonBridge.calculateNumerology(name, dateOfBirth);
    return result;
  } catch (error) {
    console.error('Error calculating numerology:', error);
    throw error;
  }
};

/**
 * Get Current Dasha Period
 */
export const getCurrentDasha = async (dateOfBirth: string): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    console.log('Python bridge not available, skipping dasha calculation');
    return null; // Return null instead of throwing
  }
  try {
    const result = await PythonBridge.getCurrentDasha(dateOfBirth);
    return result;
  } catch (error) {
    console.error('Error getting dasha:', error);
    return null; // Graceful fallback
  }
};

/**
 * Search Knowledge Base
 */
export const searchKnowledge = async (query: string): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    const result = await PythonBridge.searchKnowledgeBase(query);
    return result;
  } catch (error) {
    console.error('Error searching knowledge:', error);
    throw error;
  }
};

export const analyzeCareer = async (chartJson: string): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.analyzeCareer(chartJson);
  } catch (error) {
    console.error('Error analyzing career:', error);
    throw error;
  }
};

export const analyzeFinancial = async (chartJson: string): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.analyzeFinancial(chartJson);
  } catch (error) {
    console.error('Error analyzing financial:', error);
    throw error;
  }
};

export const getGemstoneRecommendations = async (chartJson: string, question: string = ''): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.getGemstoneRecommendations(chartJson, question);
  } catch (error) {
    console.error('Error getting gemstone recommendations:', error);
    throw error;
  }
};

export const analyzeCompatibility = async (chartAJson: string, chartBJson: string): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.analyzeCompatibility(chartAJson, chartBJson);
  } catch (error) {
    console.error('Error analyzing compatibility:', error);
    throw error;
  }
};

export const getMuhuratAnalysis = async (chartJson: string, eventType: string): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.getMuhuratAnalysis(chartJson, eventType);
  } catch (error) {
    console.error('Error getting muhurat analysis:', error);
    throw error;
  }
};

export const analyzeVarshaphal = async (chartJson: string): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.analyzeVarshaphal(chartJson);
  } catch (error) {
    console.error('Error analyzing varshaphal:', error);
    throw error;
  }
};

export const analyzeSoulmate = async (chartJson: string, gender: string = 'male'): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.analyzeSoulmate(chartJson, gender);
  } catch (error) {
    console.error('Error analyzing soulmate:', error);
    throw error;
  }
};

export const getNameRecommendations = async (chartJson: string, gender: string = 'male'): Promise<any> => {
  if (!isPythonBridgeAvailable) {
    throw new Error('Python bridge not available');
  }
  try {
    return await PythonBridge.getNameRecommendations(chartJson, gender);
  } catch (error) {
    console.error('Error getting name recommendations:', error);
    throw error;
  }
};

export default {
  calculateChart,
  getRemedies,
  calculateNumerology,
  getCurrentDasha,
  searchKnowledge,
  analyzeCareer,
  analyzeFinancial,
  getGemstoneRecommendations,
  analyzeCompatibility,
  getMuhuratAnalysis,
  analyzeVarshaphal,
  analyzeSoulmate,
  getNameRecommendations,
};
