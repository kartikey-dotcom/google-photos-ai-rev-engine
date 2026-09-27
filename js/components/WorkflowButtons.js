/**
 * Workflow Action Buttons Component
 * Coordinates the 4 deterministic analytical triggers, active highlights, and disabled states.
 */
export class WorkflowButtonsComponent {
  /**
   * @param {Object} options
   * @param {Function} options.onWorkflowTrigger - Callback when a workflow button is clicked
   */
  constructor({ onWorkflowTrigger }) {
    this.onWorkflowTrigger = onWorkflowTrigger;
    this.buttons = document.querySelectorAll(".workflow-btn");
    this.activeWorkflowId = null;

    this.bindEvents();
  }

  bindEvents() {
    this.buttons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const workflowId = btn.getAttribute("data-workflow");
        this.setActive(workflowId);
        this.onWorkflowTrigger(workflowId);
      });
    });
  }

  /**
   * Highlight the active workflow button
   * @param {string} workflowId
   */
  setActive(workflowId) {
    this.activeWorkflowId = workflowId;
    this.buttons.forEach((btn) => {
      const match = btn.getAttribute("data-workflow") === workflowId;
      btn.classList.toggle("active", match);
    });
  }

  /**
   * Disable/enable buttons during async inference
   * @param {boolean} disabled
   */
  setDisabled(disabled) {
    this.buttons.forEach((btn) => {
      btn.disabled = disabled;
    });
  }

  getActiveWorkflowId() {
    return this.activeWorkflowId;
  }
}
