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
  1: {x: 58, y: 255}, 2: {x: 110, y: 300}, 3: {x: 178, y: 320}, 4: {x: 245, y: 300},
  5: {x: 300, y: 255}, 6: {x: 320, y: 190}, 7: {x: 300, y: 115}, 8: {x: 245, y: 62},
  9: {x: 178, y: 40}, 10: {x: 110, y: 62}, 11: {x: 58, y: 115}, 12: {x: 40, y: 190},
};

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
    const grouped: Record<number, string[]> = {1: [], 2: [], 3: [], 4: [], 5: [], 6: [], 7: [], 8: [], 9: [], 10: [], 11: [], 12: []};

    Object.entries(pMap || {}).forEach(([name, p]) => {
      const house = Number(p?.house || 0);
      if (house >= 1 && house <= 12 && name !== 'Ascendant') {
        grouped[house].push(PLANET_SHORT[name] || name.slice(0, 2));
      }
    });

    return {houseSigns: signs, housePlanets: grouped};
  }, [chart, division]);

  return (
    <View style={[styles.wrap, {width: size, height: size}]}> 
      <Text style={styles.title}>|| North Indian Chart ({division}) ||</Text>
      <View style={styles.board}>
        <View style={styles.diagMainA} />
        <View style={styles.diagMainB} />
        <View style={styles.diagTopRight} />
        <View style={styles.diagBottomRight} />
        <View style={styles.diagTopLeft} />
        <View style={styles.diagBottomLeft} />
      </View>

      {Object.entries(HOUSE_POS).map(([h, pos]) => {
        const house = Number(h);
        const s = SIGN_SHORT[houseSigns[house]] || '--';
        const planets = housePlanets[house]?.join(', ');
        return (
          <View key={h} style={[styles.houseLabel, {left: (pos.x / 360) * size - 18, top: (pos.y / 360) * size - 14}]}> 
            <Text style={styles.signText}>{s}{house}</Text>
            {!!planets && <Text style={styles.planetText}>{planets}</Text>}
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
  board: {
    position: 'absolute',
    left: 20,
    top: 36,
    width: 320,
    height: 320,
    backgroundColor: '#F9E9C6',
    borderWidth: 2,
    borderColor: '#C18739',
    overflow: 'hidden',
  },
  diagMainA: {
    position: 'absolute',
    left: -65,
    top: 158,
    width: 450,
    height: 1.5,
    backgroundColor: '#B88E50',
    transform: [{rotate: '45deg'}],
  },
  diagMainB: {
    position: 'absolute',
    left: -65,
    top: 158,
    width: 450,
    height: 1.5,
    backgroundColor: '#B88E50',
    transform: [{rotate: '-45deg'}],
  },
  diagTopRight: {
    position: 'absolute',
    left: 175,
    top: 26,
    width: 220,
    height: 1.5,
    backgroundColor: '#B88E50',
    transform: [{rotate: '45deg'}],
  },
  diagBottomRight: {
    position: 'absolute',
    left: 175,
    top: 292,
    width: 220,
    height: 1.5,
    backgroundColor: '#B88E50',
    transform: [{rotate: '-45deg'}],
  },
  diagTopLeft: {
    position: 'absolute',
    left: -74,
    top: 26,
    width: 220,
    height: 1.5,
    backgroundColor: '#B88E50',
    transform: [{rotate: '-45deg'}],
  },
  diagBottomLeft: {
    position: 'absolute',
    left: -74,
    top: 292,
    width: 220,
    height: 1.5,
    backgroundColor: '#B88E50',
    transform: [{rotate: '45deg'}],
  },
  title: {
    textAlign: 'center',
    color: '#5B4331',
    fontSize: 20,
    fontWeight: '700',
    marginBottom: 8,
  },
  houseLabel: {
    position: 'absolute',
    minWidth: 36,
    alignItems: 'center',
  },
  signText: {
    color: '#9E2A1F',
    fontWeight: '700',
    fontSize: 14,
  },
  planetText: {
    color: '#1E40AF',
    fontWeight: '600',
    fontSize: 11,
  },
});

export default NorthIndianChart;
