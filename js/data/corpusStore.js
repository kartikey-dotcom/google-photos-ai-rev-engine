import { SEED_CORPUS } from './seedCorpus.js';
import { validateFeedbackRecord, sanitizeFeedbackRecord } from './schema.js';

/**
 * In-Memory Corpus Store & Filtering Utility
 * Manages raw VoC feedback ingestion, schema validation, and serialization.
 */
export class CorpusStore {
  constructor() {
    this.corpus = [];
    this.loadSeedCorpus();
  }

  /**
   * Load and validate seed corpus records
   */
  loadSeedCorpus() {
    this.corpus = SEED_CORPUS.map((rawRecord, index) => {
      const validation = validateFeedbackRecord(rawRecord);
      if (!validation.valid) {
        console.warn(`Record at index ${index} failed schema validation:`, validation.errors);
        return sanitizeFeedbackRecord(rawRecord, index + 1);
      }
      return rawRecord;
    });
  }

  /**
   * Get all records filtered by active source toggles
   * @param {Record<string, boolean>} [sourceFilters]
   * @returns {Array<object>}
   */
  getActiveRecords(sourceFilters = {}) {
    return this.corpus.filter(record => {
      // If source not explicitly set to false, it is considered active
      return sourceFilters[record.source] !== false;
    });
  }

  /**
   * Total number of records in storage
   * @returns {number}
   */
  getTotalCount() {
    return this.corpus.length;
  }

  /**
   * Get count breakdown by source
   * @returns {Record<string, number>}
   */
  getSourceCounts() {
    const counts = {};
    for (const record of this.corpus) {
      counts[record.source] = (counts[record.source] || 0) + 1;
    }
    return counts;
  }

  /**
   * Serialize an array of records into formatted JSON string for prompt injection
   * (Fulfills Task 2.3 requirement)
   * @param {Array<object>} [records]
   * @param {number} [indent=2]
   * @returns {string}
   */
  serializeRecords(records, indent = 2) {
    const target = records || this.corpus;
    return JSON.stringify(target, null, indent);
  }

  /**
   * Ingest a new record dynamically with schema validation
   * @param {object} record
   * @returns {{ success: boolean, id?: string, errors?: string[] }}
   */
  addRecord(record) {
    const validation = validateFeedbackRecord(record);
    if (!validation.valid) {
      return { success: false, errors: validation.errors };
    }
    this.corpus.push(record);
    return { success: true, id: record.id };
  }

  /**
   * Replace the entire corpus with a new dataset (e.g. from BigDataConnector)
   * @param {Array<object>} newRecords 
   */
  replaceCorpus(newRecords) {
    this.corpus = newRecords.map((rawRecord, index) => {
      const validation = validateFeedbackRecord(rawRecord);
      if (!validation.valid) {
        return sanitizeFeedbackRecord(rawRecord, index + 1);
      }
      return rawRecord;
    });
  }

  /**
   * Get detailed corpus summary for PM diagnostics
   * @returns {object}
   */
  getCorpusSummary() {
    const sourceBreakdown = this.getSourceCounts();
    const allTags = new Set();
    this.corpus.forEach(r => {
      if (r.metadata && Array.isArray(r.metadata.tags)) {
        r.metadata.tags.forEach(t => allTags.add(t));
      }
    });

    return {
      totalRecords: this.corpus.length,
      sourceBreakdown,
      uniqueTagsCount: allTags.size,
      tags: Array.from(allTags)
    };
  }
}

export const corpusStore = new CorpusStore();
