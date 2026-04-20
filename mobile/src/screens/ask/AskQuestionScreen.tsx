/**
 * Ask Question Screen
 * Intent-aware Q&A for all major astrology menus using chart-backed analyzers.
 */
import React, {useEffect, useMemo, useState} from 'react';
import {View, Text, StyleSheet, TextInput, TouchableOpacity, ScrollView, Alert, ActivityIndicator} from 'react-native';
import {THEME} from '../../constants/theme';
import {
  searchKnowledge,
  analyzeCareer,
  analyzeFinancial,
  getGemstoneRecommendations,
  getNameRecommendations,
  getMuhuratAnalysis,
  analyzeVarshaphal,
  analyzeCompatibility,
} from '../../services/PythonBridge';
import {getActiveProfileWithChart, getOrCreateChartForProfile, getProfiles, UserProfile} from '../../services/profileData';

const CATEGORY_LABELS: {[key: string]: string} = {
  career: 'Career & Profession',
  finance: 'Financial Outlook',
  gemstones: 'Gemstone Guide',
  matchmaking: 'Matchmaking',
  muhurat: 'Muhurat Finder',
  varshaphal: 'Varshaphal',
  name: 'Name Recommendation',
};

const QUESTION_SETS: {[key: string]: string[]} = {
  career: [
    'When can I expect a job offer?',
    'Will I get promotion this year or next year?',
    'Is this a good period for job switch?',
    'Which profession aligns best with my chart?',
    'Is business better than job for me now?',
    'How to improve career momentum in next 3 months?',
  ],
  finance: [
    'Is this a good period for investment?',
    'How should I manage debt and savings now?',
    'Can I expect salary growth in next 6 months?',
    'Which sectors are favorable for my finances?',
    'Should I take a conservative or aggressive approach now?',
    'When are better windows for major financial decisions?',
  ],
  gemstones: [
    'Which gemstone is best for my current dasha?',
    'When should I start wearing recommended gemstone?',
    'Is there any risk if I wear this gemstone now?',
    'Which metal and day are ideal for wearing?',
    'Can I use substitute stones effectively?',
    'Which gemstone supports career and finance both?',
  ],
  matchmaking: [
    'How strong is our compatibility overall?',
    'What are our biggest relationship strengths?',
    'What are conflict triggers and how to avoid them?',
    'Are marriage prospects favorable in near term?',
    'How can we improve communication compatibility?',
    'What remedies can improve marriage harmony?',
  ],
  muhurat: [
    'Find muhurat for marriage in next 2 months',
    'Best dates for business launch in next 30 days',
    'Good dates for housewarming this quarter',
    'Auspicious timings for travel plans',
    'Best dates for education-related beginning',
    'Which weekdays are strongest for my event type?',
  ],
  varshaphal: [
    'How is my overall year going?',
    'How is this year for career growth?',
    'How is this year for money and investments?',
    'How is relationship and family trend this year?',
    'Which months need caution this year?',
    'What remedies are most useful this year?',
  ],
  name: [
    'Which names are auspicious from my nakshatra?',
    'Best starting syllables for naming?',
    'Suggest names for baby boy',
    'Suggest names for baby girl',
    'Can I optimize spelling for better vibration?',
    'Can you suggest lucky business/store name roots?',
  ],
};

const DEFAULT_CATEGORY = 'career';
const PRESET_QUESTIONS: {[key: string]: string} = Object.keys(QUESTION_SETS).reduce((acc, key) => {
  acc[key] = QUESTION_SETS[key][0];
  return acc;
}, {} as {[key: string]: string});

const ASTRO_DOMAIN_KEYWORDS = [
  'chart', 'horoscope', 'kundli', 'kundali', 'lagna', 'ascendant', 'rashi', 'nakshatra', 'dasha', 'mahadasha',
  'planet', 'graha', 'transit', 'career', 'finance', 'investment', 'wealth', 'money', 'muhurat', 'matchmaking',
  'compatibility', 'gemstone', 'name', 'numerology', 'varshaphal', 'vedic', 'astrology', 'dosha', 'house',
  'marriage', 'remedy', 'yoga', 'prediction', 'bhava', 'moon sign', 'sun sign',
];

interface ProfileWithChart {
  profile: UserProfile;
  chart: any;
}

type CareerIntent = 'job' | 'promotion' | 'switch' | 'business' | 'salary' | 'general';
type FinanceIntent = 'investment' | 'debt' | 'salary' | 'risk' | 'savings' | 'general';
type MatchIntent = 'timing' | 'conflict' | 'communication' | 'compatibility' | 'remedy' | 'general';
type GemIntent = 'wearing' | 'safety' | 'substitute' | 'selection' | 'general';
type VarshaIntent = 'career' | 'finance' | 'relationship' | 'health' | 'general';
type NameIntent = 'boy' | 'girl' | 'business' | 'spelling' | 'general';
type MuhuratIntent = 'marriage' | 'business' | 'housewarming' | 'travel' | 'education';

type AskConfidence = 'High' | 'Moderate' | 'Selective';

interface ResolvedIntent {
  intent: string;
  usedLocalAI: boolean;
  wasAmbiguous: boolean;
}

interface AskCategoryResult {
  text: string;
}

const toTextList = (items: any[] = [], limit = 4): string[] => {
  if (!Array.isArray(items)) return [];
  return items
    .filter(Boolean)
    .slice(0, limit)
    .map(item => (typeof item === 'string' ? item : JSON.stringify(item)));
};

const getPlanetData = (planets: any, planet: string): any => {
  if (!planets) return null;
  if (Array.isArray(planets)) {
    return planets.find((p: any) => String(p?.name || '').toLowerCase() === planet.toLowerCase()) || null;
  }
  return planets?.[planet] || null;
};

const getPlanetHouse = (source: any, planet: string): number | null => {
  const data = getPlanetData(source?.planets || source, planet);
  const raw = Number(data?.house);
  if (!Number.isFinite(raw) || raw < 1 || raw > 12) {
    return null;
  }
  return Math.round(raw);
};

const scoreHouseStrength = (house: number | null, high: number, mid: number, low: number): number => {
  if (!house) return low;
  if ([2, 6, 10, 11].includes(house)) return high;
  if ([1, 5, 9].includes(house)) return mid;
  return low;
};

const addDays = (days: number): string => {
  const dt = new Date();
  dt.setDate(dt.getDate() + days);
  return dt.toISOString().slice(0, 10);
};

const buildWindowPack = (chart: any, planets: string[], topScore: number, basis: 'career' | 'finance' | 'relationship') => {
  let score = 0;

  planets.forEach(planet => {
    score += scoreHouseStrength(getPlanetHouse(chart, planet), 18, 10, 5);
    score += scoreHouseStrength(getPlanetHouse(chart?.divisional_charts?.D9, planet), 12, 7, 4);
    score += scoreHouseStrength(getPlanetHouse(chart?.divisional_charts?.D10, planet), 14, 9, 4);
    if (basis === 'finance') {
      score += scoreHouseStrength(getPlanetHouse(chart?.divisional_charts?.D2, planet), 16, 10, 5);
    }
  });

  const currentDasha = String(chart?.dasha?.current_dasha || chart?.dasha?.mahadasha || '').toLowerCase();
  if (planets.some(p => currentDasha.includes(p.toLowerCase()))) {
    score += 15;
  }

  score += Math.min(18, Math.round(topScore / 12));
  score = Math.max(20, Math.min(95, score));
  const confidence = score >= 72 ? 'High' : score >= 55 ? 'Moderate' : 'Selective';

  return {
    confidence,
    score,
    windows: [
      {label: 'Immediate', start: addDays(7), end: addDays(30)},
      {label: 'Follow-through', start: addDays(31), end: addDays(75)},
      {label: 'Consolidation', start: addDays(76), end: addDays(160)},
    ],
  };
};

const detectCareerIntent = (query: string): CareerIntent => {
  const q = query.toLowerCase();
  if (/job|offer|interview|hired|joining/.test(q)) return 'job';
  if (/promotion|appraisal|role upgrade|lead|manager/.test(q)) return 'promotion';
  if (/switch|change job|transition|move company|new domain/.test(q)) return 'switch';
  if (/business|startup|entrepreneur|own work/.test(q)) return 'business';
  if (/salary|income|package|raise|increment/.test(q)) return 'salary';
  return 'general';
};

const detectFinanceIntent = (query: string): FinanceIntent => {
  const q = query.toLowerCase();
  if (/invest|investment|stock|mutual fund|property/.test(q)) return 'investment';
  if (/debt|loan|emi/.test(q)) return 'debt';
  if (/salary|income|increment|raise|package/.test(q)) return 'salary';
  if (/risk|volatile|safe|conservative|aggressive/.test(q)) return 'risk';
  if (/save|savings|budget|expenses/.test(q)) return 'savings';
  return 'general';
};

const detectMatchIntent = (query: string): MatchIntent => {
  const q = query.toLowerCase();
  if (/marriage timing|when.*marry|wedding/.test(q)) return 'timing';
  if (/conflict|fight|argument|ego/.test(q)) return 'conflict';
  if (/communication|understand|emotional/.test(q)) return 'communication';
  if (/remedy|improve|harmony|solution/.test(q)) return 'remedy';
  if (/compatibility|match|score|guna/.test(q)) return 'compatibility';
  return 'general';
};

const detectGemIntent = (query: string): GemIntent => {
  const q = query.toLowerCase();
  if (/wear|when|start|day|metal/.test(q)) return 'wearing';
  if (/safe|risk|side effect|harm/.test(q)) return 'safety';
  if (/substitute|alternative|uparatna/.test(q)) return 'substitute';
  if (/which|best|recommend/.test(q)) return 'selection';
  return 'general';
};

const detectVarshaIntent = (query: string): VarshaIntent => {
  const q = query.toLowerCase();
  if (/career|job|promotion/.test(q)) return 'career';
  if (/money|finance|investment|income/.test(q)) return 'finance';
  if (/relationship|marriage|family|love/.test(q)) return 'relationship';
  if (/health|stress|disease|fitness/.test(q)) return 'health';
  return 'general';
};

const detectNameIntent = (query: string): NameIntent => {
  const q = query.toLowerCase();
  if (/boy|son|male/.test(q)) return 'boy';
  if (/girl|daughter|female/.test(q)) return 'girl';
  if (/business|brand|company|store|shop/.test(q)) return 'business';
  if (/spelling|numerology spelling|letter change/.test(q)) return 'spelling';
  return 'general';
};

const deriveMuhuratEventType = (query: string): string => {
  const q = query.toLowerCase();
  if (/marriage|wedding|vivah/.test(q)) return 'marriage';
  if (/business|shop|office|launch/.test(q)) return 'business';
  if (/housewarming|griha|home entry/.test(q)) return 'housewarming';
  if (/travel|journey|trip/.test(q)) return 'travel';
  if (/education|study|admission|course/.test(q)) return 'education';
  return 'business';
};

const isAstroDomainQuestion = (query: string): boolean => {
  const q = query.toLowerCase();
  return ASTRO_DOMAIN_KEYWORDS.some(keyword => q.includes(keyword));
};

const buildOutOfDomainReply = (question: string): string => {
  return [
    `You can ask anything, but I am specialized for astrology and chart-based guidance.`,
    '',
    `For this question: "${question}"`,
    `I cannot give a reliable personalized answer from astrology engines because it is outside the core domain.`,
    '',
    'Best results are for: career timing, finance outlook, gemstones, matchmaking, muhurat, varshaphal, remedies, and name guidance.',
    'If you want, ask this in astrology form and I will answer with your D1/D2/D3/D7/D9/D10 chart context.',
  ].join('\n');
};

const hasExplicitMuhuratEvent = (query: string): boolean => {
  const q = query.toLowerCase();
  return /marriage|wedding|vivah|business|shop|office|launch|housewarming|griha|home entry|travel|journey|trip|education|study|admission|course/.test(q);
};

const extractClassifierLabel = (text: string, allowed: string[]): string | null => {
  const normalized = String(text || '').toLowerCase();
  for (const label of allowed) {
    if (normalized.includes(label.toLowerCase())) {
      return label;
    }
  }
  return null;
};

const inferIntentWithLocalAI = async (
  query: string,
  allowed: string[],
): Promise<string | null> => {
  try {
    const prompt = [
      'Classify the user question into exactly one label.',
      `Labels: ${allowed.join(', ')}`,
      'Return only the label.',
      `Question: ${query}`,
    ].join(' ');

    const response = await searchKnowledge(prompt);
    const text = String(response?.results?.[0]?.text || '');
    return extractClassifierLabel(text, allowed);
  } catch {
    return null;
  }
};

const confidenceFromScore = (score: number): AskConfidence => {
  if (score >= 72) return 'High';
  if (score >= 55) return 'Moderate';
  return 'Selective';
};

const clampScore = (value: number, min = 20, max = 95): number => {
  return Math.max(min, Math.min(max, value));
};

const resolveIntentWithFallback = async (category: string, query: string): Promise<ResolvedIntent> => {
  switch (category) {
    case 'career': {
      const detected = detectCareerIntent(query);
      if (detected !== 'general') return {intent: detected, usedLocalAI: false, wasAmbiguous: false};
      const inferred = await inferIntentWithLocalAI(query, ['job', 'promotion', 'switch', 'business', 'salary', 'general']);
      return {intent: inferred || detected, usedLocalAI: Boolean(inferred && inferred !== 'general'), wasAmbiguous: true};
    }
    case 'finance': {
      const detected = detectFinanceIntent(query);
      if (detected !== 'general') return {intent: detected, usedLocalAI: false, wasAmbiguous: false};
      const inferred = await inferIntentWithLocalAI(query, ['investment', 'debt', 'salary', 'risk', 'savings', 'general']);
      return {intent: inferred || detected, usedLocalAI: Boolean(inferred && inferred !== 'general'), wasAmbiguous: true};
    }
    case 'matchmaking': {
      const detected = detectMatchIntent(query);
      if (detected !== 'general') return {intent: detected, usedLocalAI: false, wasAmbiguous: false};
      const inferred = await inferIntentWithLocalAI(query, ['timing', 'conflict', 'communication', 'compatibility', 'remedy', 'general']);
      return {intent: inferred || detected, usedLocalAI: Boolean(inferred && inferred !== 'general'), wasAmbiguous: true};
    }
    case 'gemstones': {
      const detected = detectGemIntent(query);
      if (detected !== 'general') return {intent: detected, usedLocalAI: false, wasAmbiguous: false};
      const inferred = await inferIntentWithLocalAI(query, ['wearing', 'safety', 'substitute', 'selection', 'general']);
      return {intent: inferred || detected, usedLocalAI: Boolean(inferred && inferred !== 'general'), wasAmbiguous: true};
    }
    case 'varshaphal': {
      const detected = detectVarshaIntent(query);
      if (detected !== 'general') return {intent: detected, usedLocalAI: false, wasAmbiguous: false};
      const inferred = await inferIntentWithLocalAI(query, ['career', 'finance', 'relationship', 'health', 'general']);
      return {intent: inferred || detected, usedLocalAI: Boolean(inferred && inferred !== 'general'), wasAmbiguous: true};
    }
    case 'name': {
      const detected = detectNameIntent(query);
      if (detected !== 'general') return {intent: detected, usedLocalAI: false, wasAmbiguous: false};
      const inferred = await inferIntentWithLocalAI(query, ['boy', 'girl', 'business', 'spelling', 'general']);
      return {intent: inferred || detected, usedLocalAI: Boolean(inferred && inferred !== 'general'), wasAmbiguous: true};
    }
    case 'muhurat': {
      const detected = deriveMuhuratEventType(query) as MuhuratIntent;
      if (hasExplicitMuhuratEvent(query)) {
        return {intent: detected, usedLocalAI: false, wasAmbiguous: false};
      }
      const inferred = await inferIntentWithLocalAI(query, ['marriage', 'business', 'housewarming', 'travel', 'education']);
      return {intent: inferred || detected, usedLocalAI: Boolean(inferred), wasAmbiguous: true};
    }
    default:
      return {intent: 'general', usedLocalAI: false, wasAmbiguous: false};
  }
};

const computeAnswerConfidence = (category: string, data: any, intentMeta: ResolvedIntent): AskConfidence => {
  let score = 58;

  switch (category) {
    case 'career':
      score = Number(data?.recommendations?.[0]?.score || 58);
      break;
    case 'finance':
      score = Number(data?.personalized?.recommendations?.[0]?.total_strength || data?.market?.overall_strength || 58);
      break;
    case 'varshaphal':
      score = Number(data?.overall_rating || 60);
      break;
    case 'matchmaking':
      score = Number(data?.percentage || 55);
      break;
    case 'gemstones': {
      const primaryCount = Array.isArray(data?.primary_recommendations) ? data.primary_recommendations.length : 0;
      const anyCount =
        primaryCount +
        (Array.isArray(data?.secondary_recommendations) ? data.secondary_recommendations.length : 0) +
        (Array.isArray(data?.supporting_recommendations) ? data.supporting_recommendations.length : 0);
      score = primaryCount > 0 ? 76 : anyCount > 0 ? 62 : 45;
      break;
    }
    case 'name': {
      const suggestions = Array.isArray(data?.name_suggestions) ? data.name_suggestions.length : 0;
      score = suggestions >= 5 ? 74 : suggestions > 0 ? 60 : 46;
      break;
    }
    case 'muhurat': {
      const upcoming = Array.isArray(data?.upcoming_dates) ? data.upcoming_dates.length : 0;
      score = upcoming >= 4 ? 72 : upcoming > 0 ? 58 : 46;
      break;
    }
    default:
      score = 55;
      break;
  }

  if (intentMeta.usedLocalAI) score -= 6;
  if (intentMeta.wasAmbiguous && !intentMeta.usedLocalAI) score -= 10;

  return confidenceFromScore(clampScore(score));
};

const formatCareer = (data: any, query: string, chart: any, intentOverride?: CareerIntent): string => {
  if (!data?.success) {
    return data?.error || 'Career analysis could not be generated right now.';
  }

  const intent = intentOverride || detectCareerIntent(query);
  const topScore = Number(data?.recommendations?.[0]?.score || 0);
  const planetsByIntent: Record<CareerIntent, string[]> = {
    job: ['Saturn', 'Mercury', 'Sun'],
    promotion: ['Sun', 'Jupiter', 'Saturn'],
    switch: ['Rahu', 'Mercury', 'Mars'],
    business: ['Mercury', 'Jupiter', 'Mars'],
    salary: ['Jupiter', 'Venus', 'Sun'],
    general: ['Saturn', 'Mercury', 'Jupiter'],
  };
  const windows = buildWindowPack(chart, planetsByIntent[intent], topScore, 'career');

  const introByIntent: Record<CareerIntent, string> = {
    job: 'Direct Answer: Job opportunity is active, strongest in the first two windows below.',
    promotion: 'Direct Answer: Promotion potential is realistic when visibility and role ownership increase in near term.',
    switch: 'Direct Answer: A switch is possible; targeted moves are better than broad random applications.',
    business: 'Direct Answer: Independent/business path is supported if launched with phased execution.',
    salary: 'Direct Answer: Salary growth is likely through role-value proof plus timed negotiation.',
    general: 'Direct Answer: Career growth is supported with timing and sector alignment.',
  };

  const recs = Array.isArray(data?.recommendations) ? data.recommendations.slice(0, 3) : [];
  const lines: string[] = [
    introByIntent[intent],
    '',
    `Timing Confidence: ${windows.confidence} (${windows.score}/95)`,
    'Basis: D1 + D9 + D10 + current dasha.',
    '',
    'Practical Windows',
    ...windows.windows.map((w: any, i: number) => `${i + 1}. ${w.label}: ${w.start} to ${w.end}`),
    '',
    'Top Career Sectors',
  ];

  recs.forEach((rec: any, i: number) => {
    lines.push(
      `${i + 1}. ${rec?.sector || 'Sector'} (${rec?.strength || 'Good'})`,
      `Score: ${rec?.score ?? '-'} / ${rec?.max_score ?? '-'}`,
      `Guidance: ${rec?.advice || 'Focus on consistent skill-building and practical execution.'}`,
    );
    const factors = toTextList(rec?.factors, 2);
    if (factors.length) {
      lines.push(`Why: ${factors.join(' | ')}`);
    }
    lines.push('');
  });

  return lines.join('\n').trim();
};

const formatFinancial = (data: any, query: string, chart: any, intentOverride?: FinanceIntent): string => {
  if (!data?.success) {
    return data?.error || 'Financial analysis could not be generated right now.';
  }

  const intent = intentOverride || detectFinanceIntent(query);
  const topScore = Number(data?.personalized?.recommendations?.[0]?.total_strength || 0);
  const planetsByIntent: Record<FinanceIntent, string[]> = {
    investment: ['Jupiter', 'Mercury', 'Venus'],
    debt: ['Saturn', 'Mars', 'Jupiter'],
    salary: ['Jupiter', 'Sun', 'Mercury'],
    risk: ['Saturn', 'Rahu', 'Mercury'],
    savings: ['Saturn', 'Moon', 'Jupiter'],
    general: ['Jupiter', 'Mercury', 'Saturn'],
  };
  const windows = buildWindowPack(chart, planetsByIntent[intent], topScore, 'finance');

  const intentAnswer: Record<FinanceIntent, string> = {
    investment: 'Direct Answer: Investment is feasible, but allocate gradually and avoid concentrated risk.',
    debt: 'Direct Answer: Debt reduction should be prioritized before high-risk growth moves.',
    salary: 'Direct Answer: Income growth is possible through role-value visibility and timed negotiation.',
    risk: 'Direct Answer: Use selective risk now; preserve capital on weak windows.',
    savings: 'Direct Answer: Savings discipline is more rewarding than speculative decisions right now.',
    general: 'Direct Answer: Financial outlook is workable with disciplined timing and risk control.',
  };

  const market = data?.market || {};
  const personal = Array.isArray(data?.personalized?.recommendations)
    ? data.personalized.recommendations.slice(0, 3)
    : [];

  const lines: string[] = [
    intentAnswer[intent],
    '',
    `Timing Confidence: ${windows.confidence} (${windows.score}/95)`,
    'Basis: D1 + D2 + D9 + D10 + current dasha.',
    '',
    'Practical Windows',
    ...windows.windows.map((w: any, i: number) => `${i + 1}. ${w.label}: ${w.start} to ${w.end}`),
    '',
    `Market Sentiment: ${market?.market_sentiment || 'Neutral'}`,
    `Overall Strength: ${market?.overall_strength ?? 'N/A'}`,
    '',
    'Personalized Sector Picks',
  ];

  personal.forEach((rec: any, index: number) => {
    lines.push(
      `${index + 1}. ${rec?.sector || 'Sector'} (${rec?.rating || 'Moderate'})`,
      `Natal: ${rec?.natal_strength ?? '-'} | Transit: ${rec?.transit_strength ?? '-'} | Total: ${rec?.total_strength ?? '-'}`,
      `Guidance: ${rec?.advice || 'Invest with disciplined risk management and gradual allocation.'}`,
      '',
    );
  });

  return lines.join('\n').trim();
};

const formatGemstones = (data: any, query: string, intentOverride?: GemIntent): string => {
  const primary = Array.isArray(data?.primary_recommendations) ? data.primary_recommendations : [];
  const secondary = Array.isArray(data?.secondary_recommendations) ? data.secondary_recommendations : [];
  const supporting = Array.isArray(data?.supporting_recommendations) ? data.supporting_recommendations : [];
  const all = [...primary, ...secondary, ...supporting].slice(0, 3);
  const intent = intentOverride || detectGemIntent(query);

  if (!all.length) {
    return 'No high-priority gemstone is required right now. Your chart appears balanced for this concern.';
  }

  let directAnswer = 'Direct Answer: Top gemstone recommendations are listed below.';
  if (intent === 'wearing') {
    directAnswer = 'Direct Answer: Start gemstone wearing on the suggested day in waxing Moon phase when possible.';
  }
  if (intent === 'safety') {
    directAnswer = 'Direct Answer: Gemstone should be worn only if matching your chart recommendation and current dasha support.';
  }
  if (intent === 'substitute') {
    directAnswer = 'Direct Answer: Substitute stones can work with lower intensity; choose chart-aligned options only.';
  }

  const lines: string[] = [directAnswer, '', 'Recommended Gemstones'];
  all.forEach((rec: any, index: number) => {
    lines.push(
      `${index + 1}. ${rec?.primary || 'Gemstone'} (${rec?.priority || 'Suggested'})`,
      `Planet: ${rec?.planet || '-'} | Metal: ${rec?.metal || '-'} | Day: ${rec?.day || '-'}`,
      `Benefit: ${rec?.benefits || 'Strengthens favorable planetary outcomes.'}`,
    );
    if (rec?.reason) {
      lines.push(`Reason: ${rec.reason}`);
    }
    lines.push('');
  });

  return lines.join('\n').trim();
};

const formatNames = (data: any, query: string, intentOverride?: NameIntent): string => {
  if (!data?.success) {
    return data?.error || 'Name recommendations could not be generated right now.';
  }

  const intent = intentOverride || detectNameIntent(query);
  const suggested = toTextList(data?.name_suggestions, 8);
  const syllables = toTextList(data?.traditional_syllables, 4);

  let directAnswer = 'Direct Answer: Use nakshatra-linked syllables first, then choose natural pronunciation.';
  if (intent === 'boy') directAnswer = 'Direct Answer: Boy-name options should start from the same auspicious syllable group.';
  if (intent === 'girl') directAnswer = 'Direct Answer: Girl-name options should remain within your nakshatra syllable band.';
  if (intent === 'business') directAnswer = 'Direct Answer: Business names should start with your auspicious syllables and be easy to recall.';
  if (intent === 'spelling') directAnswer = 'Direct Answer: Spelling optimization can be done, but keep phonetic clarity primary.';

  return [
    directAnswer,
    '',
    `Moon Nakshatra: ${data?.moon_nakshatra || 'Unknown'}`,
    `Ruling Planet: ${data?.nakshatra_lord || 'Unknown'}`,
    `Auspicious Syllables: ${syllables.join(', ') || 'N/A'}`,
    '',
    `Suggested Names: ${suggested.join(', ') || 'N/A'}`,
    '',
    `Guidance: ${(toTextList(data?.naming_guidance, 1)[0]) || 'Choose a melodious name aligned with nakshatra sounds.'}`,
  ].join('\n');
};

const formatMuhurat = (data: any, query: string, eventTypeOverride?: MuhuratIntent): string => {
  if (!data?.success) {
    return data?.error || 'Muhurat guidance could not be generated right now.';
  }

  const eventType = eventTypeOverride || (deriveMuhuratEventType(query) as MuhuratIntent);
  const days = toTextList(data?.favorable_days, 4).join(', ');
  const tips = toTextList(data?.personal_tips, 3);
  const upcoming = Array.isArray(data?.upcoming_dates) ? data.upcoming_dates.slice(0, 5) : [];

  const lines: string[] = [
    `Direct Answer: Best current muhurat pattern for ${eventType} is shown below.`,
    '',
    `Range Used: ${(data?.selected_range?.start_date || '-')} to ${(data?.selected_range?.end_date || '-')}`,
    `Current Month (${data?.current_month || 'Now'}): ${data?.current_month_favorable ? 'Favorable' : 'Use selective windows'}`,
    `Best Days: ${days || 'N/A'}`,
    '',
    'Upcoming Good Dates',
  ];

  upcoming.forEach((item: any) => {
    lines.push(`- ${item?.date || '-'} (${item?.day || '-'})`);
  });

  if (tips.length) {
    lines.push('', 'Personal Tips');
    tips.forEach(t => lines.push(`- ${t}`));
  }

  return lines.join('\n').trim();
};

const formatVarshaphal = (data: any, query: string, chart: any, intentOverride?: VarshaIntent): string => {
  if (!data?.success) {
    return data?.error || 'Varshaphal analysis could not be generated right now.';
  }

  const intent = intentOverride || detectVarshaIntent(query);
  const topScore = Number(data?.overall_rating || 60);
  const planetsByIntent: Record<VarshaIntent, string[]> = {
    career: ['Sun', 'Saturn', 'Mercury'],
    finance: ['Jupiter', 'Venus', 'Mercury'],
    relationship: ['Venus', 'Moon', 'Jupiter'],
    health: ['Sun', 'Mars', 'Moon'],
    general: ['Sun', 'Jupiter', 'Saturn'],
  };
  const windows = buildWindowPack(chart, planetsByIntent[intent], topScore, 'career');

  const highlights = toTextList((data?.year_highlights || []).map((h: any) => h?.forecast), 3);
  const challenges = toTextList(data?.challenges, 3);
  const remedies = toTextList(data?.remedies, 3);

  return [
    'Direct Answer: Annual trend is actionable with month-wise focus and remedy discipline.',
    '',
    `Year ${data?.year || ''} Forecast`,
    data?.overall_forecast || 'Steady progress with disciplined effort.',
    '',
    `Timing Confidence: ${windows.confidence} (${windows.score}/95)`,
    'Practical Windows (near-term)',
    ...windows.windows.map((w: any, i: number) => `${i + 1}. ${w.label}: ${w.start} to ${w.end}`),
    '',
    'Major Highlights',
    ...highlights.map(h => `- ${h}`),
    '',
    'Key Challenges',
    ...challenges.map(c => `- ${c}`),
    '',
    'Helpful Remedies',
    ...remedies.map(r => `- ${r}`),
  ].join('\n').trim();
};

const formatCompatibility = (data: any, query: string, chart: any, intentOverride?: MatchIntent): string => {
  if (!data?.success) {
    return data?.error || 'Compatibility analysis could not be generated right now.';
  }

  const intent = intentOverride || detectMatchIntent(query);
  const topScore = Number(data?.percentage || 50);
  const windows = buildWindowPack(chart, ['Venus', 'Jupiter', 'Moon'], topScore, 'relationship');

  const strengths = toTextList(data?.strengths, 3);
  const challenges = toTextList(data?.challenges, 3);
  const remedies = toTextList(data?.remedies, 3);

  let direct = 'Direct Answer: Compatibility is measured and workable using strengths + remedy discipline.';
  if (intent === 'timing') {
    direct = 'Direct Answer: Relationship timing is better in the first two windows if communication remains stable.';
  }
  if (intent === 'conflict') {
    direct = 'Direct Answer: Conflict risk can be reduced with predictable communication and routine clarity.';
  }
  if (intent === 'communication') {
    direct = 'Direct Answer: Communication improves when emotional validation is prioritized before logic.';
  }
  if (intent === 'remedy') {
    direct = 'Direct Answer: Remedies can improve harmony when done consistently by both partners.';
  }

  const lines: string[] = [
    direct,
    '',
    `Compatibility Score: ${data?.gunas ?? '-'} / ${data?.max_gunas ?? 36} (${data?.percentage ?? '-'}%)`,
    `Result: ${data?.category || 'Compatibility report'}`,
    `Moon Signs: ${data?.moon_sign_a || '-'} ↔ ${data?.moon_sign_b || '-'}`,
    `Ascendants: ${data?.ascendant_a || '-'} ↔ ${data?.ascendant_b || '-'}`,
  ];

  if (intent === 'timing') {
    lines.push('', `Timing Confidence: ${windows.confidence} (${windows.score}/95)`, 'Near-term Windows');
    windows.windows.forEach((w: any, i: number) => lines.push(`${i + 1}. ${w.label}: ${w.start} to ${w.end}`));
  }

  lines.push(
    '',
    'Strengths',
    ...strengths.map(s => `- ${s}`),
    '',
    'Challenges',
    ...challenges.map(c => `- ${c}`),
    '',
    'Remedies',
    ...remedies.map(r => `- ${r}`),
  );

  return lines.join('\n').trim();
};

const formatCategoryAnswer = (category: string, data: any, chart: any, query: string, resolvedIntent: string): AskCategoryResult => {
  switch (category) {
    case 'career':
      return {
        text: formatCareer(data, query, chart, resolvedIntent as CareerIntent),
      };
    case 'finance':
      return {
        text: formatFinancial(data, query, chart, resolvedIntent as FinanceIntent),
      };
    case 'gemstones':
      return {
        text: formatGemstones(data, query, resolvedIntent as GemIntent),
      };
    case 'name':
      return {
        text: formatNames(data, query, resolvedIntent as NameIntent),
      };
    case 'muhurat':
      return {
        text: formatMuhurat(data, query, resolvedIntent as MuhuratIntent),
      };
    case 'varshaphal':
      return {
        text: formatVarshaphal(data, query, chart, resolvedIntent as VarshaIntent),
      };
    case 'matchmaking':
      return {
        text: formatCompatibility(data, query, chart, resolvedIntent as MatchIntent),
      };
    default:
      return {
        text: 'Please select a valid category and ask your question.',
      };
  }
};

const AskQuestionScreen = ({route}: any) => {
  const preset = route?.params?.preset;
  const [selectedCategory, setSelectedCategory] = useState(DEFAULT_CATEGORY);
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [answer, setAnswer] = useState('');
  const [answerConfidence, setAnswerConfidence] = useState<AskConfidence | null>(null);
  const [profileWithChart, setProfileWithChart] = useState<ProfileWithChart | null>(null);

  const currentQuestionSet = useMemo(() => QUESTION_SETS[selectedCategory] || QUESTION_SETS[DEFAULT_CATEGORY], [selectedCategory]);

  useEffect(() => {
    void loadProfileAndPreset();
  }, [preset]);

  const loadProfileAndPreset = async () => {
    try {
      const data = await getActiveProfileWithChart();
      setProfileWithChart(data);
    } catch (err) {
      console.log('No active profile with chart:', err);
      setProfileWithChart(null);
    }

    const category = preset && CATEGORY_LABELS[preset] ? preset : DEFAULT_CATEGORY;
    setSelectedCategory(category);
    setQuery(PRESET_QUESTIONS[category] || PRESET_QUESTIONS[DEFAULT_CATEGORY]);
    setAnswerConfidence(null);
  };

  const handleSearch = async () => {
    if (!query.trim()) {
      Alert.alert('Validation', 'Please enter a question');
      return;
    }

    setLoading(true);
    try {
      const trimmedQuery = query.trim();
      if (!isAstroDomainQuestion(trimmedQuery)) {
        setAnswer(buildOutOfDomainReply(trimmedQuery));
        setAnswerConfidence('Selective');
        return;
      }

      if (!profileWithChart?.chart) {
        Alert.alert('No Profile', 'Please create and select a profile first to get personalized astrology answers');
        return;
      }

      let responseData: any = null;
      const chartJson = JSON.stringify(profileWithChart.chart);
      const resolved = await resolveIntentWithFallback(selectedCategory, trimmedQuery);

      switch (selectedCategory) {
        case 'career':
          responseData = await analyzeCareer(chartJson);
          break;

        case 'finance':
          responseData = await analyzeFinancial(chartJson);
          break;

        case 'gemstones':
          responseData = await getGemstoneRecommendations(chartJson, trimmedQuery);
          break;

        case 'name':
          responseData = await getNameRecommendations(chartJson, 'male');
          break;

        case 'muhurat':
          responseData = await getMuhuratAnalysis(chartJson, resolved.intent);
          break;

        case 'varshaphal':
          responseData = await analyzeVarshaphal(chartJson);
          break;

        case 'matchmaking': {
          const profiles = await getProfiles();
          const activeId = profileWithChart.profile.id;
          const other = profiles.find(p => p.id !== activeId);
          if (!other) {
            setAnswer('Matchmaking requires two profiles. Please add another person profile in Profiles, then retry.');
            setLoading(false);
            return;
          }
          const otherChart = await getOrCreateChartForProfile(other);
          responseData = await analyzeCompatibility(chartJson, JSON.stringify(otherChart));
          break;
        }

        default:
          setAnswer('Please select a valid category first.');
          setAnswerConfidence(null);
          setLoading(false);
          return;
      }

      const formatted = formatCategoryAnswer(selectedCategory, responseData, profileWithChart.chart, trimmedQuery, resolved.intent);
      const confidence = computeAnswerConfidence(selectedCategory, responseData, resolved);
      setAnswer(formatted.text);
      setAnswerConfidence(confidence);
    } catch (error: any) {
      console.error('Error:', error);
      Alert.alert('Error', error?.message || 'Failed to analyze your chart. Please try again.');
      setAnswerConfidence(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      {profileWithChart ? (
        <View style={styles.profileBanner}>
          <Text style={styles.profileName}>👤 {profileWithChart.profile.name}</Text>
          <Text style={styles.profileDetails}>{profileWithChart.profile.date} • {profileWithChart.profile.location}</Text>
        </View>
      ) : (
        <View style={styles.warningBanner}>
          <Text style={styles.warningText}>⚠️ No profile selected. Create a profile first for personalized answers.</Text>
        </View>
      )}

      <View style={styles.powered}>
        <Text style={styles.poweredText}>💡 Intent-aware ask engine: typed questions are mapped to chart-backed answers with realistic timing where relevant.</Text>
        <Text style={styles.scopeHint}>You can ask any question. Best answers are astrology-focused and read your D1/D2/D3/D7/D9/D10 chart context.</Text>
      </View>

      <Text style={styles.fieldLabel}>Choose a question category:</Text>
      <View style={styles.categoryRow}>
        {Object.keys(CATEGORY_LABELS).map(key => (
          <TouchableOpacity
            key={key}
            style={[styles.categoryChip, selectedCategory === key && styles.categoryChipActive]}
            onPress={() => {
              setSelectedCategory(key);
              setQuery(PRESET_QUESTIONS[key]);
            }}>
            <Text style={[styles.categoryText, selectedCategory === key && styles.categoryTextActive]}>
              {CATEGORY_LABELS[key]}
            </Text>
          </TouchableOpacity>
        ))}
      </View>

      <Text style={styles.fieldLabel}>Suggested Questions:</Text>
      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.suggestRow}>
        {currentQuestionSet.map(item => (
          <TouchableOpacity key={item} style={styles.suggestChip} onPress={() => setQuery(item)}>
            <Text style={styles.suggestText}>{item}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <Text style={styles.fieldLabel}>Question:</Text>
      <TextInput
        style={styles.input}
        value={query}
        onChangeText={setQuery}
        multiline
        placeholder="Ask your question..."
        placeholderTextColor="#999"
      />

      <TouchableOpacity style={[styles.button, loading || !profileWithChart?.chart ? styles.buttonDisabled : {}]} onPress={handleSearch} disabled={loading || !profileWithChart?.chart}>
        {loading ? <ActivityIndicator color="#fff" /> : <Text style={styles.buttonText}>🔮 Get Personalized Answer</Text>}
      </TouchableOpacity>

      {answer ? (
        <View style={styles.answerCard}>
          <View style={styles.answerHeader}>
            <Text style={styles.answerTitle}>📘 Personalized Answer:</Text>
            {answerConfidence ? (
              <View style={[styles.confidenceBadge, answerConfidence === 'High' ? styles.confidenceHigh : answerConfidence === 'Moderate' ? styles.confidenceModerate : styles.confidenceSelective]}>
                <Text style={styles.confidenceText}>{answerConfidence} Confidence</Text>
              </View>
            ) : null}
          </View>
          <Text style={styles.answerText}>{answer}</Text>
          <View style={styles.answerMeta}>
            <Text style={styles.answerMetaText}>
              ✨ Based on {profileWithChart?.profile.name}'s chart • Category: {CATEGORY_LABELS[selectedCategory]}
            </Text>
          </View>
        </View>
      ) : null}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {flex: 1, backgroundColor: THEME.background},
  content: {padding: 16, paddingBottom: 24},
  profileBanner: {backgroundColor: '#E8F4F8', borderRadius: 10, padding: 12, marginBottom: 12, borderLeftWidth: 4, borderLeftColor: THEME.primary},
  profileName: {fontSize: 15, fontWeight: '700', color: THEME.text, marginBottom: 4},
  profileDetails: {fontSize: 12, color: THEME.textLight},
  warningBanner: {backgroundColor: '#FEE2E2', borderRadius: 10, padding: 12, marginBottom: 12, borderLeftWidth: 4, borderLeftColor: '#DC2626'},
  warningText: {fontSize: 12, color: '#991B1B', fontWeight: '500'},
  powered: {backgroundColor: '#FEF3C7', borderRadius: 8, padding: 12, marginBottom: 12},
  poweredText: {fontSize: 12, color: '#92400E', fontWeight: '600'},
  scopeHint: {fontSize: 11, color: '#7C3A00', marginTop: 6},
  fieldLabel: {fontSize: 13, color: THEME.textLight, marginBottom: 8, fontWeight: '600'},
  categoryRow: {flexDirection: 'row', flexWrap: 'wrap', gap: 8, marginBottom: 14},
  categoryChip: {borderWidth: 1, borderColor: THEME.primary, borderRadius: 14, paddingHorizontal: 11, paddingVertical: 7, backgroundColor: '#fff'},
  categoryChipActive: {backgroundColor: THEME.primary},
  categoryText: {fontSize: 12, color: THEME.primary, fontWeight: '500'},
  categoryTextActive: {color: '#fff'},
  suggestRow: {marginBottom: 12},
  suggestChip: {borderRadius: 14, backgroundColor: '#EFF6FF', paddingHorizontal: 10, paddingVertical: 8, marginRight: 8, borderWidth: 1, borderColor: '#C9E0FF'},
  suggestText: {fontSize: 12, color: '#234A83'},
  input: {backgroundColor: '#fff', borderColor: '#E0E0E0', borderWidth: 1, borderRadius: 10, paddingHorizontal: 12, paddingVertical: 11, marginBottom: 12, minHeight: 90, textAlignVertical: 'top', color: THEME.text, fontSize: 13},
  button: {backgroundColor: THEME.primary, borderRadius: 10, paddingVertical: 13, paddingHorizontal: 16, alignItems: 'center', alignSelf: 'flex-start', marginBottom: 14},
  buttonDisabled: {opacity: 0.5},
  buttonText: {color: '#fff', fontWeight: '700', fontSize: 14},
  answerCard: {backgroundColor: THEME.card, borderRadius: 12, padding: 14, marginTop: 12, borderLeftWidth: 4, borderLeftColor: THEME.primary},
  answerHeader: {flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10, gap: 8},
  answerTitle: {fontSize: 15, fontWeight: '700', color: THEME.text, marginBottom: 10},
  confidenceBadge: {paddingHorizontal: 8, paddingVertical: 4, borderRadius: 999},
  confidenceHigh: {backgroundColor: '#DCFCE7'},
  confidenceModerate: {backgroundColor: '#FEF9C3'},
  confidenceSelective: {backgroundColor: '#FEE2E2'},
  confidenceText: {fontSize: 11, fontWeight: '700', color: '#1F2937'},
  answerText: {fontSize: 13, color: THEME.text, lineHeight: 21, marginBottom: 10},
  answerMeta: {backgroundColor: '#ECFDF5', borderRadius: 8, padding: 10, marginTop: 8},
  answerMetaText: {fontSize: 11, color: '#065F46', fontWeight: '500'},
});

export default AskQuestionScreen;
