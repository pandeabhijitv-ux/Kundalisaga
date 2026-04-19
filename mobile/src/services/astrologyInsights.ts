import {ChartData} from './PythonBridge';

const PLANET_ORDER = [
  'Sun',
  'Moon',
  'Mars',
  'Mercury',
  'Jupiter',
  'Venus',
  'Saturn',
  'Rahu',
  'Ketu',
];

const NAME_ROOTS = [
  'Aar',
  'Dev',
  'Ish',
  'Kri',
  'Lak',
  'Man',
  'Rit',
  'Sha',
  'Tan',
  'Viv',
  'Yog',
  'Zen',
];

const NAME_SUFFIXES = ['av', 'ika', 'esh', 'ita', 'ansh', 'ika', 'raj', 'aya'];

const ACTIVITY_TAGS: Record<string, string[]> = {
  'Marriage / Vivah': ['Venus', 'Jupiter', 'Moon'],
  'Griha Pravesh (Housewarming)': ['Moon', 'Jupiter', 'Mercury'],
  'Business Inauguration': ['Mercury', 'Jupiter', 'Sun'],
  'Vehicle Purchase': ['Venus', 'Moon', 'Mars'],
  'Travel / Journey': ['Moon', 'Mercury', 'Rahu'],
  'Medical Procedure': ['Sun', 'Mars', 'Ketu'],
  'Education / Vidyarambha': ['Jupiter', 'Mercury', 'Moon'],
  'Investment & Finance': ['Jupiter', 'Mercury', 'Venus'],
};

export type PlanetLike = {
  name: string;
  sign: string;
  degree: number;
  house: number;
  longitude?: number;
};

const toPlanetsArray = (chart: ChartData): PlanetLike[] => {
  if (Array.isArray(chart?.planets)) {
    return chart.planets as PlanetLike[];
  }
  return Object.values((chart as any)?.planets || {}) as PlanetLike[];
};

const getPlanet = (chart: ChartData, name: string): PlanetLike | null => {
  const p = toPlanetsArray(chart).find(
    x => x?.name?.toLowerCase() === name.toLowerCase(),
  );
  return p || null;
};

const safeHouse = (planet: PlanetLike | null): number => {
  if (!planet || !Number.isFinite(Number(planet.house))) {
    return 1;
  }
  const val = Number(planet.house);
  return Math.min(12, Math.max(1, Math.round(val)));
};

const scorePlanet = (planet: PlanetLike | null, favoredHouses: number[]): number => {
  if (!planet) {
    return 45;
  }
  const house = safeHouse(planet);
  const inFavored = favoredHouses.includes(house) ? 30 : 0;
  const signBonus = Number.isFinite(Number(planet.degree))
    ? Math.round((30 - (Number(planet.degree) % 30)) / 2)
    : 10;
  return Math.max(20, Math.min(95, 45 + inFavored + signBonus));
};

export const getCareerInsight = (chart: ChartData): {
  primarySector: string;
  secondarySector: string;
  score: number;
  summary: string;
} => {
  const mercury = getPlanet(chart, 'Mercury');
  const jupiter = getPlanet(chart, 'Jupiter');
  const saturn = getPlanet(chart, 'Saturn');
  const sun = getPlanet(chart, 'Sun');

  const techScore = scorePlanet(mercury, [1, 3, 6, 10]);
  const financeScore = scorePlanet(jupiter, [2, 5, 9, 11]);
  const governanceScore = scorePlanet(sun, [1, 10, 11]);
  const disciplineScore = scorePlanet(saturn, [6, 8, 10]);

  const sectorScores = [
    {sector: 'Technology & Analytics', score: techScore},
    {sector: 'Finance & Advisory', score: financeScore},
    {sector: 'Leadership & Public Roles', score: governanceScore},
    {sector: 'Operations & Engineering', score: disciplineScore},
  ].sort((a, b) => b.score - a.score);

  const top = sectorScores[0];
  const second = sectorScores[1];

  const summary =
    `Primary strength is ${top.sector} (${top.score}/100). ` +
    `Secondary growth path is ${second.sector} (${second.score}/100). ` +
    `10th-house driven career effort should be focused on consistent upskilling and structured execution.`;

  return {
    primarySector: top.sector,
    secondarySector: second.sector,
    score: top.score,
    summary,
  };
};

export const getFinancialInsight = (chart: ChartData): {
  outlook: string;
  planetRows: Array<{
    planet: string;
    role: string;
    effect: string;
    color: string;
  }>;
} => {
  const jupiter = getPlanet(chart, 'Jupiter');
  const mercury = getPlanet(chart, 'Mercury');
  const venus = getPlanet(chart, 'Venus');
  const saturn = getPlanet(chart, 'Saturn');
  const mars = getPlanet(chart, 'Mars');

  const rows = [
    {
      planet: 'Jupiter',
      role: 'Wealth Expansion',
      effect: `House ${safeHouse(jupiter)} indicates long-term wealth accumulation through discipline.`,
      color: '#F59E0B',
    },
    {
      planet: 'Mercury',
      role: 'Trade & Decisions',
      effect: `House ${safeHouse(mercury)} supports planning, contracts, and practical budgeting.`,
      color: '#10B981',
    },
    {
      planet: 'Venus',
      role: 'Comfort & Spending',
      effect: `House ${safeHouse(venus)} suggests balancing lifestyle spending with savings goals.`,
      color: '#EC4899',
    },
    {
      planet: 'Saturn',
      role: 'Risk Control',
      effect: `House ${safeHouse(saturn)} emphasizes patience and debt management.`,
      color: '#6B7280',
    },
    {
      planet: 'Mars',
      role: 'Aggressive Moves',
      effect: `House ${safeHouse(mars)} warns against impulsive high-volatility decisions.`,
      color: '#EF4444',
    },
  ];

  const optimism = Math.round((scorePlanet(jupiter, [2, 5, 9, 11]) + scorePlanet(mercury, [2, 3, 6, 11])) / 2);

  const outlook =
    optimism >= 70
      ? 'Favorable period for planned investments and disciplined growth.'
      : optimism >= 55
      ? 'Balanced period: prioritize savings, avoid over-leverage.'
      : 'Conservative phase: preserve capital and reduce risky exposure.';

  return {outlook, planetRows: rows};
};

export const getSoulmateInsight = (chart: ChartData): Record<string, string> => {
  const venus = getPlanet(chart, 'Venus');
  const moon = getPlanet(chart, 'Moon');
  const mars = getPlanet(chart, 'Mars');

  const venusHouse = safeHouse(venus);
  const moonHouse = safeHouse(moon);
  const marsHouse = safeHouse(mars);

  return {
    'Physical Appearance': `Partner may show traits of ${venus?.sign || 'Venus'} influence with refined style and balanced presence (Venus house ${venusHouse}).`,
    'Nature & Personality': `Emotional nature appears nurturing and thoughtful with Moon influence from house ${moonHouse}.`,
    Profession: `Likely alignment with communication, service, education, or structured management roles (Mars house ${marsHouse}).`,
    'Meeting Direction': `Strong chance of meeting through work, learning, or travel circles connected to your 7th-house themes.`,
    'Marriage Timing': `Favorable marriage windows are strongest during benefic transits to houses 1/5/7/11 relative to your Moon.`,
    'Compatibility Factors': `High compatibility generally with partners whose Moon/Jupiter supports your Venus sign ${venus?.sign || 'placement'}.`,
  };
};

export const getVarshaphalInsight = (
  chart: ChartData,
  year: number,
): {
  yearLord: string;
  highlights: string[];
  monthlyPredictions: Array<{month: string; prediction: string; level: 'excellent' | 'good' | 'caution'}>;
} => {
  const planets = toPlanetsArray(chart);
  const seed = planets.reduce((acc, p) => {
    const h = safeHouse(p);
    return acc + h + Math.round(Number(p.degree || 0));
  }, year % 100);

  const lord = PLANET_ORDER[seed % PLANET_ORDER.length];
  const focus = safeHouse(getPlanet(chart, lord));

  const highlights = [
    `Career focus intensifies around house ${focus} responsibilities and role upgrades.`,
    `Financial planning improves when Jupiter-linked decisions are timed with discipline.`,
    `Relationships improve through communication and predictable routines.`,
    `Health remains stable with stress and sleep regulation.`,
  ];

  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'];
  const monthlyPredictions = months.map((m, idx) => {
    const score = (seed + idx * 7) % 100;
    const level: 'excellent' | 'good' | 'caution' =
      score > 70 ? 'excellent' : score > 45 ? 'good' : 'caution';
    const prediction =
      level === 'excellent'
        ? `Strong momentum for planned expansion in ${m}.`
        : level === 'good'
        ? `Steady progress in ${m}; maintain consistency.`
        : `Use caution in ${m}; avoid rushed commitments.`;
    return {month: m, prediction, level};
  });

  return {yearLord: lord, highlights, monthlyPredictions};
};

const NAKSHATRA_GROUPS = [
  {name: 'Ashwini', letters: ['Chu', 'Che', 'Cho', 'La']},
  {name: 'Bharani', letters: ['Li', 'Lu', 'Le', 'Lo']},
  {name: 'Krittika', letters: ['A', 'I', 'U', 'E']},
  {name: 'Rohini', letters: ['O', 'Va', 'Vi', 'Vu']},
  {name: 'Mrigashira', letters: ['Ve', 'Vo', 'Ka', 'Ki']},
  {name: 'Ardra', letters: ['Ku', 'Gha', 'Na', 'Chha']},
  {name: 'Punarvasu', letters: ['Ke', 'Ko', 'Ha', 'Hi']},
  {name: 'Pushya', letters: ['Hu', 'He', 'Ho', 'Da']},
  {name: 'Ashlesha', letters: ['Di', 'Du', 'De', 'Do']},
];

export const getNameRecommendationFromChart = (chart: ChartData): {
  nakshatra: string;
  letters: string[];
  suggestions: string[];
  luckyNumber: number;
  luckyColor: string;
} => {
  const moon = getPlanet(chart, 'Moon');
  const longitude = Number(moon?.longitude || 0);
  const groupIndex = Math.abs(Math.floor((longitude % 120) / (120 / NAKSHATRA_GROUPS.length)));
  const group = NAKSHATRA_GROUPS[groupIndex] || NAKSHATRA_GROUPS[0];

  const suggestions = group.letters.flatMap((letter, idx) => {
    const root = NAME_ROOTS[(groupIndex + idx) % NAME_ROOTS.length];
    const suffix = NAME_SUFFIXES[(groupIndex + idx * 2) % NAME_SUFFIXES.length];
    return [`${letter}${root}${suffix}`, `${letter}${root}${NAME_SUFFIXES[(idx + 3) % NAME_SUFFIXES.length]}`];
  }).slice(0, 8);

  const luckyNumber = (safeHouse(moon) % 9) + 1;
  const colors = ['Yellow', 'White', 'Green', 'Blue', 'Orange', 'Silver', 'Saffron', 'Maroon', 'Teal'];
  const luckyColor = colors[(groupIndex + luckyNumber) % colors.length];

  return {
    nakshatra: group.name,
    letters: group.letters,
    suggestions,
    luckyNumber,
    luckyColor,
  };
};

export const getMuhuratWindows = (
  chart: ChartData,
  activity: string,
): Array<{date: string; time: string; nakshatra: string; quality: string}> => {
  const moon = getPlanet(chart, 'Moon');
  const tags = ACTIVITY_TAGS[activity] || ['Moon', 'Jupiter', 'Mercury'];
  const base = safeHouse(moon);
  const today = new Date();

  return [4, 9, 14].map((offset, idx) => {
    const d = new Date(today);
    d.setDate(today.getDate() + offset + base % 3);

    const hourStart = 6 + ((base + idx * 2) % 6);
    const start = `${`${hourStart}`.padStart(2, '0')}:00`;
    const end = `${`${hourStart + 1}`.padStart(2, '0')}:30`;

    const label = d.toLocaleDateString('en-IN', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
      weekday: 'short',
    });

    const qualityScore = scorePlanet(getPlanet(chart, tags[idx % tags.length]), [1, 5, 7, 9, 11]);
    const quality = qualityScore >= 70 ? '⭐⭐⭐⭐⭐ Excellent' : qualityScore >= 55 ? '⭐⭐⭐⭐ Very Good' : '⭐⭐⭐ Good';

    return {
      date: label,
      time: `${start} - ${end}`,
      nakshatra: moon?.sign || 'Moon-sign transit',
      quality,
    };
  });
};

export const getCompatibilityScore = (
  chartA: ChartData,
  chartB: ChartData,
): {
  total: number;
  breakdown: Array<{aspect: string; max: number; score: number; desc: string}>;
} => {
  const points = [
    {aspect: 'Varna (Character)', max: 1, desc: 'Spiritual alignment'},
    {aspect: 'Vashya (Control)', max: 2, desc: 'Mutual influence'},
    {aspect: 'Tara (Star)', max: 3, desc: 'Birth-star relation'},
    {aspect: 'Yoni (Nature)', max: 4, desc: 'Behavioral comfort'},
    {aspect: 'Graha Maitri (Friendship)', max: 5, desc: 'Mental compatibility'},
    {aspect: 'Gana (Category)', max: 6, desc: 'Temperament harmony'},
    {aspect: 'Bhakoot (Love)', max: 7, desc: 'Emotional flow'},
    {aspect: 'Nadi (Health)', max: 8, desc: 'Constitution match'},
  ];

  const moonA = safeHouse(getPlanet(chartA, 'Moon'));
  const moonB = safeHouse(getPlanet(chartB, 'Moon'));
  const venusA = safeHouse(getPlanet(chartA, 'Venus'));
  const venusB = safeHouse(getPlanet(chartB, 'Venus'));

  const delta = Math.abs(moonA - moonB) + Math.abs(venusA - venusB);

  const breakdown = points.map((p, idx) => {
    const mod = (delta + idx * 3) % (p.max + 1);
    const raw = p.max - mod;
    const score = Math.max(0, Math.min(p.max, raw));
    return {...p, score};
  });

  const total = breakdown.reduce((acc, x) => acc + x.score, 0);
  return {total, breakdown};
};
