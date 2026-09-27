# Phase-Wise Implementation Plan: AI-Powered Discovery Engine for Google Photos

**Project Title:** AI-Powered Discovery Engine for Google Photos (Internal PM Intelligence Tool)  
**Target Organization:** Google LLC — Personal Search & Google Photos (`com.google.android.apps.photos`)  
**Target Users:** Google Photos Core Experience & Semantic Search Product Managers (PMs)  
**Domain:** Computational Photography, Semantic Image Retrieval & Personal Knowledge Management (PKM)  
**Document Version:** 1.0.0  
**Status:** Approved Engineering Roadmap  
**Reference Documents:**  
* [problemStatement.md](file:///c:/Users/DELL/OneDrive/Desktop/3RD%20ATTEMPT/problemStatement.md)  
* [architecture.md](file:///c:/Users/DELL/OneDrive/Desktop/3RD%20ATTEMPT/architecture.md)  

---

## 1. Executive Implementation Overview & Scope Discipline

This document outlines the **7-Phase Engineering Execution Plan** for building, testing, and hardening the **AI-Powered Discovery Engine for Google Photos**.

The system ingests, normalizes, and synthesizes unstructured multi-channel customer feedback across **Reddit (`r/GooglePhotos`)**, **Google Play Store**, **Apple App Store**, and **Google Support Forums** to deconstruct **human memory retrieval failures** and bridge the **Semantic-Episodic Gap**.

```mermaid
gantt
    title Google Photos VoC Discovery Engine — Phased Implementation Roadmap
    dateFormat  X
    axisFormat Phase %d
    section Core Infrastructure
    Phase 1: Project Setup, Design Tokens & 30/70 Layout :p1, 0, 1
    Phase 2: Types, Ingestion Engine & Simulated Corpus   :p2, 1, 2
    section LLM & Logic
    Phase 3: Prompt Orchestrator & Gemini 1.5 Client     :p3, 2, 3
    section UI Components
    Phase 4: Left Control Sidebar & Source Toggles       :p4, 3, 4
    Phase 5: Canvas State Machine & Markdown AST Parser  :p5, 4, 5
    section Export & Hardening
    Phase 6: Clipboard Service & Slide Export Utility    :p6, 5, 6
    Phase 7: End-to-End QA, Prompt Verification & Audit  :p7, 6, 7
```

### Strict Non-Negotiables & Scope Boundaries
* **Deterministic Non-Chatbot Contract**: The UI contains **zero conversational freeform chat inputs**, message threads, or generic assistant dialogues. Interaction is driven solely by **4 dedicated analytical workflow buttons**.
* **Strict Parameter Envelope**: Google Gemini 1.5 (Pro/Flash) inference must be strictly clamped at `Temperature: 0.2` and `Top_P: 0.8` to prevent creative hallucinations and ensure fact-grounded reporting.
* **Rigid Output Syntax Contracts**:
  * **Workflow 1**: Strict `###` category names, `-` bullet definitions, and `>` blockquote verbatim evidence.
  * **Workflow 2**: Exact 3-column Markdown T-Chart Table (`Retained Episodic Anchors` vs `Forgotten System Demands` vs `Failure Mode`).
  * **Workflow 3**: Numbered list with bold names and explicit `Friction Score: High/Medium/Low`.
  * **Workflow 4**: Exactly 2 Product Opportunity Areas (POAs) with `### Problem Space`, `### Proposed AI Solution`, and `### Hypothesis to Test`.
* **Zero-Trust API Key Lifecycle**: The API key is stored exclusively in **ephemeral browser memory** (never in `localStorage`, cookies, or remote logs) with masked UI input.
* **Google Material 30/70 Layout**: Rigid desktop grid with 30% control sidebar and 70% reading canvas adhering to Google Internal Tooling design standards.

---

## 2. Phased Engineering Breakdown

```
+---------------------------------------------------------------------------------------------------------+
|                                  PHASE DELIVERABLES & OBJECTIVES MATRIX                                 |
+---------+-----------------------------------+-----------------------------------------------------------+
| Phase   | Phase Name                        | Primary Deliverables & Key Outputs                        |
+---------+-----------------------------------+-----------------------------------------------------------+
| **P1**  | **Foundation & Google Shell**     | Modern web shell, Google Material CSS tokens, 30/70 grid  |
| **P2**  | **Corpus Ingestion & Data Store** | TypeScript schema, 7 multi-channel VoC seed records       |
| **P3**  | **Gemini API & Prompt Contracts** | REST client, multi-shot prompt builders, error handlers   |
| **P4**  | **Control Sidebar Component**     | Masked API key input, 4 source toggles, 4 workflow buttons|
| **P5**  | **Main Canvas & State Machine**   | Idle graphic, loading skeletons, error banner, markdown   |
| **P6**  | **Export & Clipboard Engine**     | 1-click clipboard copy, checkmark toast, slide-ready text |
| **P7**  | **Verification & QA Hardening**   | 4-workflow validation, latency audit, security sign-off   |
+---------+-----------------------------------+-----------------------------------------------------------+
```

---

### Phase 1: Project Setup, Design Tokens & Desktop Shell Layout

**Objective:** Establish a high-performance, responsive desktop application structure using HTML5, modern vanilla JavaScript / React, and a Google Material-compliant design token system.

#### Detailed Engineering Tasks:
- [x] **1.1 Workspace Architecture & Scaffolding:**
  - Create directory structure:
    ```text
    /
    ├── index.html              # Main application entry point
    ├── css/
    │   ├── tokens.css          # Google Material design tokens (palette, spacing, typography)
    │   └── main.css            # Component styles & layout rules
    ├── js/
    │   ├── config/             # Constants, default prompts, and parameters
    │   ├── data/               # Seed VoC corpus and schema definitions
    │   ├── services/           # Gemini API client, clipboard service
    │   ├── components/         # Sidebar, Canvas, Header, Skeleton components
    │   └── app.js              # Application state coordinator & initialization
    ```
- [x] **1.2 Design Tokens & Visual Language (`css/tokens.css`):**
  - **Color Palette (Google Material 3 / Internal Tools):**
    - Google Blue Primary: `#1a73e8` (Hover: `#1765cc`, Active: `#1558b0`, Light tint: `#e8f0fe`)
    - Surface & Canvas: `#ffffff` (Main canvas), `#f8f9fa` (Sidebar / Card background)
    - Borders & Outlines: `#dadce0` (Card dividers), `#e8eaed` (Subtle separators)
    - Text: `#202124` (Primary text), `#5f6368` (Secondary / descriptive text), `#80868b` (Muted)
    - Error: `#d93025` (Border/text), `#fce8e6` (Background alert tint)
    - Success: `#188038` (Confirmation badge), `#e6f4ea` (Success tint)
  - **Typography:**
    - Load Google Fonts: `Inter` and `Google Sans` / `Roboto` (Weights: 400, 500, 600, 700).
    - Establish base line-height: `1.65` for optimal reading pane legibility.
- [x] **1.3 Master 30/70 Desktop Layout (`index.html` & `css/main.css`):**
  - Construct header: Google Photos pinwheel icon, system title (*"Google Photos VoC Intelligence Engine"*), version badge (*"Internal PM Tool v1.0"*).
  - Build flex/grid layout:
    - **Left Sidebar (`width: 30%`, min `320px`, max `400px`):** Fixed height, vertical scroll.
    - **Main Canvas (`width: 70%`, min `680px`):** White reading pane with centered reading container (`max-width: 920px`).

#### Phase 1 Verification Milestone:
* Clean, responsive desktop layout renders in browser with crisp Google Material styling and exact 30/70 split.

---

### Phase 2: Types, Ingestion Engine & Simulated VoC Corpus

**Objective:** Implement data models, validation constraints, and seed a multi-channel corpus of unstructured feedback representing genuine memory retrieval failures.

#### Detailed Engineering Tasks:
- [x] **2.1 TypeScript / JSDoc Data Schema (`js/data/schema.js`):**
  - Define `UserFeedbackRecord` schema:
    ```typescript
    interface UserFeedbackRecord {
      id: string;
      source: "r/GooglePhotos" | "Play Store" | "App Store" | "Google Support Forum";
      type: "Reddit Post" | "1-Star Review" | "2-Star Review" | "Support Thread" | "Feature Request";
      content: string;
      metadata: {
        upvotes?: number;
        rating?: number;
        device?: string;
        date: string;
        tags: string[];
      };
    }
    ```
- [x] **2.2 High-Signal Simulated Corpus (`js/data/seedCorpus.js`):**
  - Curate 7+ rich, edge-case feedback records reflecting real user friction:
    1. **`voc-001` (Reddit)**: Trip to Rome, searching *"pasta"* returns recipe screenshots; retained cue: raining and wearing red jacket.
    2. **`voc-002` (Play Store)**: Pixel 7 user searching for dog; returns 400 generic dog photos instead of specific posture (*"sleeping on messy desk"*).
    3. **`voc-003` (Google Support)**: Concert tickets/receipts pollution; searching *"concert"* surfaces 200 Spotify screenshots.
    4. **`voc-004` (Reddit)**: Tire pressure sticker photo; user forced to cross-reference WhatsApp chat history before date scrubbing.
    5. **`voc-005` (App Store)**: iPhone 15 user recalling purple haze sunset in Greece; search returns 1,200 generic sunsets.
    6. **`voc-006` (Reddit)**: Web meme vs. real cat photo pollution; mixing saved web media into life archive.
    7. **`voc-007` (Google Support)**: Family photo with mom holding baby in green armchair; 20 minutes of chronological scrubbing.
- [x] **2.3 Corpus Store & Filtering Utility (`js/data/corpusStore.js`):**
  - Implement reactive store: `getActiveRecords(sourceFilters: Record<string, boolean>): UserFeedbackRecord[]`.
  - Provide helper method to serialize filtered records into formatted JSON strings for prompt injection.

#### Phase 2 Verification Milestone:
* Calling `corpusStore.getActiveRecords()` returns filtered subsets and logs valid JSON without errors.

---

### Phase 3: Prompt Orchestrator & Gemini 1.5 Client

**Objective:** Construct the deterministic multi-shot prompt assembly pipeline and create a resilient Google Gemini REST API client.

#### Detailed Engineering Tasks:
- [x] **3.1 Prompt Template Assembler (`js/services/promptBuilder.js`):**
  - Implement system prompt contracts for each of the 4 workflows:
    - **Workflow 1 (`taxonomy`)**: Act as Principal PM; categorize 3 distinct edge-cases; exclude generic categories; output `###` headers, `-` bullet definitions, `>` blockquotes.
    - **Workflow 2 (`cognitive_gap`)**: Act as Principal Cognitive UX Researcher; map sensory recall vs. rigid system demands; output strictly a 3-column Markdown T-Chart.
    - **Workflow 3 (`workarounds`)**: Act as Staff PM; identify brute-force behaviors (Chronological Scrubbing, Person Pivot, etc.); output numbered list with bold names and `Friction Score: High/Medium/Low`.
    - **Workflow 4 (`poa`)**: Act as VP of Product; generate 2 POAs with `### Problem Space`, `### Proposed AI Solution`, and formal `### Hypothesis to Test`. Immediately following the 2 POAs, append a **"Comparison / Trade-off Matrix"** Markdown table comparing POA 1 vs POA 2 across: (1) Specific Retrieval Problems Solved, (2) User Impact (High/Medium/Low with rationale), and (3) Implementation Effort (High/Medium/Low with rationale).
  - Assemble complete payload injecting active corpus JSON:
    ```javascript
    export function buildWorkflowPrompt(workflowId, corpusRecords) { ... }
    ```
- [x] **3.2 Gemini API REST Client (`js/services/geminiClient.js`):**
  - Endpoint: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}` (fallback/toggle for `gemini-1.5-pro`).
  - Request Payload configuration:
    ```json
    {
      "contents": [{ "parts": [{ "text": assembledPrompt }] }],
      "generationConfig": {
        "temperature": 0.2,
        "topP": 0.8,
        "topK": 40,
        "maxOutputTokens": 2048
      }
    }
    ```
  - Error Interceptor:
    - `400`: Malformed request or model parameters.
    - `401 / 403`: Invalid or unauthorized Gemini API key.
    - `429`: Quota exceeded / rate limit warning.
    - `500 / 503`: Google AI Studio backend temporary unavailability.

#### Phase 3 Verification Milestone:
* Unit test prompt generation utility to confirm strict formatting instructions and proper JSON serialization.

---

### Phase 4: Left Control Sidebar & Trigger Subsystem

**Objective:** Implement the left control pane featuring masked API key entry, active source checkboxes, and 4 workflow trigger buttons.

#### Detailed Engineering Tasks:
- [x] **4.1 API Key Configuration Card (`js/components/ApiKeyCard.js`):**
  - Masked password input field with show/hide toggle button (eye icon).
  - Validation status indicator:
    - Gray: *"No Key Entered"*
    - Green: *"Key Configured (In-Memory Only)"*
  - Security disclaimer: *"Keys are held in browser memory only and never saved to storage or transmitted to external servers."*
- [x] **4.2 Data Source Toggle Section (`js/components/SourceSelector.js`):**
  - Checkbox controls for active corpus channels:
    - `[x] r/GooglePhotos (Reddit)`
    - `[x] Google Play Store (1-Star & 2-Star)`
    - `[x] Apple App Store (Reviews)`
    - `[x] Google Support Community`
  - Dynamic record counter: *"7 of 7 records active"*.
- [x] **4.3 Workflow Action Buttons (`js/components/WorkflowButtons.js`):**
  - 4 high-impact action cards with descriptive labels and icons:
    1. **Workflow 1**: *"Taxonomy of 'Lost' Photos"* (Tag: `Edge-Case Classification`)
    2. **Workflow 2**: *"Cognitive Gap Matrix"* (Tag: `Episodic vs. System T-Chart`)
    3. **Workflow 3**: *"Behavioral Workaround Mapping"* (Tag: `Friction Scoring`)
    4. **Workflow 4**: *"Product Opportunity Synthesis"* (Tag: `PM POAs & Hypotheses`)
  - Hover states, focus rings, and active state highlights in Google Blue (`#1a73e8`).

#### Phase 4 Verification Milestone:
* Interactive sidebar handles API key input toggling, updates active record counts when sources are unselected, and fires workflow events.

---

### Phase 5: Main Reading Canvas & State Machine Implementation

**Objective:** Build the reactive central reading canvas handling the full lifecycle of states: `IDLE`, `LOADING`, `ERROR`, and `SUCCESS`.

#### Detailed Engineering Tasks:
- [x] **5.1 State Machine Reducer (`js/state/canvasState.js`):**
  - State definition:
    ```typescript
    type State = {
      status: "IDLE" | "LOADING" | "ERROR" | "SUCCESS";
      activeWorkflow: string | null;
      loadingMessage: string;
      errorMessage: string | null;
      markdownContent: string;
    };
    ```
- [x] **5.2 State A — IDLE Screen (`js/components/IdleState.js`):**
  - Render Google Photos pinwheel graphic with smooth subtle opacity.
  - Title: *"Google Photos Memory Retrieval Intelligence"*
  - Subtitle: *"Ingesting multi-channel Voice-of-Customer feedback to deconstruct search failure heuristics and episodic memory gaps."*
  - Instructions: *"Enter your Gemini API key on the left and select an analytical workflow to begin."*
- [x] **5.3 State B — LOADING Screen (`js/components/LoadingSkeleton.js`):**
  - Render animated pulsing skeleton cards imitating headers, tables, and quote blocks.
  - Micro-copy rotator (changes every 2.5s):
    - *"Connecting to Gemini 1.5 Analytical Engine..."*
    - *"Synthesizing unstructured user complaints..."*
    - *"Extracting episodic memory failure patterns..."*
    - *"Enforcing strict PM deliverable syntax..."*
- [x] **5.4 State C — ERROR Screen (`js/components/ErrorBanner.js`):**
  - Google Material Red alert banner with icon and clear remediation copy:
    - *"API Key Required: Please provide a valid Gemini API key in the sidebar configuration."*
    - *"Quota Exceeded: Google AI Studio rate limit reached. Please wait 30 seconds and retry."*
  - Retry CTA button.
- [x] **5.5 State D — SUCCESS Screen & Markdown AST Parser (`js/components/MarkdownRenderer.js`):**
  - Parse and render Markdown cleanly:
    - `###` headers: Bold Google Sans / Inter with clear section spacing.
    - Blockquotes (`>`): Left border (`4px solid #1a73e8`), light background (`#f8f9fa`), italic quote styling.
    - Tables: Zebra striping, crisp borders (`#dadce0`), padded cells.
    - Lists: Numbered circles and bold terms.

#### Phase 5 Verification Milestone:
* Canvas transitions seamlessly across IDLE, LOADING, ERROR, and SUCCESS states. Markdown output renders with executive typography.

---

### Phase 6: Slide Export, Clipboard Utility & Micro-Interactions

**Objective:** Add PM-friendly export workflows allowing instant copying of formatted markdown reports into Google Slides, Docs, or PRDs.

#### Detailed Engineering Tasks:
- [x] **6.1 One-Click Clipboard Service (`js/services/clipboardService.js`):**
  - Uses `navigator.clipboard.writeText()` to copy raw markdown.
  - Fallback to `document.execCommand('copy')` for compatibility.
- [x] **6.2 Copy CTA Button & Toast Feedback:**
  - Placed prominently in the reading pane header: *"📋 Copy to Clipboard"*.
  - When clicked, changes instantaneously to: *"✓ Copied for Slides!"* (Google Green `#188038`) for 2.5 seconds before resetting.
- [x] **6.3 Plaintext Slide Paste Optimizer:**
  - Ensure table formatting and quotes paste cleanly without broken formatting into Google Docs and Google Slides text frames.

#### Phase 6 Verification Milestone:
* Clicking copy puts full formatted report into system clipboard and displays green checkmark confirmation toast.

---

### Phase 7: End-to-End QA, Verification & Acceptance Audit

**Objective:** Validate all 4 analytical workflows against the acceptance criteria outlined in the Problem Statement and Architecture documents.

#### Detailed Engineering Tasks:
- [x] **7.1 Workflow 1 Validation (Taxonomy of Lost Photos):**
  - Verify 3 categories generated.
  - Check absence of generic categories (e.g., *"vacation"*).
  - Assert presence of `###` headers, `-` bullet definitions, and `>` blockquote quotes.
- [x] **7.2 Workflow 2 Validation (Cognitive Gap Matrix):**
  - Verify valid 3-column Markdown table generated.
  - Assert columns: `Retained Episodic Anchors`, `Forgotten System Demands`, `Failure Mode`.
- [x] **7.3 Workflow 3 Validation (Behavioral Workarounds):**
  - Verify numbered list format.
  - Assert presence of bold names and explicit `Friction Score: High/Medium/Low`.
- [x] **7.4 Workflow 4 Validation (Product Opportunity Synthesis & Trade-off Matrix):**
  - Verify 2 distinct POAs generated with `### Problem Space`, `### Proposed AI Solution`, and `### Hypothesis to Test` sections.
  - Assert the presence of the **Comparison / Trade-off Matrix** table at the bottom comparing POA 1 vs POA 2 across Specific Retrieval Problems Solved, User Impact, and Implementation Effort.
- [x] **7.5 Resilience & Security Audit:**
  - Verify key is masked and cleared on page refresh.
  - Verify app behaves gracefully when offline or when invalid key is entered.

#### Phase 7 Verification Milestone:
* 100% test pass rate across all 4 workflows with zero conversational chatbot leakage.

---

## 3. Engineering Acceptance Checklist

| Verification Gate | Expected Criteria | Test Method | Status |
|---|---|---|---|
| **Zero-Chatbot Architecture** | No chat inputs, message histories, or conversational greetings | Visual & code inspection | **Verified** |
| **Deterministic Parameter Envelope** | `temperature: 0.2`, `topP: 0.8` hardcoded in API request | Network payload inspection | **Verified** |
| **Workflow 1 Output Syntax** | `###` category, `-` bullet definition, `>` blockquote quote | Markdown AST analysis | **Verified** |
| **Workflow 2 Output Syntax** | 3-column Markdown T-Chart Table | Table DOM element assertion | **Verified** |
| **Workflow 3 Output Syntax** | Numbered list with bold names and `Friction Score: [High/Med/Low]` | Regex pattern match | **Verified** |
| **Workflow 4 Output Syntax** | 2 POAs (Problem, Solution, Hypothesis) + Comparison/Trade-off Matrix table | Header & table structure audit | **Verified** |
| **API Key Ephemerality** | Key never written to `localStorage` or `sessionStorage` | DevTools storage audit | **Verified** |
| **UI State Machine** | Transitions smoothly between IDLE, LOADING, ERROR, SUCCESS | Functional UI test | **Verified** |
| **Export Action** | 1-click clipboard copy with visual feedback toast | Clipboard verification | **Verified** |
