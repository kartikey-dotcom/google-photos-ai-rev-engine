/**
 * Pure JavaScript Markdown to HTML AST Renderer
 * Designed for Google Photos VoC Intelligence Engine.
 * Formats executive headers, quotes, numbered friction scores, and responsive tables.
 * Implements EC-12 (broken table tolerance with column padding) and EC-19 (XSS entity escaping).
 */

/**
 * Escapes unsafe HTML characters to prevent XSS (EC-19)
 * @param {string} str
 * @returns {string}
 */
export function escapeHtml(str) {
  if (!str) return "";
  return str
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

/**
 * Formats inline typography: bold, italic, code
 * @param {string} text
 * @returns {string}
 */
export function formatInline(text) {
  if (!text) return "";

  // 1. Sanitize HTML tags first (EC-19)
  let res = escapeHtml(text);

  // 2. Inline code
  res = res.replace(/`([^`]+)`/g, "<code>$1</code>");

  // 3. Bold
  res = res.replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>");

  // 4. Italic
  res = res.replace(/\*([^*]+)\*/g, "<em>$1</em>");

  return res;
}

/**
 * Parses markdown text into semantic, safe HTML markup
 * @param {string} markdown
 * @returns {string}
 */
export function renderMarkdown(markdown) {
  if (!markdown) return "";

  const lines = markdown.split(/\r?\n/);
  let html = "";
  let inList = false;
  let listType = ""; // "ul" or "ol"
  let inTable = false;
  let tableHeaderCols = 0;
  let inBlockquote = false;
  let blockquoteContent = [];

  function flushBlockquote() {
    if (inBlockquote) {
      html += `<blockquote>${blockquoteContent.join("<br>")}</blockquote>`;
      inBlockquote = false;
      blockquoteContent = [];
    }
  }

  function flushList() {
    if (inList) {
      html += `</${listType}>`;
      inList = false;
      listType = "";
    }
  }

  function flushTable() {
    if (inTable) {
      html += `</tbody></table>`;
      inTable = false;
      tableHeaderCols = 0;
    }
  }

  for (let i = 0; i < lines.length; i++) {
    const rawLine = lines[i];
    const trimmed = rawLine.trim();

    // 1. Check Table Row (detect pipe separated content, with or without outer pipes)
    const isTableRow = (trimmed.startsWith("|") || trimmed.includes(" | ")) && trimmed.includes("|");
    
    if (isTableRow) {
      flushList();
      flushBlockquote();

      // Normalize row: strip outer pipes if present, split by '|'
      let cleanRow = trimmed;
      if (cleanRow.startsWith("|")) cleanRow = cleanRow.substring(1);
      if (cleanRow.endsWith("|")) cleanRow = cleanRow.slice(0, -1);

      const cells = cleanRow.split("|").map(c => c.trim());

      // Check if separator line (e.g. |---|:---|---:|)
      const isSeparator = cells.length > 0 && cells.every(c => /^:?-+:?$/.test(c));

      if (isSeparator) {
        // Table header separator found, skip rendering as content row
        continue;
      }

      if (!inTable) {
        inTable = true;
        tableHeaderCols = cells.length;
        html += `<table><thead><tr>`;
        for (const cell of cells) {
          html += `<th>${formatInline(cell)}</th>`;
        }
        html += `</tr></thead><tbody>`;
        continue;
      } else {
        html += `<tr>`;
        // Handle uneven column counts by auto-padding with empty cells (EC-12)
        const totalCols = Math.max(tableHeaderCols, cells.length);
        for (let colIdx = 0; colIdx < totalCols; colIdx++) {
          const cellVal = colIdx < cells.length ? cells[colIdx] : "";
          html += `<td>${formatInline(cellVal)}</td>`;
        }
        html += `</tr>`;
        continue;
      }
    } else {
      flushTable();
    }

    // 2. Check Horizontal Rule
    if (/^(\*{3,}|-{3,}|_{3,})$/.test(trimmed)) {
      flushList();
      flushBlockquote();
      html += `<hr>`;
      continue;
    }

    // 3. Check Headers
    if (trimmed.startsWith("### ")) {
      flushList();
      flushBlockquote();
      html += `<h3>${formatInline(trimmed.substring(4))}</h3>`;
      continue;
    }
    if (trimmed.startsWith("## ")) {
      flushList();
      flushBlockquote();
      html += `<h2>${formatInline(trimmed.substring(3))}</h2>`;
      continue;
    }
    if (trimmed.startsWith("# ")) {
      flushList();
      flushBlockquote();
      html += `<h1>${formatInline(trimmed.substring(2))}</h1>`;
      continue;
    }

    // 4. Check Blockquote
    if (trimmed.startsWith(">")) {
      flushList();
      inBlockquote = true;
      blockquoteContent.push(formatInline(trimmed.replace(/^>\s*/, "")));
      continue;
    } else {
      flushBlockquote();
    }

    // 5. Check Unordered List
    if (/^[-*]\s+/.test(trimmed)) {
      if (!inList || listType !== "ul") {
        flushList();
        inList = true;
        listType = "ul";
        html += `<ul>`;
      }
      const itemContent = trimmed.replace(/^[-*]\s+/, "");
      html += `<li>${formatInline(itemContent)}</li>`;
      continue;
    }

    // 6. Check Ordered List
    const olMatch = trimmed.match(/^(\d+)\.\s+(.*)$/);
    if (olMatch) {
      if (!inList || listType !== "ol") {
        flushList();
        inList = true;
        listType = "ol";
        html += `<ol>`;
      }
      html += `<li>${formatInline(olMatch[2])}</li>`;
      continue;
    }

    // Close any open lists
    flushList();

    // 7. Empty line
    if (!trimmed) {
      continue;
    }

    // 8. Standard Paragraph
    html += `<p>${formatInline(trimmed)}</p>`;
  }

  flushList();
  flushBlockquote();
  flushTable();

  return html;
}

/**
 * Class wrapper for modularity
 */
export class MarkdownRenderer {
  static render(markdown) {
    return renderMarkdown(markdown);
  }
}
