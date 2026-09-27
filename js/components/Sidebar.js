import { ApiKeyCardComponent } from './ApiKeyCard.js';
import { SourceSelectorComponent } from './SourceSelector.js';
import { WorkflowButtonsComponent } from './WorkflowButtons.js';

/**
 * Composite Left Sidebar Component
 * Coordinates ApiKeyCard, SourceSelector, and WorkflowButtons sub-components.
 */
export class SidebarComponent {
  /**
   * @param {Object} options
   * @param {Function} options.onKeyChange
   * @param {Function} options.onSourceChange
   * @param {Function} options.onWorkflowTrigger
   */
  constructor({ onKeyChange, onSourceChange, onWorkflowTrigger }) {
    this.apiKeyCard = new ApiKeyCardComponent({ onKeyChange });
    this.sourceSelector = new SourceSelectorComponent({ onSourceChange });
    this.workflowButtons = new WorkflowButtonsComponent({ onWorkflowTrigger });
  }

  updateCorpusCount(activeCount, totalCount) {
    this.sourceSelector.updateCountDisplay(activeCount, totalCount);
  }

  setActiveWorkflow(workflowId) {
    this.workflowButtons.setActive(workflowId);
  }

  setButtonsDisabled(disabled) {
    this.workflowButtons.setDisabled(disabled);
  }

  focusKeyInput() {
    this.apiKeyCard.focus();
  }

  getActiveFilters() {
    return this.sourceSelector.getFilters();
  }
}
