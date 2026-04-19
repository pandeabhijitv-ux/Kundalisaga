import React, {useMemo} from 'react';
import {View, Text, StyleSheet} from 'react-native';

type PlanetData = {
  name: string;
  sign: string;
  house: number;
};

type DivisionalData = {
  ascendant_sign?: string;
  planets?: Record<string, any>;
};

type ChartDataLike = {
  ascendant?: {sign?: string};
  planets?: Record<string, any>;
  planets_list?: Array<any>;
  divisional_charts?: Record<string, DivisionalData>;
};

type Props = {
  chart: ChartDataLike;
  division?: 'D1' | 'D2' | 'D3' | 'D7' | 'D9' | 'D10';
  size?: number;
};

const SIGNS = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'];
const SIGN_SHORT: Record<string, string> = {
  Aries: 'Ar', Taurus: 'Ta', Gemini: 'Ge', Cancer: 'Cn', Leo: 'Le', Virgo: 'Vi',
  Libra: 'Li', Scorpio: 'Sc', Sagittarius: 'Sg', Capricorn: 'Cp', Aquarius: 'Aq', Pisces: 'Pi',
};
const PLANET_SHORT: Record<string, string> = {
  Sun: 'Su', Moon: 'Mo', Mars: 'Ma', Mercury: 'Me', Jupiter: 'Ju', Venus: 'Ve', Saturn: 'Sa', Rahu: 'Ra', Ketu: 'Ke', Ascendant: 'As',
};

const HOUSE_POS: Record<number, {x: number; y: number}> = {
  1: {x: 180, y: 72},
  2: {x: 132, y: 88},
  3: {x: 104, y: 116},
  4: {x: 92, y: 170},
  5: {x: 104, y: 224},
  6: {x: 132, y: 252},
  7: {x: 180, y: 268},
  8: {x: 228, y: 252},
  9: {x: 256, y: 224},
  10: {x: 268, y: 170},
  11: {x: 256, y: 116},
  12: {x: 228, y: 88},
};

const CHART_LEFT = 20;
const CHART_TOP = 34;
const CHART_SIZE = 320;

function signToHouseMap(houseSigns: Record<number, string>): Record<string, number> {
  const out: Record<string, number> = {};
  for (let h = 1; h <= 12; h += 1) {
    out[houseSigns[h]] = h;
  }
  return out;
}

function toPlanetMap(chart: ChartDataLike): Record<string, any> {
  if (chart?.planets && !Array.isArray(chart.planets)) {
    return chart.planets;
  }
  const list = chart?.planets_list || (Array.isArray(chart?.planets) ? chart.planets : []);
  const out: Record<string, any> = {};
  for (const p of list) {
    if (p?.name) {
      out[p.name] = p;
    }
  }
  return out;
}

function buildHouseSigns(ascSign: string): Record<number, string> {
  const idx = Math.max(0, SIGNS.indexOf(ascSign));
  const result: Record<number, string> = {};
  for (let i = 0; i < 12; i += 1) {
    result[i + 1] = SIGNS[(idx + i) % 12];
  }
  return result;
}

const NorthIndianChart: React.FC<Props> = ({chart, division = 'D1', size = 360}) => {
  const {houseSigns, housePlanets} = useMemo(() => {
    let ascSign = chart?.ascendant?.sign || 'Aries';
    let pMap = toPlanetMap(chart);

    if (division !== 'D1') {
      const div = chart?.divisional_charts?.[division];
      if (div?.ascendant_sign) {
        ascSign = div.ascendant_sign;
      }
      if (div?.planets && !Array.isArray(div.planets)) {
        pMap = div.planets;
      }
    }

    const signs = buildHouseSigns(ascSign);
    const signHouse = signToHouseMap(signs);
    const grouped: Record<number, string[]> = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []};

    Object.entries(pMap || {}).forEach(([name, p]) => {
      if (name === 'Ascendant') return;
      const sign = p?.sign;
      const house = sign ? signHouse[sign] : undefined;
      if (house && house >= 1 && house <= 12) {
        grouped[house].push(PLANET_SHORT[name] || name.slice(0, 2));
      }
    });

    grouped[1] = ['AL', ...grouped[1]];

    return {houseSigns: signs, housePlanets: grouped};
  }, [chart, division]);

  const scale = size / 360;

  return (
    <View style={[styles.wrap, {width: size, height: size}]}> 
      <View style={[styles.headerRow, {paddingHorizontal: 10 * scale}]}> 
        <Text style={[styles.title, {fontSize: Math.max(11, 12 * scale)}]}>Natal Chart</Text>
        <Text style={[styles.divisionText, {fontSize: Math.max(11, 12 * scale)}]}>{division.replace('D', 'D-')}</Text>
      </View>

      <View style={[styles.board, {left: CHART_LEFT * scale, top: CHART_TOP * scale, width: CHART_SIZE * scale, height: CHART_SIZE * scale}]}> 
        <View style={styles.diagMainA} />
        <View style={styles.diagMainB} />
        <View style={styles.diagTopRight} />
        <View style={styles.diagBottomRight} />
        <View style={styles.diagTopLeft} />
        <View style={styles.diagBottomLeft} />
      </View>

      {Object.entries(HOUSE_POS).map(([h, pos]) => {
        const house = Number(h);
        const signName = houseSigns[house] || '';
        const signShort = SIGN_SHORT[signName] || '--';
        const signNum = Math.max(1, SIGNS.indexOf(signName) + 1);
        const planets = housePlanets[house] || [];
        return (
          <View
            key={h}
            style={[
              styles.houseLabel,
              {
                left: pos.x * scale - 24 * scale,
                top: pos.y * scale - 16 * scale,
                minWidth: 48 * scale,
              },
            ]}
          > 
            <View style={styles.signRow}>
              <Text style={[styles.signText, {fontSize: Math.max(12, 18 * scale)}]}>{signShort}</Text>
              <Text style={[styles.signNumText, {fontSize: Math.max(8, 10 * scale)}]}>{signNum}</Text>
            </View>
            {planets.length > 0 && (
              <Text style={[styles.planetText, {fontSize: Math.max(8, 11 * scale)}]}>{planets.join(' ')}</Text>
            )}
          </View>
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  wrap: {
    alignSelf: 'center',
    position: 'relative',
  },
  headerRow: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: 2,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    zIndex: 5,
  },
  board: {
    position: 'absolute',
    backgroundColor: '#ECECEC',
    borderWidth: 1.5,
    borderColor: '#111111',
    overflow: 'hidden',
  },
  diagMainA: {
    position: 'absolute',
    left: -64,
    top: 159,
    width: 448,
    height: 1,
    backgroundColor: '#111111',
    transform: [{rotate: '45deg'}],
  },
  diagMainB: {
    position: 'absolute',
    left: -64,
    top: 159,
    width: 448,
    height: 1,
    backgroundColor: '#111111',
    transform: [{rotate: '-45deg'}],
  },
  diagTopRight: {
    position: 'absolute',
    left: 175,
    top: 26,
    width: 220,
    height: 1,
    backgroundColor: '#111111',
    transform: [{rotate: '45deg'}],
  },
  diagBottomRight: {
    position: 'absolute',
    left: 175,
    top: 292,
    width: 220,
    height: 1,
    backgroundColor: '#111111',
    transform: [{rotate: '-45deg'}],
  },
  diagTopLeft: {
    position: 'absolute',
    left: -74,
    top: 26,
    width: 220,
    height: 1,
    backgroundColor: '#111111',
    transform: [{rotate: '-45deg'}],
  },
  diagBottomLeft: {
    position: 'absolute',
    left: -74,
    top: 292,
    width: 220,
    height: 1,
    backgroundColor: '#111111',
    transform: [{rotate: '45deg'}],
  },
  title: {
    color: '#111111',
    fontWeight: '600',
  },
  divisionText: {
    color: '#111111',
    fontWeight: '600',
  },
  houseLabel: {
    position: 'absolute',
    alignItems: 'center',
  },
  signRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'center',
  },
  signText: {
    color: '#CC2A2A',
    fontWeight: '600',
    lineHeight: 20,
  },
  signNumText: {
    color: '#177F3E',
    marginLeft: 2,
    marginTop: 2,
    fontWeight: '600',
  },
  planetText: {
    color: '#2E5FBF',
    fontWeight: '600',
    textAlign: 'center',
    marginTop: 1,
  },
});

export default NorthIndianChart;
