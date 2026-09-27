/**
 * Canvas State Machine & Reducer
 * Manages the reactive lifecycle of the Executive Reading Canvas:
 * IDLE -> LOADING -> ERROR / SUCCESS
 */

/**
 * @typedef {"IDLE" | "LOADING" | "ERROR" | "SUCCESS"} CanvasStatus
 * 
 * @typedef {Object} CanvasState
 * @property {CanvasStatus} status - Active UI status
 * @property {string | null} activeWorkflow - Currently selected workflow ID
 * @property {string} loadingMessage - Current micro-copy message during synthesis
 * @property {string | null} errorTitle - Error banner headline
 * @property {string | null} errorMessage - Error diagnostic explanation
 * @property {string} markdownContent - Rendered markdown report output
 */

/** @type {CanvasState} */
export const initialCanvasState = {
  status: "IDLE",
  activeWorkflow: null,
  loadingMessage: "",
  errorTitle: null,
  errorMessage: null,
  markdownContent: ""
};

/**
 * Pure state machine reducer for canvas transitions
 * @param {CanvasState} state
 * @param {Object} action
 * @returns {CanvasState}
 */
export function canvasStateReducer(state, action) {
  switch (action.type) {
    case "SET_IDLE":
      return {
        ...initialCanvasState
      };

    case "START_LOADING":
      return {
        ...state,
        status: "LOADING",
        activeWorkflow: action.workflowId || state.activeWorkflow,
        loadingMessage: action.loadingMessage || "Connecting to Gemini 1.5 Analytical Engine...",
        errorTitle: null,
        errorMessage: null,
        markdownContent: ""
      };

    case "UPDATE_LOADING_MESSAGE":
      return {
        ...state,
        loadingMessage: action.loadingMessage
      };

    case "SET_ERROR":
      return {
        ...state,
        status: "ERROR",
        errorTitle: action.title || "Analytical Pipeline Error",
        errorMessage: action.message || "An unexpected error occurred during analytical synthesis.",
        markdownContent: ""
      };

    case "SET_SUCCESS":
      return {
        ...state,
        status: "SUCCESS",
        markdownContent: action.markdown || "",
        errorTitle: null,
        errorMessage: null
      };

    default:
      return state;
  }
}

/**
 * Observable Canvas State Store
 */
export class CanvasStateStore {
  constructor(initialState = initialCanvasState) {
    this.state = { ...initialState };
    this.listeners = new Set();
  }

  getState() {
    return { ...this.state };
  }

  dispatch(action) {
    const prevState = this.state;
    this.state = canvasStateReducer(this.state, action);
    this.notify(prevState);
  }

  subscribe(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  notify(prevState) {
    for (const listener of this.listeners) {
      listener(this.state, prevState);
    }
  }
}
