[app]

# (str) Title of your application
title = Voice Analyzer

# (str) Package name
package.name = voiceanalyzer

# (str) Package domain (needed for android/ios packaging)
package.domain = com.voiceanalyzer

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include/let git ignore
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3,json,db,txt

# (list) Source files to exclude from the app (don't include them)
source.exclude_exts = spec,pyc,pyo,db

# (list) List of directories to exclude (relative to source.dir)
source.exclude_dirs = tests, bin, .git, __pycache__, .buildozer

# (str) Version of your application
version = 1.0.0

# (str) Application requirements (Python modules)
requirements = python3,kivy==2.3.0,kivymd==1.1.1,requests==2.31.0,plyer==2.1,pyjnius==1.6.0,android==1.0

# (str) Custom source folders for requirements
# requirements.source.kivy = kivy

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET, RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, MODIFY_AUDIO_SETTINGS

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private to copy the application in the private directory.
android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
android.ndk_path = 

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
android.sdk_path = 

# (list) Gradle dependencies to add
android.gradle_dependencies = 'androidx.appcompat:appcompat:1.6.1', 'com.google.android.material:material:1.9.0'

# (bool) Enable or disable unpacking of dependencies
android.enable_java_import = True

# (list) Java classes to add as dependencies
android.add_src =

# (list) Android AAR archives to add (leave empty to not add any)
android.add_aars =

# (list) Gradle repositories to add {repositories, flatDirs}
android.gradle_repositories = 'mavenCentral()', 'google()'

# (list) Add java requirements
android.add_java =

# (str) Bootstrap mode for kivy (pygame, sdl2)
bootstrap = sdl2

# (str) Log level (debug, info, warning, error, critical)
log_level = 2

# (bool) Show log in console (off, on)
console = on

# (str) Path to the configuration file for remote debugging
remote_debugging_auto_forward = 

# (bool) Allow the application to be precompiled
android.allow_backup = True

# (bool) Whether the application can be installed on external storage
android.install_location = auto

# (str) The Android theme to use
android.theme = Theme.Material

# (str) The Android window background color
android.window_background_color = #FFFFFF

# (list) Meta-data to add to the application
android.meta_data =

# (list) Intent filters to add
android.intent_filters =

# (str) Additional Android manifest elements
android.manifest_entries = 

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (str) Android logcat output file
android.logcat_output = %(source.dir)s/.buildozer/android/logcat.txt

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (bool) Wipe all build directories before building
wipe_build = False

# (bool) We want to build only for android
android = True

# (bool) We want to build for iOS
ios = False

# (str) Path to the iOS certificate (optional)
ios.codesign.certificate =

# (str) Path to the iOS certificate key (optional)
ios.codesign.key =

# (list) iOS frameworks to add (optional)
ios.frameworks =

# (str) Path to the Android SDK directory (optional)
android.sdk_path =

# (str) Path to the Android NDK directory (optional)
android.ndk_path =

# (str) Path to the Android ant directory (optional)
android.ant_path =

# (bool) Accept Android SDK license
android.accept_sdk_license = True

# (str) The Android architecture to build for
android.arch = arm64-v8a, armeabi-v7a

# (str) Android entry point (leave empty to use default)
android.entrypoint = org.kivy.android.PythonActivity

# (str) Full name of the Android Java class (leave empty to use default)
android.fullscreen = 0

# (str) Android theme (leave empty to use default)
android.theme = Theme.Material

# (str) Android private storage mode (apps, private)
android.private_storage = apps

# (str) Android NDK API (leave empty for default)
android.ndk_api =

# (str) Android SDK API (leave empty for default)
android.sdk_api =

# (str) Android NDK version (leave empty for default)
android.ndk_version =

# (bool) Use the new Android packaging system (Android Gradle plugin)
android.gradle = True

# (bool) Use the old Android packaging system (Ant)
android.ant = False

# (str) Path to the Java source directory (optional)
android.java_src_dir =

# (str) Path to the Java build directory (optional)
android.java_build_dir =

# (str) Path to the Java compiled classes directory (optional)
android.java_classes_dir =

# (str) Path to the Java libraries directory (optional)
android.java_libs_dir =

# (str) Path to the AndroidManifest.xml file (optional)
android.manifest_entries =

# (str) Additional Java source files to include (optional)
android.add_src =

# (str) Additional Java libraries (JAR) to include (optional)
android.add_jar =

# (str) Additional Java libraries (AAR) to include (optional)
android.add_aar =

# (str) Additional Gradle dependencies (optional)
android.gradle_dependencies =

# (str) Additional Gradle repositories (optional)
android.gradle_repositories =

# (str) Additional Gradle plugins (optional)
android.gradle_plugins =

# (str) Path to the ProGuard configuration file (optional)
android.proguard_filename =

# (bool) Sign the APK
android.sign = True

# (str) Path to the keystore (optional)
android.keystore =

# (str) Keystore password (optional)
android.keystore_password =

# (str) Keystore alias (optional)
android.keystore_alias =

# (str) Keystore alias password (optional)
android.keystore_alias_password =

# (bool) Use the debug keystore (for development)
android.debug_keystore = True

# (bool) Use the release keystore (for production)
android.release_keystore = False
