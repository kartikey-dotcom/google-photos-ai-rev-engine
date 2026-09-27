/**
 * Big Data Lake Simulation & Context Optimizer
 * Simulates connecting to a backend database of 25,450 records and
 * performing a smart stratified sampling down to 150 high-signal records.
 */

const SOURCES = ["r/GooglePhotos", "Play Store", "App Store", "Google Support Forum"];
const TYPES = ["Reddit Post", "1-Star Review", "2-Star Review", "Support Thread", "Feature Request"];

export class BigDataConnector {
  constructor() {
    this.totalRecords = 25450;
  }

  /**
   * Simulate querying 25k records and returning a 150-record stratified sample
   * @returns {Promise<Array<object>>}
   */
  async querySmartSample() {
    // Generate 150 diverse, high-signal mock records on the fly
    const sampleSize = 150;
    const records = [];

    // Common retrieval failure scenarios
    const baseContent = [
      "I searched for 'red jacket raining' and got zero results, but I know it's there.",
      "Trying to find my dog sleeping on the desk. Got 400 photos of random dogs instead.",
      "Search for 'concert' shows me 1,200 screenshots of Spotify playlists and tickets.",
      "Looked for a purple sunset in Greece, gave me every sunset I ever took.",
      "Cannot find the photo of my mom in the green armchair. Searching 'mom' gives 10,000 photos.",
      "Why does it show me web memes when I search for my real cat?",
      "I'm looking for the tire pressure sticker photo I took 4 months ago. Can't find it without scrolling."
    ];

    for (let i = 0; i < sampleSize; i++) {
      const source = SOURCES[i % SOURCES.length];
      const type = TYPES[i % TYPES.length];
      
      const record = {
        id: `bigdata-voc-${String(i).padStart(4, '0')}`,
        source: source,
        type: type,
        content: baseContent[i % baseContent.length] + ` (User comment #${i} from large dataset query highlighting episodic retrieval gap)`,
        metadata: {
          upvotes: Math.floor(Math.random() * 500),
          rating: source.includes('Store') ? (Math.random() > 0.5 ? 1 : 2) : undefined,
          device: (i % 2 === 0) ? "Pixel 8 Pro" : "iPhone 15 Pro",
          date: `2026-09-${String(Math.floor(Math.random() * 28) + 1).padStart(2, '0')}`,
          tags: ["retrieval_failure", "episodic_gap", "search_friction"]
        }
      };
      records.push(record);
    }

    return records;
  }
}
