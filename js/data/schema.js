/**
 * TypeScript / JSDoc Data Schema Contracts for Google Photos VoC Intelligence Engine
 */

/**
 * @typedef {"r/GooglePhotos" | "Play Store" | "App Store" | "Google Support Forum"} VoCSource
 */

/**
 * @typedef {"Reddit Post" | "1-Star Review" | "2-Star Review" | "Support Thread" | "Feature Request"} FeedbackType
 */

/**
 * @typedef {Object} FeedbackMetadata
 * @property {number} [upvotes] - Upvotes or community agreement count
 * @property {number} [rating] - App Store / Play Store numerical star rating (1-5)
 * @property {string} [device] - User hardware context (e.g., Pixel 7 Pro, iPhone 15 Pro)
 * @property {string} date - ISO Date string of feedback submission
 * @property {string[]} tags - Categorical heuristics tags (e.g. search_failure, screenshots)
 */

/**
 * @typedef {Object} UserFeedbackRecord
 * @property {string} id - Unique identifier (e.g. voc-001)
 * @property {VoCSource} source - Channel origin
 * @property {FeedbackType} type - Document format type
 * @property {string} content - Raw unstructured customer complaint or review text
 * @property {FeedbackMetadata} metadata - Ingestion metadata
 */

export const VALID_SOURCES = [
  "r/GooglePhotos",
  "Play Store",
  "App Store",
  "Google Support Forum"
];

export const VALID_TYPES = [
  "Reddit Post",
  "1-Star Review",
  "2-Star Review",
  "Support Thread",
  "Feature Request"
];

export const SOURCE_LABELS = {
  "r/GooglePhotos": "r/GooglePhotos (Reddit)",
  "Play Store": "Google Play Store (1-Star & 2-Star)",
  "App Store": "Apple App Store (Reviews)",
  "Google Support Forum": "Google Support Forum"
};

/**
 * Validates a UserFeedbackRecord against schema constraints
 * @param {any} record
 * @returns {{ valid: boolean, errors: string[] }}
 */
export function validateFeedbackRecord(record) {
  const errors = [];

  if (!record || typeof record !== "object") {
    return { valid: false, errors: ["Record must be a non-null object"] };
  }

  if (!record.id || typeof record.id !== "string") {
    errors.push("Missing or invalid string field: 'id'");
  }

  if (!VALID_SOURCES.includes(record.source)) {
    errors.push(`Invalid 'source': '${record.source}'. Must be one of: ${VALID_SOURCES.join(", ")}`);
  }

  if (!VALID_TYPES.includes(record.type)) {
    errors.push(`Invalid 'type': '${record.type}'. Must be one of: ${VALID_TYPES.join(", ")}`);
  }

  if (!record.content || typeof record.content !== "string" || record.content.trim().length === 0) {
    errors.push("Missing or empty string field: 'content'");
  }

  if (!record.metadata || typeof record.metadata !== "object") {
    errors.push("Missing or invalid object field: 'metadata'");
  } else {
    if (!record.metadata.date || typeof record.metadata.date !== "string") {
      errors.push("Missing or invalid 'metadata.date'");
    }
    if (!Array.isArray(record.metadata.tags)) {
      errors.push("Invalid 'metadata.tags': must be an array of strings");
    }
  }

  return {
    valid: errors.length === 0,
    errors
  };
}

/**
 * Defensive sanitizer providing schema defaults for corrupted or incomplete records
 * (Implements EC-08 safeguard from edge-case.md)
 * @param {any} record
 * @param {number} fallbackIndex
 * @returns {UserFeedbackRecord}
 */
export function sanitizeFeedbackRecord(record, fallbackIndex = 1) {
  if (!record || typeof record !== "object") {
    return {
      id: `voc-fallback-${fallbackIndex}`,
      source: "Google Support Forum",
      type: "Support Thread",
      content: "No customer feedback content provided.",
      metadata: {
        date: new Date().toISOString().split("T")[0],
        tags: ["unspecified"]
      }
    };
  }

  return {
    id: typeof record.id === "string" && record.id ? record.id : `voc-fallback-${fallbackIndex}`,
    source: VALID_SOURCES.includes(record.source) ? record.source : "Google Support Forum",
    type: VALID_TYPES.includes(record.type) ? record.type : "Support Thread",
    content: typeof record.content === "string" && record.content.trim() ? record.content.trim() : "No customer feedback content provided.",
    metadata: {
      upvotes: typeof record.metadata?.upvotes === "number" ? record.metadata.upvotes : undefined,
      rating: typeof record.metadata?.rating === "number" ? record.metadata.rating : undefined,
      device: typeof record.metadata?.device === "string" ? record.metadata.device : undefined,
      date: typeof record.metadata?.date === "string" ? record.metadata.date : new Date().toISOString().split("T")[0],
      tags: Array.isArray(record.metadata?.tags) ? record.metadata.tags : ["unspecified"]
    }
  };
}
