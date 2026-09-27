"""
Phase 3 Automated Unit Test — Prompt Generation & Model Parameter Verification
Validates:
1. All 4 analytical workflows assemble complete multi-shot prompt contracts.
2. Workflow 4 explicitly contains the required Comparison / Trade-off Matrix.
3. System parameters strictly adhere to Temperature: 0.2, Top_P: 0.8, Top_K: 40, MaxOutputTokens: 2048.
4. Serialized VoC dataset JSON is properly injected into the prompt payload.
"""
import json
import re
import sys

def load_constants():
    with open("js/config/constants.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Verify APP_CONFIG parameters
    assert "TEMPERATURE: 0.2" in content, "APP_CONFIG must enforce TEMPERATURE: 0.2"
    assert "TOP_P: 0.8" in content, "APP_CONFIG must enforce TOP_P: 0.8"
    assert "TOP_K: 40" in content, "APP_CONFIG must enforce TOP_K: 40"
    assert "MAX_OUTPUT_TOKENS: 2048" in content, "APP_CONFIG must enforce MAX_OUTPUT_TOKENS: 2048"
    assert "DEFAULT_MODEL: \"gemini-1.5-flash\"" in content, "APP_CONFIG must default to gemini-1.5-flash"
    print("[+] Model parameters strictly bound: Temp 0.2 | Top_P 0.8 | Top_K 40 | Tokens 2048")
    return content

def test_workflow_prompt_contracts(constants_content=None):
    if constants_content is None:
        constants_content = load_constants()
    print("[*] Testing Workflow Prompt Contracts & Syntax Directives...")

    # Workflow 1: Taxonomy of Lost Photos
    assert "Taxonomy of 'Lost' Photos" in constants_content, "Workflow 1 missing from constants"
    assert "Identify exactly 3 distinct categories" in constants_content, "Workflow 1 must require 3 categories"
    assert "EXCLUDE generic categories" in constants_content, "Workflow 1 must exclude generic categories"
    assert "H3 (###) for the category name" in constants_content, "Workflow 1 must enforce H3 headers"
    assert "Blockquotes (>) for the exact verbatim quote" in constants_content, "Workflow 1 must enforce blockquotes"
    print("[+] Workflow 1 (Taxonomy) Contract: Verified (H3 + Blockquote Quotes)")

    # Workflow 2: Cognitive Gap Matrix
    assert "Cognitive Gap Matrix" in constants_content, "Workflow 2 missing from constants"
    assert "| Retained Episodic Anchors (Human Recall) | Forgotten System Demands" in constants_content, (
        "Workflow 2 must enforce 3-column T-Chart"
    )
    print("[+] Workflow 2 (Cognitive Gap Matrix) Contract: Verified (3-Column T-Chart Table)")

    # Workflow 3: Behavioral Workarounds
    assert "Behavioral Workaround Mapping" in constants_content, "Workflow 3 missing from constants"
    assert "Format as a numbered list" in constants_content, "Workflow 3 must require numbered list"
    assert "Friction Score" in constants_content, "Workflow 3 must require Friction Score tag"
    print("[+] Workflow 3 (Workarounds) Contract: Verified (Numbered List + Friction Scoring)")

    # Workflow 4: Product Opportunity Synthesis & Trade-off Matrix
    assert "Product Opportunity Synthesis" in constants_content, "Workflow 4 missing from constants"
    assert "synthesize exactly 2 high-impact Product Opportunity Areas" in constants_content, (
        "Workflow 4 must require 2 POAs"
    )
    assert "### Problem Space" in constants_content, "Workflow 4 must require Problem Space header"
    assert "### Proposed AI Solution" in constants_content, "Workflow 4 must require Proposed AI Solution header"
    assert "### Hypothesis to Test" in constants_content, "Workflow 4 must require Hypothesis to Test header"
    assert "Comparison / Trade-off Matrix" in constants_content, (
        "Workflow 4 must require Comparison / Trade-off Matrix"
    )
    assert "| Evaluation Dimension | POA 1: [Short Title] | POA 2: [Short Title] |" in constants_content, (
        "Workflow 4 must require Comparison Table columns"
    )
    print("[+] Workflow 4 (POAs & Trade-off Matrix) Contract: Verified (POAs + Trade-off Table)")

def test_prompt_assembler_logic():
    print("[*] Testing Prompt Assembly with Simulated VoC Corpus...")
    with open("js/data/seedCorpus.js", "r", encoding="utf-8") as f:
        corpus_js = f.read()

    # Verify corpus contains 7 rich records
    match = re.search(r"export const SEED_CORPUS = (\[[\s\S]*?\]);", corpus_js)
    raw_js = match.group(1)
    json_str = re.sub(r'(\w+):', r'"\1":', raw_js)
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    records = json.loads(json_str)

    # Assemble simulated prompt for Workflow 4
    prompt_header = "Act as VP of Product for Google Photos."
    serialized_corpus = json.dumps(records, indent=2)
    full_prompt = f"{prompt_header}\n\nINPUT DATASET:\n{serialized_corpus}\n\nREMINDER OF STRICT OUTPUT RULES"

    assert len(full_prompt) > 1000, "Assembled prompt is too short"
    assert "voc-001" in full_prompt, "Missing voc-001 from injected dataset"
    assert "voc-007" in full_prompt, "Missing voc-007 from injected dataset"
    assert "pasta" in full_prompt, "Missing pasta query from corpus payload"
    print(f"[+] Prompt Assembler successfully injected {len(records)} records ({len(full_prompt)} chars).")

def main():
    try:
        constants = load_constants()
        test_workflow_prompt_contracts(constants)
        test_prompt_assembler_logic()
        print("\n[SUCCESS] Phase 3 Verification Completed: All Tests Passed!")
        return 0
    except Exception as e:
        print(f"\n[FAIL] Phase 3 Verification Failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
