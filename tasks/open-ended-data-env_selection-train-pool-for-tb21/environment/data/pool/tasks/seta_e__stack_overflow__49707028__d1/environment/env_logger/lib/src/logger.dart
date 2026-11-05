import 'env_detector.dart';

class EnvLogger {
  final String tag;
  const EnvLogger(this.tag);

  void debug(String message) {
    if (isDebugMode) {
      print('[$tag][DEBUG] $message');
    }
  }

  void info(String message) {
    print('[$tag][INFO] $message');
  }

  void error(String message) {
    print('[$tag][ERROR] $message');
  }

  void assertLog(String message) {
    assert(() {
      print('[$tag][ASSERT] $message');
      return true;
    }());
  }
}
