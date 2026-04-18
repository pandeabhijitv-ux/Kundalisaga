import React, {useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView} from 'react-native';
import {THEME} from '../constants/theme';

const CATEGORIES = [
  {
    name: 'Ganesh',
    icon: '🐘',
    color: '#FFF3E0',
    stotras: [
      {title: 'Ganesh Vandana', lines: 'Vakratunda Mahakaya, Suryakoti Samaprabha\nNirvighnam Kuru Me Deva, Sarva Karyeshu Sarvada', meaning: 'O Lord Ganesha with curved trunk and huge body, possessing the brilliance of crores of suns, please make all my works free from obstacles.'},
      {title: 'Shri Ganesh Mantra', lines: 'Om Gam Ganapataye Namah', meaning: 'Salutations to the remover of obstacles, Lord Ganesha.'},
    ],
  },
  {
    name: 'Navagraha',
    icon: '🌟',
    color: '#E3F2FD',
    stotras: [
      {title: 'Navagraha Mantra', lines: 'Om Brahmaa Murari Stripurantakaari\nBhanu Shashi Bhumi Suto Buddhashcha\nGurusch Shukra Shani Raahu Ketu\nKurvantu Sarve Mama Suprabhatam', meaning: 'May Brahma, Vishnu, Shiva, Mars, Moon, Saturn, Mercury, Jupiter, Venus, Saturn, Rahu and Ketu bless me every morning.'},
    ],
  },
  {
    name: 'Surya',
    icon: '☀️',
    color: '#FFFDE7',
    stotras: [
      {title: 'Surya Namaskar Mantra', lines: 'Om Mitraaya Namah\nOm Ravaye Namah\nOm Suryaya Namah\nOm Bhaanave Namah\nOm Khagaya Namah', meaning: 'Salutations to the friend of all, to the radiant one, to the sun, to the one who illuminates, to the one who moves swiftly.'},
      {title: 'Aditya Hridayam (Verse 1)', lines: 'Tato Yuddhapariśrāntaṃ samare cintayā sthitam\nRāvaṇaṃ cāgrato dṛṣṭvā yuddha-kālaṃ upasthitam', meaning: 'Then the sage Agastya appeared before the weary Rama who was standing pensively on the battlefield with Ravana before him.'},
    ],
  },
  {
    name: 'Chandra',
    icon: '🌙',
    color: '#E8EAF6',
    stotras: [
      {title: 'Chandra Mantra', lines: 'Om Shraam Shreem Shroum Sah Chandramasye Namah', meaning: 'Salutations to the Moon, who bestows peace, calms the mind, and blesses with emotional balance.'},
    ],
  },
  {
    name: 'Shiva',
    icon: '🔱',
    color: '#E8F5E9',
    stotras: [
      {title: 'Maha Mrityunjaya Mantra', lines: 'Om Tryambakam Yajamahe\nSugandhim Pushtivardhanam\nUrvarukamiva Bandhanan\nMrityor Mukshiya Maamritat', meaning: 'We worship the three-eyed Shiva who is fragrant and nourishes all beings. Free us from the bondage of death, grant us immortality as the cucumber is freed from its vine.'},
      {title: 'Om Namah Shivaya', lines: 'Om Namah Shivaya\nOm Namah Shivaya\nOm Namah Shivaya', meaning: 'Salutations to Shiva, the auspicious one, the destroyer of ego.'},
    ],
  },
  {
    name: 'Vishnu',
    icon: '💙',
    color: '#E1F5FE',
    stotras: [
      {title: 'Vishnu Sahasranama (Opening)', lines: 'Shuklaambara Dharam Vishnum Shashivarnam Chaturbhujam\nPrasanna Vadanam Dhyaayet Sarva Vighno Upashaantaye', meaning: 'Meditate on Vishnu who is dressed in white, who is all pervading, has the colour of moon, has four hands, and has pleasant countenance, to destroy all obstacles.'},
    ],
  },
];

const StotrasScreen = () => {
  const [expanded, setExpanded] = useState<string | null>(null);
  const [expandedStotra, setExpandedStotra] = useState<string | null>(null);

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>🙏</Text>
        <Text style={styles.title}>Stotras & Prayers</Text>
        <Text style={styles.subtitle}>Sacred Vedic mantras and hymns</Text>
      </View>

      {CATEGORIES.map(cat => (
        <View key={cat.name} style={styles.categoryCard}>
          <TouchableOpacity style={[styles.categoryHeader, {backgroundColor: cat.color}]} onPress={() => setExpanded(expanded === cat.name ? null : cat.name)}>
            <Text style={styles.categoryIcon}>{cat.icon}</Text>
            <Text style={styles.categoryName}>{cat.name} Stotras</Text>
            <Text style={styles.arrow}>{expanded === cat.name ? '▲' : '▼'}</Text>
          </TouchableOpacity>

          {expanded === cat.name && cat.stotras.map(s => (
            <View key={s.title} style={styles.stotraItem}>
              <TouchableOpacity onPress={() => setExpandedStotra(expandedStotra === s.title ? null : s.title)}>
                <Text style={styles.stotraTitle}>📿 {s.title}</Text>
              </TouchableOpacity>
              {expandedStotra === s.title && (
                <>
                  <View style={styles.sanskritBox}>
                    <Text style={styles.sanskritText}>{s.lines}</Text>
                  </View>
                  <Text style={styles.meaningLabel}>Meaning:</Text>
                  <Text style={styles.meaningText}>{s.meaning}</Text>
                </>
              )}
            </View>
          ))}
        </View>
      ))}

      <View style={styles.tipCard}>
        <Text style={styles.tipText}>💡 Tip: Recite mantras during brahma muhurta (before sunrise) for maximum benefit.</Text>
      </View>
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
  categoryCard: {backgroundColor: '#fff', borderRadius: 12, marginBottom: 14, overflow: 'hidden', elevation: 2},
  categoryHeader: {flexDirection: 'row', alignItems: 'center', padding: 14},
  categoryIcon: {fontSize: 24, marginRight: 10},
  categoryName: {flex: 1, fontSize: 16, fontWeight: 'bold', color: THEME.text},
  arrow: {fontSize: 12, color: THEME.textLight},
  stotraItem: {padding: 14, borderTopWidth: 1, borderTopColor: '#F0E8D8'},
  stotraTitle: {fontSize: 15, fontWeight: '600', color: THEME.primary, marginBottom: 8},
  sanskritBox: {backgroundColor: '#FFF8F0', borderRadius: 8, padding: 12, marginBottom: 8},
  sanskritText: {fontSize: 14, color: THEME.text, lineHeight: 24, fontStyle: 'italic'},
  meaningLabel: {fontSize: 12, fontWeight: 'bold', color: THEME.textLight, marginBottom: 4},
  meaningText: {fontSize: 13, color: THEME.text, lineHeight: 20},
  tipCard: {backgroundColor: '#E8F5E9', borderRadius: 12, padding: 14},
  tipText: {fontSize: 13, color: '#2E7D32', lineHeight: 20},
});

export default StotrasScreen;
