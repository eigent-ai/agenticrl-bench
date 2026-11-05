import 'dart:io';

/// Environment mode detection for the env_logger package.
///
/// Provides boolean flags that indicate the current compilation mode.
/// These flags are intended to be compile-time constants so that dead-code
/// elimination can strip unused branches in release builds.

// True when the application is running in debug (development) mode.
bool get isDebugMode =>
    Platform.environment.containsKey('APP_DEBUG') &&
    Platform.environment['APP_DEBUG'] == '1';

// True when the application was compiled in release mode.
bool get isReleaseMode =>
    Platform.environment.containsKey('APP_RELEASE') &&
    Platform.environment['APP_RELEASE'] == '1';

// True when the application was compiled in profile mode.
bool get isProfileMode =>
    Platform.environment.containsKey('APP_PROFILE') &&
    Platform.environment['APP_PROFILE'] == '1';

// True when the application is running on the web platform.
bool get isWeb =>
    Platform.environment.containsKey('APP_WEB') &&
    Platform.environment['APP_WEB'] == '1';
