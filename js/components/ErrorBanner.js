/**
 * Error Banner Component
 * Renders Google Material Red alert banner with contextual remediation guidance
 * and interactive 1-click retry button.
 */
export class ErrorBannerComponent {
  /**
   * @param {Object} options
   * @param {HTMLElement} [options.containerElement]
   * @param {Function} options.onRetry
   */
  constructor({ containerElement, onRetry }) {
    this.container = containerElement || document.getElementById("errorStateContainer");
    this.titleEl = document.getElementById("errorTitle");
    this.messageEl = document.getElementById("errorMessageText");
    this.retryBtn = document.getElementById("errorRetryBtn");
    this.onRetry = onRetry;

    this.bindEvents();
  }

  bindEvents() {
    if (this.retryBtn) {
      this.retryBtn.addEventListener("click", () => {
        if (typeof this.onRetry === "function") {
          this.onRetry();
        }
      });
    }
  }

  /**
   * Display error banner with contextual diagnosis
   * @param {Object} options
   * @param {string} [options.title]
   * @param {string} [options.message]
   * @param {"API_KEY_REQUIRED" | "QUOTA_EXCEEDED" | "NO_SOURCES" | "NETWORK_ERROR" | "GENERAL"} [options.errorType]
   */
  show({ title, message, errorType } = {}) {
    if (this.container) {
      this.container.style.display = "flex";
    }

    let resolvedTitle = title || "Analytical Pipeline Error";
    let resolvedMessage = message || "An unexpected error occurred during analytical synthesis.";

    // Contextual remediation templates as per Phase 5.4
    if (errorType === "API_KEY_REQUIRED") {
      resolvedTitle = "API Key Required";
      resolvedMessage = "Please provide a valid Gemini API key in the sidebar configuration before running synthesis.";
    } else if (errorType === "QUOTA_EXCEEDED") {
      resolvedTitle = "Quota Exceeded";
      resolvedMessage = "Google AI Studio rate limit reached. Please wait 30 seconds and retry.";
    } else if (errorType === "NO_SOURCES") {
      resolvedTitle = "No Ingestion Sources Selected";
      resolvedMessage = "All feedback channels are currently disabled. Please enable at least one VoC source in the sidebar to run the analytical synthesis.";
    } else if (errorType === "NETWORK_ERROR") {
      resolvedTitle = "Network Connectivity Drop";
      resolvedMessage = "Unable to reach Google AI Studio. Please verify your internet connection or check corporate firewall proxy settings.";
    }

    if (this.titleEl) {
      this.titleEl.textContent = resolvedTitle;
    }
    if (this.messageEl) {
      this.messageEl.textContent = resolvedMessage;
    }
  }

  hide() {
    if (this.container) {
      this.container.style.display = "none";
    }
  }

  isVisible() {
    return this.container && this.container.style.display !== "none";
  }
}
