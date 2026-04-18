import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, Alert} from 'react-native';
import {THEME} from '../constants/theme';

const PACKAGES = [
  {id: 1, credits: 10, price: '₹10', bonus: '', popular: false, color: '#E8F5E9'},
  {id: 2, credits: 50, price: '₹45', bonus: '10% OFF', popular: false, color: '#E3F2FD'},
  {id: 3, credits: 100, price: '₹80', bonus: '20% OFF', popular: true, color: '#FFF3E0'},
  {id: 4, credits: 250, price: '₹175', bonus: '30% OFF', popular: false, color: '#F3E5F5'},
];

const FEATURE_COSTS = [
  {feature: 'Birth Chart Analysis', cost: 10},
  {feature: 'Daily Horoscope', cost: 5},
  {feature: 'Kundali Matching', cost: 15},
  {feature: 'Muhurat Finder', cost: 10},
  {feature: 'Gemstone Guide', cost: 10},
  {feature: 'Ask AI Astrologer', cost: 5},
];

const BuyCreditsScreen = () => {
  const [selected, setSelected] = useState<number | null>(null);

  const handlePurchase = () => {
    if (!selected) {Alert.alert('Select a Package', 'Please choose a credit package first.'); return;}
    const pkg = PACKAGES.find(p => p.id === selected);
    Alert.alert(
      'Payment via UPI',
      `Please pay ${pkg?.price} to:\nUPI ID: kundalii.saga@upi\n\nAfter payment, credits will be added within 5 minutes.`,
      [{text: 'OK'}],
    );
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>💳</Text>
        <Text style={styles.title}>Buy Credits</Text>
        <Text style={styles.subtitle}>Credits unlock detailed Vedic astrology insights</Text>
      </View>

      <View style={styles.balanceCard}>
        <Text style={styles.balanceLabel}>Current Balance</Text>
        <Text style={styles.balanceValue}>💎 0 Credits</Text>
      </View>

      <Text style={styles.sectionTitle}>Choose a Package</Text>
      {PACKAGES.map(pkg => (
        <TouchableOpacity
          key={pkg.id}
          style={[styles.packageCard, {backgroundColor: pkg.color}, selected === pkg.id && styles.selectedCard]}
          onPress={() => setSelected(pkg.id)}>
          {pkg.popular && <View style={styles.popularBadge}><Text style={styles.popularText}>POPULAR</Text></View>}
          <View style={styles.packageRow}>
            <View>
              <Text style={styles.packageCredits}>💎 {pkg.credits} Credits</Text>
              {pkg.bonus ? <Text style={styles.packageBonus}>{pkg.bonus}</Text> : null}
            </View>
            <View style={styles.priceBox}>
              <Text style={styles.packagePrice}>{pkg.price}</Text>
            </View>
          </View>
          {selected === pkg.id && <Text style={styles.checkmark}>✔ Selected</Text>}
        </TouchableOpacity>
      ))}

      <TouchableOpacity style={styles.button} onPress={handlePurchase}>
        <Text style={styles.buttonText}>💳 Proceed to Pay via UPI</Text>
      </TouchableOpacity>

      <Text style={styles.sectionTitle}>What Do Credits Cost?</Text>
      <View style={styles.costTable}>
        {FEATURE_COSTS.map((f, i) => (
          <View key={i} style={[styles.costRow, i % 2 === 0 && styles.costRowAlt]}>
            <Text style={styles.costFeature}>{f.feature}</Text>
            <Text style={styles.costAmount}>💎 {f.cost}</Text>
          </View>
        ))}
      </View>

      <Text style={styles.note}>Credits are non-refundable. For support, contact support@kundalii.app</Text>
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
  balanceCard: {backgroundColor: THEME.primary, borderRadius: 12, padding: 18, alignItems: 'center', marginBottom: 20},
  balanceLabel: {color: 'rgba(255,255,255,0.8)', fontSize: 13},
  balanceValue: {color: '#fff', fontSize: 24, fontWeight: 'bold', marginTop: 4},
  sectionTitle: {fontSize: 16, fontWeight: 'bold', color: THEME.text, marginBottom: 12},
  packageCard: {borderRadius: 12, padding: 16, marginBottom: 12, elevation: 1, borderWidth: 2, borderColor: 'transparent'},
  selectedCard: {borderColor: THEME.primary},
  popularBadge: {backgroundColor: THEME.primary, borderRadius: 4, paddingHorizontal: 8, paddingVertical: 2, alignSelf: 'flex-start', marginBottom: 8},
  popularText: {color: '#fff', fontSize: 10, fontWeight: 'bold'},
  packageRow: {flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center'},
  packageCredits: {fontSize: 18, fontWeight: 'bold', color: THEME.text},
  packageBonus: {fontSize: 12, color: '#059669', fontWeight: 'bold', marginTop: 2},
  priceBox: {backgroundColor: 'rgba(255,255,255,0.7)', borderRadius: 8, paddingHorizontal: 14, paddingVertical: 8},
  packagePrice: {fontSize: 18, fontWeight: 'bold', color: THEME.primary},
  checkmark: {color: THEME.primary, fontWeight: 'bold', marginTop: 8},
  button: {backgroundColor: THEME.primary, borderRadius: 12, padding: 14, alignItems: 'center', marginBottom: 24},
  buttonText: {color: '#fff', fontWeight: 'bold', fontSize: 15},
  costTable: {backgroundColor: '#fff', borderRadius: 12, overflow: 'hidden', marginBottom: 16, elevation: 2},
  costRow: {flexDirection: 'row', justifyContent: 'space-between', padding: 12},
  costRowAlt: {backgroundColor: '#FFF8F0'},
  costFeature: {fontSize: 13, color: THEME.text},
  costAmount: {fontSize: 13, fontWeight: 'bold', color: THEME.primary},
  note: {fontSize: 12, color: THEME.textLight, textAlign: 'center', lineHeight: 18},
});

export default BuyCreditsScreen;
