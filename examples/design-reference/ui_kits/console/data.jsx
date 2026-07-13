/* Static demo data for the helm workbench kit. */
window.HelmData = {
  AAPL: {
    name: "Apple Inc.", symbol: "AAPL", exchange: "NASDAQ", letter: "A",
    price: "$305.24", today: "+$10.86 (+3.69%)", dir: "up",
    past: "+$92.69 (+43.63%)", pastLabel: "Past year",
    seed: 7, drift: 0.55,
    stats: [
      ["Prev Close", "$294.38"], ["Market Cap", "$4.48T"], ["Open", "$294.09"],
      ["P/E Ratio", "35.51"], ["Day Range", "$293.68 – $306.64"], ["Dividend Yield", "0.4%"],
    ],
    facts: [
      ["Symbol", "AAPL"], ["IPO Date", "Dec 12, 1980"], ["CEO", "Timothy D. Cook"],
      ["Full-time Employees", "166000"], ["Sector", "Technology"], ["Industry", "Consumer Electronics"],
      ["Country", "US"], ["Exchange", "NASDAQ"], ["Website", "www.apple.com"],
    ],
    about: "Apple Inc. is a global technology corporation that specializes in the conceptualization, production, and sale of a diverse suite of electronic devices. Its comprehensive hardware lineup features the well-known iPhone smartphones, Mac personal computers, and versatile iPad tablets.",
    consensus: { label: "Buy", analysts: 111, bearish: 7, neutral: 34, bullish: 70, counts: [0, 7, 34, 69, 1], low: "$253.00", current: "$305.24", avg: "$327.00", avgPct: "+7.13%", high: "$400.00" },
  },
  NVDA: {
    name: "NVIDIA Corp.", symbol: "NVDA", exchange: "NASDAQ", letter: "N",
    price: "$1,204.55", today: "+$28.40 (+2.41%)", dir: "up",
    past: "+$512.10 (+73.95%)", pastLabel: "Past year",
    seed: 3, drift: 0.75,
    stats: [
      ["Prev Close", "$1,176.15"], ["Market Cap", "$2.96T"], ["Open", "$1,180.00"],
      ["P/E Ratio", "72.40"], ["Day Range", "$1,171.30 – $1,208.88"], ["Dividend Yield", "0.02%"],
    ],
    facts: [
      ["Symbol", "NVDA"], ["IPO Date", "Jan 22, 1999"], ["CEO", "Jensen Huang"],
      ["Full-time Employees", "29600"], ["Sector", "Technology"], ["Industry", "Semiconductors"],
      ["Country", "US"], ["Exchange", "NASDAQ"], ["Website", "www.nvidia.com"],
    ],
    about: "NVIDIA Corporation designs and supplies graphics processing units, systems-on-chip, and full-stack accelerated computing platforms. Its data-center GPUs power the large-scale training and inference behind modern AI systems.",
    consensus: { label: "Buy", analysts: 64, bearish: 2, neutral: 8, bullish: 54, counts: [0, 2, 8, 46, 8], low: "$900.00", current: "$1,204.55", avg: "$1,310.00", avgPct: "+8.75%", high: "$1,500.00" },
  },
  TSLA: {
    name: "Tesla, Inc.", symbol: "TSLA", exchange: "NASDAQ", letter: "T",
    price: "$188.02", today: "-$4.11 (-2.14%)", dir: "down",
    past: "-$52.60 (-21.86%)", pastLabel: "Past year",
    seed: 11, drift: -0.3,
    stats: [
      ["Prev Close", "$192.13"], ["Market Cap", "$599B"], ["Open", "$191.80"],
      ["P/E Ratio", "47.20"], ["Day Range", "$186.40 – $193.10"], ["Dividend Yield", "—"],
    ],
    facts: [
      ["Symbol", "TSLA"], ["IPO Date", "Jun 29, 2010"], ["CEO", "Elon Musk"],
      ["Full-time Employees", "140473"], ["Sector", "Consumer Cyclical"], ["Industry", "Auto Manufacturers"],
      ["Country", "US"], ["Exchange", "NASDAQ"], ["Website", "www.tesla.com"],
    ],
    about: "Tesla, Inc. designs, manufactures and sells fully electric vehicles, energy generation and storage systems, and related services, alongside its autonomous-driving software programs.",
    consensus: { label: "Hold", analysts: 52, bearish: 14, neutral: 24, bullish: 14, counts: [4, 10, 24, 12, 2], low: "$120.00", current: "$188.02", avg: "$196.00", avgPct: "+4.24%", high: "$310.00" },
  },
  RELIANCE: {
    name: "Reliance Industries", symbol: "RELIANCE", exchange: "NSE", letter: "R",
    price: "₹2,904.15", today: "+₹31.20 (+1.09%)", dir: "up",
    past: "+₹412.80 (+16.57%)", pastLabel: "Past year",
    seed: 5, drift: 0.4,
    stats: [
      ["Prev Close", "₹2,872.95"], ["Market Cap", "₹19.65L Cr"], ["Open", "₹2,880.00"],
      ["P/E Ratio", "28.40"], ["Day Range", "₹2,868.10 – ₹2,912.40"], ["Dividend Yield", "0.34%"],
    ],
    facts: [
      ["Symbol", "RELIANCE"], ["Listed", "Nov 29, 1977"], ["Chairman", "Mukesh D. Ambani"],
      ["Full-time Employees", "347362"], ["Sector", "Energy / Conglomerate"], ["Industry", "Oil & Gas Refining"],
      ["Country", "IN"], ["Exchange", "NSE · BSE"], ["Website", "www.ril.com"],
    ],
    about: "Reliance Industries is India's largest private-sector conglomerate, spanning oil-to-chemicals, retail, and digital services. Jio Platforms and Reliance Retail drive its consumer businesses alongside the legacy energy franchise.",
    consensus: { label: "Buy", analysts: 38, bearish: 3, neutral: 12, bullish: 23, counts: [1, 2, 12, 20, 3], low: "₹2,400.00", current: "₹2,904.15", avg: "₹3,150.00", avgPct: "+8.47%", high: "₹3,500.00" },
  },
  BTC: {
    kind: "crypto",
    name: "Bitcoin", symbol: "BTC/USD", exchange: "Crypto · 24/7", letter: "B",
    price: "$118,240", today: "+$2,110 (+1.82%)", dir: "up",
    past: "+$46,380 (+64.55%)", pastLabel: "Past year",
    seed: 13, drift: 0.6,
    stats: [
      ["24h Low", "$114,890"], ["Market Cap", "$2.33T"], ["24h High", "$119,760"],
      ["24h Volume", "$48.2B"], ["Circulating", "19.71M BTC"], ["Dominance", "54.1%"],
    ],
    facts: [
      ["Pair", "BTC/USD"], ["Launched", "Jan 3, 2009"], ["Creator", "Satoshi Nakamoto"],
      ["Max Supply", "21M BTC"], ["Asset Class", "Cryptocurrency"], ["Consensus", "Proof of Work"],
      ["Market", "24/7"], ["Halving", "Apr 2028 (est.)"], ["Website", "bitcoin.org"],
    ],
    about: "Bitcoin is the largest cryptocurrency by market capitalization — a decentralized, proof-of-work network whose fixed 21M supply underpins its store-of-value thesis. It trades continuously, 24/7, across global venues.",
    consensus: { label: "Buy", analysts: 24, bearish: 4, neutral: 8, bullish: 12, counts: [1, 3, 8, 10, 2], low: "$80,000", current: "$118,240", avg: "$135,000", avgPct: "+14.17%", high: "$180,000" },
  },
  ETH: {
    kind: "crypto",
    name: "Ethereum", symbol: "ETH/USD", exchange: "Crypto · 24/7", letter: "E",
    price: "$4,312.77", today: "-$66.20 (-1.51%)", dir: "down",
    past: "+$1,890.40 (+78.04%)", pastLabel: "Past year",
    seed: 17, drift: 0.5,
    stats: [
      ["24h Low", "$4,268.10"], ["Market Cap", "$518.6B"], ["24h High", "$4,402.35"],
      ["24h Volume", "$21.7B"], ["Circulating", "120.3M ETH"], ["Staked", "28.9%"],
    ],
    facts: [
      ["Pair", "ETH/USD"], ["Launched", "Jul 30, 2015"], ["Creator", "Vitalik Buterin et al."],
      ["Max Supply", "— (burn-offset)"], ["Asset Class", "Cryptocurrency"], ["Consensus", "Proof of Stake"],
      ["Market", "24/7"], ["Gas (avg)", "4.2 gwei"], ["Website", "ethereum.org"],
    ],
    about: "Ethereum is the leading smart-contract platform — the settlement layer for stablecoins, DeFi, and tokenized assets. Its proof-of-stake design pays staking yield while transaction fees burn supply.",
    consensus: { label: "Hold", analysts: 30, bearish: 6, neutral: 12, bullish: 12, counts: [2, 4, 12, 10, 2], low: "$3,000", current: "$4,312", avg: "$4,800", avgPct: "+11.30%", high: "$6,000" },
  },
};

/* Seeded random-walk series so charts are stable per ticker/range. */
window.helmSeries = function (seed, drift, n = 60) {
  let s = seed;
  const rnd = () => { s = (s * 16807 + 11) % 2147483647; return (s % 1000) / 1000; };
  const pts = [50];
  for (let i = 1; i < n; i++) {
    pts.push(Math.max(6, Math.min(94, pts[i - 1] + (rnd() - 0.5 + drift * 0.09) * 7)));
  }
  return pts;
};
