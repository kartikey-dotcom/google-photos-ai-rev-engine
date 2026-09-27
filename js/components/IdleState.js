/**
 * Idle State Screen Component
 * Manages the default welcoming canvas view with Google Photos pinwheel,
 * problem overview, and 3-step setup instructions.
 */
export class IdleStateComponent {
  /**
   * @param {HTMLElement} containerElement
   */
  constructor(containerElement) {
    this.container = containerElement || document.getElementById("idleStateContainer");
  }

  show() {
    if (this.container) {
      this.container.style.display = "flex";
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
