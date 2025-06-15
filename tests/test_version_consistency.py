import os
import toml
import yaml

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
README_FILE = os.path.join(PROJECT_DIR, "README.md")
TOML_FILE = os.path.join(PROJECT_DIR, "pyproject.toml")
CITATION_FILE = os.path.join(PROJECT_DIR, "CITATION.cff")
CHANGELOG_FILE = os.path.join(PROJECT_DIR, "ChangeLog.md")
REQUIREMENTS_DOCS_FILE = os.path.join(PROJECT_DIR, "docs", "requirements.txt")
REQUIREMENTS_TESTS_FILE = os.path.join(PROJECT_DIR, "tests", "requirements.txt")
REQUIREMENTS_BENCHMARKS_FILE = os.path.join(PROJECT_DIR, "benchmarks", "requirements.txt")
REQUIREMENT_FILES = [REQUIREMENTS_DOCS_FILE,
                     REQUIREMENTS_BENCHMARKS_FILE]

def test_version_consistency():
    toml_version = toml.load(TOML_FILE)["project"]["version"]
    with open(CITATION_FILE, "r") as f:
        citation_content = yaml.safe_load(f)
    citation_version = citation_content["version"]
    assert citation_version == toml_version
    with open(README_FILE, "r") as f:
        for line in f.readline():
            if "`](ChangeLog.md#release-" in line:
                assert f"[`{toml_version}`](ChangeLog.md#release-{toml_version.replace('.', '')})" in line
    with open(CHANGELOG_FILE, "r") as f:
        for line in f.readlines():
            if line.startswith("## "):
                assert toml_version in line
                break
        else: assert False, "Version not found in CHANGELOG.md"
    for requirements_file in REQUIREMENT_FILES:
        with open(requirements_file, "r") as f:
            for line in f.readlines():
                if line.startswith("py-ste == "):
                    assert line.startswith(f"py-ste == {toml_version}")
                    break
            else: assert False, f"Version not found in {requirements_file.split(PROJECT_DIR)[1]}"