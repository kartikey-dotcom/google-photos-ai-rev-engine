/**
 * Loading Skeleton Component
 * Renders pulsing shimmer skeleton cards and orchestrates micro-copy rotator
 * every 2.5s to maintain transparent progress during LLM inference.
 */
export class LoadingSkeletonComponent {
  /**
   * @param {HTMLElement} containerElement
   */
  constructor(containerElement) {
    this.container = containerElement || document.getElementById("loadingStateContainer");
    this.statusTextEl = document.getElementById("loadingStatusText");
    this.timer = null;
    this.defaultMessages = [
      "Connecting to Gemini 1.5 Analytical Engine...",
      "Synthesizing unstructured user complaints...",
      "Extracting episodic memory failure patterns...",
      "Enforcing strict PM deliverable syntax..."
    ];
    this.activeMessages = [...this.defaultMessages];
    this.currentIndex = 0;
  }

  /**
   * Display pulsing skeleton and start 2.5s micro-copy rotation
   * @param {string[]} [messages]
   */
  show(messages) {
    if (this.container) {
      this.container.style.display = "flex";
    }

    if (Array.isArray(messages) && messages.length > 0) {
      this.activeMessages = messages;
    } else {
      this.activeMessages = [...this.defaultMessages];
    }

    this.currentIndex = 0;
    if (this.statusTextEl) {
      this.statusTextEl.textContent = this.activeMessages[0];
    }

    this.clearTimer();

    // 2.5-second micro-copy rotator interval as specified in Phase 5.3
    this.timer = setInterval(() => {
      this.currentIndex = (this.currentIndex + 1) % this.activeMessages.length;
      if (this.statusTextEl) {
        this.statusTextEl.textContent = this.activeMessages[this.currentIndex];
      }
    }, 2500);
  }

  hide() {
    this.clearTimer();
    if (this.container) {
      this.container.style.display = "none";
    }
  }

  clearTimer() {
    if (this.timer) {
      clearInterval(this.timer);
      this.timer = null;
    }
  }

  getCurrentMessage() {
    return this.activeMessages[this.currentIndex] || "";
  }

  isVisible() {
    return this.container && this.container.style.display !== "none";
  }
}
