// Plain-language explanations for the words the game uses. Each entry lists the phrases that
// should be underlined in the game's text (longest phrases are matched first).

export const GLOSSARY = [
  { id: 'gdp', term: 'GDP', match: ['GDP', 'size of the economy'],
    text: 'Gross Domestic Product: the value of everything an island makes and sells in a year. It is the size of the economy.',
    example: 'If Coralia makes 140 billion pesos of goods and services a year, that is its GDP.' },
  { id: 'pct_gdp', term: '% of GDP', match: ['% of GDP', '% GDP', '% of the economy'],
    text: 'Compares a number with the size of the whole economy, so rich and poor islands can be compared fairly.',
    example: 'Debt of 50% of GDP means the government owes half of what the whole island produces in a year.' },
  { id: 'income', term: 'Income per person', match: ['income per person'],
    text: "The island's GDP divided by its population: roughly what an average person earns in a year. Shown in Aurum ducats, the world's common money, so islands can be compared.",
    example: 'Aurelia: 68,000 ducats a year. Kalani: 850 ducats a year.' },
  { id: 'inflation', term: 'Inflation', match: ['inflation'],
    text: 'How fast prices are rising. 5% inflation means that what cost 100 a year ago now costs 105.',
    example: 'If bread goes from 2.00 to 2.20 in a year, bread inflation was 10%.' },
  { id: 'interest', term: 'Interest rate', match: ['interest rates', 'interest rate', 'rates'],
    text: 'The price of borrowing money, set by the central bank. Higher rates make loans dearer, so people borrow and spend less, which cools prices.',
    example: 'At 6%, a 1,000 loan costs 60 a year in interest.' },
  { id: 'central_bank', term: 'Central bank', match: ['central bank', 'Deputy Governor', 'Monetary Policy Committee'],
    text: "The island's bank for banks. It sets interest rates, can create new money, and holds the reserves." },
  { id: 'currency', term: 'Currency', match: ['currency', 'exchange rate'],
    text: "The island's own money. Its value against other money decides how expensive imports are. The dashboard shows it as an index: 100 is this morning's value.",
    example: 'If the currency falls from 100 to 90, imported phones and fuel cost about 10% more.' },
  { id: 'reserves', term: 'Reserves', match: ['reserves', 'savings (reserves)'],
    text: 'Foreign money the central bank keeps in its safe, counted in months of imports it could pay for. When reserves run out, nobody will sell the island fuel or food.',
    example: '3 months of reserves = enough foreign money to pay for 3 months of imports.' },
  { id: 'debt', term: 'Government debt', match: ['debt burden', 'debt', 'borrowing'],
    text: 'Everything the government has borrowed and still owes. It is usually shown as a % of GDP.' },
  { id: 'deficit', term: 'Deficit', match: ['deficit'],
    text: 'When the government spends more in a year than it collects in taxes. The gap is borrowed, so it adds to the debt.' },
  { id: 'lender', term: 'Lenders', match: ['lenders', 'lender', 'creditors', 'investors', 'bond buyers'],
    text: 'People, banks and funds who lend money to the government or companies and expect it back with interest. If they get scared, they charge more or stop lending.' },
  { id: 'bonds', term: 'Bonds', match: ['bonds', 'bond'],
    text: 'An IOU a government sells to raise money. The buyer lends the money now and gets paid back later with interest.',
    example: 'A 100 bond at 5% pays the lender 5 a year, then the 100 back at the end.' },
  { id: 'default', term: 'Default / restructuring', match: ['default', 'restructure', 'restructured', 'accept less'],
    text: "When a borrower can't or won't repay in full. Lenders take a loss, and they charge much more (or refuse) to lend again." },
  { id: 'printing', term: 'Printing money', match: ['printed money', 'print money', 'printing', 'creates money', 'create money', 'new money'],
    text: 'When the central bank creates new money from nothing. If there are no more goods to buy, the extra money pushes prices up.' },
  { id: 'qe', term: 'Bond buying (QE)', match: ['buy bonds', 'buy government bonds', 'quantitative easing'],
    text: 'The central bank creates money to buy bonds. It pushes cash into the economy and makes borrowing cheaper.' },
  { id: 'bank_lending', term: 'Bank lending', match: ['lending', 'credit'],
    text: 'Most money is created when banks make loans: the loan appears as new money in the borrower\'s account. When banks stop lending, less new money is made.' },
  { id: 'deposit', term: 'Deposits', match: ['deposits', 'deposit'],
    text: 'Money people keep in the bank. Banks lend most of it out, so if everyone wants it back at once (a bank run), even a healthy bank can run out of cash.' },
  { id: 'bank_run', term: 'Bank run', match: ['bank run'],
    text: "When many savers rush to withdraw their money because they fear the bank will fail, which can make it fail." },
  { id: 'bailout', term: 'Bailout', match: ['bail it out', 'bailout', 'bailed out', 'rescue'],
    text: 'When the government (taxpayers) pays to save a failing company or bank.' },
  { id: 'bail_in', term: 'Bail-in', match: ['bail-in', 'share the loss'],
    text: "Instead of taxpayers, the bank's owners and biggest savers take the loss." },
  { id: 'nationalise', term: 'Nationalise', match: ['nationalise', 'nationalised'],
    text: 'The government takes over ownership of a company or bank.' },
  { id: 'tariff', term: 'Tariff', match: ['tariffs', 'tariff', 'import taxes'],
    text: "A tax on goods coming from abroad. It protects local producers, but shoppers pay more, and other islands often hit back with their own tariffs." },
  { id: 'sanctions', term: 'Sanctions', match: ['sanctions', 'sanction'],
    text: 'Refusing to trade with an island to punish it, for example by not buying its oil.' },
  { id: 'imports', term: 'Imports & exports', match: ['imports', 'exports', 'imported', 'exporters', 'importers'],
    text: 'Imports are goods bought from abroad (fuel, phones). Exports are goods sold abroad (cars, clothes, fish). Exports bring foreign money in; imports send it out.' },
  { id: 'subsidy', term: 'Subsidy', match: ['subsidise', 'subsidy', 'subsidies'],
    text: 'When the government pays part of the price of something so people or companies pay less. It keeps prices down but costs the budget.' },
  { id: 'austerity', term: 'Austerity', match: ['austerity', 'tighten the belt', 'spending cuts'],
    text: 'Cutting government spending (or raising taxes) to reduce borrowing. It calms debt worries but slows the economy and can cost jobs.' },
  { id: 'unemployment', term: 'Unemployment', match: ['unemployment', 'jobless rate'],
    text: 'The share of people who want a job but cannot find one.' },
  { id: 'trust', term: 'Trust in money (credibility)', match: ['trust in its money', 'credibility'],
    text: "How much people believe the island's money will keep its value. High trust keeps inflation low, because shops and workers don't rush to raise prices." },
  { id: 'imf', term: 'IMF / UN package', match: ['IMF', 'UN / IMF', 'rescue package'],
    text: 'The International Monetary Fund lends to countries in a crisis, usually with conditions such as spending cuts. The UN coordinates aid for the poorest.' },
  { id: 'capital_controls', term: 'Capital controls', match: ['capital controls', 'money leaving'],
    text: 'Limits on moving money out of the island. They slow a currency crash but scare away investors.' },
  { id: 'safe_haven', term: 'Safe haven', match: ['safe place', 'safe ducats', 'ducats'],
    text: "Aurum's money, the ducat, is the world's reserve currency. In a crisis, scared investors move their money into ducats, which pulls money out of small islands." },
  { id: 'supply_shock', term: 'Supply shock', match: ['supply shock', 'supply chains', 'supply'],
    text: 'When something becomes scarce (oil, grain, parts), so its price rises, even if people are not spending more.' },
  { id: 'demand', term: 'Demand', match: ['demand', 'spending collapses'],
    text: 'How much people, companies and the government want to buy. Too much demand pushes prices up; too little costs jobs.' },
  { id: 'recession', term: 'Recession / slump', match: ['recession', 'slump'],
    text: 'When the economy shrinks: less is made and sold, and people lose jobs.' },
  { id: 'wage_spiral', term: 'Wage-price spiral', match: ['wage-price spiral'],
    text: 'Prices rise, so workers want higher pay; businesses pass the higher pay on as higher prices, and round it goes.' },
  { id: 'price_cap', term: 'Price cap', match: ['price cap', 'cap prices', 'cap bread prices'],
    text: 'A law setting the most a seller can charge. It helps buyers at first, but sellers may stop selling, leaving empty shelves and black markets.' },
  { id: 'black_market', term: 'Black market', match: ['black market'],
    text: 'Illegal trading, usually at much higher prices, when goods are scarce or price-capped.' },
  { id: 'mortgage', term: 'Mortgage', match: ['mortgages', 'mortgage'],
    text: 'A loan to buy a home. If the borrower stops paying, the bank can repossess (take) the home.' },
  { id: 'insurance', term: 'Insurance', match: ['insurers', 'insurance', 'premiums'],
    text: 'Paying a company a regular fee (a premium) so it covers you if something bad happens. Without it, ships won\'t sail and banks won\'t lend.' },
  { id: 'ratings', term: 'Ratings agencies', match: ['ratings agencies', 'junk'],
    text: "Companies that grade how safe it is to lend to a government. 'Junk' means risky, so borrowing gets much more expensive." },
  { id: 'amnesty', term: 'Tax amnesty', match: ['tax amnesty', 'amnesty'],
    text: 'A deal where people who hid money can declare it and pay a small fine instead of being punished.' },
  { id: 'fiscal_rule', term: 'Fiscal rule', match: ['debt limit', 'fiscal rule'],
    text: 'A law limiting how much the government may borrow, often checked by an independent watchdog.' },
  { id: 'lockdown', term: 'Lockdown', match: ['lockdown'],
    text: 'An order for people to stay home to slow a virus. It saves lives but shuts down a lot of spending.' },
  { id: 'furlough', term: 'Wage scheme (furlough)', match: ['furlough', 'idle workers'],
    text: 'The government pays most of the wages of workers who cannot work, so firms keep them on instead of firing them.' },
  { id: 'approval', term: 'Approval', match: ['approval'],
    text: 'The share of people who think you are doing a good job as Governor.' },
  { id: 'sustainability', term: 'Sustainability', match: ['sustainability'],
    text: "A score for how well the island can keep going: its nature, its finances, its savings, its biggest employer, its people and trust in its money." },
  { id: 'energy', term: 'Energy independence', match: ['energy independence', 'imported fuel'],
    text: 'How much of its energy the island makes itself. The more fuel it imports, the harder an oil price rise hits.' },
]

const byPhrase = new Map()
for (const entry of GLOSSARY) for (const phrase of entry.match) byPhrase.set(phrase.toLowerCase(), entry)
const phrases = [...byPhrase.keys()].sort((a, b) => b.length - a.length)
const escape = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
// Whole words only; a few phrases start or end with a symbol (e.g. "% GDP"), so check the edges by hand.
const PATTERN = new RegExp(phrases.map(escape).join('|'), 'gi')
const isWordChar = (c) => !!c && /[A-Za-z0-9]/.test(c)

/** Split text into plain strings and glossary hits: [{ text, entry? }]. Each term is marked once per text. */
export function splitTerms(text, seen = new Set()) {
  const out = []
  let last = 0
  for (const m of text.matchAll(PATTERN)) {
    const start = m.index
    const end = start + m[0].length
    if (isWordChar(text[start - 1]) && isWordChar(m[0][0])) continue
    if (isWordChar(text[end]) && isWordChar(m[0].at(-1))) continue
    const entry = byPhrase.get(m[0].toLowerCase())
    if (seen.has(entry.id)) continue
    seen.add(entry.id)
    if (start > last) out.push({ text: text.slice(last, start) })
    out.push({ text: m[0], entry })
    last = end
  }
  if (last < text.length) out.push({ text: text.slice(last) })
  return out
}
