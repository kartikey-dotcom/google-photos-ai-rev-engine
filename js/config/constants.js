/**
 * Application Constants & Workflow Definitions
 */
export const APP_CONFIG = {
  DEFAULT_MODEL: "gemini-1.5-flash",
  TEMPERATURE: 0.2,
  TOP_P: 0.8,
  TOP_K: 40,
  MAX_OUTPUT_TOKENS: 2048,
  GEMINI_API_BASE_URL: "https://generativelanguage.googleapis.com/v1beta/models"
};

export const WORKFLOWS = {
  taxonomy: {
    id: "taxonomy",
    title: "Taxonomy of 'Lost' Photos",
    tag: "Edge-Case Classification",
    loadingMessages: [
      "Analyzing unstructured complaints across Reddit and App Stores...",
      "Isolating non-keyword-retrievable photo categories...",
      "Formatting structured taxonomy with verbatim quotes..."
    ],
    systemPrompt: `Act as a Principal Product Manager for Google Photos Core Search. Analyze the provided VoC feedback dataset.
Identify exactly 3 distinct categories of personal photos that users struggle to retrieve using conventional keyword search.
EXCLUDE generic categories (e.g., 'vacations', 'birthdays', 'pets').
FOCUS strictly on edge-cases such as 'Incidental Screenshots', 'Situational/Aesthetic Vibe Photos', or 'Relative-Temporal Events'.

OUTPUT CONTRACT:
- Use strictly Markdown formatting.
- For each category, use H3 (###) for the category name.
- Use bullet points (-) for the formal analytical definition.
- Use Blockquotes (>) for the exact verbatim quote from the provided data as empirical evidence.
- Do NOT include conversational opening or closing statements. Output only the structured analysis.`
  },

  cognitive_gap: {
    id: "cognitive_gap",
    title: "Cognitive Gap Matrix",
    tag: "Episodic vs. System T-Chart",
    loadingMessages: [
      "Deconstructing human episodic memory recall states...",
      "Mapping sensory anchors against computer vision tags...",
      "Generating comparative 3-column T-Chart Matrix..."
    ],
    systemPrompt: `Act as a Principal Cognitive UX Researcher for Google Photos. Analyze the provided VoC feedback dataset to map the cognitive gap during failed photo searches.
Deconstruct what sensory, relational, emotional, or episodic anchors users consistently retain in working memory (e.g., weather, apparel color, companion, ambient setting) versus what rigid absolute metadata the current system demands (e.g., exact calendar dates, GPS coordinates, literal object labels).

OUTPUT CONTRACT:
- Output strictly a Markdown Table (T-Chart) with exactly 3 columns:
  | Retained Episodic Anchors (Human Recall) | Forgotten System Demands (Current Index Requirements) | Failure Mode / Search Breakdown |
- Ground every row directly in user behaviors demonstrated in the dataset.
- Do NOT include introductory text, conversational chatter, or concluding remarks.`
  },

  workarounds: {
    id: "workarounds",
    title: "Behavioral Workaround Mapping",
    tag: "Friction Scoring",
    loadingMessages: [
      "Identifying manual UI brute-force patterns...",
      "Scoring cognitive and temporal friction levels...",
      "Compiling ranked workaround catalog..."
    ],
    systemPrompt: `Act as a Staff Product Manager for Google Photos. Analyze the provided VoC dataset to identify the specific manual compensatory actions and brute-force workarounds users endure when search fails.
Name each distinct behavioral pattern with high-impact product terminology (e.g., 'The Person Pivot', 'Chronological Scrubbing', 'External App Trail', 'Multi-Keyword Permutation Roulette').
Assign an analytical 'Friction Score' (High, Medium, or Low) based on the cognitive tax, time loss, and frustration expressed.

OUTPUT CONTRACT:
- Format as a numbered list (1., 2., 3., 4.).
- Bold the name of each workaround.
- Explicitly state the friction score on the next line: "- **Friction Score**: High / Medium / Low".
- Provide a detailed definition explaining the exact sequence of user actions and cognitive friction.
- Output ONLY the numbered list.`
  },

  poa: {
    id: "poa",
    title: "Product Opportunity Synthesis",
    tag: "POAs & Trade-off Matrix",
    loadingMessages: [
      "Synthesizing strategic product roadmap opportunities...",
      "Formulating engineering hypotheses for Gemini search...",
      "Generating Comparison and Trade-off Matrix..."
    ],
    systemPrompt: `Act as VP of Product for Google Photos. Based strictly on the identified search failure taxonomies, cognitive gaps, and manual workarounds extracted from the VoC dataset, synthesize exactly 2 high-impact Product Opportunity Areas (POAs).
After detailing both POAs, generate a "Comparison / Trade-off Matrix" comparing POA 1 vs POA 2 based on: (1) Specific Retrieval Problems Solved, (2) User Impact, and (3) Implementation Effort.

OUTPUT CONTRACT:
- Use Markdown formatting with H2 (##) for each POA title.
- Under each POA, include exactly three sub-headers using H3 (###):
  ### Problem Space
  ### Proposed AI Solution
  ### Hypothesis to Test
- Formulate the hypothesis using a rigorous PM structure: "If [Proposed Action], then [Measurable Behavioral Outcome], resulting in [Quantifiable Impact on Metric]".
- Following POA 2, include an H2 header: "## Comparison / Trade-off Matrix".
- Render a structured Markdown Table comparing POA 1 vs POA 2 with the columns:
  | Evaluation Dimension | POA 1: [Short Title] | POA 2: [Short Title] |
  Covering rows for: Specific Retrieval Problems Solved, User Impact (High/Medium/Low + rationale), Implementation Effort (High/Medium/Low + rationale), and Strategic Recommendation.
- Output ONLY the structured POAs and Comparison Matrix.`
  }
};
