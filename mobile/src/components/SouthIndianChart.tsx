import React, {useMemo} from 'react';
import {View, Text, StyleSheet} from 'react-native';

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

const CELL_POS: Record<string, {row: number; col: number}> = {
  Pisces: {row: 0, col: 0},
  Aries: {row: 0, col: 1},
  Taurus: {row: 0, col: 2},
  Gemini: {row: 0, col: 3},
  Cancer: {row: 1, col: 3},
  Leo: {row: 2, col: 3},
  Virgo: {row: 3, col: 3},
  Libra: {row: 3, col: 2},
  Scorpio: {row: 3, col: 1},
  Sagittarius: {row: 3, col: 0},
  Capricorn: {row: 2, col: 0},
  Aquarius: {row: 1, col: 0},
};

function toPlanetMap(chart: ChartDataLike): Record<string, any> {
  if (chart?.planets && !Array.isArray(chart.planets)) return chart.planets;
  const list = chart?.planets_list || (Array.isArray(chart?.planets) ? chart.planets : []);
  const out: Record<string, any> = {};
  for (const p of list) {
    if (p?.name) out[p.name] = p;
  }
  return out;
}

function parseHouse(value: unknown): number | undefined {
  const n = Number(value);
  if (Number.isInteger(n) && n >= 1 && n <= 12) return n;
  return undefined;
}

function buildHouseSigns(ascSign: string): Record<number, string> {
  const idx = Math.max(0, SIGNS.indexOf(ascSign));
  const out: Record<number, string> = {};
  for (let i = 0; i < 12; i += 1) out[i + 1] = SIGNS[(idx + i) % 12];
  return out;
}

function signToHouseMap(houseSigns: Record<number, string>): Record<string, number> {
  const out: Record<string, number> = {};
  for (let h = 1; h <= 12; h += 1) out[houseSigns[h]] = h;
  return out;
}

function chunkPlanets(planets: string[], perLine = 3): string[] {
  if (!Array.isArray(planets) || planets.length === 0) return [];
  const lines: string[] = [];
  for (let i = 0; i < planets.length; i += perLine) lines.push(planets.slice(i, i + perLine).join(' '));
  return lines;
}

const SouthIndianChart: React.FC<Props> = ({chart, division = 'D1', size = 360}) => {
  const {ascSign, houseBySign, planetsBySign} = useMemo(() => {
    let resolvedAscSign = chart?.ascendant?.sign || 'Aries';
    let pMap = toPlanetMap(chart);

    if (division !== 'D1') {
      const div = chart?.divisional_charts?.[division];
      if (div?.ascendant_sign) resolvedAscSign = div.ascendant_sign;
      if (div?.planets && !Array.isArray(div.planets)) pMap = div.planets;
    }

    const houseSigns = buildHouseSigns(resolvedAscSign);
    const signHouse = signToHouseMap(houseSigns);
    const grouped: Record<string, string[]> = {};
    SIGNS.forEach(s => { grouped[s] = []; });

    Object.entries(pMap || {}).forEach(([name, p]) => {
      if (name === 'Ascendant') return;
      const sign = String(p?.sign || '').trim();
      const house = parseHouse(p?.house);
      const derivedSign = house ? houseSigns[house] : sign;
      if (grouped[derivedSign]) {
        grouped[derivedSign].push(PLANET_SHORT[name] || name.slice(0, 2));
      }
    });

    return {ascSign: resolvedAscSign, houseBySign: signHouse, planetsBySign: grouped};
  }, [chart, division]);

  const boardSize = size - 24;
  const cellSize = boardSize / 4;

  return (
    <View style={[styles.wrap, {width: size}]}> 
      <View style={styles.headerRow}>
        <Text style={styles.title}>South Indian Chart</Text>
        <Text style={styles.divisionText}>{division.replace('D', 'D-')}</Text>
      </View>

      <View style={[styles.board, {width: boardSize, height: boardSize}]}> 
        {SIGNS.map(sign => {
          const pos = CELL_POS[sign];
          const isAsc = sign === ascSign;
          const houseNum = houseBySign[sign] || 0;
          const lines = chunkPlanets(planetsBySign[sign] || [], 3);

          return (
            <View
              key={sign}
              style={[
                styles.cell,
                {
                  width: cellSize,
                  height: cellSize,
                  left: pos.col * cellSize,
                  top: pos.row * cellSize,
                },
                isAsc && styles.ascCell,
              ]}
            >
              <View style={styles.signRow}>
                <Text style={styles.signText}>{SIGN_SHORT[sign]}</Text>
                <Text style={styles.signNumText}>{SIGNS.indexOf(sign) + 1}</Text>
              </View>
              <Text style={styles.houseTag}>H{houseNum}</Text>
              {lines.map((line, i) => (
                <Text key={`${sign}-${i}`} style={styles.planetText}>{line}</Text>
              ))}
            </View>
          );
        })}

        <View style={[styles.centerBox, {left: cellSize, top: cellSize, width: cellSize * 2, height: cellSize * 2}]}> 
          <Text style={styles.centerText}>Lagna: {SIGN_SHORT[ascSign] || ascSign}</Text>
        </View>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  wrap: {
    alignSelf: 'center',
    alignItems: 'center',
  },
  headerRow: {
    width: '100%',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
    paddingHorizontal: 6,
  },
  title: {
    color: '#111111',
    fontWeight: '600',
    fontSize: 12,
  },
  divisionText: {
    color: '#111111',
    fontWeight: '600',
    fontSize: 12,
  },
  board: {
    position: 'relative',
    backgroundColor: '#F3E4C2',
    borderWidth: 1.5,
    borderColor: '#C98E44',
  },
  cell: {
    position: 'absolute',
    borderWidth: 1,
    borderColor: '#1A1A1A',
    backgroundColor: '#F8EDD3',
    paddingHorizontal: 4,
    paddingVertical: 3,
  },
  ascCell: {
    backgroundColor: '#FFF3D9',
    borderColor: '#D17A00',
    borderWidth: 1.5,
  },
  centerBox: {
    position: 'absolute',
    borderWidth: 1,
    borderColor: '#1A1A1A',
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: '#EFE3C7',
  },
  centerText: {
    color: '#8A4B00',
    fontWeight: '700',
    fontSize: 11,
  },
  signRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
  },
  signText: {
    color: '#CC2A2A',
    fontWeight: '700',
    fontSize: 16,
    lineHeight: 18,
  },
  signNumText: {
    color: '#177F3E',
    marginLeft: 2,
    marginTop: 1,
    fontWeight: '700',
    fontSize: 9,
  },
  houseTag: {
    color: '#5B4A2A',
    fontSize: 9,
    fontWeight: '600',
    marginTop: 1,
  },
  planetText: {
    color: '#2E5FBF',
    fontWeight: '600',
    fontSize: 10,
    lineHeight: 12,
    marginTop: 1,
  },
});

export default SouthIndianChart;
