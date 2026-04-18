import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, ActivityIndicator} from 'react-native';
import {THEME} from '../constants/theme';

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const VarshaphalScreen = () => {
  const [selectedYear, setSelectedYear] = useState(2026);
  const [loading, setLoading] = useState(false);
  const [predictions, setPredictions] = useState<any>(null);

  const calculate = () => {
    setLoading(true);
    setTimeout(() => {
      setPredictions({
        year: selectedYear,
        yearLord: 'Jupiter',
        monthlyPredictions: [
          {month: 'Jan', prediction: 'Favorable for career growth', level: 'good'},
          {month: 'Feb', prediction: 'Focus on health; avoid conflicts', level: 'caution'},
          {month: 'Mar', prediction: 'Excellent for financial decisions', level: 'excellent'},
          {month: 'Apr', prediction: 'Travel opportunities arise', level: 'good'},
          {month: 'May', prediction: 'Relationship harmony improves', level: 'excellent'},
          {month: 'Jun', prediction: 'Minor obstacles; stay patient', level: 'caution'},
        ],
        highlights: [
          '📈 Career: Promotion or new opportunities in Q1',
          '💰 Finance: Good investment returns expected',
          '❤️ Love: Strengthening of bonds, possible marriage',
          '🏥 Health: Watch digestive system in monsoon',
        ],
      });
      setLoading(false);
    }, 1500);
  };

  const levelColor = (l: string) => l === 'excellent' ? '#059669' : l === 'good' ? '#2563EB' : '#D97706';

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>📅</Text>
        <Text style={styles.title}>Varshaphal</Text>
        <Text style={styles.subtitle}>Annual predictions based on solar return chart</Text>
      </View>

      <View style={styles.yearSelector}>
        <TouchableOpacity onPress={() => setSelectedYear(y => y - 1)} style={styles.yearBtn}><Text style={styles.yearBtnText}>◀</Text></TouchableOpacity>
        <Text style={styles.yearText}>{selectedYear}</Text>
        <TouchableOpacity onPress={() => setSelectedYear(y => y + 1)} style={styles.yearBtn}><Text style={styles.yearBtnText}>▶</Text></TouchableOpacity>
      </View>

      <TouchableOpacity style={styles.button} onPress={calculate} disabled={loading}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>📊 Calculate Annual Predictions</Text>}
      </TouchableOpacity>

      {predictions && (
        <>
          <View style={styles.highlightCard}>
            <Text style={styles.sectionTitle}>🌟 Year {predictions.year} Highlights (Lord: {predictions.yearLord})</Text>
            {predictions.highlights.map((h: string, i: number) => (
              <Text key={i} style={styles.highlight}>{h}</Text>
            ))}
          </View>

          <Text style={styles.sectionTitle}>Monthly Forecast</Text>
          {predictions.monthlyPredictions.map((m: any, i: number) => (
            <View key={i} style={styles.monthRow}>
              <View style={[styles.monthBadge, {backgroundColor: levelColor(m.level)}]}>
                <Text style={styles.monthText}>{m.month}</Text>
              </View>
              <Text style={styles.monthPrediction}>{m.prediction}</Text>
            </View>
          ))}
        </>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#FFF8F0'},
  content: {padding: 16, paddingBottom: 40},
  header: {alignItems: 'center', paddingVertical: 20, marginBottom: 16},
  icon: {fontSize: 48, marginBottom: 8},
  title: {fontSize: 22, fontWeight: 'bold', color: THEME.primary, textAlign: 'center'},
  subtitle: {fontSize: 14, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  yearSelector: {flexDirection: 'row', alignItems: 'center', justifyContent: 'center', marginBottom: 20},
  yearBtn: {backgroundColor: THEME.primary, width: 40, height: 40, borderRadius: 20, alignItems: 'center', justifyContent: 'center'},
  yearBtnText: {color: '#fff', fontSize: 18},
  yearText: {fontSize: 28, fontWeight: 'bold', color: THEME.text, marginHorizontal: 24},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 20},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  highlightCard: {backgroundColor: '#fff', borderRadius: 12, padding: 16, marginBottom: 20, elevation: 2},
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 10},
  highlight: {fontSize: 14, color: THEME.text, marginBottom: 6, lineHeight: 20},
  monthRow: {flexDirection: 'row', alignItems: 'center', backgroundColor: '#fff', borderRadius: 10, padding: 12, marginBottom: 8, elevation: 1},
  monthBadge: {width: 44, height: 44, borderRadius: 8, alignItems: 'center', justifyContent: 'center', marginRight: 12},
  monthText: {color: '#fff', fontWeight: 'bold', fontSize: 13},
  monthPrediction: {flex: 1, fontSize: 13, color: THEME.text, lineHeight: 18},
});

export default VarshaphalScreen;
