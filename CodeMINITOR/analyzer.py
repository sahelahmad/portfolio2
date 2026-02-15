import ast
import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Constants 
HISTORY_FILE = Path("history.json")
MAX_FUNCTION_LINES = 20
MAX_FILE_LINES = 300
DEFAULT_SCORE = 100

console = Console()


class CodeAnalyzer:
    """Responsible for parsing Python files and extracting structural metrics."""

    def __init__(self, filepath: Path):
        self.filepath = filepath
        self.metrics: Dict[str, int] = {}

    def analyze(self) -> Dict[str, int]:
        """Parses the source code using AST and calculates key metrics."""
        try:
            source = self.filepath.read_text(encoding="utf-8")
            tree = ast.parse(source)
        except (SyntaxError, UnicodeDecodeError) as e:
            console.print(f"[bold red]Parsing Error:[/bold red] {e}")
            sys.exit(1)

        functions = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef)]
        
        self.metrics = {
            "lines": len(source.splitlines()),
            "functions": len(functions),
            "imports": len([n for n in ast.walk(tree) if isinstance(n, (ast.Import, ast.ImportFrom))]),
            "docstrings": len([n for n in functions if ast.get_docstring(n)]),
            "type_hints": self._count_type_hints(functions),
            "long_functions": self._count_long_functions(functions),
        }
        return self.metrics

    def _count_type_hints(self, functions: List[ast.FunctionDef]) -> int:
        """Counts how many functions utilize type hinting for arguments or return values."""
        count = 0
        for node in functions:
            has_return_hint = node.returns is not None
            has_args_hint = any(arg.annotation for arg in node.args.args)
            if has_return_hint or has_args_hint:
                count += 1
        return count

    def _count_long_functions(self, functions: List[ast.FunctionDef]) -> int:
        """Identifies functions exceeding the defined line limit."""
        return sum(1 for n in functions if (n.end_lineno - n.lineno) > MAX_FUNCTION_LINES)


class ScoreEngine:
    """Handles the logic for grading the code based on extracted metrics."""

    @staticmethod
    def calculate(metrics: Dict[str, int]) -> int:
        """Calculates a final score out of 100 based on best practices."""
        score = DEFAULT_SCORE

        if metrics["functions"] == 0:
            score -= 30
        else:
            # Penalize for missing documentation or type safety
            if metrics["docstrings"] < metrics["functions"]:
                score -= 10
            if metrics["type_hints"] < metrics["functions"]:
                score -= 10

        if metrics["long_functions"] > 0:
            score -= 10
        if metrics["lines"] > MAX_FILE_LINES:
            score -= 10

        return max(score, 0)


class HistoryStore:
    """Manages persistence of analysis scores in a JSON file."""

    def __init__(self, filename: Path):
        self.filename = filename

    def save_score(self, score: int) -> None:
        """Appends a new score to the historical data."""
        history = self.get_all()
        history.append(score)
        try:
            self.filename.write_text(json.dumps(history), encoding="utf-8")
        except IOError as e:
            console.print(f"[yellow]Warning: Persistent storage failed: {e}[/yellow]")

    def get_all(self) -> List[int]:
        """Retrieves all previous scores from the history file."""
        if not self.filename.exists():
            return []
        try:
            return json.loads(self.filename.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, IOError):
            return []

    def get_statistics(self) -> Dict[str, Any]:
        """Calculates aggregate statistics from the history."""
        history = self.get_all()
        if not history:
            return {"runs": 0, "average": 0, "best": 0}
        return {
            "runs": len(history),
            "average": sum(history) / len(history),
            "best": max(history),
        }


def render_dashboard(filepath: Path, metrics: Dict[str, int], score: int, stats: Dict[str, Any]) -> None:
    """Displays a rich, formatted dashboard in the terminal."""
    # Metrics Table
    table = Table(title="Code Quality Metrics", title_style="bold cyan")
    table.add_column("Metric", style="white")
    table.add_column("Value", justify="right", style="green")

    for key, value in metrics.items():
        table.add_row(key.replace("_", " ").capitalize(), str(value))

    # Header and Main Table
    console.print(Panel(f"Target File: [bold yellow]{filepath.name}[/bold yellow]", subtitle="Analysis Engine v2.0"))
    console.print(table)
    
    # Conditional coloring for the score
    score_color = "green" if score >= 80 else "yellow" if score >= 60 else "red"
    console.print(Panel(f"Final Score: [bold {score_color}]{score}/100[/bold {score_color}]", expand=False))

    # Historical Stats
    stats_display = (
        f"Total Analyses: {stats['runs']}\n"
        f"Lifetime Average: {stats['average']:.2f}\n"
        f"Personal Best: {stats['best']}"
    )
    console.print(Panel(stats_display, title="Historical Trends", border_style="dim"))


def main() -> None:
    """Main execution flow."""
    if len(sys.argv) != 2:
        console.print("[bold red]Usage:[/bold red] python analyzer.py <path_to_file.py>")
        sys.exit(1)

    file_path = Path(sys.argv[1])

    if not file_path.is_file() or file_path.suffix != ".py":
        console.print(f"[bold red]Error:[/bold red] Invalid Python file: {file_path}")
        sys.exit(1)

    # 1. Analyze
    analyzer = CodeAnalyzer(file_path)
    metrics = analyzer.analyze()
    
    # 2. Grade
    score = ScoreEngine.calculate(metrics)
    
    # 3. Store
    history = HistoryStore(HISTORY_FILE)
    history.save_score(score)
    
    # 4. Display
    render_dashboard(file_path, metrics, score, history.get_statistics())


if __name__ == "__main__":
    main()  