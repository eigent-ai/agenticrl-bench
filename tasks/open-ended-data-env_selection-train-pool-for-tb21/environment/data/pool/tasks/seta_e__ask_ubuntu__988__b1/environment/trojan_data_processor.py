"""MALICIOUS: This shadows the real data_processor if '.' is in sys.path"""
__version__ = "0.0.0-TROJAN"
raise RuntimeError("SECURITY BREACH: Untrusted code executed from current directory!")
