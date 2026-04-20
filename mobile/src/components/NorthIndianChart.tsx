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
  planets?: Record<string, any> | Array<any>;
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

// Coordinates are normalized to match the PWA North Indian chart layout.
const HOUSE_POS: Record<number, {x: number; y: number}> = {
  1: {x: 0.50, y: 0.12},
  2: {x: 0.19, y: 0.16},
  3: {x: 0.10, y: 0.26},
  4: {x: 0.10, y: 0.50},
  5: {x: 0.10, y: 0.74},
  6: {x: 0.19, y: 0.84},
  7: {x: 0.50, y: 0.90},
  8: {x: 0.81, y: 0.84},
  9: {x: 0.90, y: 0.74},
  10: {x: 0.90, y: 0.50},
  11: {x: 0.90, y: 0.26},
  12: {x: 0.81, y: 0.16},
};

const CHART_LEFT = 18;
const CHART_TOP = 34;
const CHART_SIZE = 324;

function chunkPlanets(planets: string[], perLine = 3): string[] {
  if (!Array.isArray(planets) || planets.length === 0) return [];
  const lines: string[] = [];
  for (let i = 0; i < planets.length; i += perLine) {
    lines.push(planets.slice(i, i + perLine).join(' '));
  }
  return lines;
}

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

function parseHouse(value: unknown): number | undefined {
  const asNumber = Number(value);
  if (Number.isInteger(asNumber) && asNumber >= 1 && asNumber <= 12) {
    return asNumber;
  }
  return undefined;
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
      const houseFromData = parseHouse(p?.house);
      const sign = p?.sign;
      const house = houseFromData || (sign ? signHouse[sign] : undefined);
      if (house && house >= 1 && house <= 12) {
        grouped[house].push(PLANET_SHORT[name] || name.slice(0, 2));
      }
    });

    return {houseSigns: signs, housePlanets: grouped};
  }, [chart, division]);

  const scale = size / 360;

  return (
    <View style={[styles.wrap, {width: size, height: size}]}> 
      <View style={[styles.headerRow, {paddingHorizontal: 10 * scale}]}> 
        <Text style={[styles.title, {fontSize: Math.max(11, 12 * scale)}]}>North Indian Chart</Text>
        <Text style={[styles.divisionText, {fontSize: Math.max(11, 12 * scale)}]}>{division.replace('D', 'D-')}</Text>
      </View>

      <View style={[styles.board, {left: CHART_LEFT * scale, top: CHART_TOP * scale, width: CHART_SIZE * scale, height: CHART_SIZE * scale}]}> 
        <View style={styles.diagMainA} />
        <View style={styles.diagMainB} />
        <View style={styles.diagTopRight} />
        <View style={styles.diagBottomRight} />
        <View style={styles.diagTopLeft} />
        <View style={styles.diagBottomLeft} />
        <Text style={[styles.lagnaMark, {fontSize: Math.max(9, 10 * scale)}]}>+ लग्न +</Text>
      </View>

      {Object.entries(HOUSE_POS).map(([h, pos]) => {
        const house = Number(h);
        const signName = houseSigns[house] || '';
        const signShort = SIGN_SHORT[signName] || '--';
        const signNum = Math.max(1, SIGNS.indexOf(signName) + 1);
        const planets = housePlanets[house] || [];
        const planetLines = chunkPlanets(planets, 3);
        const isAscHouse = house === 1;
        return (
          <View
            key={h}
            style={[
              styles.houseLabel,
              isAscHouse && styles.ascHouseLabel,
              {
                left: (CHART_LEFT + CHART_SIZE * pos.x) * scale - 34 * scale,
                top: (CHART_TOP + CHART_SIZE * pos.y) * scale - 18 * scale,
                minWidth: 68 * scale,
              },
            ]}
          > 
            <View style={styles.signRow}>
              <Text style={[styles.signText, {fontSize: Math.max(12, 18 * scale)}]}>{signShort}</Text>
              <Text style={[styles.signNumText, {fontSize: Math.max(8, 10 * scale)}]}>{signNum}</Text>
            </View>
            {isAscHouse ? <Text style={[styles.ascTag, {fontSize: Math.max(8, 9 * scale)}]}>Asc</Text> : null}
            {planetLines.map((line, index) => (
              <Text key={`${house}-p-${index}`} style={[styles.planetText, {fontSize: Math.max(8, 11 * scale)}]}>{line}</Text>
            ))}
          </View>
        );
      })}

      <View style={[styles.legendRow, {left: 8 * scale, right: 8 * scale, bottom: 2 * scale}]}> 
        <Text style={[styles.legendText, {fontSize: Math.max(8, 9 * scale)}]}>Signs</Text>
        <Text style={[styles.legendText, styles.legendPlanets, {fontSize: Math.max(8, 9 * scale)}]}>Planets</Text>
      </View>
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
    backgroundColor: '#F3E4C2',
    borderWidth: 1.5,
    borderColor: '#C98E44',
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
  lagnaMark: {
    position: 'absolute',
    left: 0,
    right: 0,
    top: '47%',
    textAlign: 'center',
    color: '#BF360C',
    fontWeight: '700',
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
  ascHouseLabel: {
    backgroundColor: '#FFF3D9',
    borderRadius: 10,
    paddingHorizontal: 6,
    paddingVertical: 2,
    borderWidth: 1,
    borderColor: '#E8C58E',
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
    marginTop: 1,
    fontWeight: '600',
  },
  ascTag: {
    color: '#8A4B00',
    fontWeight: '700',
    marginTop: 1,
  },
  planetText: {
    color: '#2E5FBF',
    fontWeight: '600',
    textAlign: 'center',
    marginTop: 1,
    lineHeight: 12,
  },
  legendRow: {
    position: 'absolute',
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  legendText: {
    color: '#B03A2E',
    fontWeight: '600',
  },
  legendPlanets: {
    color: '#2E5FBF',
  },
});

export default NorthIndianChart;
