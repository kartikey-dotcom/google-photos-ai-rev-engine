import { CanvasStateStore } from '../state/canvasState.js';
import { IdleStateComponent } from './IdleState.js';
import { LoadingSkeletonComponent } from './LoadingSkeleton.js';
import { ErrorBannerComponent } from './ErrorBanner.js';
import { renderMarkdown } from '../services/markdownRenderer.js';

/**
 * Main Reading Canvas Component (State Machine Coordinator)
 * Coordinates the full lifecycle: IDLE -> LOADING -> ERROR -> SUCCESS.
 */
export class CanvasComponent {
  /**
   * @param {Object} options
   * @param {Function} options.onRetry
   * @param {Function} options.onCopy
   */
  constructor({ onRetry, onCopy }) {
    this.onRetry = onRetry;
    this.onCopy = onCopy;

    // Header & Action elements
    this.titleEl = document.getElementById("canvasTitleDisplay");
    this.tagEl = document.getElementById("canvasTagDisplay");
    this.copyBtn = document.getElementById("copyReportBtn");
    this.copyBtnText = document.getElementById("copyBtnText");

    // State container elements
    this.idleContainer = document.getElementById("idleStateContainer");
    this.loadingContainer = document.getElementById("loadingStateContainer");
    this.errorContainer = document.getElementById("errorStateContainer");
    this.reportContainer = document.getElementById("reportContentContainer");

    // Instantiate State Sub-Components
    this.idleState = new IdleStateComponent(this.idleContainer);
    this.loadingSkeleton = new LoadingSkeletonComponent(this.loadingContainer);
    this.errorBanner = new ErrorBannerComponent({
      containerElement: this.errorContainer,
      onRetry: () => this.onRetry()
    });

    // Reactive State Store
    this.stateStore = new CanvasStateStore();

    this.bindEvents();
  }

  bindEvents() {
    if (this.copyBtn) {
      this.copyBtn.addEventListener("click", () => {
        if (typeof this.onCopy === "function") {
          this.onCopy();
        }
      });
    }
  }

  /**
   * Set workflow metadata in sticky canvas header
   * @param {string} title
   * @param {string} tag
   */
  setHeaderInfo(title, tag) {
    if (this.titleEl) this.titleEl.textContent = title;
    if (this.tagEl) this.tagEl.textContent = tag;
  }

  /**
   * Transition Canvas UI State via state machine reducer
   * @param {"IDLE" | "LOADING" | "ERROR" | "SUCCESS"} state
   * @param {Object} [payload]
   */
  setState(state, payload = {}) {
    // 1. Dispatch action to state machine store
    switch (state) {
      case "IDLE":
        this.stateStore.dispatch({ type: "SET_IDLE" });
        break;
      case "LOADING":
        this.stateStore.dispatch({
          type: "START_LOADING",
          workflowId: payload.workflowId,
          loadingMessage: payload.loadingMessages?.[0]
        });
        break;
      case "ERROR":
        this.stateStore.dispatch({
          type: "SET_ERROR",
          title: payload.title,
          message: payload.message
        });
        break;
      case "SUCCESS":
        this.stateStore.dispatch({
          type: "SET_SUCCESS",
          markdown: payload.markdown
        });
        break;
    }

    // 2. Reflect state changes in DOM
    this.idleState.hide();
    this.loadingSkeleton.hide();
    this.errorBanner.hide();
    if (this.reportContainer) {
      this.reportContainer.style.display = "none";
    }

    switch (state) {
      case "IDLE":
        this.idleState.show();
        if (this.copyBtn) this.copyBtn.disabled = true;
        this.setHeaderInfo("Executive Reading Canvas", "Ready");
        break;

      case "LOADING":
        if (this.copyBtn) this.copyBtn.disabled = true;
        this.loadingSkeleton.show(payload.loadingMessages);
        break;

      case "ERROR":
        if (this.copyBtn) this.copyBtn.disabled = true;
        this.errorBanner.show({
          title: payload.title,
          message: payload.message,
          errorType: payload.errorType
        });
        break;

      case "SUCCESS":
        if (this.copyBtn) this.copyBtn.disabled = false;
        if (this.reportContainer) {
          this.reportContainer.style.display = "block";
          const rawMarkdown = payload.markdown || "";
          const renderedHtml = renderMarkdown(rawMarkdown);
          this.reportContainer.innerHTML = renderedHtml;
        }
        break;
    }
  }

  /**
   * Flash copy button with checkmark feedback
   */
  setCopySuccess() {
    if (!this.copyBtnText || !this.copyBtn) return;
    const prevText = this.copyBtnText.textContent;
    this.copyBtnText.textContent = "✓ Copied for Slides!";
    this.copyBtn.classList.add("copied");

    setTimeout(() => {
      this.copyBtnText.textContent = prevText || "Copy to Clipboard";
      this.copyBtn.classList.remove("copied");
    }, 2500);
  }

  /**
   * Get current state snapshot
   * @returns {import('../state/canvasState.js').CanvasState}
   */
  getState() {
    return this.stateStore.getState();
  }
}
