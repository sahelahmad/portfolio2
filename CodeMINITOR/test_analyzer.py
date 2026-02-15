import json
import tempfile
from pathlib import Path

import pytest

from analyzer import CodeAnalyzer, ScoreEngine, HistoryStore


# -----------------------------
# Helper: Create temporary file
# -----------------------------
def create_temp_python_file(content: str) -> Path:
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".py")
    temp_file.write(content.encode("utf-8"))
    temp_file.close()
    return Path(temp_file.name)


# -----------------------------
# CodeAnalyzer Tests
# -----------------------------
def test_analyzer_counts_functions():
    code = """
def hello():
    return "hi"
"""
    file_path = create_temp_python_file(code)
    analyzer = CodeAnalyzer(file_path)
    metrics = analyzer.analyze()

    assert metrics["functions"] == 1
    assert metrics["lines"] > 0


def test_analyzer_detects_docstring():
    code = '''
def hello():
    """This is a docstring"""
    return "hi"
'''
    file_path = create_temp_python_file(code)
    analyzer = CodeAnalyzer(file_path)
    metrics = analyzer.analyze()

    assert metrics["docstrings"] == 1


def test_analyzer_detects_type_hints():
    code = """
def add(x: int, y: int) -> int:
    return x + y
"""
    file_path = create_temp_python_file(code)
    analyzer = CodeAnalyzer(file_path)
    metrics = analyzer.analyze()

    assert metrics["type_hints"] == 1


# -----------------------------
# ScoreEngine Tests
# -----------------------------
def test_score_perfect():
    metrics = {
        "lines": 50,
        "functions": 1,
        "imports": 0,
        "docstrings": 1,
        "type_hints": 1,
        "long_functions": 0,
    }

    score = ScoreEngine.calculate(metrics)
    assert score == 100


def test_score_penalty_no_functions():
    metrics = {
        "lines": 50,
        "functions": 0,
        "imports": 0,
        "docstrings": 0,
        "type_hints": 0,
        "long_functions": 0,
    }

    score = ScoreEngine.calculate(metrics)
    assert score == 70


# -----------------------------
# HistoryStore Tests
# -----------------------------
def test_history_store_save_and_load(tmp_path):
    history_file = tmp_path / "history.json"
    store = HistoryStore(history_file)

    store.save_score(80)
    store.save_score(90)

    history = store.get_all()

    assert history == [80, 90]


def test_history_statistics(tmp_path):
    history_file = tmp_path / "history.json"
    store = HistoryStore(history_file)

    store.save_score(80)
    store.save_score(100)

    stats = store.get_statistics()

    assert stats["runs"] == 2
    assert stats["best"] == 100
    assert stats["average"] == 90
