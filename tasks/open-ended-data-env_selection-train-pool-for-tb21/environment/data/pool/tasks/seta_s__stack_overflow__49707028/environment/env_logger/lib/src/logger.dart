import 'env_detector.dart';

/// A logger whose verbosity adapts to the current compilation mode.
class EnvLogger {
  final String tag;

  const EnvLogger(this.tag);

  /// Prints only when compiled in debug mode.
  void debug(String message) {
    if (isDebugMode) {
      print('[$tag][DEBUG] $message');
    }
  }

  /// Always prints, regardless of mode.
  void info(String message) {
    print('[$tag][INFO] $message');
  }

  /// Always prints, regardless of mode.
  void error(String message) {
    print('[$tag][ERROR] $message');
  }

  /// Uses an assert block — executes the callback only in debug (JIT) mode
  /// where Dart assertions are enabled.
  void assertLog(String message) {
    assert(() {
      print('[$tag][ASSERT] $message');
      return true;
    }());
  }
}
