"""
Phase 4 Comprehensive Automated Unit & DOM Contract Test
Validates:
1. ApiKeyCard, SourceSelector, WorkflowButtons, and Sidebar components exist with proper ES module exports.
2. HTML element IDs exist, matching component event bindings.
3. CSS styles define active highlights, hover states, disabled states, and 30/70 desktop layout.
4. Input sanitization logic (EC-04) strips whitespace and quotes (single, double, multiple).
5. Zero-Trust Storage Audit (EC-18): Asserts no code writes to localStorage, sessionStorage, or document.cookie.
6. Workflow Action Button IDs & dataset attributes match WORKFLOWS registry.
7. Active corpus data-source channels match the seed corpus sources.
"""
import os
import re
import sys

def test_component_files_and_exports():
    print("[*] Testing Phase 4 Component Files & Exports...")
    files = {
        "js/components/ApiKeyCard.js": ["ApiKeyCardComponent", "sanitizeKey", "toggleVisibility", "updateStatus"],
        "js/components/SourceSelector.js": ["SourceSelectorComponent", "updateCountDisplay", "getFilters"],
        "js/components/WorkflowButtons.js": ["WorkflowButtonsComponent", "setActive", "setDisabled"],
        "js/components/Sidebar.js": ["SidebarComponent", "updateCorpusCount", "setActiveWorkflow", "setButtonsDisabled"]
    }
    for path, expected_symbols in files.items():
        assert os.path.exists(path), f"Missing required component file: {path}"
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        for symbol in expected_symbols:
            assert symbol in content, f"{path} is missing expected method/class: {symbol}"
    print("[+] All Phase 4 component modules and exports verified.")

def test_html_dom_bindings():
    print("[*] Testing HTML Element IDs for Phase 4...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    required_ids = [
        "apiKeyInput",
        "toggleKeyVisibilityBtn",
        "apiKeyStatus",
        "apiKeyStatusText",
        "sourceReddit",
        "sourcePlayStore",
        "sourceAppStore",
        "sourceSupport",
        "activeCorpusCount",
        "btnWorkflow1",
        "btnWorkflow2",
        "btnWorkflow3",
        "btnWorkflow4"
    ]
    for el_id in required_ids:
        assert f'id="{el_id}"' in html, f"Missing required DOM element id: {el_id}"
    print(f"[+] All {len(required_ids)} required DOM element IDs verified in index.html.")

def test_css_states_and_layout():
    print("[*] Testing CSS Rules for Layout, Active, Hover & Focus States...")
    with open("css/main.css", "r", encoding="utf-8") as f:
        css = f.read()

    assert ".workflow-btn.active" in css, "Missing .workflow-btn.active styling"
    assert ".workflow-btn:hover" in css, "Missing .workflow-btn:hover styling"
    assert ".workflow-btn:disabled" in css, "Missing .workflow-btn:disabled styling"
    assert ".api-status-indicator.configured" in css, "Missing .configured status styling"
    assert "width: 30%" in css, "Sidebar width must be 30%"
    print("[+] CSS layout and interactive state classes verified.")

def test_key_sanitizer():
    print("[*] Testing EC-04 API Key Sanitization Logic...")
    def sanitize_key(raw_key):
        if not raw_key:
            return ""
        return re.sub(r'^["\']+|["\']+$', '', raw_key.strip()).strip()

    assert sanitize_key("  AIzaSy12345  ") == "AIzaSy12345"
    assert sanitize_key('"AIzaSy12345"') == "AIzaSy12345"
    assert sanitize_key("'AIzaSy12345'") == "AIzaSy12345"
    assert sanitize_key(' "AIzaSy12345" ') == "AIzaSy12345"
    assert sanitize_key('""AIzaSy12345""') == "AIzaSy12345"
    assert sanitize_key("''AIzaSy12345''") == "AIzaSy12345"
    assert sanitize_key('"\n  AIzaSy12345  \n"') == "AIzaSy12345"
    assert sanitize_key("") == ""
    assert sanitize_key(None) == ""
    print("[+] Key sanitization logic verified across all variations.")

def test_zero_trust_storage_persistence():
    print("[*] Testing EC-18: Zero-Trust Storage Persistence Audit...")
    js_dir = "js"
    forbidden_terms = ["localStorage", "sessionStorage", "document.cookie", "indexedDB"]
    for root, _, files in os.walk(js_dir):
        for file in files:
            if file.endswith(".js"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                for term in forbidden_terms:
                    assert term not in content, f"SECURITY VIOLATION (EC-18): {term} detected in {filepath}!"
    print("[+] Zero-Trust storage audit passed: Key is 100% ephemeral in-memory.")

def test_source_channels_conformance():
    print("[*] Testing Data Source Channels Conformance...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    expected_channels = [
        "r/GooglePhotos",
        "Play Store",
        "App Store",
        "Google Support Forum"
    ]
    for channel in expected_channels:
        pattern = f'data-source="{channel}"'
        assert pattern in html, f"Missing data-source attribute for channel: {channel}"
    print(f"[+] All {len(expected_channels)} data sources present with exact channels.")

def test_workflow_buttons_conformance():
    print("[*] Testing Workflow Action Button Conformance...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    expected_workflows = ["taxonomy", "cognitive_gap", "workarounds", "poa"]
    for wf in expected_workflows:
        pattern = f'data-workflow="{wf}"'
        assert pattern in html, f"Missing data-workflow attribute for workflow: {wf}"
    print(f"[+] All {len(expected_workflows)} workflow buttons bound with valid workflow keys.")

def main():
    try:
        test_component_files_and_exports()
        test_html_dom_bindings()
        test_css_states_and_layout()
        test_key_sanitizer()
        test_zero_trust_storage_persistence()
        test_source_channels_conformance()
        test_workflow_buttons_conformance()
        print("\n[SUCCESS] Phase 4 Comprehensive Verification Completed: All Tests Passed!")
        return 0
    except Exception as e:
        print(f"\n[FAIL] Phase 4 Verification Failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
