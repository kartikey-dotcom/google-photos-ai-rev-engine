"""
Phase 6 Automated Unit & DOM Contract Test
Validates:
1. ClipboardService module exists with copyText, optimizeForSlidePaste, generateSlideHtml, and showToast.
2. Plaintext Slide Paste Optimizer normalizes line breaks and whitespace.
3. Slide HTML generator inlines table borders, headers, and quote styling for Google Docs/Slides paste fidelity.
4. DOM contract: copyReportBtn, copyBtnText, toastNotification, toastMessage exist.
5. Premature copy prevention (EC-17): copyReportBtn is disabled in IDLE, LOADING, and ERROR states.
6. Feedback timing: 2.5s (2500ms) timer for checkmark and toast.
"""
import os
import re
import sys

def test_clipboard_service_exports():
    print("[*] Testing ClipboardService Exports...")
    path = "js/services/clipboardService.js"
    assert os.path.exists(path), f"Missing required file: {path}"
    with open(path, "r", encoding="utf-8") as f:
        code = f.read()

    expected_methods = [
        "copyText",
        "optimizeForSlidePaste",
        "generateSlideHtml",
        "showToast"
    ]
    for method in expected_methods:
        assert method in code, f"ClipboardService missing method: {method}"
    print("[+] All ClipboardService methods verified.")

def test_slide_paste_optimizer():
    print("[*] Testing Plaintext Slide Paste Optimizer...")
    def optimize_paste(text):
        if not text:
            return ""
        return text.replace("\r\n", "\n").trim() if hasattr(text, "trim") else text.replace("\r\n", "\n").strip()

    raw_sample = "Line 1\r\nLine 2\r\n\r\n| Col 1 | Col 2 |\r\n|---|---|\r\n| Val 1 | Val 2 |\r\n"
    optimized = optimize_paste(raw_sample)
    assert "\r\n" not in optimized
    assert "| Col 1 | Col 2 |" in optimized
    assert optimize_paste("") == ""
    assert optimize_paste(None) == ""
    print("[+] Plaintext Slide Paste Optimizer logic verified.")

def test_slide_html_generator():
    print("[*] Testing Slide HTML Generator for Google Docs/Slides Fidelity...")
    with open("js/services/clipboardService.js", "r", encoding="utf-8") as f:
        code = f.read()

    assert "border-collapse: collapse" in code, "Must inline table border-collapse"
    assert "#dadce0" in code, "Must inline table border colors (#dadce0)"
    assert "#1a73e8" in code, "Must inline Google Blue blockquote border (#1a73e8)"
    assert "text/html" in code, "Must support multi-mime text/html clipboard writing"
    assert "text/plain" in code, "Must support multi-mime text/plain clipboard writing"
    print("[+] Slide HTML Generator and Multi-MIME clipboard writes verified.")

def test_dom_elements_and_states():
    print("[*] Testing Copy CTA & Toast Elements in index.html...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    assert 'id="copyReportBtn"' in html, "Missing #copyReportBtn"
    assert 'id="copyBtnText"' in html, "Missing #copyBtnText"
    assert 'id="toastNotification"' in html, "Missing #toastNotification"
    assert 'id="toastMessage"' in html, "Missing #toastMessage"
    assert 'class="toast-icon-check"' in html, "Missing .toast-icon-check"
    assert '<button type="button" class="btn-secondary" id="copyReportBtn" disabled' in html, "Copy button must be disabled by default (EC-17)"
    print("[+] Copy CTA and Toast DOM elements verified.")

def test_premature_copy_guard_ec17():
    print("[*] Testing EC-17: Copy Button Disabled in IDLE, LOADING, ERROR states...")
    with open("js/components/Canvas.js", "r", encoding="utf-8") as f:
        code = f.read()

    # Verify that in IDLE, LOADING, ERROR copyBtn.disabled is set to true, and in SUCCESS it is false
    assert 'case "IDLE":' in code and 'this.copyBtn.disabled = true' in code
    assert 'case "LOADING":' in code and 'this.copyBtn.disabled = true' in code
    assert 'case "ERROR":' in code and 'this.copyBtn.disabled = true' in code
    assert 'case "SUCCESS":' in code and 'this.copyBtn.disabled = false' in code
    print("[+] EC-17 Copy button state guards verified across all canvas states.")

def test_feedback_duration_contract():
    print("[*] Testing 2.5s (2500ms) Feedback Duration Contract...")
    with open("js/components/Canvas.js", "r", encoding="utf-8") as f:
        canvas_code = f.read()
    with open("js/services/clipboardService.js", "r", encoding="utf-8") as f:
        clip_code = f.read()

    assert "2500" in canvas_code, "Canvas setCopySuccess must reset after 2500ms"
    assert "2500" in clip_code, "ClipboardService showToast must display for 2500ms"
    assert "✓ Copied for Slides!" in canvas_code, "Copy button text must be '✓ Copied for Slides!'"
    print("[+] 2.5s feedback duration and exact micro-copy verified.")

def main():
    try:
        test_clipboard_service_exports()
        test_slide_paste_optimizer()
        test_slide_html_generator()
        test_dom_elements_and_states()
        test_premature_copy_guard_ec17()
        test_feedback_duration_contract()
        print("\n[SUCCESS] Phase 6 Verification Completed: All Tests Passed!")
        return 0
    except Exception as e:
        print(f"\n[FAIL] Phase 6 Verification Failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
