// What pushed inflation up (or down): one entry per cause the simulation tracks.
// A scenario can override the fuel/food/supply wording to fit its crisis.

export const CAUSES = {
  expectations: ['What people already expected', 'Inflation feeds on itself: if everyone expects prices to rise, shops and workers build that in.'],
  fuel: ['Fuel prices', 'Fuel costs travel into transport, farming and factories.'],
  food: ['Food prices', 'What it cost to grow, import and transport food.'],
  supply: ['Scarce or pricier goods', 'Goods got harder or costlier to get hold of.'],
  printing: ['Newly printed money', 'More money but the same amount of goods, so each unit of money buys less.'],
  currency: ['A weaker currency', 'When your money is worth less abroad, everything you import costs more.'],
  wages: ['Wage rises passed on', 'Higher pay means higher costs, which businesses pass on as higher prices.'],
  demand: ['Spending vs. supply', 'Positive means people were spending more than the island could produce. Negative means a slump pulled prices down.'],
}

export const CAUSE_COLORS = {
  expectations: '#868e96',
  demand: '#4dabf7',
  fuel: '#f76707',
  food: '#74b816',
  supply: '#845ef7',
  currency: '#f59f00',
  printing: '#e03131',
  wages: '#1098ad',
}
