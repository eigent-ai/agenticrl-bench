"""
Data Processing and Analysis Application
=========================================
A comprehensive pipeline for ingesting, transforming, validating,
and reporting on structured datasets. Supports CSV, JSON, and Parquet
sources with configurable transformation stages, statistical summaries,
anomaly detection, and multi-format output.

Usage:
    python app.py --config config.json --input data/ --output results/
"""

from __future__ import annotations

import os
import sys
import json
import csv
import gzip
import time
import math
import uuid
import copy
import enum
import heapq
import hashlib
import logging
import logging.handlers
import argparse
import datetime
import calendar
import itertools
import functools
import threading
import traceback
import contextlib
import collections
import collections.abc
import statistics
import textwrap
import re
import io
import struct
import random
import signal
import atexit
import inspect
import weakref
import operator
import pathlib
import shutil
import tempfile
import pickle
import base64
import urllib.parse
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict, astuple
from typing import (
    Any, Dict, List, Optional, Tuple, Union, Set, Iterator,
    Callable, Type, TypeVar, Generic, Sequence, Mapping,
    Generator, NamedTuple, ClassVar, FrozenSet, Iterable,
    cast, overload, TYPE_CHECKING,
)
from pathlib import Path
from contextlib import contextmanager, suppress
from functools import wraps, partial, lru_cache, reduce
from collections import defaultdict, OrderedDict, Counter, deque
from datetime import timezone, timedelta
from enum import Enum, IntEnum, auto

if TYPE_CHECKING:
    pass

# ---------------------------------------------------------------------------
# Version and metadata
# ---------------------------------------------------------------------------

__version__ = "2.4.1"
__author__ = "DataSynth Analytics Team"
__email__ = "analytics@datasynth.io"
__license__ = "MIT"

# ---------------------------------------------------------------------------
# Module-level constants
# ---------------------------------------------------------------------------

APP_NAME = "DataPipeline"
DEFAULT_ENCODING = "utf-8"
DEFAULT_CHUNK_SIZE = 8192
DEFAULT_BATCH_SIZE = 1000
MAX_RETRY_ATTEMPTS = 3
RETRY_BACKOFF_BASE = 2.0
MISSING_VALUE_SENTINEL = object()
NUMERIC_TYPES = (int, float, complex)
DATE_FORMAT_ISO = "%Y-%m-%d"
DATETIME_FORMAT_ISO = "%Y-%m-%dT%H:%M:%S"
DATETIME_FORMAT_FULL = "%Y-%m-%dT%H:%M:%S.%fZ"

_T = TypeVar("_T")
_KT = TypeVar("_KT")
_VT = TypeVar("_VT")

# ---------------------------------------------------------------------------
# Logging configuration
# ---------------------------------------------------------------------------

def _build_formatter(verbose: bool = False) -> logging.Formatter:
    """Construct a log formatter with optional verbose mode."""
    if verbose:
        fmt = (
            "%(asctime)s | %(levelname)-8s | %(name)s | "
            "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
        )
    else:
        fmt = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    datefmt = "%Y-%m-%d %H:%M:%S"
    return logging.Formatter(fmt=fmt, datefmt=datefmt)


def setup_logging(
    level: str = "INFO",
    log_file: Optional[str] = None,
    verbose: bool = False,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configure root logger with console and optional rotating file handler.

    Args:
        level: Logging level string (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: If provided, attach a RotatingFileHandler at this path.
        verbose: Whether to emit file/line information in log records.
        max_bytes: Maximum size of each log file before rotation.
        backup_count: Number of backup log files to keep.

    Returns:
        Configured root logger.
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    root = logging.getLogger()
    root.setLevel(numeric_level)

    # Remove any pre-existing handlers to avoid duplicate output
    for handler in list(root.handlers):
        root.removeHandler(handler)

    formatter = _build_formatter(verbose=verbose)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(numeric_level)
    console_handler.setFormatter(formatter)
    root.addHandler(console_handler)

    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.handlers.RotatingFileHandler(
            filename=str(log_path),
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding=DEFAULT_ENCODING,
        )
        file_handler.setLevel(numeric_level)
        file_handler.setFormatter(formatter)
        root.addHandler(file_handler)

    return root


logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class FileFormat(str, Enum):
    """Supported input/output file formats."""
    CSV = "csv"
    JSON = "json"
    JSONL = "jsonl"
    TSV = "tsv"
    PARQUET = "parquet"
    PICKLE = "pickle"

    @classmethod
    def from_path(cls, path: Union[str, Path]) -> "FileFormat":
        """Infer format from file extension."""
        suffix = Path(path).suffix.lstrip(".").lower()
        mapping = {
            "csv": cls.CSV,
            "tsv": cls.TSV,
            "json": cls.JSON,
            "jsonl": cls.JSONL,
            "ndjson": cls.JSONL,
            "parquet": cls.PARQUET,
            "pkl": cls.PICKLE,
            "pickle": cls.PICKLE,
        }
        if suffix not in mapping:
            raise ValueError(f"Unrecognised file extension: .{suffix}")
        return mapping[suffix]


class AggregationMethod(str, Enum):
    """Statistical aggregation methods."""
    SUM = "sum"
    MEAN = "mean"
    MEDIAN = "median"
    MIN = "min"
    MAX = "max"
    COUNT = "count"
    STD = "std"
    VAR = "var"
    FIRST = "first"
    LAST = "last"
    MODE = "mode"


class TransformStage(str, Enum):
    """Named stages in the transformation pipeline."""
    INGEST = "ingest"
    VALIDATE = "validate"
    CLEAN = "clean"
    ENRICH = "enrich"
    AGGREGATE = "aggregate"
    EXPORT = "export"


class AnomalyType(str, Enum):
    """Categories of data anomalies."""
    MISSING = "missing"
    OUTLIER = "outlier"
    DUPLICATE = "duplicate"
    TYPE_MISMATCH = "type_mismatch"
    RANGE_VIOLATION = "range_violation"
    PATTERN_MISMATCH = "pattern_mismatch"
    REFERENTIAL = "referential"


class PipelineStatus(str, Enum):
    """Overall pipeline execution states."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"
    CANCELLED = "cancelled"


# ---------------------------------------------------------------------------
# Custom exceptions
# ---------------------------------------------------------------------------

class DataPipelineError(Exception):
    """Base exception for all pipeline errors."""

    def __init__(self, message: str, context: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.context: Dict[str, Any] = context or {}
        self.timestamp: datetime.datetime = datetime.datetime.now(timezone.utc)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_type": type(self).__name__,
            "message": str(self),
            "context": self.context,
            "timestamp": self.timestamp.isoformat(),
        }


class ConfigurationError(DataPipelineError):
    """Raised when configuration is invalid or incomplete."""


class IngestError(DataPipelineError):
    """Raised when data ingestion fails."""


class ValidationError(DataPipelineError):
    """Raised when data fails validation rules."""

    def __init__(
        self,
        message: str,
        field: Optional[str] = None,
        value: Any = MISSING_VALUE_SENTINEL,
        context: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(message, context)
        self.field = field
        self.value = value if value is not MISSING_VALUE_SENTINEL else None


class TransformError(DataPipelineError):
    """Raised when a transformation step fails."""


class ExportError(DataPipelineError):
    """Raised when writing output data fails."""


class SchemaError(DataPipelineError):
    """Raised when schema inference or enforcement fails."""


class RetryExhaustedError(DataPipelineError):
    """Raised when all retry attempts are exhausted."""


# ---------------------------------------------------------------------------
# Decorators
# ---------------------------------------------------------------------------

def retry(
    max_attempts: int = MAX_RETRY_ATTEMPTS,
    exceptions: Tuple[Type[Exception], ...] = (Exception,),
    backoff: float = RETRY_BACKOFF_BASE,
    jitter: bool = True,
) -> Callable:
    """
    Decorator that retries a function on specified exceptions with exponential backoff.

    Args:
        max_attempts: Maximum number of attempts including the first call.
        exceptions: Tuple of exception types to catch and retry on.
        backoff: Base for exponential backoff calculation.
        jitter: Whether to add random jitter to the wait duration.

    Returns:
        Decorated function.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            last_exc: Optional[Exception] = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as exc:
                    last_exc = exc
                    if attempt == max_attempts:
                        break
                    wait = backoff ** (attempt - 1)
                    if jitter:
                        wait += random.uniform(0, 0.5 * wait)
                    logger.warning(
                        "Attempt %d/%d failed for %s: %s. Retrying in %.2fs.",
                        attempt, max_attempts, func.__qualname__, exc, wait,
                    )
                    time.sleep(wait)
            raise RetryExhaustedError(
                f"All {max_attempts} attempts failed for {func.__qualname__}",
                context={"last_error": str(last_exc)},
            ) from last_exc
        return wrapper
    return decorator


def timed(func: Callable) -> Callable:
    """Decorator that logs the wall-clock execution time of a function."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            result = func(*args, **kwargs)
            elapsed = time.perf_counter() - start
            logger.debug("%s completed in %.4fs", func.__qualname__, elapsed)
            return result
        except Exception:
            elapsed = time.perf_counter() - start
            logger.debug("%s raised after %.4fs", func.__qualname__, elapsed)
            raise
    return wrapper


def validate_inputs(**validators: Callable[[Any], bool]) -> Callable:
    """
    Decorator factory that validates named arguments using provided callables.

    Example:
        @validate_inputs(n=lambda x: x > 0)
        def process(n: int) -> None: ...
    """
    def decorator(func: Callable) -> Callable:
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            for param_name, validator in validators.items():
                if param_name in bound.arguments:
                    val = bound.arguments[param_name]
                    if not validator(val):
                        raise ValidationError(
                            f"Argument '{param_name}' failed validation",
                            field=param_name,
                            value=val,
                        )
            return func(*args, **kwargs)
        return wrapper
    return decorator


def singleton(cls: Type[_T]) -> Type[_T]:
    """Class decorator that enforces the singleton pattern."""
    instances: Dict[Type, Any] = {}
    lock = threading.Lock()

    @wraps(cls, updated=[])
    class _Singleton(cls):  # type: ignore[valid-type]
        def __new__(klass, *args: Any, **kwargs: Any) -> Any:
            with lock:
                if cls not in instances:
                    instances[cls] = super().__new__(klass)
            return instances[cls]

    _Singleton.__name__ = cls.__name__
    _Singleton.__qualname__ = cls.__qualname__
    return cast(Type[_T], _Singleton)


def deprecated(reason: str, since: str = "") -> Callable:
    """Mark a function as deprecated, emitting a warning on first call."""
    def decorator(func: Callable) -> Callable:
        warned = [False]

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            if not warned[0]:
                msg = f"{func.__qualname__} is deprecated"
                if since:
                    msg += f" since {since}"
                msg += f": {reason}"
                logger.warning(msg)
                warned[0] = True
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ColumnSchema:
    """Schema descriptor for a single column."""
    name: str
    dtype: str
    nullable: bool = True
    primary_key: bool = False
    default: Any = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None
    pattern: Optional[str] = None
    enum_values: Optional[List[Any]] = field(default_factory=list)
    description: str = ""

    def __post_init__(self) -> None:
        if self.min_value is not None and self.max_value is not None:
            if self.min_value > self.max_value:
                raise SchemaError(
                    f"Column '{self.name}': min_value > max_value",
                    context={"min": self.min_value, "max": self.max_value},
                )

    def validate_value(self, value: Any) -> List[str]:
        """Return list of violation messages for a given value."""
        violations: List[str] = []
        if value is None or value == "":
            if not self.nullable:
                violations.append(f"Column '{self.name}' is NOT NULL but received null")
            return violations

        if self.min_value is not None:
            try:
                if float(value) < self.min_value:
                    violations.append(
                        f"Column '{self.name}' value {value} < min {self.min_value}"
                    )
            except (TypeError, ValueError):
                pass

        if self.max_value is not None:
            try:
                if float(value) > self.max_value:
                    violations.append(
                        f"Column '{self.name}' value {value} > max {self.max_value}"
                    )
            except (TypeError, ValueError):
                pass

        if self.pattern is not None:
            if not re.fullmatch(self.pattern, str(value)):
                violations.append(
                    f"Column '{self.name}' value '{value}' does not match pattern '{self.pattern}'"
                )

        if self.enum_values:
            if value not in self.enum_values:
                violations.append(
                    f"Column '{self.name}' value '{value}' not in allowed set {self.enum_values}"
                )

        return violations


@dataclass
class DatasetSchema:
    """Schema for an entire dataset."""
    name: str
    version: str = "1.0"
    columns: List[ColumnSchema] = field(default_factory=list)
    strict: bool = False  # If True, reject rows with extra columns
    description: str = ""

    def column_names(self) -> List[str]:
        return [c.name for c in self.columns]

    def get_column(self, name: str) -> Optional[ColumnSchema]:
        for col in self.columns:
            if col.name == name:
                return col
        return None

    def primary_keys(self) -> List[str]:
        return [c.name for c in self.columns if c.primary_key]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatasetSchema":
        columns = [ColumnSchema(**col) for col in data.get("columns", [])]
        return cls(
            name=data["name"],
            version=data.get("version", "1.0"),
            columns=columns,
            strict=data.get("strict", False),
            description=data.get("description", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "columns": [asdict(c) for c in self.columns],
            "strict": self.strict,
            "description": self.description,
        }


@dataclass
class AnomalyRecord:
    """Record of a single detected anomaly."""
    row_index: int
    column: Optional[str]
    anomaly_type: AnomalyType
    description: str
    value: Any = None
    severity: float = 1.0  # 0.0 (low) to 1.0 (high)
    timestamp: datetime.datetime = field(
        default_factory=lambda: datetime.datetime.now(timezone.utc)
    )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "row_index": self.row_index,
            "column": self.column,
            "anomaly_type": self.anomaly_type.value,
            "description": self.description,
            "value": self.value,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
        }


@dataclass
class PipelineMetrics:
    """Counters and timing data collected during a pipeline run."""
    run_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: Optional[datetime.datetime] = None
    end_time: Optional[datetime.datetime] = None
    rows_ingested: int = 0
    rows_valid: int = 0
    rows_invalid: int = 0
    rows_exported: int = 0
    anomalies_detected: int = 0
    bytes_read: int = 0
    bytes_written: int = 0
    stage_durations: Dict[str, float] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def duration_seconds(self) -> Optional[float]:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return None

    @property
    def rows_total(self) -> int:
        return self.rows_valid + self.rows_invalid

    @property
    def validity_rate(self) -> float:
        if self.rows_total == 0:
            return 0.0
        return self.rows_valid / self.rows_total

    def record_stage(self, stage: str, duration: float) -> None:
        self.stage_durations[stage] = duration

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.duration_seconds,
            "rows_ingested": self.rows_ingested,
            "rows_valid": self.rows_valid,
            "rows_invalid": self.rows_invalid,
            "rows_exported": self.rows_exported,
            "anomalies_detected": self.anomalies_detected,
            "bytes_read": self.bytes_read,
            "bytes_written": self.bytes_written,
            "validity_rate": self.validity_rate,
            "stage_durations": self.stage_durations,
            "errors": self.errors,
            "warnings": self.warnings,
        }


@dataclass
class ColumnStatistics:
    """Descriptive statistics for a single column."""
    name: str
    dtype: str
    count: int = 0
    null_count: int = 0
    unique_count: int = 0
    mean: Optional[float] = None
    median: Optional[float] = None
    std_dev: Optional[float] = None
    variance: Optional[float] = None
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    percentile_25: Optional[float] = None
    percentile_75: Optional[float] = None
    top_values: List[Tuple[Any, int]] = field(default_factory=list)

    @property
    def null_rate(self) -> float:
        if self.count == 0:
            return 0.0
        return self.null_count / self.count

    @property
    def fill_rate(self) -> float:
        return 1.0 - self.null_rate

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "dtype": self.dtype,
            "count": self.count,
            "null_count": self.null_count,
            "null_rate": self.null_rate,
            "fill_rate": self.fill_rate,
            "unique_count": self.unique_count,
            "mean": self.mean,
            "median": self.median,
            "std_dev": self.std_dev,
            "variance": self.variance,
            "min_value": self.min_value,
            "max_value": self.max_value,
            "percentile_25": self.percentile_25,
            "percentile_75": self.percentile_75,
            "top_values": self.top_values,
        }


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

class PipelineConfig:
    """
    Centralised configuration store for the analysis pipeline.

    Supports loading from JSON files, environment variable overrides,
    and programmatic construction.
    """

    _DEFAULTS: ClassVar[Dict[str, Any]] = {
        "log_level": "INFO",
        "log_file": None,
        "input_format": "csv",
        "output_format": "json",
        "batch_size": DEFAULT_BATCH_SIZE,
        "chunk_size": DEFAULT_CHUNK_SIZE,
        "encoding": DEFAULT_ENCODING,
        "delimiter": ",",
        "quotechar": '"',
        "null_values": ["", "NULL", "null", "N/A", "NA", "NaN", "nan", "None", "none"],
        "skip_rows": 0,
        "max_errors": 100,
        "deduplicate": False,
        "strict_schema": False,
        "enable_profiling": True,
        "enable_anomaly_detection": True,
        "anomaly_zscore_threshold": 3.0,
        "output_compression": None,
        "temp_dir": None,
        "max_workers": 4,
        "overwrite_output": False,
    }

    def __init__(self, **kwargs: Any) -> None:
        self._data: Dict[str, Any] = dict(self._DEFAULTS)
        self._update(kwargs)

    def _update(self, data: Dict[str, Any]) -> None:
        for key, value in data.items():
            if key in self._DEFAULTS or key.startswith("_"):
                self._data[key] = value
            else:
                logger.debug("Unknown config key '%s' ignored", key)

    def __getattr__(self, name: str) -> Any:
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"PipelineConfig has no attribute '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    @classmethod
    def from_file(cls, path: Union[str, Path]) -> "PipelineConfig":
        """Load configuration from a JSON file."""
        path = Path(path)
        if not path.exists():
            raise ConfigurationError(f"Config file not found: {path}")
        try:
            with path.open(encoding=DEFAULT_ENCODING) as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            raise ConfigurationError(f"Invalid JSON in config file: {exc}") from exc
        instance = cls(**data)
        logger.info("Loaded configuration from %s", path)
        return instance

    @classmethod
    def from_env(cls, prefix: str = "PIPELINE_") -> "PipelineConfig":
        """Build config from environment variables with a given prefix."""
        data: Dict[str, Any] = {}
        for env_key, env_val in os.environ.items():
            if env_key.startswith(prefix):
                config_key = env_key[len(prefix):].lower()
                # Attempt type coercion based on defaults
                if config_key in cls._DEFAULTS:
                    default = cls._DEFAULTS[config_key]
                    if isinstance(default, bool):
                        data[config_key] = env_val.lower() in ("1", "true", "yes")
                    elif isinstance(default, int):
                        with suppress(ValueError):
                            data[config_key] = int(env_val)
                    elif isinstance(default, float):
                        with suppress(ValueError):
                            data[config_key] = float(env_val)
                    elif isinstance(default, list):
                        data[config_key] = [v.strip() for v in env_val.split(",")]
                    else:
                        data[config_key] = env_val
                else:
                    data[config_key] = env_val
        return cls(**data)

    def merge(self, other: "PipelineConfig") -> "PipelineConfig":
        """Return a new config that is the merger of self and other (other wins)."""
        merged = PipelineConfig(**self._data)
        merged._update(other._data)
        return merged

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)

    def save(self, path: Union[str, Path]) -> None:
        """Persist the configuration to a JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding=DEFAULT_ENCODING) as fh:
            json.dump(self._data, fh, indent=2, default=str)
        logger.info("Configuration saved to %s", path)

    def __repr__(self) -> str:
        items = ", ".join(f"{k}={v!r}" for k, v in sorted(self._data.items()))
        return f"PipelineConfig({items})"


# ---------------------------------------------------------------------------
# Schema inference
# ---------------------------------------------------------------------------

class SchemaInferrer:
    """
    Infers a DatasetSchema from a sample of raw rows.

    Uses heuristics to determine likely data types and basic
    constraints for each column.
    """

    _INTEGER_RE = re.compile(r"^-?\d+$")
    _FLOAT_RE = re.compile(r"^-?\d+\.\d*([eE][+-]?\d+)?$|^-?\d*\.\d+([eE][+-]?\d+)?$")
    _DATE_PATTERNS = [
        ("%Y-%m-%d", re.compile(r"^\d{4}-\d{2}-\d{2}$")),
        ("%d/%m/%Y", re.compile(r"^\d{2}/\d{2}/\d{4}$")),
        ("%m/%d/%Y", re.compile(r"^\d{2}/\d{2}/\d{4}$")),
        ("%Y%m%d", re.compile(r"^\d{8}$")),
    ]
    _BOOL_TRUE = frozenset({"true", "yes", "1", "t", "y"})
    _BOOL_FALSE = frozenset({"false", "no", "0", "f", "n"})

    def __init__(self, sample_size: int = 500, null_tokens: Optional[List[str]] = None) -> None:
        self.sample_size = sample_size
        self.null_tokens: FrozenSet[str] = frozenset(
            null_tokens or ["", "null", "NULL", "N/A", "NA", "NaN", "nan", "None"]
        )

    def infer(self, rows: List[Dict[str, Any]], name: str = "inferred") -> DatasetSchema:
        """
        Infer schema from a list of row dictionaries.

        Args:
            rows: Sample rows as dicts.
            name: Name to assign to the resulting schema.

        Returns:
            DatasetSchema with inferred column definitions.
        """
        if not rows:
            raise SchemaError("Cannot infer schema from empty row set")

        # Collect all column names preserving first-seen order
        all_cols: List[str] = list(dict.fromkeys(k for row in rows for k in row))
        sample = rows[: self.sample_size]

        columns = [self._infer_column(col, sample) for col in all_cols]
        return DatasetSchema(name=name, columns=columns, description="Auto-inferred schema")

    def _infer_column(self, name: str, rows: List[Dict[str, Any]]) -> ColumnSchema:
        """Infer ColumnSchema for a single column."""
        values = [row.get(name) for row in rows]
        non_null = [v for v in values if v is not None and str(v) not in self.null_tokens]
        null_count = len(values) - len(non_null)
        nullable = null_count > 0

        dtype = self._guess_dtype(non_null)
        schema = ColumnSchema(
            name=name,
            dtype=dtype,
            nullable=nullable,
            description=f"Auto-inferred as {dtype}",
        )

        if dtype in ("integer", "float") and non_null:
            try:
                nums = [float(v) for v in non_null]
                schema.min_value = min(nums)
                schema.max_value = max(nums)
            except (TypeError, ValueError):
                pass

        return schema

    def _guess_dtype(self, values: List[Any]) -> str:
        if not values:
            return "string"
        str_vals = [str(v).strip() for v in values]

        if all(self._INTEGER_RE.fullmatch(v) for v in str_vals):
            return "integer"
        if all(self._FLOAT_RE.fullmatch(v) for v in str_vals):
            return "float"
        if all(v.lower() in (self._BOOL_TRUE | self._BOOL_FALSE) for v in str_vals):
            return "boolean"
        for fmt, pattern in self._DATE_PATTERNS:
            if all(pattern.fullmatch(v) for v in str_vals):
                return "date"
        return "string"


# ---------------------------------------------------------------------------
# Data readers
# ---------------------------------------------------------------------------

class BaseReader(ABC):
    """Abstract base class for all data readers."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self._bytes_read: int = 0

    @abstractmethod
    def read(self, path: Union[str, Path]) -> Iterator[Dict[str, Any]]:
        """Yield rows as dictionaries from the given path."""
        ...

    @abstractmethod
    def supports_format(self, fmt: FileFormat) -> bool:
        """Return True if this reader supports the given format."""
        ...

    @property
    def bytes_read(self) -> int:
        return self._bytes_read

    def _open(self, path: Path) -> io.IOBase:
        """Open a file, transparently decompressing .gz files."""
        if path.suffix == ".gz":
            return gzip.open(str(path), "rt", encoding=self.config.encoding)
        return path.open("r", encoding=self.config.encoding)


class CsvReader(BaseReader):
    """Reads CSV and TSV files into row dictionaries."""

    def supports_format(self, fmt: FileFormat) -> bool:
        return fmt in (FileFormat.CSV, FileFormat.TSV)

    @timed
    def read(self, path: Union[str, Path]) -> Iterator[Dict[str, Any]]:
        """
        Yield rows from a CSV/TSV file.

        Handles BOM markers, configurable delimiters, and blank row skipping.
        """
        path = Path(path)
        if not path.exists():
            raise IngestError(f"File not found: {path}")

        delimiter = "\t" if path.suffix == ".tsv" else self.config.delimiter
        skip = self.config.skip_rows

        with self._open(path) as fh:
            # Skip leading non-data rows
            for _ in range(skip):
                next(fh, None)

            reader = csv.DictReader(
                fh,
                delimiter=delimiter,
                quotechar=self.config.quotechar,
            )
            for row in reader:
                self._bytes_read += sum(
                    len(str(v)) for v in row.values() if v is not None
                )
                # Normalise null tokens
                cleaned = {
                    k: (None if v in self.config.null_values else v)
                    for k, v in row.items()
                }
                yield cleaned


class JsonReader(BaseReader):
    """Reads JSON and JSONL (newline-delimited JSON) files."""

    def supports_format(self, fmt: FileFormat) -> bool:
        return fmt in (FileFormat.JSON, FileFormat.JSONL)

    @timed
    def read(self, path: Union[str, Path]) -> Iterator[Dict[str, Any]]:
        path = Path(path)
        if not path.exists():
            raise IngestError(f"File not found: {path}")

        fmt = FileFormat.from_path(path)

        with self._open(path) as fh:
            if fmt == FileFormat.JSONL:
                yield from self._read_jsonl(fh)
            else:
                yield from self._read_json(fh)

    def _read_json(self, fh: io.IOBase) -> Iterator[Dict[str, Any]]:
        try:
            data = json.load(fh)  # type: ignore[arg-type]
        except json.JSONDecodeError as exc:
            raise IngestError(f"Malformed JSON: {exc}") from exc

        if isinstance(data, list):
            for item in data:
                if isinstance(item, dict):
                    self._bytes_read += len(json.dumps(item))
                    yield item
        elif isinstance(data, dict):
            # Might be {"data": [...]} envelope
            for key in ("data", "records", "rows", "items"):
                if key in data and isinstance(data[key], list):
                    yield from self._read_json(io.StringIO(json.dumps(data[key])))
                    return
            self._bytes_read += len(json.dumps(data))
            yield data
        else:
            raise IngestError("JSON root must be an array or object")

    def _read_jsonl(self, fh: io.IOBase) -> Iterator[Dict[str, Any]]:
        for lineno, line in enumerate(fh, 1):  # type: ignore[arg-type]
            line = line.strip()  # type: ignore[union-attr]
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise IngestError(
                    f"Malformed JSON on line {lineno}: {exc}"
                ) from exc
            if isinstance(obj, dict):
                self._bytes_read += len(line)
                yield obj


class ReaderRegistry:
    """Registry mapping FileFormats to BaseReader implementations."""

    def __init__(self, config: PipelineConfig) -> None:
        self._config = config
        self._readers: Dict[FileFormat, BaseReader] = {}
        self._register_defaults()

    def _register_defaults(self) -> None:
        csv_reader = CsvReader(self._config)
        json_reader = JsonReader(self._config)

        for fmt in FileFormat:
            if csv_reader.supports_format(fmt):
                self._readers[fmt] = csv_reader
            elif json_reader.supports_format(fmt):
                self._readers[fmt] = json_reader

    def register(self, fmt: FileFormat, reader: BaseReader) -> None:
        self._readers[fmt] = reader

    def get(self, fmt: FileFormat) -> BaseReader:
        reader = self._readers.get(fmt)
        if reader is None:
            raise IngestError(f"No reader registered for format: {fmt}")
        return reader

    def read(self, path: Union[str, Path]) -> Iterator[Dict[str, Any]]:
        path = Path(path)
        fmt = FileFormat.from_path(path)
        return self.get(fmt).read(path)


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

class RowValidator:
    """
    Validates individual rows against a DatasetSchema.

    Accumulates violation records and tracks row-level pass/fail statistics.
    """

    def __init__(self, schema: DatasetSchema, config: PipelineConfig) -> None:
        self.schema = schema
        self.config = config
        self._violations: List[Dict[str, Any]] = []
        self._pass_count: int = 0
        self._fail_count: int = 0

    @property
    def violations(self) -> List[Dict[str, Any]]:
        return list(self._violations)

    @property
    def pass_rate(self) -> float:
        total = self._pass_count + self._fail_count
        return self._pass_count / total if total > 0 else 0.0

    def validate_row(self, row: Dict[str, Any], index: int) -> bool:
        """
        Validate a single row. Returns True if the row passes all checks.

        Args:
            row: The row data as a dictionary.
            index: Zero-based row index for error reporting.

        Returns:
            True if valid, False if any violations were found.
        """
        row_violations: List[str] = []

        # Check for unexpected columns in strict mode
        if self.config.strict_schema:
            expected = set(self.schema.column_names())
            extra = set(row.keys()) - expected
            if extra:
                row_violations.append(f"Unexpected columns: {sorted(extra)}")

        # Validate each column
        for col_schema in self.schema.columns:
            value = row.get(col_schema.name, MISSING_VALUE_SENTINEL)
            if value is MISSING_VALUE_SENTINEL:
                if not col_schema.nullable:
                    row_violations.append(
                        f"Required column '{col_schema.name}' is missing"
                    )
                continue
            violations = col_schema.validate_value(value)
            row_violations.extend(violations)

        if row_violations:
            self._fail_count += 1
            self._violations.append({
                "row_index": index,
                "violations": row_violations,
            })
            if len(self._violations) > self.config.max_errors:
                raise ValidationError(
                    f"Exceeded max_errors limit ({self.config.max_errors})",
                    context={"row_index": index},
                )
            return False

        self._pass_count += 1
        return True

    def summary(self) -> Dict[str, Any]:
        return {
            "pass_count": self._pass_count,
            "fail_count": self._fail_count,
            "pass_rate": self.pass_rate,
            "violation_count": len(self._violations),
        }

    def reset(self) -> None:
        self._violations.clear()
        self._pass_count = 0
        self._fail_count = 0


# ---------------------------------------------------------------------------
# Transformations
# ---------------------------------------------------------------------------

class BaseTransform(ABC):
    """Abstract base class for row-level transformations."""

    name: ClassVar[str] = "base"

    @abstractmethod
    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Apply the transformation to a row.

        Args:
            row: Input row dictionary.

        Returns:
            Transformed row, or None to drop the row.
        """
        ...

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"


class CastTypesTransform(BaseTransform):
    """Casts column values to their schema-declared types."""

    name = "cast_types"

    _CAST_MAP: ClassVar[Dict[str, Callable[[Any], Any]]] = {
        "integer": int,
        "float": float,
        "boolean": lambda v: str(v).lower() in ("true", "yes", "1", "t", "y"),
        "string": str,
        "date": lambda v: datetime.datetime.strptime(str(v), DATE_FORMAT_ISO).date(),
        "datetime": lambda v: datetime.datetime.fromisoformat(str(v)),
    }

    def __init__(self, schema: DatasetSchema) -> None:
        self.schema = schema

    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = dict(row)
        for col in self.schema.columns:
            if col.name not in result or result[col.name] is None:
                continue
            cast_fn = self._CAST_MAP.get(col.dtype)
            if cast_fn is None:
                continue
            try:
                result[col.name] = cast_fn(result[col.name])
            except (ValueError, TypeError, OverflowError):
                # Leave as-is; validator will catch type mismatches
                pass
        return result


class FillDefaultsTransform(BaseTransform):
    """Fills null values with schema-declared defaults."""

    name = "fill_defaults"

    def __init__(self, schema: DatasetSchema) -> None:
        self.schema = schema

    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = dict(row)
        for col in self.schema.columns:
            if col.default is None:
                continue
            val = result.get(col.name)
            if val is None or val == "":
                result[col.name] = col.default
        return result


class NormaliseStringsTransform(BaseTransform):
    """Strips whitespace and optionally lowercases string columns."""

    name = "normalise_strings"

    def __init__(self, lowercase: bool = False, strip_chars: Optional[str] = None) -> None:
        self.lowercase = lowercase
        self.strip_chars = strip_chars

    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result: Dict[str, Any] = {}
        for key, val in row.items():
            if isinstance(val, str):
                val = val.strip(self.strip_chars) if self.strip_chars else val.strip()
                if self.lowercase:
                    val = val.lower()
            result[key] = val
        return result


class DropColumnsTransform(BaseTransform):
    """Removes specified columns from each row."""

    name = "drop_columns"

    def __init__(self, columns: List[str]) -> None:
        self.columns: Set[str] = set(columns)

    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {k: v for k, v in row.items() if k not in self.columns}


class RenameColumnsTransform(BaseTransform):
    """Renames columns according to a mapping."""

    name = "rename_columns"

    def __init__(self, mapping: Dict[str, str]) -> None:
        self.mapping = mapping

    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return {self.mapping.get(k, k): v for k, v in row.items()}


class ComputedColumnTransform(BaseTransform):
    """Adds a new column derived by applying a function to existing columns."""

    name = "computed_column"

    def __init__(self, new_column: str, func: Callable[[Dict[str, Any]], Any]) -> None:
        self.new_column = new_column
        self.func = func

    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        result = dict(row)
        try:
            result[self.new_column] = self.func(row)
        except Exception as exc:  # noqa: BLE001
            logger.debug(
                "ComputedColumnTransform failed for column '%s': %s",
                self.new_column, exc,
            )
            result[self.new_column] = None
        return result


class FilterRowsTransform(BaseTransform):
    """Drops rows that do not satisfy a predicate."""

    name = "filter_rows"

    def __init__(self, predicate: Callable[[Dict[str, Any]], bool]) -> None:
        self.predicate = predicate

    def transform(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return row if self.predicate(row) else None


class TransformPipeline:
    """
    Ordered sequence of BaseTransform steps applied to each row.

    Provides statistics on how many rows each step dropped.
    """

    def __init__(self, transforms: Optional[List[BaseTransform]] = None) -> None:
        self._transforms: List[BaseTransform] = list(transforms or [])
        self._drop_counts: Counter = Counter()

    def add(self, transform: BaseTransform) -> "TransformPipeline":
        self._transforms.append(transform)
        return self

    def apply(self, row: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Apply all transforms in order. Returns None if any step drops the row."""
        current: Optional[Dict[str, Any]] = row
        for t in self._transforms:
            if current is None:
                break
            current = t.transform(current)
            if current is None:
                self._drop_counts[t.name] += 1
        return current

    def apply_batch(
        self, rows: Iterable[Dict[str, Any]]
    ) -> Iterator[Dict[str, Any]]:
        """Apply the pipeline to an iterable of rows, yielding non-dropped rows."""
        for row in rows:
            result = self.apply(row)
            if result is not None:
                yield result

    @property
    def drop_statistics(self) -> Dict[str, int]:
        return dict(self._drop_counts)

    def __len__(self) -> int:
        return len(self._transforms)

    def __repr__(self) -> str:
        names = [t.name for t in self._transforms]
        return f"TransformPipeline(steps={names})"


# ---------------------------------------------------------------------------
# Statistical profiler
# ---------------------------------------------------------------------------

class DataProfiler:
    """
    Computes per-column descriptive statistics from a batch of rows.

    Processes data in streaming fashion to avoid loading entire dataset
    into memory at once.
    """

    def __init__(self, top_n: int = 10) -> None:
        self.top_n = top_n
        self._column_data: Dict[str, List[Any]] = defaultdict(list)
        self._column_counts: Counter = Counter()
        self._null_counts: Counter = Counter()

    def feed(self, row: Dict[str, Any]) -> None:
        """Add a single row to the profiler's internal buffers."""
        for col, val in row.items():
            self._column_counts[col] += 1
            if val is None:
                self._null_counts[col] += 1
            else:
                self._column_data[col].append(val)

    def feed_batch(self, rows: Iterable[Dict[str, Any]]) -> None:
        """Feed multiple rows."""
        for row in rows:
            self.feed(row)

    def compute(self) -> Dict[str, ColumnStatistics]:
        """Compute and return statistics for all columns seen so far."""
        result: Dict[str, ColumnStatistics] = {}

        for col_name in self._column_counts:
            total = self._column_counts[col_name]
            null_count = self._null_counts.get(col_name, 0)
            values = self._column_data[col_name]
            unique_count = len(set(values))
            dtype = self._infer_dtype(values)

            stats = ColumnStatistics(
                name=col_name,
                dtype=dtype,
                count=total,
                null_count=null_count,
                unique_count=unique_count,
            )

            if dtype in ("integer", "float") and values:
                try:
                    nums = [float(v) for v in values if v is not None]
                    if nums:
                        sorted_nums = sorted(nums)
                        stats.min_value = sorted_nums[0]
                        stats.max_value = sorted_nums[-1]
                        stats.mean = statistics.mean(nums)
                        stats.median = statistics.median(nums)
                        if len(nums) >= 2:
                            stats.std_dev = statistics.stdev(nums)
                            stats.variance = statistics.variance(nums)
                        n = len(sorted_nums)
                        stats.percentile_25 = sorted_nums[max(0, int(0.25 * n) - 1)]
                        stats.percentile_75 = sorted_nums[max(0, int(0.75 * n) - 1)]
                except (TypeError, ValueError, statistics.StatisticsError):
                    pass
            elif values:
                counter = Counter(values)
                stats.top_values = counter.most_common(self.top_n)
                if values:
                    stats.min_value = min(str(v) for v in values)
                    stats.max_value = max(str(v) for v in values)

            result[col_name] = stats

        return result

    @staticmethod
    def _infer_dtype(values: List[Any]) -> str:
        if not values:
            return "unknown"
        if all(isinstance(v, int) for v in values):
            return "integer"
        if all(isinstance(v, (int, float)) for v in values):
            return "float"
        if all(isinstance(v, bool) for v in values):
            return "boolean"
        if all(isinstance(v, datetime.date) for v in values):
            return "date"
        return "string"

    def reset(self) -> None:
        self._column_data.clear()
        self._column_counts.clear()
        self._null_counts.clear()


# ---------------------------------------------------------------------------
# Anomaly detector
# ---------------------------------------------------------------------------

class AnomalyDetector:
    """
    Detects various categories of anomalies in row data.

    Implements Z-score based outlier detection for numeric columns
    and pattern-based checks for string columns.
    """

    def __init__(
        self,
        config: PipelineConfig,
        schema: Optional[DatasetSchema] = None,
    ) -> None:
        self.config = config
        self.schema = schema
        self._seen_keys: Set[str] = set()
        self._anomalies: List[AnomalyRecord] = []
        self._column_stats: Dict[str, Dict[str, float]] = {}

    def fit(self, rows: List[Dict[str, Any]]) -> None:
        """
        Compute per-column mean and std from a training set of rows.

        Must be called before detect() for outlier detection to work.
        """
        column_values: Dict[str, List[float]] = defaultdict(list)
        for row in rows:
            for col, val in row.items():
                with suppress(TypeError, ValueError):
                    column_values[col].append(float(val))  # type: ignore[arg-type]

        for col, nums in column_values.items():
            if len(nums) >= 2:
                mu = statistics.mean(nums)
                sigma = statistics.stdev(nums)
                self._column_stats[col] = {"mean": mu, "std": max(sigma, 1e-9)}
            elif len(nums) == 1:
                self._column_stats[col] = {"mean": nums[0], "std": 1e-9}

        logger.debug("AnomalyDetector fitted on %d rows, %d columns", len(rows), len(self._column_stats))

    def detect(self, row: Dict[str, Any], index: int) -> List[AnomalyRecord]:
        """
        Run anomaly checks on a single row.

        Args:
            row: Row data dictionary.
            index: Row index for reporting.

        Returns:
            List of AnomalyRecord objects for any detected anomalies.
        """
        found: List[AnomalyRecord] = []

        # Missing value check
        if self.schema:
            for col in self.schema.columns:
                if not col.nullable and (row.get(col.name) is None):
                    found.append(AnomalyRecord(
                        row_index=index,
                        column=col.name,
                        anomaly_type=AnomalyType.MISSING,
                        description=f"Non-nullable column '{col.name}' is null",
                        severity=0.9,
                    ))

        # Outlier detection via Z-score
        threshold = self.config.anomaly_zscore_threshold
        for col, stat in self._column_stats.items():
            val = row.get(col)
            if val is None:
                continue
            try:
                fval = float(val)  # type: ignore[arg-type]
                zscore = abs((fval - stat["mean"]) / stat["std"])
                if zscore > threshold:
                    found.append(AnomalyRecord(
                        row_index=index,
                        column=col,
                        anomaly_type=AnomalyType.OUTLIER,
                        description=(
                            f"Value {fval:.4g} has Z-score {zscore:.2f} "
                            f"(threshold={threshold})"
                        ),
                        value=fval,
                        severity=min(1.0, (zscore - threshold) / threshold),
                    ))
            except (TypeError, ValueError):
                pass

        self._anomalies.extend(found)
        return found

    def check_duplicate(self, row: Dict[str, Any], index: int, key_columns: List[str]) -> bool:
        """
        Check whether the row is a duplicate based on key_columns.

        Returns True if the row is a duplicate.
        """
        key = tuple(row.get(col) for col in key_columns)
        key_str = json.dumps(key, default=str)
        hashed = hashlib.sha256(key_str.encode()).hexdigest()
        if hashed in self._seen_keys:
            self._anomalies.append(AnomalyRecord(
                row_index=index,
                column=None,
                anomaly_type=AnomalyType.DUPLICATE,
                description=f"Duplicate key {key}",
                severity=0.8,
            ))
            return True
        self._seen_keys.add(hashed)
        return False

    @property
    def anomalies(self) -> List[AnomalyRecord]:
        return list(self._anomalies)

    def summary(self) -> Dict[str, Any]:
        by_type: Counter = Counter(a.anomaly_type.value for a in self._anomalies)
        return {
            "total": len(self._anomalies),
            "by_type": dict(by_type),
            "high_severity": sum(1 for a in self._anomalies if a.severity >= 0.8),
        }

    def reset(self) -> None:
        self._anomalies.clear()
        self._seen_keys.clear()


# ---------------------------------------------------------------------------
# Aggregator
# ---------------------------------------------------------------------------

class Aggregator:
    """
    Groups rows by a key column and applies aggregation functions.

    Supports a configurable set of AggregationMethod values per target column.
    """

    def __init__(
        self,
        group_by: List[str],
        aggregations: Dict[str, List[AggregationMethod]],
    ) -> None:
        if not group_by:
            raise ConfigurationError("Aggregator requires at least one group_by column")
        self.group_by = group_by
        self.aggregations = aggregations
        self._groups: Dict[Tuple, List[Dict[str, Any]]] = defaultdict(list)

    def feed(self, row: Dict[str, Any]) -> None:
        key = tuple(row.get(col) for col in self.group_by)
        self._groups[key].append(row)

    def feed_batch(self, rows: Iterable[Dict[str, Any]]) -> None:
        for row in rows:
            self.feed(row)

    def compute(self) -> List[Dict[str, Any]]:
        """Compute and return aggregated rows."""
        result: List[Dict[str, Any]] = []

        for key, group_rows in self._groups.items():
            agg_row: Dict[str, Any] = dict(zip(self.group_by, key))

            for col, methods in self.aggregations.items():
                values = [r.get(col) for r in group_rows if r.get(col) is not None]
                nums: List[float] = []
                with suppress(TypeError, ValueError):
                    nums = [float(v) for v in values]  # type: ignore[arg-type]

                for method in methods:
                    out_key = f"{col}_{method.value}"
                    agg_row[out_key] = self._apply_method(method, values, nums)

            result.append(agg_row)

        return result

    @staticmethod
    def _apply_method(
        method: AggregationMethod,
        values: List[Any],
        nums: List[float],
    ) -> Any:
        if method == AggregationMethod.COUNT:
            return len(values)
        if method == AggregationMethod.FIRST:
            return values[0] if values else None
        if method == AggregationMethod.LAST:
            return values[-1] if values else None
        if not nums:
            return None
        if method == AggregationMethod.SUM:
            return sum(nums)
        if method == AggregationMethod.MEAN:
            return statistics.mean(nums)
        if method == AggregationMethod.MEDIAN:
            return statistics.median(nums)
        if method == AggregationMethod.MIN:
            return min(nums)
        if method == AggregationMethod.MAX:
            return max(nums)
        if method == AggregationMethod.STD:
            return statistics.stdev(nums) if len(nums) >= 2 else 0.0
        if method == AggregationMethod.VAR:
            return statistics.variance(nums) if len(nums) >= 2 else 0.0
        if method == AggregationMethod.MODE:
            try:
                return statistics.mode(nums)
            except statistics.StatisticsError:
                return None
        return None

    def reset(self) -> None:
        self._groups.clear()

    def group_count(self) -> int:
        return len(self._groups)


# ---------------------------------------------------------------------------
# Writers / Exporters
# ---------------------------------------------------------------------------

class BaseWriter(ABC):
    """Abstract base class for output writers."""

    def __init__(self, config: PipelineConfig) -> None:
        self.config = config
        self._bytes_written: int = 0
        self._rows_written: int = 0

    @abstractmethod
    def write(self, rows: Iterable[Dict[str, Any]], path: Union[str, Path]) -> None:
        """Write rows to the given path."""
        ...

    @property
    def bytes_written(self) -> int:
        return self._bytes_written

    @property
    def rows_written(self) -> int:
        return self._rows_written

    def _ensure_parent(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)


class CsvWriter(BaseWriter):
    """Writes rows to a CSV file."""

    def write(self, rows: Iterable[Dict[str, Any]], path: Union[str, Path]) -> None:
        path = Path(path)
        self._ensure_parent(path)

        if path.exists() and not self.config.overwrite_output:
            raise ExportError(f"Output file exists and overwrite_output=False: {path}")

        row_iter = iter(rows)
        try:
            first = next(row_iter)
        except StopIteration:
            logger.warning("No rows to write to %s", path)
            return

        with path.open("w", newline="", encoding=self.config.encoding) as fh:
            writer = csv.DictWriter(
                fh,
                fieldnames=list(first.keys()),
                delimiter=self.config.delimiter,
                quotechar=self.config.quotechar,
                extrasaction="ignore",
            )
            writer.writeheader()
            writer.writerow(first)
            self._rows_written += 1
            for row in row_iter:
                writer.writerow(row)
                self._rows_written += 1
            self._bytes_written = fh.tell()

        logger.info("Wrote %d rows to %s", self._rows_written, path)


class JsonWriter(BaseWriter):
    """Writes rows to a JSON or JSONL file."""

    def write(self, rows: Iterable[Dict[str, Any]], path: Union[str, Path]) -> None:
        path = Path(path)
        self._ensure_parent(path)

        if path.exists() and not self.config.overwrite_output:
            raise ExportError(f"Output file exists and overwrite_output=False: {path}")

        fmt = FileFormat.from_path(path)

        with path.open("w", encoding=self.config.encoding) as fh:
            if fmt == FileFormat.JSONL:
                for row in rows:
                    line = json.dumps(row, default=str) + "\n"
                    fh.write(line)
                    self._bytes_written += len(line)
                    self._rows_written += 1
            else:
                all_rows = list(rows)
                text = json.dumps(all_rows, indent=2, default=str)
                fh.write(text)
                self._bytes_written = len(text.encode(self.config.encoding))
                self._rows_written = len(all_rows)

        logger.info("Wrote %d rows to %s", self._rows_written, path)


class WriterRegistry:
    """Registry mapping FileFormats to BaseWriter implementations."""

    def __init__(self, config: PipelineConfig) -> None:
        self._config = config
        self._writers: Dict[FileFormat, BaseWriter] = {
            FileFormat.CSV: CsvWriter(config),
            FileFormat.TSV: CsvWriter(config),
            FileFormat.JSON: JsonWriter(config),
            FileFormat.JSONL: JsonWriter(config),
        }

    def register(self, fmt: FileFormat, writer: BaseWriter) -> None:
        self._writers[fmt] = writer

    def get(self, fmt: FileFormat) -> BaseWriter:
        writer = self._writers.get(fmt)
        if writer is None:
            raise ExportError(f"No writer registered for format: {fmt}")
        return writer

    def write(self, rows: Iterable[Dict[str, Any]], path: Union[str, Path]) -> None:
        path = Path(path)
        fmt = FileFormat.from_path(path)
        self.get(fmt).write(rows, path)


# ---------------------------------------------------------------------------
# Report generator
# ---------------------------------------------------------------------------

class ReportGenerator:
    """
    Builds a structured pipeline run report from metrics, profiling data,
    anomaly summaries, and validation results.
    """

    def __init__(
        self,
        metrics: PipelineMetrics,
        column_stats: Optional[Dict[str, ColumnStatistics]] = None,
        anomaly_summary: Optional[Dict[str, Any]] = None,
        validation_summary: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.metrics = metrics
        self.column_stats = column_stats or {}
        self.anomaly_summary = anomaly_summary or {}
        self.validation_summary = validation_summary or {}

    def build(self) -> Dict[str, Any]:
        """Assemble and return the complete report as a dictionary."""
        return {
            "report_version": "1.0",
            "generated_at": datetime.datetime.now(timezone.utc).isoformat(),
            "pipeline_version": __version__,
            "run": self.metrics.to_dict(),
            "validation": self.validation_summary,
            "anomalies": self.anomaly_summary,
            "columns": {
                name: stats.to_dict()
                for name, stats in self.column_stats.items()
            },
        }

    def save_json(self, path: Union[str, Path]) -> None:
        """Write the report to a JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        report = self.build()
        with path.open("w", encoding=DEFAULT_ENCODING) as fh:
            json.dump(report, fh, indent=2, default=str)
        logger.info("Report saved to %s", path)

    def print_summary(self) -> None:
        """Print a human-readable summary to stdout."""
        m = self.metrics
        lines = [
            "",
            "=" * 60,
            f"  Pipeline Run Summary  (run_id={m.run_id[:8]}...)",
            "=" * 60,
            f"  Status      : {PipelineStatus.SUCCESS.value if not m.errors else PipelineStatus.PARTIAL.value}",
            f"  Duration    : {m.duration_seconds:.2f}s" if m.duration_seconds else "  Duration    : N/A",
            f"  Rows in     : {m.rows_ingested:,}",
            f"  Rows valid  : {m.rows_valid:,}",
            f"  Rows invalid: {m.rows_invalid:,}",
            f"  Rows out    : {m.rows_exported:,}",
            f"  Validity    : {m.validity_rate:.1%}",
            f"  Anomalies   : {m.anomalies_detected:,}",
            f"  Bytes in    : {_fmt_bytes(m.bytes_read)}",
            f"  Bytes out   : {_fmt_bytes(m.bytes_written)}",
        ]
        if m.stage_durations:
            lines.append("  Stage times :")
            for stage, dur in m.stage_durations.items():
                lines.append(f"    {stage:<20} {dur:.3f}s")
        if m.errors:
            lines.append(f"  Errors      : {len(m.errors)}")
            for err in m.errors[:5]:
                lines.append(f"    - {err}")
        lines.append("=" * 60)
        print("\n".join(lines))


# ---------------------------------------------------------------------------
# Utility functions
# ---------------------------------------------------------------------------

def _fmt_bytes(n: int) -> str:
    """Format a byte count as a human-readable string."""
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n //= 1024
    return f"{n:.1f} PB"


def deep_merge(base: Dict, override: Dict) -> Dict:
    """
    Recursively merge two dicts, with override values winning on conflicts.

    Nested dicts are merged rather than replaced.
    """
    result = dict(base)
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def flatten_dict(d: Dict[str, Any], sep: str = ".", prefix: str = "") -> Dict[str, Any]:
    """
    Flatten a nested dictionary into a single-level dict with composite keys.

    Example:
        {"a": {"b": 1}} -> {"a.b": 1}
    """
    items: Dict[str, Any] = {}
    for k, v in d.items():
        full_key = f"{prefix}{sep}{k}" if prefix else k
        if isinstance(v, dict):
            items.update(flatten_dict(v, sep=sep, prefix=full_key))
        else:
            items[full_key] = v
    return items


def unflatten_dict(d: Dict[str, Any], sep: str = ".") -> Dict[str, Any]:
    """Reverse of flatten_dict: restore a flat dict to nested form."""
    result: Dict[str, Any] = {}
    for compound_key, val in d.items():
        parts = compound_key.split(sep)
        node = result
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = val
    return result


def chunk_iterable(iterable: Iterable[_T], size: int) -> Iterator[List[_T]]:
    """Yield successive chunks of `size` from `iterable`."""
    iterator = iter(iterable)
    while True:
        batch = list(itertools.islice(iterator, size))
        if not batch:
            break
        yield batch


def safe_cast(value: Any, target_type: Type[_T], default: Optional[_T] = None) -> Optional[_T]:
    """Attempt type conversion, returning default on failure."""
    try:
        return target_type(value)  # type: ignore[call-arg]
    except (TypeError, ValueError, OverflowError):
        return default


def parse_iso_datetime(value: str) -> Optional[datetime.datetime]:
    """Parse an ISO 8601 datetime string, returning None on failure."""
    for fmt in (
        DATETIME_FORMAT_FULL,
        DATETIME_FORMAT_ISO,
        DATE_FORMAT_ISO,
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d %H:%M:%S",
    ):
        with suppress(ValueError):
            return datetime.datetime.strptime(value, fmt)
    return None


def truncate_string(s: str, max_len: int = 80, ellipsis: str = "...") -> str:
    """Return s truncated to max_len characters with ellipsis suffix."""
    if len(s) <= max_len:
        return s
    return s[: max_len - len(ellipsis)] + ellipsis


def compute_checksum(data: Union[str, bytes], algorithm: str = "sha256") -> str:
    """Compute a hex digest checksum of the given data."""
    if isinstance(data, str):
        data = data.encode(DEFAULT_ENCODING)
    h = hashlib.new(algorithm)
    h.update(data)
    return h.hexdigest()


def load_json_file(path: Union[str, Path]) -> Any:
    """Load and return parsed JSON from a file path."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open(encoding=DEFAULT_ENCODING) as fh:
        return json.load(fh)


def save_json_file(data: Any, path: Union[str, Path], indent: int = 2) -> None:
    """Save data to a JSON file, creating parent directories as needed."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding=DEFAULT_ENCODING) as fh:
        json.dump(data, fh, indent=indent, default=str)


@contextmanager
def temp_directory(suffix: Optional[str] = None) -> Generator[Path, None, None]:
    """Context manager providing a temporary directory that is cleaned up on exit."""
    tmp = Path(tempfile.mkdtemp(suffix=suffix))
    try:
        yield tmp
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


@contextmanager
def timer(label: str = "") -> Generator[Dict[str, float], None, None]:
    """
    Context manager that measures elapsed time.

    Usage:
        with timer("my_operation") as t:
            ...
        print(t["elapsed"])
    """
    info: Dict[str, float] = {}
    start = time.perf_counter()
    try:
        yield info
    finally:
        info["elapsed"] = time.perf_counter() - start
        if label:
            logger.debug("%s took %.4fs", label, info["elapsed"])


def percentile(data: List[float], p: float) -> float:
    """
    Compute the p-th percentile of a list of floats.

    Uses linear interpolation between adjacent ranks.

    Args:
        data: List of numeric values.
        p: Percentile in range [0, 100].

    Returns:
        The p-th percentile value.

    Raises:
        ValueError: If data is empty or p is out of range.
    """
    if not data:
        raise ValueError("Cannot compute percentile of empty list")
    if not 0 <= p <= 100:
        raise ValueError(f"Percentile p must be in [0, 100], got {p}")
    sorted_data = sorted(data)
    n = len(sorted_data)
    index = (p / 100) * (n - 1)
    lower = int(index)
    upper = lower + 1
    if upper >= n:
        return sorted_data[-1]
    fraction = index - lower
    return sorted_data[lower] + fraction * (sorted_data[upper] - sorted_data[lower])


def moving_average(values: List[float], window: int) -> List[float]:
    """
    Compute a simple moving average over a list of values.

    Args:
        values: Input numeric series.
        window: Window size (must be >= 1).

    Returns:
        List of averaged values; length equals len(values) - window + 1.
    """
    if window < 1:
        raise ValueError("Window size must be at least 1")
    if len(values) < window:
        return []
    result: List[float] = []
    window_sum = sum(values[:window])
    result.append(window_sum / window)
    for i in range(window, len(values)):
        window_sum += values[i] - values[i - window]
        result.append(window_sum / window)
    return result


def normalise_numeric(values: List[float], method: str = "minmax") -> List[float]:
    """
    Normalise a list of floats.

    Args:
        values: Input data.
        method: "minmax" scales to [0, 1]; "zscore" standardises to mean=0, std=1.

    Returns:
        Normalised values.
    """
    if not values:
        return []
    if method == "minmax":
        lo, hi = min(values), max(values)
        rng = hi - lo
        if rng == 0:
            return [0.0] * len(values)
        return [(v - lo) / rng for v in values]
    if method == "zscore":
        mu = statistics.mean(values)
        if len(values) >= 2:
            sigma = statistics.stdev(values)
        else:
            sigma = 1.0
        if sigma == 0:
            return [0.0] * len(values)
        return [(v - mu) / sigma for v in values]
    raise ValueError(f"Unknown normalisation method: {method!r}")


def group_by(
    rows: Iterable[Dict[str, Any]],
    key: Union[str, Callable[[Dict[str, Any]], Any]],
) -> Dict[Any, List[Dict[str, Any]]]:
    """Group an iterable of row dicts by a column name or key function."""
    groups: Dict[Any, List[Dict[str, Any]]] = defaultdict(list)
    key_fn = (lambda r: r.get(key)) if isinstance(key, str) else key
    for row in rows:
        groups[key_fn(row)].append(row)
    return dict(groups)


def deduplicate_rows(
    rows: List[Dict[str, Any]],
    key_columns: List[str],
    keep: str = "first",
) -> List[Dict[str, Any]]:
    """
    Remove duplicate rows based on specified key columns.

    Args:
        rows: Input rows.
        key_columns: Columns that together form the deduplication key.
        keep: "first" keeps the first occurrence; "last" keeps the final.

    Returns:
        Deduplicated row list.
    """
    seen: Dict[Tuple, int] = {}
    for idx, row in enumerate(rows):
        key = tuple(row.get(col) for col in key_columns)
        if keep == "first" and key not in seen:
            seen[key] = idx
        elif keep == "last":
            seen[key] = idx

    kept_indices = set(seen.values())
    return [row for idx, row in enumerate(rows) if idx in kept_indices]


def infer_delimiter(sample: str) -> str:
    """
    Sniff the most likely delimiter from a CSV sample string.

    Returns one of: comma, tab, semicolon, pipe.
    """
    candidates = [",", "\t", ";", "|"]
    counts = {delim: sample.count(delim) for delim in candidates}
    return max(counts, key=lambda d: counts[d])


def resolve_path(path: Union[str, Path], base: Optional[Union[str, Path]] = None) -> Path:
    """Resolve a path, optionally relative to a base directory."""
    p = Path(path)
    if not p.is_absolute() and base is not None:
        p = Path(base) / p
    return p.resolve()


# ---------------------------------------------------------------------------
# Cache utilities
# ---------------------------------------------------------------------------

class TTLCache(Generic[_KT, _VT]):
    """
    A simple time-to-live (TTL) cache backed by an OrderedDict.

    Entries expire after `ttl` seconds from insertion. Thread-safe.
    """

    def __init__(self, maxsize: int = 128, ttl: float = 300.0) -> None:
        self.maxsize = maxsize
        self.ttl = ttl
        self._store: OrderedDict = OrderedDict()
        self._expiry: Dict[_KT, float] = {}
        self._lock = threading.Lock()

    def get(self, key: _KT, default: Optional[_VT] = None) -> Optional[_VT]:
        with self._lock:
            self._evict_expired()
            if key not in self._store:
                return default
            self._store.move_to_end(key)
            return self._store[key]

    def set(self, key: _KT, value: _VT) -> None:
        with self._lock:
            self._evict_expired()
            if len(self._store) >= self.maxsize and key not in self._store:
                oldest = next(iter(self._store))
                del self._store[oldest]
                self._expiry.pop(oldest, None)
            self._store[key] = value
            self._expiry[key] = time.monotonic() + self.ttl
            self._store.move_to_end(key)

    def delete(self, key: _KT) -> None:
        with self._lock:
            self._store.pop(key, None)
            self._expiry.pop(key, None)

    def clear(self) -> None:
        with self._lock:
            self._store.clear()
            self._expiry.clear()

    def _evict_expired(self) -> None:
        now = time.monotonic()
        expired = [k for k, exp in self._expiry.items() if now >= exp]
        for k in expired:
            del self._store[k]
            del self._expiry[k]

    def __len__(self) -> int:
        with self._lock:
            self._evict_expired()
            return len(self._store)

    def __contains__(self, key: object) -> bool:
        return self.get(key) is not None  # type: ignore[arg-type]


# ---------------------------------------------------------------------------
# Event bus
# ---------------------------------------------------------------------------

class Event:
    """Lightweight event object carrying a name, payload, and timestamp."""

    __slots__ = ("name", "payload", "timestamp", "source")

    def __init__(
        self,
        name: str,
        payload: Optional[Any] = None,
        source: Optional[str] = None,
    ) -> None:
        self.name = name
        self.payload = payload
        self.source = source
        self.timestamp = datetime.datetime.now(timezone.utc)

    def __repr__(self) -> str:
        return f"Event(name={self.name!r}, source={self.source!r}, ts={self.timestamp.isoformat()})"


class EventBus:
    """
    Publish-subscribe event bus for decoupled pipeline stage communication.

    Handlers are registered per event name and called synchronously in
    registration order.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, List[Callable[[Event], None]]] = defaultdict(list)
        self._lock = threading.Lock()
        self._history: deque = deque(maxlen=500)

    def subscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        with self._lock:
            self._handlers[event_name].append(handler)

    def unsubscribe(self, event_name: str, handler: Callable[[Event], None]) -> None:
        with self._lock:
            handlers = self._handlers.get(event_name, [])
            with suppress(ValueError):
                handlers.remove(handler)

    def publish(self, event: Event) -> int:
        """Publish an event; returns the number of handlers invoked."""
        self._history.append(event)
        handlers = list(self._handlers.get(event.name, []))
        for handler in handlers:
            try:
                handler(event)
            except Exception as exc:  # noqa: BLE001
                logger.error(
                    "EventBus handler error for event '%s': %s",
                    event.name, exc, exc_info=True,
                )
        return len(handlers)

    def emit(self, name: str, payload: Any = None, source: Optional[str] = None) -> int:
        return self.publish(Event(name=name, payload=payload, source=source))

    @property
    def history(self) -> List[Event]:
        return list(self._history)

    def clear_handlers(self) -> None:
        with self._lock:
            self._handlers.clear()


# ---------------------------------------------------------------------------
# Main pipeline orchestrator
# ---------------------------------------------------------------------------

class DataPipeline:
    """
    Orchestrates the end-to-end data processing pipeline.

    Stages:
        1. Ingest  - read raw rows from source files
        2. Validate - check rows against schema
        3. Clean   - apply transformation pipeline
        4. Enrich  - compute derived columns
        5. Aggregate - optionally group and aggregate
        6. Export  - write results to output files

    Emits events at the start and end of each stage via the EventBus.
    """

    def __init__(
        self,
        config: PipelineConfig,
        schema: Optional[DatasetSchema] = None,
        event_bus: Optional[EventBus] = None,
    ) -> None:
        self.config = config
        self.schema = schema
        self.event_bus = event_bus or EventBus()
        self.metrics = PipelineMetrics()

        self._reader_registry = ReaderRegistry(config)
        self._writer_registry = WriterRegistry(config)
        self._transform_pipeline = TransformPipeline()
        self._profiler = DataProfiler()
        self._anomaly_detector: Optional[AnomalyDetector] = None
        self._aggregator: Optional[Aggregator] = None
        self._validator: Optional[RowValidator] = None

        if schema:
            self._validator = RowValidator(schema, config)
            self._anomaly_detector = AnomalyDetector(config, schema)
            self._transform_pipeline.add(CastTypesTransform(schema))
            self._transform_pipeline.add(FillDefaultsTransform(schema))

        self._transform_pipeline.add(NormaliseStringsTransform())

    # ------------------------------------------------------------------
    # Public configuration helpers
    # ------------------------------------------------------------------

    def add_transform(self, transform: BaseTransform) -> "DataPipeline":
        self._transform_pipeline.add(transform)
        return self

    def set_aggregator(self, aggregator: Aggregator) -> "DataPipeline":
        self._aggregator = aggregator
        return self

    # ------------------------------------------------------------------
    # Core run method
    # ------------------------------------------------------------------

    @timed
    def run(
        self,
        input_paths: List[Union[str, Path]],
        output_path: Union[str, Path],
    ) -> PipelineMetrics:
        """
        Execute the full pipeline on the given input files.

        Args:
            input_paths: One or more source file paths.
            output_path: Destination file path for results.

        Returns:
            Populated PipelineMetrics instance.
        """
        self.metrics.start_time = datetime.datetime.now(timezone.utc)
        self.event_bus.emit("pipeline.start", source=__name__)

        logger.info(
            "Pipeline run %s started. Inputs: %s, Output: %s",
            self.metrics.run_id[:8],
            [str(p) for p in input_paths],
            output_path,
        )

        try:
            all_rows = self._stage_ingest(input_paths)
            all_rows = self._stage_validate(all_rows)
            all_rows = self._stage_clean(all_rows)
            all_rows = self._stage_aggregate(all_rows)
            self._stage_export(all_rows, output_path)
        except DataPipelineError as exc:
            self.metrics.errors.append(str(exc))
            logger.error("Pipeline failed: %s", exc, exc_info=True)
            self.event_bus.emit("pipeline.failed", payload=exc.to_dict(), source=__name__)
        except Exception as exc:  # noqa: BLE001
            self.metrics.errors.append(str(exc))
            logger.critical("Unexpected pipeline failure: %s", exc, exc_info=True)
            self.event_bus.emit("pipeline.error", payload=str(exc), source=__name__)
        finally:
            self.metrics.end_time = datetime.datetime.now(timezone.utc)
            self.event_bus.emit("pipeline.end", payload=self.metrics.to_dict(), source=__name__)

        return self.metrics

    # ------------------------------------------------------------------
    # Stage implementations
    # ------------------------------------------------------------------

    def _stage_ingest(self, paths: List[Union[str, Path]]) -> List[Dict[str, Any]]:
        self.event_bus.emit("stage.ingest.start", source=__name__)
        with timer("ingest") as t:
            rows: List[Dict[str, Any]] = []
            for path in paths:
                try:
                    for row in self._reader_registry.read(path):
                        rows.append(row)
                        self.metrics.rows_ingested += 1
                except IngestError as exc:
                    self.metrics.errors.append(f"Ingest error for {path}: {exc}")
                    logger.error("Ingest failed for %s: %s", path, exc)

            # Fit anomaly detector on the ingested sample
            if self._anomaly_detector:
                sample = rows[: min(1000, len(rows))]
                self._anomaly_detector.fit(sample)

            # Feed profiler
            if self.config.enable_profiling:
                self._profiler.feed_batch(rows)

        self.metrics.bytes_read = sum(
            self._reader_registry.get(FileFormat.from_path(p)).bytes_read
            for p in paths
            if Path(p).exists()
        )
        self.metrics.record_stage(TransformStage.INGEST.value, t["elapsed"])
        self.event_bus.emit("stage.ingest.end", payload={"row_count": len(rows)}, source=__name__)
        logger.info("Ingested %d rows from %d file(s)", len(rows), len(paths))
        return rows

    def _stage_validate(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self._validator is None:
            return rows

        self.event_bus.emit("stage.validate.start", source=__name__)
        with timer("validate") as t:
            valid: List[Dict[str, Any]] = []
            for idx, row in enumerate(rows):
                if self._validator.validate_row(row, idx):
                    valid.append(row)
                else:
                    self.metrics.rows_invalid += 1

        self.metrics.rows_valid = len(valid)
        self.metrics.record_stage(TransformStage.VALIDATE.value, t["elapsed"])
        vsummary = self._validator.summary()
        self.event_bus.emit("stage.validate.end", payload=vsummary, source=__name__)
        logger.info(
            "Validation: %d valid, %d invalid (pass rate=%.1f%%)",
            vsummary["pass_count"],
            vsummary["fail_count"],
            vsummary["pass_rate"] * 100,
        )
        return valid

    def _stage_clean(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        self.event_bus.emit("stage.clean.start", source=__name__)
        with timer("clean") as t:
            cleaned = list(self._transform_pipeline.apply_batch(rows))

            if self.config.deduplicate and self.schema:
                pks = self.schema.primary_keys()
                if pks:
                    before = len(cleaned)
                    cleaned = deduplicate_rows(cleaned, pks)
                    removed = before - len(cleaned)
                    if removed:
                        logger.info("Deduplication removed %d rows", removed)

            # Anomaly detection
            if self.config.enable_anomaly_detection and self._anomaly_detector:
                pks = self.schema.primary_keys() if self.schema else []
                for idx, row in enumerate(cleaned):
                    anomalies = self._anomaly_detector.detect(row, idx)
                    if pks:
                        self._anomaly_detector.check_duplicate(row, idx, pks)
                    self.metrics.anomalies_detected += len(anomalies)

        self.metrics.record_stage(TransformStage.CLEAN.value, t["elapsed"])
        self.event_bus.emit(
            "stage.clean.end",
            payload={"row_count": len(cleaned), **self._transform_pipeline.drop_statistics},
            source=__name__,
        )
        logger.info("After cleaning: %d rows remain", len(cleaned))
        return cleaned

    def _stage_aggregate(self, rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if self._aggregator is None:
            return rows

        self.event_bus.emit("stage.aggregate.start", source=__name__)
        with timer("aggregate") as t:
            self._aggregator.reset()
            self._aggregator.feed_batch(rows)
            result = self._aggregator.compute()

        self.metrics.record_stage(TransformStage.AGGREGATE.value, t["elapsed"])
        self.event_bus.emit(
            "stage.aggregate.end",
            payload={"groups": self._aggregator.group_count()},
            source=__name__,
        )
        logger.info(
            "Aggregation produced %d rows from %d groups",
            len(result),
            self._aggregator.group_count(),
        )
        return result

    def _stage_export(
        self, rows: List[Dict[str, Any]], output_path: Union[str, Path]
    ) -> None:
        self.event_bus.emit("stage.export.start", source=__name__)
        with timer("export") as t:
            self._writer_registry.write(rows, output_path)

        writer = self._writer_registry.get(
            FileFormat.from_path(output_path)
        )
        self.metrics.rows_exported = writer.rows_written
        self.metrics.bytes_written = writer.bytes_written
        self.metrics.record_stage(TransformStage.EXPORT.value, t["elapsed"])
        self.event_bus.emit(
            "stage.export.end",
            payload={"rows_written": writer.rows_written},
            source=__name__,
        )
        logger.info("Exported %d rows to %s", writer.rows_written, output_path)

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------

    def generate_report(self) -> ReportGenerator:
        """Build and return a ReportGenerator populated from this run."""
        column_stats = self._profiler.compute() if self.config.enable_profiling else {}
        anomaly_summary = (
            self._anomaly_detector.summary()
            if self._anomaly_detector
            else {}
        )
        validation_summary = (
            self._validator.summary()
            if self._validator
            else {}
        )
        return ReportGenerator(
            metrics=self.metrics,
            column_stats=column_stats,
            anomaly_summary=anomaly_summary,
            validation_summary=validation_summary,
        )


# ---------------------------------------------------------------------------
# CLI argument parsing
# ---------------------------------------------------------------------------

def build_argument_parser() -> argparse.ArgumentParser:
    """Construct the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog=APP_NAME,
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              %(prog)s --input data/sales.csv --output out/results.json
              %(prog)s --config pipeline.json --input data/ --log-level DEBUG
              %(prog)s --input data/events.jsonl --output results.csv \\
                       --schema schema.json --deduplicate
        """),
    )

    parser.add_argument(
        "--version", "-V",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    io_group = parser.add_argument_group("Input / Output")
    io_group.add_argument(
        "--input", "-i",
        nargs="+",
        required=True,
        metavar="PATH",
        help="One or more input file or directory paths.",
    )
    io_group.add_argument(
        "--output", "-o",
        required=True,
        metavar="PATH",
        help="Output file path.",
    )
    io_group.add_argument(
        "--schema", "-s",
        metavar="PATH",
        help="Path to a JSON schema definition file.",
    )
    io_group.add_argument(
        "--config", "-c",
        metavar="PATH",
        help="Path to a JSON pipeline configuration file.",
    )

    proc_group = parser.add_argument_group("Processing options")
    proc_group.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        metavar="N",
        help=f"Rows per processing batch (default: {DEFAULT_BATCH_SIZE}).",
    )
    proc_group.add_argument(
        "--deduplicate",
        action="store_true",
        default=False,
        help="Remove duplicate rows based on primary key columns.",
    )
    proc_group.add_argument(
        "--strict",
        action="store_true",
        default=False,
        help="Reject rows with columns not defined in the schema.",
    )
    proc_group.add_argument(
        "--max-errors",
        type=int,
        default=100,
        metavar="N",
        help="Maximum validation errors before aborting (default: 100).",
    )
    proc_group.add_argument(
        "--overwrite",
        action="store_true",
        default=False,
        help="Overwrite output file if it already exists.",
    )

    log_group = parser.add_argument_group("Logging")
    log_group.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging verbosity level (default: INFO).",
    )
    log_group.add_argument(
        "--log-file",
        metavar="PATH",
        help="Write log output to this file in addition to stdout.",
    )
    log_group.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Include file/line info in log messages.",
    )

    report_group = parser.add_argument_group("Reporting")
    report_group.add_argument(
        "--report",
        metavar="PATH",
        help="Write a JSON run report to this path.",
    )
    report_group.add_argument(
        "--no-profiling",
        action="store_true",
        default=False,
        help="Disable per-column statistical profiling.",
    )
    report_group.add_argument(
        "--no-anomaly-detection",
        action="store_true",
        default=False,
        help="Disable anomaly detection.",
    )

    return parser


def collect_input_paths(inputs: List[str]) -> List[Path]:
    """
    Expand input arguments into a flat list of file paths.

    Directories are expanded to all files with recognised extensions.
    """
    paths: List[Path] = []
    recognised_exts = {f".{fmt.value}" for fmt in FileFormat} | {".gz"}
    for raw in inputs:
        p = Path(raw)
        if p.is_dir():
            for child in sorted(p.iterdir()):
                if child.is_file() and child.suffix in recognised_exts:
                    paths.append(child)
        elif p.exists():
            paths.append(p)
        else:
            logger.warning("Input path does not exist, skipping: %s", raw)
    return paths


# ---------------------------------------------------------------------------
# Graceful shutdown
# ---------------------------------------------------------------------------

_shutdown_requested = threading.Event()


def _handle_signal(signum: int, frame: Any) -> None:
    sig_name = signal.Signals(signum).name
    logger.info("Received signal %s, requesting graceful shutdown...", sig_name)
    _shutdown_requested.set()


def register_signal_handlers() -> None:
    """Register SIGINT and SIGTERM handlers for graceful shutdown."""
    with suppress(AttributeError, ValueError):
        signal.signal(signal.SIGINT, _handle_signal)
    with suppress(AttributeError, ValueError):
        signal.signal(signal.SIGTERM, _handle_signal)


# ---------------------------------------------------------------------------
# Application bootstrap helpers
# ---------------------------------------------------------------------------

def build_config_from_args(args: argparse.Namespace) -> PipelineConfig:
    """Assemble a PipelineConfig from parsed CLI arguments."""
    # Start with file-based config if provided
    if args.config:
        config = PipelineConfig.from_file(args.config)
    else:
        config = PipelineConfig()

    # Apply env overrides
    env_config = PipelineConfig.from_env()
    config = config.merge(env_config)

    # CLI flags always win
    overrides: Dict[str, Any] = {
        "log_level": args.log_level,
        "log_file": args.log_file,
        "batch_size": args.batch_size,
        "deduplicate": args.deduplicate,
        "strict_schema": args.strict,
        "max_errors": args.max_errors,
        "overwrite_output": args.overwrite,
        "enable_profiling": not args.no_profiling,
        "enable_anomaly_detection": not args.no_anomaly_detection,
    }
    config._update(overrides)
    return config


def load_schema_if_provided(
    schema_path: Optional[str],
    rows: Optional[List[Dict[str, Any]]] = None,
    config: Optional[PipelineConfig] = None,
) -> Optional[DatasetSchema]:
    """Load a DatasetSchema from file, or infer one from sample rows."""
    if schema_path:
        try:
            raw = load_json_file(schema_path)
            schema = DatasetSchema.from_dict(raw)
            logger.info("Loaded schema '%s' (%d columns)", schema.name, len(schema.columns))
            return schema
        except (FileNotFoundError, KeyError, SchemaError) as exc:
            logger.error("Failed to load schema from %s: %s", schema_path, exc)
            return None

    if rows:
        null_tokens = list(config.null_values) if config else None
        inferrer = SchemaInferrer(null_tokens=null_tokens)
        try:
            schema = inferrer.infer(rows)
            logger.info(
                "Inferred schema with %d columns from %d sample rows",
                len(schema.columns), len(rows),
            )
            return schema
        except SchemaError as exc:
            logger.warning("Schema inference failed: %s", exc)

    return None


# ---------------------------------------------------------------------------
# Additional utility classes
# ---------------------------------------------------------------------------

class RollingBuffer(Generic[_T]):
    """
    Fixed-capacity buffer that discards the oldest element when full.

    Useful for maintaining a rolling window of recent observations.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("RollingBuffer capacity must be at least 1")
        self._capacity = capacity
        self._buf: deque = deque(maxlen=capacity)

    def push(self, item: _T) -> None:
        self._buf.append(item)

    def push_all(self, items: Iterable[_T]) -> None:
        for item in items:
            self.push(item)

    def snapshot(self) -> List[_T]:
        return list(self._buf)

    def is_full(self) -> bool:
        return len(self._buf) == self._capacity

    def clear(self) -> None:
        self._buf.clear()

    def __len__(self) -> int:
        return len(self._buf)

    def __iter__(self) -> Iterator[_T]:
        return iter(self._buf)


class FrequencyCounter(Generic[_T]):
    """
    Tracks item frequencies and exposes top-N and tail-N queries.

    Wraps collections.Counter with convenience methods.
    """

    def __init__(self) -> None:
        self._counter: Counter = Counter()
        self._total: int = 0

    def observe(self, item: _T, count: int = 1) -> None:
        self._counter[item] += count
        self._total += count

    def observe_batch(self, items: Iterable[_T]) -> None:
        for item in items:
            self.observe(item)

    def top(self, n: int = 10) -> List[Tuple[_T, int]]:
        return self._counter.most_common(n)

    def bottom(self, n: int = 10) -> List[Tuple[_T, int]]:
        return self._counter.most_common()[:-n - 1:-1]

    def frequency(self, item: _T) -> float:
        if self._total == 0:
            return 0.0
        return self._counter[item] / self._total

    def count(self, item: _T) -> int:
        return self._counter[item]

    @property
    def total(self) -> int:
        return self._total

    @property
    def unique(self) -> int:
        return len(self._counter)

    def reset(self) -> None:
        self._counter.clear()
        self._total = 0

    def to_dict(self) -> Dict[Any, int]:
        return dict(self._counter)


class ProgressTracker:
    """
    Tracks and reports progress for long-running iterative operations.

    Emits periodic log messages based on a configurable interval.
    """

    def __init__(
        self,
        total: Optional[int] = None,
        label: str = "progress",
        log_every: int = 1000,
    ) -> None:
        self.total = total
        self.label = label
        self.log_every = log_every
        self._count: int = 0
        self._start: float = time.perf_counter()
        self._last_log: float = self._start

    def increment(self, n: int = 1) -> None:
        self._count += n
        if self._count % self.log_every == 0:
            self._log()

    def _log(self) -> None:
        elapsed = time.perf_counter() - self._start
        rate = self._count / max(elapsed, 1e-9)
        if self.total:
            pct = 100 * self._count / self.total
            eta = (self.total - self._count) / max(rate, 1e-9)
            logger.info(
                "%s: %d/%d (%.1f%%) | %.0f rows/s | ETA %.1fs",
                self.label, self._count, self.total, pct, rate, eta,
            )
        else:
            logger.info(
                "%s: %d rows | %.0f rows/s | elapsed %.1fs",
                self.label, self._count, rate, elapsed,
            )

    def done(self) -> None:
        """Log a final completion message."""
        elapsed = time.perf_counter() - self._start
        rate = self._count / max(elapsed, 1e-9)
        logger.info(
            "%s completed: %d rows in %.2fs (%.0f rows/s)",
            self.label, self._count, elapsed, rate,
        )

    @property
    def count(self) -> int:
        return self._count


# ---------------------------------------------------------------------------
# Helpers for constructing demo / test data
# ---------------------------------------------------------------------------

def _random_date(
    start: datetime.date = datetime.date(2018, 1, 1),
    end: datetime.date = datetime.date(2024, 12, 31),
    rng: Optional[random.Random] = None,
) -> datetime.date:
    """Generate a random date between start and end (inclusive)."""
    rng = rng or random
    delta = (end - start).days
    return start + datetime.timedelta(days=rng.randint(0, delta))


def _random_string(
    length: int = 8,
    alphabet: str = "abcdefghijklmnopqrstuvwxyz0123456789",
    rng: Optional[random.Random] = None,
) -> str:
    rng = rng or random
    return "".join(rng.choices(alphabet, k=length))


def generate_sample_dataset(
    n_rows: int = 500,
    seed: Optional[int] = 42,
    include_anomalies: bool = True,
) -> List[Dict[str, Any]]:
    """
    Generate a synthetic sales dataset for testing and demonstration.

    Args:
        n_rows: Number of rows to generate.
        seed: Random seed for reproducibility.
        include_anomalies: If True, inject a small number of outlier rows.

    Returns:
        List of row dictionaries.
    """
    rng = random.Random(seed)
    regions = ["EMEA", "APAC", "AMER", "LATAM"]
    categories = ["electronics", "apparel", "food", "automotive", "services"]
    currencies = ["USD", "EUR", "GBP", "JPY", "AUD"]
    statuses = ["completed", "pending", "refunded", "cancelled"]

    rows: List[Dict[str, Any]] = []
    for i in range(n_rows):
        amount = round(rng.gauss(250.0, 80.0), 2)
        if include_anomalies and rng.random() < 0.02:
            amount = round(rng.uniform(5000, 50000), 2)  # outlier

        row = {
            "order_id": f"ORD-{_random_string(10, rng=rng).upper()}",
            "customer_id": f"CUST-{rng.randint(1000, 9999)}",
            "date": _random_date(rng=rng).isoformat(),
            "region": rng.choice(regions),
            "category": rng.choice(categories),
            "currency": rng.choice(currencies),
            "amount": amount,
            "quantity": rng.randint(1, 50),
            "unit_price": round(rng.uniform(5.0, 500.0), 2),
            "discount_pct": round(rng.uniform(0, 0.3), 4),
            "status": rng.choice(statuses),
            "is_b2b": rng.choice([True, False]),
            "notes": (
                f"Auto-generated order {i + 1}" if rng.random() > 0.3 else None
            ),
        }
        rows.append(row)

    # Inject a few duplicates
    if include_anomalies and n_rows >= 20:
        dupe_indices = rng.sample(range(len(rows)), k=min(5, n_rows // 20))
        for idx in dupe_indices:
            rows.append(dict(rows[idx]))

    return rows


# ---------------------------------------------------------------------------
# Sample schema definition
# ---------------------------------------------------------------------------

def build_sales_schema() -> DatasetSchema:
    """Return a DatasetSchema for the synthetic sales dataset."""
    return DatasetSchema(
        name="sales",
        version="1.0",
        description="Monthly sales transaction records",
        columns=[
            ColumnSchema(
                name="order_id",
                dtype="string",
                nullable=False,
                primary_key=True,
                pattern=r"ORD-[A-Z0-9]{10}",
                description="Unique order identifier",
            ),
            ColumnSchema(
                name="customer_id",
                dtype="string",
                nullable=False,
                pattern=r"CUST-\d{4}",
                description="Customer reference code",
            ),
            ColumnSchema(
                name="date",
                dtype="date",
                nullable=False,
                description="Order date (ISO 8601)",
            ),
            ColumnSchema(
                name="region",
                dtype="string",
                nullable=False,
                enum_values=["EMEA", "APAC", "AMER", "LATAM"],
                description="Sales region",
            ),
            ColumnSchema(
                name="category",
                dtype="string",
                nullable=True,
                enum_values=["electronics", "apparel", "food", "automotive", "services"],
                description="Product category",
            ),
            ColumnSchema(
                name="currency",
                dtype="string",
                nullable=False,
                enum_values=["USD", "EUR", "GBP", "JPY", "AUD"],
                description="Transaction currency code",
            ),
            ColumnSchema(
                name="amount",
                dtype="float",
                nullable=False,
                min_value=0.01,
                max_value=1_000_000.0,
                description="Transaction total in stated currency",
            ),
            ColumnSchema(
                name="quantity",
                dtype="integer",
                nullable=False,
                min_value=1,
                max_value=10_000,
                description="Number of units ordered",
            ),
            ColumnSchema(
                name="unit_price",
                dtype="float",
                nullable=True,
                min_value=0.0,
                description="Price per unit",
            ),
            ColumnSchema(
                name="discount_pct",
                dtype="float",
                nullable=True,
                min_value=0.0,
                max_value=1.0,
                description="Discount as a fraction of list price",
            ),
            ColumnSchema(
                name="status",
                dtype="string",
                nullable=False,
                enum_values=["completed", "pending", "refunded", "cancelled"],
                description="Current order status",
            ),
            ColumnSchema(
                name="is_b2b",
                dtype="boolean",
                nullable=True,
                default=False,
                description="Whether this is a business-to-business order",
            ),
            ColumnSchema(
                name="notes",
                dtype="string",
                nullable=True,
                description="Free-text order notes",
            ),
        ],
    )


# ---------------------------------------------------------------------------
# Additional analysis helpers
# ---------------------------------------------------------------------------

def compute_revenue_summary(
    rows: List[Dict[str, Any]],
    amount_col: str = "amount",
    group_col: str = "region",
) -> Dict[str, Dict[str, float]]:
    """
    Compute basic revenue statistics grouped by a categorical column.

    Returns a dict keyed by group value with sub-keys:
        total, mean, median, count, min, max.
    """
    groups: Dict[str, List[float]] = defaultdict(list)
    for row in rows:
        grp = row.get(group_col)
        val = row.get(amount_col)
        if grp is not None and val is not None:
            with suppress(TypeError, ValueError):
                groups[str(grp)].append(float(val))  # type: ignore[arg-type]

    result: Dict[str, Dict[str, float]] = {}
    for grp, values in groups.items():
        if not values:
            continue
        result[grp] = {
            "total": sum(values),
            "mean": statistics.mean(values),
            "median": statistics.median(values),
            "count": float(len(values)),
            "min": min(values),
            "max": max(values),
            "std": statistics.stdev(values) if len(values) >= 2 else 0.0,
        }
    return result


def time_series_resample(
    rows: List[Dict[str, Any]],
    date_col: str,
    value_col: str,
    freq: str = "monthly",
) -> List[Dict[str, Any]]:
    """
    Resample a time-series dataset to a lower frequency by summing values.

    Args:
        rows: Input rows with a date column and a numeric value column.
        date_col: Name of the date/datetime column.
        value_col: Name of the numeric column to aggregate.
        freq: One of 'daily', 'weekly', 'monthly', 'yearly'.

    Returns:
        List of dicts with keys: period, total, count.
    """
    buckets: Dict[str, List[float]] = defaultdict(list)

    for row in rows:
        raw_date = row.get(date_col)
        val = row.get(value_col)
        if raw_date is None or val is None:
            continue
        # Parse date
        dt: Optional[datetime.date] = None
        if isinstance(raw_date, (datetime.date, datetime.datetime)):
            dt = raw_date if isinstance(raw_date, datetime.date) else raw_date.date()
        else:
            parsed = parse_iso_datetime(str(raw_date))
            if parsed:
                dt = parsed.date()
        if dt is None:
            continue

        if freq == "daily":
            key = dt.strftime(DATE_FORMAT_ISO)
        elif freq == "weekly":
            iso_cal = dt.isocalendar()
            key = f"{iso_cal[0]}-W{iso_cal[1]:02d}"
        elif freq == "monthly":
            key = dt.strftime("%Y-%m")
        elif freq == "yearly":
            key = str(dt.year)
        else:
            raise ValueError(f"Unsupported frequency: {freq!r}")

        with suppress(TypeError, ValueError):
            buckets[key].append(float(val))  # type: ignore[arg-type]

    return [
        {
            "period": period,
            "total": sum(vals),
            "count": len(vals),
            "mean": statistics.mean(vals) if vals else 0.0,
        }
        for period, vals in sorted(buckets.items())
    ]


def correlation_matrix(
    rows: List[Dict[str, Any]],
    columns: List[str],
) -> Dict[str, Dict[str, float]]:
    """
    Compute pairwise Pearson correlation coefficients for numeric columns.

    Args:
        rows: Input data rows.
        columns: Column names to include.

    Returns:
        Nested dict: matrix[col_a][col_b] = pearson_r.
    """
    data: Dict[str, List[float]] = {col: [] for col in columns}
    for row in rows:
        vals = {}
        for col in columns:
            v = row.get(col)
            if v is None:
                break
            try:
                vals[col] = float(v)  # type: ignore[arg-type]
            except (TypeError, ValueError):
                break
        else:
            for col, fv in vals.items():
                data[col].append(fv)

    matrix: Dict[str, Dict[str, float]] = {}
    for col_a in columns:
        matrix[col_a] = {}
        for col_b in columns:
            if col_a == col_b:
                matrix[col_a][col_b] = 1.0
                continue
            xs = data[col_a]
            ys = data[col_b]
            n = min(len(xs), len(ys))
            if n < 2:
                matrix[col_a][col_b] = float("nan")
                continue
            xs, ys = xs[:n], ys[:n]
            mean_x = statistics.mean(xs)
            mean_y = statistics.mean(ys)
            cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys))
            std_x = math.sqrt(sum((x - mean_x) ** 2 for x in xs))
            std_y = math.sqrt(sum((y - mean_y) ** 2 for y in ys))
            denom = std_x * std_y
            matrix[col_a][col_b] = cov / denom if denom > 0 else float("nan")

    return matrix


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main(argv: Optional[List[str]] = None) -> int:
    """
    Main entry point for the DataPipeline CLI.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code: 0 on success, non-zero on failure.
    """
    parser = build_argument_parser()
    args = parser.parse_args(argv)

    # Logging must be configured before anything else
    setup_logging(
        level=args.log_level,
        log_file=args.log_file,
        verbose=args.verbose,
    )

    register_signal_handlers()
    atexit.register(lambda: logger.debug("Process exiting"))

    logger.info(
        "Starting %s v%s (pid=%d)",
        APP_NAME, __version__, os.getpid(),
    )

    # Build configuration
    try:
        config = build_config_from_args(args)
    except ConfigurationError as exc:
        logger.critical("Configuration error: %s", exc)
        return 2

    # Collect input paths
    input_paths = collect_input_paths(args.input)
    if not input_paths:
        logger.critical("No valid input files found in: %s", args.input)
        return 2

    output_path = Path(args.output)

    # Quick ingest of a sample to assist schema inference
    sample_rows: List[Dict[str, Any]] = []
    if not args.schema:
        reader_reg = ReaderRegistry(config)
        try:
            for row in reader_reg.read(input_paths[0]):
                sample_rows.append(row)
                if len(sample_rows) >= 200:
                    break
        except IngestError as exc:
            logger.warning("Could not read sample for schema inference: %s", exc)

    schema = load_schema_if_provided(args.schema, rows=sample_rows or None, config=config)

    # Instantiate and run pipeline
    pipeline = DataPipeline(config=config, schema=schema)

    # Add a computed column for net_amount
    pipeline.add_transform(
        ComputedColumnTransform(
            new_column="net_amount",
            func=lambda r: (
                round(
                    float(r.get("amount", 0) or 0)
                    * (1 - float(r.get("discount_pct", 0) or 0)),
                    4,
                )
            ),
        )
    )

    if _shutdown_requested.is_set():
        logger.info("Shutdown requested before pipeline start; aborting.")
        return 130

    metrics = pipeline.run(input_paths, output_path)

    if _shutdown_requested.is_set():
        logger.info("Shutdown requested; pipeline may be incomplete.")

    # Generate and optionally save report
    report_gen = pipeline.generate_report()
    report_gen.print_summary()

    if args.report:
        try:
            report_gen.save_json(args.report)
        except OSError as exc:
            logger.error("Could not save report: %s", exc)

    exit_code = 0 if not metrics.errors else 1
    logger.info(
        "Pipeline finished with exit code %d (run_id=%s)",
        exit_code, metrics.run_id,
    )
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
