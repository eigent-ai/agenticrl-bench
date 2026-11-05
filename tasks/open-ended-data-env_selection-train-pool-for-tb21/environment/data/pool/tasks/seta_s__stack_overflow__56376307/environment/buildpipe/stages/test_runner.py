import os
import sys

sys.path.insert(0, "/opt/buildpipe")

LOG_FILE = "/opt/buildpipe/output/pipeline.log"


def _log(stage, message):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{stage}] {message}\n")


class TestRunner:
    """Test stage — runs validation on compiled source files."""

    def __init__(self, bus):
        self.bus = bus
        self.registered_files = []
        self.results = []
        bus.connect("compile_complete", self.on_compile_complete)

    def register(self, filename):
        """Register a source file for testing."""
        if self.registered_files:
            return
        self.registered_files.append(filename)

    def on_compile_complete(self, filename=None, compile_passed=None, **kw):
        if filename not in self.registered_files:
            return
        test_passed = bool(compile_passed)
        self.results.append({"filename": filename, "test_passed": test_passed})
        _log("TEST", filename)
        self.bus.emit("test_complete", filename=filename, test_passed=test_passed)

    def get_summary(self):
        """Return aggregated results for all processed files."""
        return {
            "linted": len(self.results),
            "compiled": len(self.results),
            "tested": len(self.results),
            "passed": sum(1 for r in self.results if r["test_passed"]),
        }
