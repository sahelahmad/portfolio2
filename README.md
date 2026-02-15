
# 🔬 Code Quality Analyzer

> Production-grade Python static analysis tool powered by AST

A modular, testable, and extensible CLI tool that analyzes Python source code using the Abstract Syntax Tree (AST) to evaluate structural quality and enforce best practices.

Designed with clean architecture principles, separation of concerns, and long-term scalability in mind.

---

## ✨ Why This Project Exists

Most beginner tools count lines.

This tool understands structure.

Instead of superficial metrics, this analyzer parses Python files into their AST representation and evaluates architectural health, documentation quality, type safety, and structural discipline.

It simulates how real static analysis tools think — but in a simplified, extensible form.

---

## 🧠 Core Capabilities

* AST-based structural analysis
* Deterministic scoring engine (0–100)
* Quality deduction rules
* Persistent analysis history
* Lifetime performance statistics
* Rich terminal dashboard visualization
* Clean, testable, layered architecture
* Fully unit-testable components

---

## 🏗️ Architecture Overview

The system follows **Single Responsibility Principle (SRP)** and layered separation:

| Layer                | Responsibility                       |
| -------------------- | ------------------------------------ |
| `CodeAnalyzer`       | Parses and extracts metrics from AST |
| `ScoreEngine`        | Applies scoring rules                |
| `HistoryStore`       | Manages JSON persistence             |
| `render_dashboard()` | Presentation layer (rich UI)         |
| `main()`             | Application orchestration            |

Each component is isolated and independently testable.

No logic leakage between layers.

---

## 📊 Metrics Collected

The analyzer extracts:

* Total functions
* Total imports
* Presence of module docstring
* Type hints usage
* Long functions (>20 lines)
* Total file length
* Structural consistency indicators

All derived directly from the Python AST.

---

## 🎯 Scoring Model

Score starts at **100** and deducts based on violations:

| Rule                           | Deduction |
| ------------------------------ | --------- |
| No functions defined           | -30       |
| Missing module docstring       | -10       |
| No type hints used             | -10       |
| Functions longer than 20 lines | -10       |
| File exceeds 300 lines         | -10       |

Minimum score: 0
Deterministic and predictable scoring logic.

---

## 📈 Historical Tracking

Every analysis is persisted in `history.json`.

Stored data:

* Timestamp
* Score
* File name

The system calculates:

* Total analyses
* Lifetime average score
* Best score ever achieved

This transforms the tool from a one-time analyzer into a progress tracker.

---

## 🖥️ Example Usage

```bash
python analyzer.py path/to/file.py
```

Example:

```bash
python analyzer.py sample.py
```

The terminal will render:

* Metrics table
* Final quality score
* Historical statistics

All presented using the `rich` library.

---

## 🧪 Testing Strategy

All business logic is isolated from the CLI.

Unit tests cover:

* Scoring logic
* History storage
* JSON handling
* Edge cases

Run tests with:


Test-driven architecture ensures reliability and maintainability.



## 📁 Project Structure

```
code-quality-analyzer/
│
├── analyzer.py
├── history.json
├── tests/
│   └── test_history.py
├── requirements.txt
└── README.md
```

---

## 🛠 Design Principles Applied

* Clean Architecture
* Separation of Concerns
* Single Responsibility Principle
* Deterministic business logic
* Stateless scoring engine
* Persistence abstraction
* CLI as thin orchestration layer

---

## 🔮 Future Roadmap

Planned enhancements:

* Cyclomatic complexity analysis
* Class-level architecture scoring
* Unused import detection
* Exportable reports (JSON / CSV)
* CLI flags with argparse
* SQLite-backed history
* GitHub Actions CI pipeline
* Plugin system for custom rules

---

## 💡 What This Project Demonstrates

This is not a beginner script.

It demonstrates:

* Deep understanding of Python AST
* Practical OOP design
* Real-world project structuring
* Persistence handling
* CLI application design
* Testability-first architecture
* Engineering thinking beyond syntax

---

## 👨‍💻 Author

Sahel
Python Developer | Focused on Code Quality, Architecture & Engineering Discipline


