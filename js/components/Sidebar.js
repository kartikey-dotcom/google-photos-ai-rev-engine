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
   * @param {Function} options.onPipelineRun
   */
  constructor({ onKeyChange, onSourceChange, onWorkflowTrigger, onPipelineRun }) {
    this.apiKeyCard = new ApiKeyCardComponent({ onKeyChange });
    this.sourceSelector = new SourceSelectorComponent({ onSourceChange });
    this.workflowButtons = new WorkflowButtonsComponent({ onWorkflowTrigger });

    const pipelineBtn = document.getElementById('runPipelineBtn');
    if (pipelineBtn && onPipelineRun) {
      pipelineBtn.addEventListener('click', () => {
        onPipelineRun();
      });
    }
    this.pipelineBtn = pipelineBtn;
  }

  updateCorpusCount(activeCount, totalCount) {
    this.sourceSelector.updateCountDisplay(activeCount, totalCount);
  }

  setActiveWorkflow(workflowId) {
    this.workflowButtons.setActive(workflowId);
  }

  setButtonsDisabled(disabled) {
    this.workflowButtons.setDisabled(disabled);
    if (this.pipelineBtn) {
      this.pipelineBtn.disabled = disabled;
    }
  }

  focusKeyInput() {
    this.apiKeyCard.focus();
  }

  getActiveFilters() {
    return this.sourceSelector.getFilters();
  }
}
