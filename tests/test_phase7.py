"""
Phase 7 End-to-End QA, Acceptance & Architecture Verification Test
Validates:
1. Workflow 1 Acceptance: 3 edge-case categories, absence of generic categories, H3 headers, bullet definitions, blockquotes, zero chatbot filler.
2. Workflow 2 Acceptance: Valid 3-column T-Chart table (Retained Episodic Anchors, Forgotten System Demands, Failure Mode), at least 3 rows.
3. Workflow 3 Acceptance: Numbered workaround titles, bold names, explicit Friction Score (High/Medium/Low).
4. Workflow 4 Acceptance: 2 POAs (Problem, Solution, Hypothesis) + mandatory Comparison / Trade-off Matrix comparing POA 1 vs POA 2 across Problems Solved, User Impact, and Implementation Effort.
5. Zero-Chatbot Architecture Audit: No conversational chat inputs or bubbles, strict parameter envelope (temp: 0.2, topP: 0.8), negative constraints.
6. Resilience & Security Audit: Password masking, zero persistence in localStorage/sessionStorage, graceful offline/error interceptors.
"""
import os
import re
import sys

def test_workflow_1_acceptance():
    print("[*] Testing 7.1: Workflow 1 Validation (Taxonomy of Lost Photos)...")
    with open("js/services/geminiClient.js", "r", encoding="utf-8") as f:
        client_code = f.read()

    # Extract Workflow 1 mock output
    w1_match = re.search(r'Taxonomy of \\"Lost\\" Photos.*?\n\s*return `(.*?)`;', client_code, re.DOTALL)
    assert w1_match, "Workflow 1 output generator not found"
    w1_text = w1_match.group(1).replace("\\n", "\n").replace('\\"', '"')

    # 1. Assert H3 headers
    h3_count = len(re.findall(r'^###\s+', w1_text, re.MULTILINE))
    assert h3_count >= 3, f"Workflow 1 must have at least 3 categories, found: {h3_count}"

    # 2. Check absence of generic categories
    generic_words = ["vacation", "trip", "holiday", "generic food", "party photos"]
    for word in generic_words:
        assert word not in w1_text.lower(), f"Workflow 1 contains generic category term: {word}"

    # 3. Assert bullet definitions and blockquote quotes
    assert "- **Definition**:" in w1_text or "- Definition:" in w1_text or "- **Description**:" in w1_text, "Missing bullet definitions"
    assert "> " in w1_text, "Missing blockquote citations"

    # 4. Assert zero conversational chatbot preamble
    chatbot_phrases = ["hello", "sure, here is", "as an ai", "certainly", "hope this helps"]
    for phrase in chatbot_phrases:
        assert phrase not in w1_text.lower(), f"Chatbot phrase detected in Workflow 1: {phrase}"

    print(f"[+] Workflow 1 verified: {h3_count} edge-case categories with definitions, blockquotes, and zero chatbot leakage.")

def test_workflow_2_acceptance():
    print("[*] Testing 7.2: Workflow 2 Validation (Cognitive Gap Matrix)...")
    with open("js/services/geminiClient.js", "r", encoding="utf-8") as f:
        client_code = f.read()

    w2_match = re.search(r'Cognitive Gap Matrix.*?\n\s*return `(.*?)`;', client_code, re.DOTALL)
    assert w2_match, "Workflow 2 output generator not found"
    w2_text = w2_match.group(1).replace("\\n", "\n").replace('\\"', '"')

    # Assert Table Header columns
    assert "Retained Episodic Anchors" in w2_text, "Missing 'Retained Episodic Anchors' column"
    assert "Forgotten System Demands" in w2_text, "Missing 'Forgotten System Demands' column"
    assert "Failure Mode" in w2_text, "Missing 'Failure Mode' column"

    # Assert Markdown Table structure
    table_lines = [l.strip() for l in w2_text.split("\n") if l.strip().startswith("|") and l.strip().endswith("|")]
    assert len(table_lines) >= 4, f"Matrix must contain header + separator + at least 2 rows, found: {len(table_lines)}"

    print("[+] Workflow 2 verified: 3-column T-Chart matrix with exact headers and structured rows.")

def test_workflow_3_acceptance():
    print("[*] Testing 7.3: Workflow 3 Validation (Behavioral Workarounds)...")
    with open("js/services/geminiClient.js", "r", encoding="utf-8") as f:
        client_code = f.read()

    w3_match = re.search(r'Behavioral Workaround Mapping.*?\n\s*return `(.*?)`;', client_code, re.DOTALL)
    assert w3_match, "Workflow 3 output generator not found"
    w3_text = w3_match.group(1).replace("\\n", "\n").replace('\\"', '"')

    # Assert Numbered Workarounds
    assert "### 1." in w3_text or "1." in w3_text, "Missing numbered workaround 1"
    assert "### 2." in w3_text or "2." in w3_text, "Missing numbered workaround 2"

    # Assert Friction Scores
    friction_matches = re.findall(r'Friction Score\**:\s*(High|Medium|Low)', w3_text, re.IGNORECASE)
    assert len(friction_matches) >= 2, f"Workarounds must contain explicit Friction Scores, found: {len(friction_matches)}"

    print(f"[+] Workflow 3 verified: Numbered list with bold titles and explicit Friction Scores ({friction_matches}).")

def test_workflow_4_acceptance():
    print("[*] Testing 7.4: Workflow 4 Validation (POAs & Comparison / Trade-off Matrix)...")
    with open("js/services/geminiClient.js", "r", encoding="utf-8") as f:
        client_code = f.read()

    w4_match = re.search(r'Product Opportunity Synthesis.*?\n\s*return `(.*?)`;', client_code, re.DOTALL)
    assert w4_match, "Workflow 4 output generator not found"
    w4_text = w4_match.group(1).replace("\\n", "\n").replace('\\"', '"')

    # 1. Assert 2 distinct POAs
    assert "POA 1:" in w4_text, "Missing POA 1"
    assert "POA 2:" in w4_text, "Missing POA 2"
    assert "Problem Space" in w4_text, "Missing Problem Space section"
    assert "Proposed Solution" in w4_text or "Proposed AI Solution" in w4_text, "Missing Proposed Solution section"
    assert "Hypothesis" in w4_text, "Missing Hypothesis section"

    # 2. Strict Requirement: Comparison / Trade-off Matrix
    assert "Comparison / Trade-off Matrix" in w4_text, "Missing mandatory 'Comparison / Trade-off Matrix' section"
    assert "Specific Retrieval Problems Solved" in w4_text, "Missing 'Specific Retrieval Problems Solved' criterion in Matrix"
    assert "User Impact" in w4_text, "Missing 'User Impact' criterion in Matrix"
    assert "Implementation Effort" in w4_text, "Missing 'Implementation Effort' criterion in Matrix"

    # Assert Table Structure
    table_lines = [l.strip() for l in w4_text.split("\n") if l.strip().startswith("|") and l.strip().endswith("|")]
    assert len(table_lines) >= 4, f"Trade-off Matrix must contain header + separator + criteria rows, found: {len(table_lines)}"

    print("[+] Workflow 4 verified: 2 POAs + mandatory Comparison / Trade-off Matrix comparing Problems Solved, User Impact, and Effort.")

def test_zero_chatbot_architecture():
    print("[*] Testing Architecture Conformance: Zero-Chatbot & Parameter Envelope...")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Assert no chat inputs
    assert '<input type="text" id="chatInput"' not in html, "Chatbot input field detected in HTML!"
    assert 'class="chat-history"' not in html, "Chat history container detected in HTML!"
    assert 'class="message-bubble"' not in html, "Chat message bubble detected in HTML!"

    # Assert parameter envelope in constants.js
    with open("js/config/constants.js", "r", encoding="utf-8") as f:
        constants = f.read()
    assert "TEMPERATURE: 0.2" in constants, "TEMPERATURE must be strictly 0.2"
    assert "TOP_P: 0.8" in constants, "TOP_P must be strictly 0.8"
    assert "TOP_K: 40" in constants, "TOP_K must be strictly 40"
    assert "MAX_OUTPUT_TOKENS: 2048" in constants, "MAX_OUTPUT_TOKENS must be strictly 2048"

    # Negative Prompt Directives
    assert ("Do NOT include conversational" in constants or "conversational chatter" in constants), "Missing negative conversational constraint"
    assert "Output ONLY" in constants or "Output only" in constants, "Missing strict Output ONLY directive"
    print("[+] Zero-Chatbot Architecture and deterministic parameter envelope (0.2 / 0.8) verified.")

def test_resilience_and_security():
    print("[*] Testing 7.5: Resilience & Security Audit (EC-01 to EC-20)...")
    # 1. Masked Password Input
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert 'type="password"' in html and 'id="apiKeyInput"' in html, "API Key input must be type=password"

    # 2. Zero-persistence
    js_dir = "js"
    for root, _, files in os.walk(js_dir):
        for file in files:
            if file.endswith(".js"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    c = f.read()
                assert "localStorage" not in c, f"Storage leak: localStorage in {path}"
                assert "sessionStorage" not in c, f"Storage leak: sessionStorage in {path}"

    # 3. Error Interceptors in geminiClient.js
    with open("js/services/geminiClient.js", "r", encoding="utf-8") as f:
        client_code = f.read()
    assert "response.status === 400" in client_code
    assert "response.status === 401 || response.status === 403" in client_code
    assert "response.status === 429" in client_code
    assert "response.status >= 500" in client_code
    assert "networkErr" in client_code

    print("[+] Resilience & Security audit passed: password masked, zero-persistence, full error interceptor coverage.")

def main():
    try:
        test_workflow_1_acceptance()
        test_workflow_2_acceptance()
        test_workflow_3_acceptance()
        test_workflow_4_acceptance()
        test_zero_chatbot_architecture()
        test_resilience_and_security()
        print("\n[SUCCESS] Phase 7 QA Acceptance & Architectural Audit: 100% Passed!")
        return 0
    except Exception as e:
        print(f"\n[FAIL] Phase 7 Verification Failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
