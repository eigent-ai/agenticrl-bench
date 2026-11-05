import os
import importlib
import pytest


def reload_device_utils():
    import device_utils
    importlib.reload(device_utils)
    return device_utils


def test_is_cpu_only_when_empty_string(monkeypatch):
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "")
    du = reload_device_utils()
    assert du.is_cpu_only_mode() is True


def test_is_not_cpu_only_when_unset(monkeypatch):
    monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
    du = reload_device_utils()
    assert du.is_cpu_only_mode() is False


def test_is_not_cpu_only_when_device_id(monkeypatch):
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "0")
    du = reload_device_utils()
    assert du.is_cpu_only_mode() is False


def test_description_cpu_only(monkeypatch):
    monkeypatch.setenv("CUDA_VISIBLE_DEVICES", "")
    du = reload_device_utils()
    assert du.get_device_description() == "cpu-only"


def test_description_auto(monkeypatch):
    monkeypatch.delenv("CUDA_VISIBLE_DEVICES", raising=False)
    du = reload_device_utils()
    assert du.get_device_description() == "auto"
