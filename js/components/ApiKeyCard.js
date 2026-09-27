/**
 * API Key Configuration Card Component
 * Manages masked API key input, eye toggle visibility, status indicators, and EC-04 input sanitization.
 */
export class ApiKeyCardComponent {
  /**
   * @param {Object} options
   * @param {Function} options.onKeyChange - Callback when sanitized key changes
   */
  constructor({ onKeyChange }) {
    this.onKeyChange = onKeyChange;

    this.inputEl = document.getElementById("apiKeyInput");
    this.toggleBtn = document.getElementById("toggleKeyVisibilityBtn");
    this.statusContainer = document.getElementById("apiKeyStatus");
    this.statusText = document.getElementById("apiKeyStatusText");
    this.eyeIcon = document.getElementById("eyeIcon");

    this.bindEvents();
  }

  bindEvents() {
    this.tryLoadFromEnv();

    if (this.inputEl) {
      this.inputEl.addEventListener("input", (e) => {
        // Sanitize accidental surrounding quotes and whitespace (EC-04 from edge-case.md)
        const rawValue = e.target.value;
        const sanitizedKey = this.sanitizeKey(rawValue);

        this.updateStatus(sanitizedKey.length > 5);
        this.onKeyChange(sanitizedKey);
      });
    }

    if (this.toggleBtn) {
      this.toggleBtn.addEventListener("click", () => {
        this.toggleVisibility();
      });
    }
  }

  async tryLoadFromEnv() {
    // 1. Check for Streamlit injected key via TOML secrets
    if (window.STREAMLIT_INJECTED_KEY && window.STREAMLIT_INJECTED_KEY.length > 5) {
      if (this.inputEl) {
        this.inputEl.value = window.STREAMLIT_INJECTED_KEY;
        this.updateStatus(true);
        this.onKeyChange(window.STREAMLIT_INJECTED_KEY);
      }
      return;
    }

    // 2. Fallback to local .env fetch
    try {
      const resp = await fetch('.env');
      if (resp.ok) {
        const text = await resp.text();
        const match = text.match(/GEMINI_API_KEY\s*=\s*([^\r\n#]+)/);
        if (match && match[1]) {
          const key = this.sanitizeKey(match[1]);
          if (key && key.length > 5 && this.inputEl) {
            this.inputEl.value = key;
            this.updateStatus(true);
            this.onKeyChange(key);
          }
        }
      }
    } catch {
      // Ignore if not accessible or running on file:// protocol
    }
  }

  /**
   * Sanitizes pasted API keys (strips whitespace and enclosing single/double quotes)
   * @param {string} rawKey
   * @returns {string}
   */
  sanitizeKey(rawKey) {
    if (!rawKey) return "";
    return rawKey.trim().replace(/^["']+|["']+$/g, "").trim();
  }

  toggleVisibility() {
    if (!this.inputEl) return;
    const isPassword = this.inputEl.type === "password";
    this.inputEl.type = isPassword ? "text" : "password";
    this.toggleBtn.title = isPassword ? "Hide API key" : "Show API key";

    // Update SVG icon path for visual feedback
    if (this.eyeIcon) {
      if (isPassword) {
        // Eye-off icon
        this.eyeIcon.innerHTML = `
          <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
          <line x1="1" y1="1" x2="23" y2="23"></line>
        `;
      } else {
        // Normal eye icon
        this.eyeIcon.innerHTML = `
          <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
          <circle cx="12" cy="12" r="3"></circle>
        `;
      }
    }
  }

  updateStatus(isConfigured) {
    if (!this.statusContainer || !this.statusText) return;

    if (isConfigured) {
      this.statusContainer.classList.add("configured");
      this.statusText.textContent = "Key Configured (In-Memory Only)";
    } else {
      this.statusContainer.classList.remove("configured");
      this.statusText.textContent = "No Key Entered (Memory Only)";
    }
  }

  focus() {
    this.inputEl?.focus();
  }

  getKey() {
    return this.sanitizeKey(this.inputEl?.value || "");
  }
}
