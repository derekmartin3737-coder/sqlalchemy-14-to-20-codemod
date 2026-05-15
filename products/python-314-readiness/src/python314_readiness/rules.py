from __future__ import annotations

from python314_readiness.models import Rule

RULE_PACK_VERSION = "2026.05.14"

PYTHON_314_SOURCE = "https://docs.python.org/3.14/whatsnew/3.14.html"
PYDANTIC_CHANGELOG_SOURCE = "https://docs.pydantic.dev/changelog/"
SETUP_PYTHON_SOURCE = "https://github.com/actions/setup-python"

RULES: dict[str, Rule] = {
    "PY314000": Rule(
        id="PY314000",
        title="Python source could not be parsed",
        category="scanner",
        severity="critical",
        classification="blocked",
        source_url=PYTHON_314_SOURCE,
        source_label="Python 3.14 documentation",
        autofix=False,
        description=(
            "The scanner could not parse a Python file, so it cannot safely "
            "classify readiness risks in that source file."
        ),
        recommendation=(
            "Fix the syntax error or exclude generated files before relying "
            "on the readiness report."
        ),
    ),
    "PY314001": Rule(
        id="PY314001",
        title="Project metadata excludes Python 3.14",
        category="metadata",
        severity="high",
        classification="manual_review",
        source_url=PYTHON_314_SOURCE,
        source_label="Python 3.14 documentation",
        autofix=False,
        description="The project's Python version metadata blocks Python 3.14.",
        recommendation=(
            "Review dependency and test compatibility, then widen the "
            "requires-python bound if the repo passes on Python 3.14."
        ),
    ),
    "PY314002": Rule(
        id="PY314002",
        title="GitHub Actions does not test Python 3.14",
        category="ci",
        severity="high",
        classification="autofix",
        source_url=SETUP_PYTHON_SOURCE,
        source_label="actions/setup-python README",
        autofix=True,
        description=(
            "The repository uses setup-python but its visible Python matrix "
            "does not include Python 3.14."
        ),
        recommendation="Add Python 3.14 to the CI matrix and run the suite.",
    ),
    "PY314003": Rule(
        id="PY314003",
        title="Runtime annotation introspection needs Python 3.14 review",
        category="annotations",
        severity="high",
        classification="manual_review",
        source_url=PYTHON_314_SOURCE,
        source_label="Python 3.14 deferred annotations and porting notes",
        autofix=False,
        description=(
            "Python 3.14 changes annotation evaluation behavior through "
            "PEP 649 and PEP 749."
        ),
        recommendation=(
            "Review annotation readers and consider annotationlib or explicit "
            "format handling where runtime values are required."
        ),
    ),
    "PY314004": Rule(
        id="PY314004",
        title="Pydantic v1 usage needs Python 3.14 migration review",
        category="pydantic",
        severity="high",
        classification="manual_review",
        source_url=PYDANTIC_CHANGELOG_SOURCE,
        source_label="Pydantic changelog",
        autofix=False,
        description=(
            "Pydantic's changelog calls out Python 3.14 compatibility work; "
            "v1-style usage should be reviewed before claiming readiness."
        ),
        recommendation=(
            "Prefer current Pydantic v2 or verify the exact pydantic.v1 "
            "compatibility path under Python 3.14."
        ),
    ),
    "PY314005": Rule(
        id="PY314005",
        title="Pydantic pin predates initial Python 3.14 support",
        category="pydantic",
        severity="medium",
        classification="manual_review",
        source_url=PYDANTIC_CHANGELOG_SOURCE,
        source_label="Pydantic changelog",
        autofix=False,
        description="The dependency pin is older than Pydantic's 2.12 line.",
        recommendation="Upgrade Pydantic or test the pinned version under 3.14.",
    ),
    "PY314006": Rule(
        id="PY314006",
        title="Process-based concurrency needs start-method review",
        category="runtime",
        severity="medium",
        classification="manual_review",
        source_url=PYTHON_314_SOURCE,
        source_label="Python 3.14 porting notes",
        autofix=False,
        description=(
            "Python 3.14 changes the default multiprocessing start method on "
            "Unix platforms other than macOS from fork to forkserver."
        ),
        recommendation=(
            "Make the multiprocessing context explicit where startup semantics "
            "or pickling behavior matter."
        ),
    ),
    "PY314007": Rule(
        id="PY314007",
        title="functools.partial in class bodies needs descriptor review",
        category="runtime",
        severity="medium",
        classification="manual_review",
        source_url=PYTHON_314_SOURCE,
        source_label="Python 3.14 porting notes",
        autofix=False,
        description=(
            "Python 3.14 makes functools.partial a method descriptor, which "
            "can affect partials assigned in class bodies."
        ),
        recommendation="Wrap class-level partials in staticmethod() if needed.",
    ),
}


def rule(rule_id: str) -> Rule:
    return RULES[rule_id]
