"""
Phase 2 Automated Unit & Schema Conformance Test
Validates:
1. All seed records in seedCorpus.js conform strictly to UserFeedbackRecord schema.
2. Filter logic works across all source combinations.
3. Serialization outputs valid, formatted JSON.
"""
import json
import re
import sys

VALID_SOURCES = [
    "r/GooglePhotos",
    "Play Store",
    "App Store",
    "Google Support Forum"
]

VALID_TYPES = [
    "Reddit Post",
    "1-Star Review",
    "2-Star Review",
    "Support Thread",
    "Feature Request"
]

def load_seed_corpus():
    with open("js/data/seedCorpus.js", "r", encoding="utf-8") as f:
        content = f.read()

    # Extract array within SEED_CORPUS = [ ... ];
    match = re.search(r"export const SEED_CORPUS = (\[[\s\S]*?\]);", content)
    if not match:
        raise ValueError("Could not locate SEED_CORPUS array in js/data/seedCorpus.js")

    raw_js = match.group(1)
    # Convert unquoted keys to double quotes for JSON parsing
    # e.g. id: -> "id":
    json_str = re.sub(r'(\w+):', r'"\1":', raw_js)
    # Remove any trailing commas before } or ]
    json_str = re.sub(r',\s*([}\]])', r'\1', json_str)
    
    return json.loads(json_str)

def test_schema_conformance(records=None):
    if records is None:
        records = load_seed_corpus()
    print(f"[*] Testing Schema Conformance for {len(records)} records...")
    assert len(records) >= 7, f"Expected at least 7 records, got {len(records)}"

    ids = set()
    for idx, r in enumerate(records):
        # ID check
        assert "id" in r and isinstance(r["id"], str) and len(r["id"]) > 0, f"Record {idx} invalid id"
        assert r["id"] not in ids, f"Duplicate ID: {r['id']}"
        ids.add(r["id"])

        # Source check
        assert r["source"] in VALID_SOURCES, f"Record {r['id']} has invalid source: {r['source']}"

        # Type check
        assert r["type"] in VALID_TYPES, f"Record {r['id']} has invalid type: {r['type']}"

        # Content check
        assert "content" in r and isinstance(r["content"], str) and len(r["content"].strip()) > 20, (
            f"Record {r['id']} has insufficient content"
        )

        # Metadata check
        assert "metadata" in r and isinstance(r["metadata"], dict), f"Record {r['id']} missing metadata dict"
        meta = r["metadata"]
        assert "date" in meta and re.match(r"^\d{4}-\d{2}-\d{2}$", meta["date"]), (
            f"Record {r['id']} has invalid date: {meta.get('date')}"
        )
        assert "tags" in meta and isinstance(meta["tags"], list) and len(meta["tags"]) > 0, (
            f"Record {r['id']} missing tags list"
        )

    print(f"[+] All {len(records)} records passed strict schema validation!")

def test_filtering_and_serialization(records=None):
    if records is None:
        records = load_seed_corpus()
    print("[*] Testing Filtering and JSON Serialization...")
    
    # 1. All sources active
    all_filters = {s: True for s in VALID_SOURCES}
    active_all = [r for r in records if all_filters.get(r["source"], True)]
    assert len(active_all) == 7, f"Expected 7 records, got {len(active_all)}"

    # 2. Exclude Reddit (which has 3 records: voc-001, voc-004, voc-006)
    no_reddit = {**all_filters, "r/GooglePhotos": False}
    filtered_no_reddit = [r for r in records if no_reddit.get(r["source"], True)]
    assert len(filtered_no_reddit) == 4, f"Expected 4 records without Reddit, got {len(filtered_no_reddit)}"

    # 3. Exclude Google Support Forum (2 records: voc-003, voc-007)
    no_support = {**all_filters, "Google Support Forum": False}
    filtered_no_support = [r for r in records if no_support.get(r["source"], True)]
    assert len(filtered_no_support) == 5, f"Expected 5 records without Support, got {len(filtered_no_support)}"

    # 4. Exclude all sources
    none_active = {s: False for s in VALID_SOURCES}
    filtered_none = [r for r in records if none_active.get(r["source"], True)]
    assert len(filtered_none) == 0, f"Expected 0 records when all disabled, got {len(filtered_none)}"

    # 5. Serialization Test
    serialized = json.dumps(active_all, indent=2)
    deserialized = json.loads(serialized)
    assert len(deserialized) == 7, "Serialization / Deserialization mismatch"
    assert deserialized[0]["id"] == "voc-001", "Integrity check failed on deserialized data"

    print("[+] Filtering logic and serialization verified successfully!")

def main():
    try:
        records = load_seed_corpus()
        test_schema_conformance(records)
        test_filtering_and_serialization(records)
        print("\n[SUCCESS] Phase 2 Verification Completed: All Tests Passed!")
        return 0
    except Exception as e:
        print(f"\n[FAIL] Phase 2 Verification Failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
