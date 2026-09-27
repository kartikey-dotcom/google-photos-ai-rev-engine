/**
 * Clipboard & Export Service
 * Provides PM-friendly export workflows allowing instant copying of formatted reports
 * into Google Slides, Docs, and PRD documents.
 * 
 * Features:
 * - Multi-format clipboard writing: text/plain (Markdown) + text/html (inline styled)
 * - Plaintext Slide Paste Optimizer for clean table & quote alignment in slide frames (EC-16)
 * - Fallback to textarea + document.execCommand('copy') for compatibility
 * - Toast notification feedback with Google Green checkmark icon
 */
export class ClipboardService {
  /**
   * Optimizes Markdown text specifically for slide notes and plaintext paste
   * @param {string} markdown
   * @returns {string}
   */
  static optimizeForSlidePaste(markdown) {
    if (!markdown) return "";
    return markdown
      .replace(/\r\n/g, "\n")
      .trim();
  }

  /**
   * Generates inline-styled HTML optimized for direct pasting into Google Slides & Docs
   * @param {string} rawHtml
   * @returns {string}
   */
  static generateSlideHtml(rawHtml) {
    if (!rawHtml) return "";
    let styled = rawHtml;
    // Inline styling ensures table borders and quote styling persist across Google Docs & Slides
    styled = styled.replace(/<table>/g, '<table style="border-collapse: collapse; width: 100%; margin: 16px 0; font-family: Roboto, Arial, sans-serif; font-size: 13px;">');
    styled = styled.replace(/<th>/g, '<th style="border: 1px solid #dadce0; background-color: #f1f3f4; padding: 8px 12px; font-weight: bold; text-align: left;">');
    styled = styled.replace(/<td>/g, '<td style="border: 1px solid #dadce0; padding: 8px 12px; text-align: left; vertical-align: top;">');
    styled = styled.replace(/<blockquote>/g, '<blockquote style="border-left: 4px solid #1a73e8; background-color: #f8f9fa; margin: 12px 0; padding: 10px 16px; font-style: italic; color: #3c4043;">');
    styled = styled.replace(/<h3>/g, '<h3 style="font-family: Arial, sans-serif; font-size: 16px; font-weight: bold; color: #1a0dab; margin: 18px 0 8px 0;">');
    styled = styled.replace(/<h2>/g, '<h2 style="font-family: Arial, sans-serif; font-size: 18px; font-weight: bold; color: #202124; margin: 24px 0 10px 0; border-bottom: 1px solid #dadce0; padding-bottom: 6px;">');
    styled = styled.replace(/<h1>/g, '<h1 style="font-family: Arial, sans-serif; font-size: 22px; font-weight: bold; color: #202124; margin: 24px 0 12px 0;">');
    return styled;
  }

  /**
   * Copy both text/plain (Markdown) and text/html (Inline-styled) to system clipboard
   * @param {string} text - Raw Markdown report
   * @param {string} [html] - Rendered HTML content
   * @returns {Promise<boolean>}
   */
  static async copyText(text, html = "") {
    if (!text) return false;

    const optimizedPlain = this.optimizeForSlidePaste(text);
    const styledHtml = html ? this.generateSlideHtml(html) : "";

    // 1. Modern Async Clipboard API with multi-mime support
    if (navigator.clipboard && window.isSecureContext) {
      try {
        if (styledHtml && typeof window.ClipboardItem !== "undefined") {
          const textBlob = new Blob([optimizedPlain], { type: "text/plain" });
          const htmlBlob = new Blob([styledHtml], { type: "text/html" });
          await navigator.clipboard.write([
            new ClipboardItem({
              "text/plain": textBlob,
              "text/html": htmlBlob
            })
          ]);
          return true;
        } else {
          await navigator.clipboard.writeText(optimizedPlain);
          return true;
        }
      } catch (err) {
        console.warn("Async multi-mime clipboard write failed, attempting writeText fallback:", err);
        try {
          await navigator.clipboard.writeText(optimizedPlain);
          return true;
        } catch (writeTextErr) {
          console.warn("writeText also failed, falling back to execCommand:", writeTextErr);
        }
      }
    }

    // 2. Fallback using hidden textarea and execCommand (EC-16)
    try {
      const textarea = document.createElement("textarea");
      textarea.value = optimizedPlain;
      textarea.style.position = "fixed";
      textarea.style.left = "-9999px";
      textarea.style.top = "-9999px";
      textarea.setAttribute("readonly", "");
      document.body.appendChild(textarea);
      textarea.focus();
      textarea.select();
      const successful = document.execCommand("copy");
      document.body.removeChild(textarea);
      return successful;
    } catch (fallbackErr) {
      console.error("Fallback clipboard copy failed:", fallbackErr);
      return false;
    }
  }

  /**
   * Display toast notification with checkmark feedback
   * @param {string} message
   * @param {number} [durationMs=2500]
   */
  static showToast(message, durationMs = 2500) {
    const toast = document.getElementById("toastNotification");
    const toastMessage = document.getElementById("toastMessage");
    if (!toast || !toastMessage) return;

    toastMessage.textContent = message;
    toast.classList.add("show");

    setTimeout(() => {
      toast.classList.remove("show");
    }, durationMs);
  }
}
