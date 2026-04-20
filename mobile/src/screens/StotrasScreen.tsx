import React, {useMemo, useState} from 'react';
import {View, Text, StyleSheet, TouchableOpacity, ScrollView, TextInput, Linking, Alert} from 'react-native';
import {THEME} from '../constants/theme';
import {STOTRA_CATALOG, STOTRA_CATEGORIES, StotraItem} from '../data/stotrasCatalog';

const CATEGORY_COLORS: Record<string, string> = {
  Ganesh: '#FFF3E0',
  Shiva: '#E8F5E9',
  'Vishnu Krishna': '#E1F5FE',
  Rama: '#FFF8E1',
  Hanuman: '#FBE9E7',
  Devi: '#FCE4EC',
  Lakshmi: '#FFFDE7',
  Saraswati: '#E8EAF6',
  Navagraha: '#E3F2FD',
  Narasimha: '#F3E5F5',
  'Dattatreya Bhairava': '#E0F2F1',
  Subrahmanya: '#F1F8E9',
  General: '#ECEFF1',
};

const StotrasScreen = () => {
  const [expandedCategory, setExpandedCategory] = useState<string | null>('Ganesh');
  const [expandedStotra, setExpandedStotra] = useState<string | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [query, setQuery] = useState<string>('');

  const filteredCatalog = useMemo(() => {
    const q = query.trim().toLowerCase();
    return STOTRA_CATALOG.filter(item => {
      if (selectedCategory !== 'All' && item.category !== selectedCategory) {
        return false;
      }
      if (!q) {
        return true;
      }

      return (
        item.title.toLowerCase().includes(q) ||
        item.deity.toLowerCase().includes(q) ||
        item.tags.some(tag => tag.toLowerCase().includes(q)) ||
        item.type.toLowerCase().includes(q)
      );
    });
  }, [query, selectedCategory]);

  const groupedCatalog = useMemo(() => {
    const grouped: Record<string, StotraItem[]> = {};
    for (const category of STOTRA_CATEGORIES) {
      grouped[category] = [];
    }

    for (const item of filteredCatalog) {
      if (!grouped[item.category]) {
        grouped[item.category] = [];
      }
      grouped[item.category].push(item);
    }

    return grouped;
  }, [filteredCatalog]);

  const categoryOptions = useMemo(() => ['All', ...STOTRA_CATEGORIES], []);

  const normalizeSourceUrl = (rawUrl: string): string => {
    const trimmed = String(rawUrl || '').trim();
    if (!trimmed) return '';
    if (/^https?:\/\//i.test(trimmed)) return trimmed;
    return `https://${trimmed}`;
  };

  const openSourceLink = async (url: string) => {
    const normalizedUrl = normalizeSourceUrl(url);
    if (!normalizedUrl) {
      Alert.alert('Invalid Link', 'This source link is missing or malformed.');
      return;
    }
    try {
      await Linking.openURL(normalizedUrl);
    } catch (error) {
      Alert.alert('Unable to Open Link', `Please try opening this link in browser:\n${normalizedUrl}`);
    }
  };

  const openSourceLinkWithDisclaimer = (url: string) => {
    Alert.alert(
      'Open External Link',
      'You are about to open an external website and leave the app experience. Continue?',
      [
        {text: 'Cancel', style: 'cancel'},
        {
          text: 'Continue',
          style: 'default',
          onPress: () => {
            void openSourceLink(url);
          },
        },
      ],
    );
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <View style={styles.header}>
        <Text style={styles.icon}>🙏</Text>
        <Text style={styles.title}>Stotras & Prayers</Text>
        <Text style={styles.subtitle}>Large catalog of Vedic hymns, stotras, kavach, and sahasranama</Text>
      </View>

      <View style={styles.searchBox}>
        <TextInput
          placeholder="Search by title, deity, type, or tag"
          placeholderTextColor="#9AA0A6"
          style={styles.searchInput}
          value={query}
          onChangeText={setQuery}
        />
      </View>

      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterStrip}>
        {categoryOptions.map(category => {
          const isActive = selectedCategory === category;
          return (
            <TouchableOpacity
              key={category}
              style={[styles.filterChip, isActive && styles.filterChipActive]}
              onPress={() => {
                setSelectedCategory(category);
                setExpandedCategory(category === 'All' ? expandedCategory : category);
              }}>
              <Text style={[styles.filterChipText, isActive && styles.filterChipTextActive]}>{category}</Text>
            </TouchableOpacity>
          );
        })}
      </ScrollView>

      <View style={styles.statsRow}>
        <Text style={styles.statsText}>{filteredCatalog.length} stotras found</Text>
        <Text style={styles.statsSubText}>Catalog source: curated public index + in-app chants</Text>
      </View>

      {STOTRA_CATEGORIES.map(category => {
        const items = groupedCatalog[category] || [];
        if (!items.length) {
          return null;
        }

        const isExpanded = expandedCategory === category;
        return (
          <View key={category} style={styles.categoryCard}>
            <TouchableOpacity
              style={[styles.categoryHeader, {backgroundColor: CATEGORY_COLORS[category] || '#F5F5F5'}]}
              onPress={() => setExpandedCategory(isExpanded ? null : category)}>
              <Text style={styles.categoryName}>{category}</Text>
              <Text style={styles.countBadge}>{items.length}</Text>
              <Text style={styles.arrow}>{isExpanded ? '▲' : '▼'}</Text>
            </TouchableOpacity>

            {isExpanded &&
              items.map(item => (
                <View key={item.id} style={styles.stotraItem}>
                  <TouchableOpacity onPress={() => setExpandedStotra(expandedStotra === item.id ? null : item.id)}>
                    <Text style={styles.stotraTitle}>📿 {item.title}</Text>
                    <Text style={styles.metaLine}>
                      {item.deity} • {item.type} • {item.hasFullText ? 'in-app text' : 'index entry'}
                    </Text>
                  </TouchableOpacity>

                  {expandedStotra === item.id && (
                    <>
                      <View style={styles.tagRow}>
                        {item.tags.map(tag => (
                          <View key={`${item.id}-${tag}`} style={styles.tagChip}>
                            <Text style={styles.tagText}>{tag}</Text>
                          </View>
                        ))}
                      </View>

                      {item.lines ? (
                        <View style={styles.sanskritBox}>
                          <Text style={styles.sanskritText}>{item.lines}</Text>
                        </View>
                      ) : null}

                      {item.meaning ? (
                        <>
                          <Text style={styles.meaningLabel}>Meaning:</Text>
                          <Text style={styles.meaningText}>{item.meaning}</Text>
                        </>
                      ) : null}

                      {!item.hasFullText && item.sourceUrl ? (
                        <TouchableOpacity style={styles.linkButton} onPress={() => openSourceLinkWithDisclaimer(item.sourceUrl as string)}>
                          <Text style={styles.linkButtonText}>Open full text source</Text>
                        </TouchableOpacity>
                      ) : null}
                    </>
                  )}
                </View>
              ))}
          </View>
        );
      })}

      {!filteredCatalog.length ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyTitle}>No results found</Text>
          <Text style={styles.emptyText}>Try a broader keyword like Shiva, Lakshmi, Navagraha, kavach, or sahasranama.</Text>
        </View>
      ) : null}

      <View style={styles.tipCard}>
        <Text style={styles.tipText}>Tip: Use this catalog as a structured reference. For long stotras, open source links and chant with proper pronunciation.</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: '#FFF8F0'},
  content: {padding: 16, paddingBottom: 40},
  header: {alignItems: 'center', paddingVertical: 20, marginBottom: 10},
  icon: {fontSize: 48, marginBottom: 8},
  title: {fontSize: 22, fontWeight: 'bold', color: THEME.primary, textAlign: 'center'},
  subtitle: {fontSize: 14, color: THEME.textLight, textAlign: 'center', marginTop: 4},
  searchBox: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    paddingHorizontal: 12,
    borderWidth: 1,
    borderColor: '#EADFD3',
    marginBottom: 12,
  },
  searchInput: {
    fontSize: 14,
    color: THEME.text,
    paddingVertical: 10,
  },
  filterStrip: {marginBottom: 10},
  filterChip: {
    paddingHorizontal: 12,
    paddingVertical: 8,
    borderRadius: 16,
    backgroundColor: '#F5EDE3',
    marginRight: 8,
  },
  filterChipActive: {backgroundColor: THEME.primary},
  filterChipText: {fontSize: 12, color: '#7B6D5A', fontWeight: '600'},
  filterChipTextActive: {color: '#FFFFFF'},
  statsRow: {flexDirection: 'row', justifyContent: 'space-between', marginBottom: 12},
  statsText: {fontSize: 13, color: THEME.text, fontWeight: '700'},
  statsSubText: {fontSize: 11, color: THEME.textLight},
  categoryCard: {backgroundColor: '#fff', borderRadius: 12, marginBottom: 14, overflow: 'hidden', elevation: 2},
  categoryHeader: {flexDirection: 'row', alignItems: 'center', padding: 14},
  categoryName: {flex: 1, fontSize: 16, fontWeight: 'bold', color: THEME.text},
  countBadge: {
    minWidth: 28,
    textAlign: 'center',
    fontSize: 12,
    color: '#5E4F3C',
    backgroundColor: '#FFFFFF',
    paddingVertical: 4,
    paddingHorizontal: 8,
    borderRadius: 12,
    marginRight: 8,
    overflow: 'hidden',
  },
  arrow: {fontSize: 12, color: THEME.textLight},
  stotraItem: {padding: 14, borderTopWidth: 1, borderTopColor: '#F0E8D8'},
  stotraTitle: {fontSize: 15, fontWeight: '600', color: THEME.primary, marginBottom: 4},
  metaLine: {fontSize: 12, color: THEME.textLight, marginBottom: 8},
  tagRow: {flexDirection: 'row', flexWrap: 'wrap', marginBottom: 8},
  tagChip: {
    backgroundColor: '#F7F1EA',
    borderRadius: 10,
    paddingHorizontal: 8,
    paddingVertical: 4,
    marginRight: 6,
    marginBottom: 6,
  },
  tagText: {fontSize: 11, color: '#7D6751'},
  sanskritBox: {backgroundColor: '#FFF8F0', borderRadius: 8, padding: 12, marginBottom: 8},
  sanskritText: {fontSize: 14, color: THEME.text, lineHeight: 22, fontStyle: 'italic'},
  meaningLabel: {fontSize: 12, fontWeight: 'bold', color: THEME.textLight, marginBottom: 4},
  meaningText: {fontSize: 13, color: THEME.text, lineHeight: 20},
  linkButton: {
    marginTop: 8,
    alignSelf: 'flex-start',
    backgroundColor: '#EFE5D9',
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 8,
  },
  linkButtonText: {fontSize: 12, color: '#6A4E35', fontWeight: '700'},
  emptyState: {
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
    marginBottom: 14,
  },
  emptyTitle: {fontSize: 15, fontWeight: '700', color: THEME.text, marginBottom: 6},
  emptyText: {fontSize: 13, color: THEME.textLight, lineHeight: 20},
  tipCard: {backgroundColor: '#E8F5E9', borderRadius: 12, padding: 14},
  tipText: {fontSize: 13, color: '#2E7D32', lineHeight: 20},
});

export default StotrasScreen;
