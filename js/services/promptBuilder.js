import { corpusStore } from '../data/corpusStore.js';
import { WORKFLOWS } from '../config/constants.js';

/**
 * Multi-Shot Prompt Assembler
 * Injects structured system instructions and serialized VoC corpus JSON.
 * @param {string | object} workflow - Workflow ID (string) or Workflow Config (object)
 * @param {Array<object>} corpusRecords - Array of UserFeedbackRecord objects
 * @returns {string} Fully assembled multi-shot prompt string
 */
export function buildWorkflowPrompt(workflow, corpusRecords) {
  const workflowConfig = typeof workflow === "string" ? WORKFLOWS[workflow] : workflow;

  if (!workflowConfig || !workflowConfig.systemPrompt) {
    throw new Error(`Invalid workflow specified for prompt assembly: ${workflow}`);
  }

  const formattedCorpus = corpusStore.serializeRecords(corpusRecords, 2);

  return `${workflowConfig.systemPrompt}

INPUT DATASET (Simulated Voice-of-Customer Feedback Corpus):
${formattedCorpus}

REMINDER OF STRICT OUTPUT RULES:
- Adhere strictly to the requested markdown syntax, header hierarchy, tables, or numbered lists.
- Do not output preamble, pleasantries, or conclusions. Ground all quotes directly in the data above.`;
}
