/**
 * Header Component for Google Photos Discovery Engine
 */
export class HeaderComponent {
  /**
   * Initialize header status and badges
   * @param {HTMLElement} headerElement
   */
  constructor(headerElement) {
    this.element = headerElement;
    this.modelNameEl = document.getElementById("modelName");
  }

  /**
   * Update active model display badge
   * @param {string} modelName
   * @param {number} temperature
   */
  setModelInfo(modelName, temperature = 0.2) {
    if (this.modelNameEl) {
      this.modelNameEl.textContent = `${modelName} (Temp: ${temperature})`;
    }
  }
}
