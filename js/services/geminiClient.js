import { APP_CONFIG } from '../config/constants.js';

/**
 * Client for Google Gemini API
 */
export class GeminiClient {
  constructor(apiKey) {
    this.apiKey = apiKey ? apiKey.trim() : "";
  }

  setApiKey(key) {
    this.apiKey = key ? key.trim() : "";
  }

  hasApiKey() {
    return Boolean(this.apiKey && this.apiKey.length > 5);
  }

  /**
   * Execute inference against Gemini model
   * @param {string} promptText
   * @param {string} [modelName]
   * @returns {Promise<string>}
   */
  async generateContent(promptText, modelName = APP_CONFIG.DEFAULT_MODEL) {
    if (!this.hasApiKey()) {
      const error = new Error("Gemini API key is missing. Please enter your API key in the configuration panel on the left.");
      error.status = 401;
      throw error;
    }

    // Mock / Offline Demo Mode for QA and Automated Verification
    if (this.apiKey.toLowerCase().includes("mock") || (typeof window !== "undefined" && window.location && window.location.search.includes("mock=true"))) {
      await new Promise(resolve => setTimeout(resolve, 600));
      return this.generateMockResponse(promptText);
    }

    const url = `${APP_CONFIG.GEMINI_API_BASE_URL}/${modelName}:generateContent?key=${encodeURIComponent(this.apiKey)}`;

    const payload = {
      contents: [
        {
          parts: [{ text: promptText }]
        }
      ],
      generationConfig: {
        temperature: APP_CONFIG.TEMPERATURE,
        topP: APP_CONFIG.TOP_P,
        topK: APP_CONFIG.TOP_K,
        maxOutputTokens: APP_CONFIG.MAX_OUTPUT_TOKENS
      }
    };

    let response;
    try {
      response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
      });
    } catch (networkErr) {
      const error = new Error("Network connection failed. Unable to reach Google AI Studio. Please verify your internet connection.");
      error.status = 0;
      throw error;
    }

    if (!response.ok) {
      let errorDetails = "Unknown API Error";
      try {
        const errorJson = await response.json();
        if (errorJson.error && errorJson.error.message) {
          errorDetails = errorJson.error.message;
        }
      } catch {
        errorDetails = await response.text();
      }

      if (response.status === 404 && modelName !== "gemini-3.8-flash") {
        console.warn(`Model ${modelName} returned 404, attempting fallback to gemini-3.8-flash...`);
        return this.generateContent(promptText, "gemini-3.8-flash");
      }

      if (response.status === 400) {
        throw new Error(`Invalid Request (400): ${errorDetails}`);
      } else if (response.status === 401 || response.status === 403) {
        throw new Error(`Authentication Failed (${response.status}): Your Gemini API key is invalid or unauthorized. Please verify your Google AI Studio credentials.`);
      } else if (response.status === 429) {
        throw new Error(`Rate Limit Exceeded (429): Google AI Studio quota exceeded. Please wait 30 seconds before triggering another analytical workflow.`);
      } else if (response.status >= 500) {
        throw new Error(`Google AI Studio Service Error (${response.status}): The Gemini backend is currently experiencing temporary issues. Please try again shortly.`);
      } else {
        throw new Error(`API Error (${response.status}): ${errorDetails}`);
      }
    }

    const data = await response.json();

    if (
      !data.candidates ||
      data.candidates.length === 0 ||
      !data.candidates[0].content ||
      !data.candidates[0].content.parts ||
      data.candidates[0].content.parts.length === 0
    ) {
      throw new Error("Empty model response: The Gemini engine completed the request but returned no text content.");
    }

    return data.candidates[0].content.parts[0].text;
  }

  /**
   * Deterministic mock generator adhering strictly to prompt contracts
   * @param {string} promptText
   * @returns {string}
   */
  generateMockResponse(promptText) {
    if (promptText.includes("Workflow 1") || promptText.includes("Taxonomy of \"Lost\" Photos")) {
      return `### Ephemeral Clutter (Functional Screenshots & Temporary Media)
- **Definition**: Informational photos taken as external memory aids (receipts, Wi-Fi stickers, menus, parking spots) that contaminate personal memory timelines.
> "I took a photo of the tire pressure sticker on my driver's side door 4 months ago... I couldn't find it when I actually needed it."
> "I have over 1,200 photos of receipts and ticket screenshots that show up when I search for 'concert'."

### Sensory & Atmosphere Recall Breakdowns
- **Definition**: Emotional and episodic memory retrieval requests where the user recalls environmental conditions (sunset colors, ambient lighting, rain) rather than cataloged objects.
> "I spent 15 minutes trying to find a picture of my girlfriend at an Italian restaurant... I remembered it was raining and she was wearing a red jacket."
> "I took a photo of a purple sunset in Greece last summer. When I search 'sunset' it shows me 400 photos of every sunset I've ever seen."

### Vague Relational & Situational Queries
- **Definition**: Complex multi-entity queries involving relationships, specific postures, or non-visual temporal anchors.
> "I wanted to find that one photo of my dog sleeping on my messy desk while I was studying for finals."`;
    }

    if (promptText.includes("Workflow 2") || promptText.includes("Cognitive Gap Matrix")) {
      return `## Cognitive Gap Matrix

| Retained Episodic Anchors | Forgotten System Demands | Failure Mode |
| :--- | :--- | :--- |
| Weather (raining), sensory cues (red jacket, cozy dinner) | Exact date or explicit OCR keyword ("restaurant") | Semantic Overload: System returns recipe screenshots instead of dinner memories |
| Contextual posture ("sleeping on messy desk") | Object classification tags ("dog", "desk") | Visual Generalization: System dumps 400 generic dog photos without pose distinction |
| Atmospheric mood (purple sunset, Greece vacation) | Precise GPS location or standard EXIF tags | Keyword Collapse: Dumps hundreds of generic sunsets across 5 years |`;
    }

    if (promptText.includes("Workflow 3") || promptText.includes("Behavioral Workaround Mapping")) {
      return `### 1. Chronological Scrubbing
- **Description**: Users manually swipe through weeks or months of photo grids when keyword search returns clutter.
- **Friction Score**: High
> "Ended up having to scroll all the way back to October manually to find my mother holding my newborn in that green armchair."

### 2. Cross-App Timestamp Triangulation
- **Description**: Users leave Google Photos to inspect WhatsApp or Messages chat logs to find the exact date an event occurred, then return to scrub to that date.
- **Friction Score**: High
> "I had to go to my WhatsApp chat with my brother to see when he texted me about our tire change before I could locate the photo."

### 3. Person Pivot Filtering
- **Description**: Users navigate to the People album to find a companion's face, then filter down from their associated photos.
- **Friction Score**: Medium
> "I had to find my friend's face album first, then scroll through all 800 photos with her just to locate the concert ticket."`;
    }

    if (promptText.includes("Workflow 4") || promptText.includes("Product Opportunity Synthesis")) {
      return `### POA 1: Episodic Attribute Fusion Engine
- **Problem Space**: Users recall sensory and situational attributes (clothing color, weather, co-present people) that are lost in traditional object-detection indexing.
- **Proposed Solution**: Multi-modal fusion layer combining contextual signals (weather API, dominant palette, posture detection, calendar events) into searchable embeddings.
- **PM Hypothesis**: Allowing multi-anchor natural language queries ("raining red jacket dinner") will reduce median retrieval time by 45%.

### POA 2: Ephemeral Utility Separation Layer
- **Problem Space**: Screenshot clutter and temporary utility photos pollute meaningful personal memories.
- **Proposed Solution**: Automated utility partition that segregates documents, receipts, Wi-Fi passwords, and barcodes into a dedicated "Utility Vault".
- **PM Hypothesis**: Isolating utilitarian screenshots will improve discovery CTR for episodic memories by 30% and reduce search abandonment.

## Comparison / Trade-off Matrix

| Dimension | POA 1: Episodic Attribute Fusion | POA 2: Ephemeral Utility Separation |
| :--- | :--- | :--- |
| **Specific Retrieval Problems Solved** | Solves sensory/episodic query mismatch where users recall atmospheric anchors rather than object tags | Solves timeline pollution and search dilution caused by temporary screenshots and receipts |
| **User Impact** | **High**: Eliminates frustrating 15-minute manual scrubbing sessions for emotionally significant memories | **High**: Immediately declutters search results across all queries and restores trust in photo search |
| **Implementation Effort** | **High**: Requires multi-modal embedding training, contextual fusion, and low-latency vector search | **Medium**: Leverages existing document OCR and screenshot classification heuristics |`;
    }

    return `### Generated Synthesis Report\n\n> "Synthesized VoC intelligence report."`;
  }
}
