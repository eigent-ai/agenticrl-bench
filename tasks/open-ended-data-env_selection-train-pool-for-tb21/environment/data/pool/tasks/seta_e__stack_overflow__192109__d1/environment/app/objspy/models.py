"""Demo model classes for testing the introspection library."""


class Base:
    """Base class with class-level attributes and a property."""

    version = "1.0"

    def __init__(self, name):
        self.name = name

    @property
    def info(self):
        return f"{self.name} (v{self.version})"

    def describe(self):
        return f"Base: {self.name}"


class Config(Base):
    """Configuration class inheriting from Base."""

    version = "2.0"
    defaults = {"timeout": 30, "retries": 3}

    def __init__(self, name):
        super().__init__(name)
        self.settings = {}
        self.enabled = True

    def apply(self, **kwargs):
        """Apply configuration settings."""
        self.settings.update(kwargs)


class Vehicle:
    """Vehicle class using __slots__ for memory efficiency."""

    __slots__ = ("make", "model", "year", "features")

    def __init__(self, make, model, year, features=None):
        self.make = make
        self.model = model
        self.year = year
        self.features = features if features is not None else []

    @classmethod
    def from_string(cls, s):
        parts = s.split(",")
        return cls(parts[0].strip(), parts[1].strip(), int(parts[2].strip()))

    def summary(self):
        return f"{self.year} {self.make} {self.model}"


class PluginRegistry:
    """Plugin registry with various attribute types including falsy values."""

    def __init__(self):
        self.plugin_count = 0
        self.description = ""
        self.hooks = []
        self.name = "registry"
        self._cache = {
            "loaded": {"core": True, "extras": False, "experimental": True},
            "pending": ["auth", "logging", "metrics", "tracing"],
            "config": {"max_retries": 3, "timeout": 30, "debug": False},
        }

    def register(self, plugin_name):
        """Register a new plugin."""
        self.plugin_count += 1
