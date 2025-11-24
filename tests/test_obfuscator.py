import pytest
from pathlib import Path
from obfuscator import obfuscate_identifier, build_class_mapping

def test_obfuscate_shift():
    assert obfuscate_identifier("btn", "shift") == "ewq"

def test_obfuscate_hash():
    result = obfuscate_identifier("btn", "hash")
    assert result.startswith("c")
    assert len(result) == 9

def test_build_mapping_excludes():
    classes = {"btn", "active", "hidden"}
    exclude = {"active"}
    mappings = build_class_mapping(classes, "shift", exclude)
    
    originals = {m.original for m in mappings}
    assert "active" not in originals
    assert "btn" in originals
    assert "hidden" in originals