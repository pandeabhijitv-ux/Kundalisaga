/**
 * Ask Question Screen
 * Knowledge base search via Python bridge.
 */
import React, {useEffect, useState} from 'react';
import {
  View,
  Text,
  StyleSheet,
  TextInput,
  TouchableOpacity,
  ScrollView,
  Alert,
} from 'react-native';
import {THEME} from '../../constants/theme';
import {searchKnowledge} from '../../services/PythonBridge';

const AskQuestionScreen = ({route}: any) => {
  const preset = route?.params?.preset;
  const [query, setQuery] = useState('What is ascendant in Vedic astrology?');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any[]>([]);

  useEffect(() => {
    if (preset === 'career') {
      setQuery('What does my chart indicate for career growth and ideal profession?');
    } else if (preset === 'finance') {
      setQuery('What astrological indications are there for financial stability and wealth timing?');
    } else if (preset === 'knowledge') {
      setQuery('Explain the role of ascendant and moon sign in Vedic astrology.');
    }
  }, [preset]);

  const handleSearch = async () => {
    if (!query.trim()) {
      Alert.alert('Validation', 'Please enter a question');
      return;
    }

    setLoading(true);
    try {
      const response = await searchKnowledge(query.trim());
      if (response?.error) {
        Alert.alert('Search Error', response.error);
      }
      setResults(response?.results || []);
    } catch (error: any) {
      Alert.alert('Error', error?.message || 'Failed to search knowledge base');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Ask Astrology Question</Text>

      <View style={styles.card}>
        <TextInput
          style={styles.input}
          value={query}
          onChangeText={setQuery}
          placeholder="Enter your astrology question"
          multiline
        />
        <TouchableOpacity style={styles.button} onPress={handleSearch} disabled={loading}>
          <Text style={styles.buttonText}>{loading ? 'Searching...' : 'Search Knowledge'}</Text>
        </TouchableOpacity>
      </View>

      <View style={styles.card}>
        <Text style={styles.sectionTitle}>Results</Text>
        {results.length === 0 ? (
          <Text style={styles.emptyText}>No results yet. Ask a question to begin.</Text>
        ) : (
          results.map((item, idx) => (
            <View key={idx} style={styles.resultItem}>
              <Text style={styles.resultScore}>Score: {Number(item?.score || 0).toFixed(2)}</Text>
              <Text style={styles.resultText}>{item?.text || ''}</Text>
              <Text style={styles.resultSource}>{item?.source || 'Unknown source'}</Text>
            </View>
          ))
        )}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: THEME.background,
  },
  content: {
    padding: 16,
    paddingBottom: 24,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 12,
  },
  card: {
    backgroundColor: THEME.card,
    borderRadius: 12,
    padding: 12,
    marginBottom: 12,
  },
  input: {
    backgroundColor: '#fff',
    borderColor: '#E0E0E0',
    borderWidth: 1,
    borderRadius: 10,
    paddingHorizontal: 12,
    paddingVertical: 10,
    marginBottom: 8,
    minHeight: 86,
    textAlignVertical: 'top',
    color: THEME.text,
  },
  button: {
    backgroundColor: THEME.primary,
    borderRadius: 10,
    paddingVertical: 12,
    alignItems: 'center',
  },
  buttonText: {
    color: '#fff',
    fontWeight: '700',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: THEME.text,
    marginBottom: 8,
  },
  resultItem: {
    borderTopColor: '#E5E5E5',
    borderTopWidth: 1,
    paddingTop: 10,
    marginTop: 10,
  },
  resultScore: {
    fontSize: 12,
    color: THEME.primary,
    marginBottom: 4,
  },
  resultText: {
    color: THEME.text,
    lineHeight: 20,
  },
  resultSource: {
    color: THEME.textLight,
    marginTop: 6,
    fontSize: 12,
  },
  emptyText: {
    color: THEME.textLight,
  },
});

export default AskQuestionScreen;
