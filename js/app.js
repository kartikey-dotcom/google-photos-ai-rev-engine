import { APP_CONFIG, WORKFLOWS } from './config/constants.js';
import { corpusStore } from './data/corpusStore.js';
import { buildWorkflowPrompt } from './services/promptBuilder.js';
import { GeminiClient } from './services/geminiClient.js';
import { ClipboardService } from './services/clipboardService.js';
import { HeaderComponent } from './components/Header.js';
import { SidebarComponent } from './components/Sidebar.js';
import { CanvasComponent } from './components/Canvas.js';
import { renderMarkdown } from './services/markdownRenderer.js';

/**
 * Main Application Orchestrator
 */
class App {
  constructor() {
    this.geminiClient = new GeminiClient("");
    this.sourceFilters = {
      "r/GooglePhotos": true,
      "Play Store": true,
      "App Store": true,
      "Google Support Forum": true
    };
    this.activeWorkflowId = null;
    this.lastReportMarkdown = "";

    this.header = null;
    this.sidebar = null;
    this.canvas = null;
  }

  init() {
    // 1. Initialize Header
    const headerEl = document.getElementById("appHeader");
    this.header = new HeaderComponent(headerEl);
    this.header.setModelInfo(APP_CONFIG.DEFAULT_MODEL, APP_CONFIG.TEMPERATURE);

    // 2. Initialize Sidebar
    this.sidebar = new SidebarComponent({
      onKeyChange: (key) => this.handleKeyChange(key),
      onSourceChange: (source, isChecked) => this.handleSourceChange(source, isChecked),
      onWorkflowTrigger: (workflowId) => this.executeWorkflow(workflowId)
    });

    // 3. Initialize Reading Canvas
    this.canvas = new CanvasComponent({
      onRetry: () => this.handleRetry(),
      onCopy: () => this.handleCopy()
    });

    // 4. Initial Counts & State
    this.updateCorpusCount();
    this.canvas.setState("IDLE");
  }

  handleKeyChange(key) {
    this.geminiClient.setApiKey(key);
  }

  handleSourceChange(source, isChecked) {
    this.sourceFilters[source] = isChecked;
    this.updateCorpusCount();
  }

  updateCorpusCount() {
    const active = corpusStore.getActiveRecords(this.sourceFilters);
    const total = corpusStore.getTotalCount();
    this.sidebar.updateCorpusCount(active.length, total);
  }

  handleRetry() {
    if (this.activeWorkflowId) {
      this.executeWorkflow(this.activeWorkflowId);
    }
  }

  async executeWorkflow(workflowId) {
    const workflowConfig = WORKFLOWS[workflowId];
    if (!workflowConfig) return;

    this.activeWorkflowId = workflowId;
    this.sidebar.setActiveWorkflow(workflowId);
    this.canvas.setHeaderInfo(workflowConfig.title, workflowConfig.tag);

    // Check API Key
    if (!this.geminiClient.hasApiKey()) {
      this.canvas.setState("ERROR", {
        title: "API Key Required",
        message: "Please enter your Google Gemini API key in the configuration card on the left sidebar before triggering this analytical workflow."
      });
      this.sidebar.focusKeyInput();
      return;
    }

    // Check Active Ingestion Sources
    const activeRecords = corpusStore.getActiveRecords(this.sourceFilters);
    if (activeRecords.length === 0) {
      this.canvas.setState("ERROR", {
        title: "No Ingestion Sources Selected",
        message: "All feedback channels are currently disabled. Please enable at least one VoC source in the sidebar to run the analytical synthesis."
      });
      return;
    }

    // Set Loading State
    this.sidebar.setButtonsDisabled(true);
    this.canvas.setState("LOADING", {
      loadingMessages: workflowConfig.loadingMessages
    });

    // Build Prompt
    const prompt = buildWorkflowPrompt(workflowConfig, activeRecords);

    try {
      const markdown = await this.geminiClient.generateContent(prompt);
      this.lastReportMarkdown = markdown;
      this.sidebar.setButtonsDisabled(false);
      this.canvas.setState("SUCCESS", { markdown });
    } catch (err) {
      console.error("Workflow Execution Error:", err);
      this.sidebar.setButtonsDisabled(false);
      this.canvas.setState("ERROR", {
        title: "Synthesis Pipeline Failure",
        message: err.message || "An unexpected error occurred during synthesis."
      });
    }
  }

  async handleCopy() {
    if (!this.lastReportMarkdown) return;

    const renderedHtml = renderMarkdown(this.lastReportMarkdown);
    const success = await ClipboardService.copyText(this.lastReportMarkdown, renderedHtml);
    if (success) {
      this.canvas.setCopySuccess();
      ClipboardService.showToast("Report copied to clipboard! Ready for Google Slides or Docs.");
    } else {
      ClipboardService.showToast("Copy failed. Please copy manually from the canvas.");
    }
  }
}

// Instantiate on DOM load
document.addEventListener("DOMContentLoaded", () => {
  const app = new App();
  app.init();
});
