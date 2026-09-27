/**
 * Data Source Selector Component
 * Manages channel checkbox toggles, dynamic count recalculation, and source filters.
 */
export class SourceSelectorComponent {
  /**
   * @param {Object} options
   * @param {Function} options.onSourceChange - Callback when a source checkbox is toggled
   */
  constructor({ onSourceChange }) {
    this.onSourceChange = onSourceChange;

    this.checkboxes = document.querySelectorAll(".source-checkbox");
    this.countBadge = document.getElementById("activeCorpusCount");

    this.filters = {
      "r/GooglePhotos": true,
      "Play Store": true,
      "App Store": true,
      "Google Support Forum": true
    };

    this.bindEvents();
  }

  bindEvents() {
    this.checkboxes.forEach((cb) => {
      // Initialize state from DOM
      const sourceName = cb.getAttribute("data-source");
      if (sourceName) {
        this.filters[sourceName] = cb.checked;
      }

      cb.addEventListener("change", (e) => {
        const source = e.target.getAttribute("data-source");
        const isChecked = e.target.checked;
        this.filters[source] = isChecked;
        this.onSourceChange(source, isChecked);
      });
    });
  }

  /**
   * Update active corpus count indicator
   * @param {number} activeCount
   * @param {number} totalCount
   */
  updateCountDisplay(activeCount, totalCount) {
    if (this.countBadge) {
      this.countBadge.textContent = `${activeCount} of ${totalCount} Records`;
      if (activeCount === 0) {
        this.countBadge.style.color = "var(--error-text)";
      } else {
        this.countBadge.style.color = "var(--text-secondary)";
      }
    }
  }

  /**
   * Returns current boolean filter map
   * @returns {Record<string, boolean>}
   */
  getFilters() {
    return { ...this.filters };
  }
}
