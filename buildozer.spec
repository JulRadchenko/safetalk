[app]

# (str) Title of your application
title = Безопасный разговор

# (str) Package name
package.name = safetalk

# (str) Package domain (needed for android/ios packaging)
package.domain = com.safetalk

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,wav

# (list) List of inclusions using pattern matching
source.include_patterns = assets/*.png,assets/*.jpg

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_exts = spec,log,pyc

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests,bin,.git,__pycache__,venv

# (list) List of exclusions using pattern matching
# source.exclude_patterns = license,images/*/.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
requirements = python3==3.10.14,hostpython3==3.10.14,kivy==2.3.0,kivymd==2.0.1.dev0,requests==2.31.0,pyjnius==1.6.1,plyer==2.1,android

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/safetalk_icon.png

# (str) Allowed orientations
# orientations = portrait

# (list) Permissions
android.permissions = RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (int) Android SDK version
android.sdk = 33

# (str) Android NDK version
android.ndk = 25b

# (bool) Enable AndroidX (required for modern libraries)
android.enable_androidx = True

# (bool) Use Gradle instead of Ant
android.gradle = True

# (int) Gradle version
android.gradle_version = 8.2.2

# (str) Java JDK version
android.java_jdk = 17

# (list) Java classes to add
# android.add_src =

# (list) Java jars to add
# android.add_jars =

# (list) Python modules to include as private (dynamically loaded)
# android.add_imports = jnius

# (str) Extra Java compile options
# android.javac_options = -Xlint:deprecation,-Xlint:unchecked

# (bool) Copy library instead of making a pybundle
# android.copy_libs = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (str) Android NDK API to use
# android.ndk_api = 21

# (bool) Use the Android NDK from the one pointed by the ANDROID_NDK env var
# android.use_ndk_cache = False

# (bool) Use the Android SDK from the one pointed by the ANDROID_HOME env var
# android.use_sdk_cache = False

# (str) Bootstrap to use for android
# android.bootstrap = sdl2

# (str) Which Google APIs to include
# android.google_apis = armeabi-v7a

# (str) Android logcat filters to use
# android.logcat_filters = *:S python:D

# (str) Entry point for the application
# android.entrypoint = org.kivy.android.PythonActivity

# (bool) Fullscreen mode
# android.fullscreen = False

# (str) Launch mode (standard, singleTop, singleTask, singleInstance)
# android.launch_mode = standard

# (list) Android services to add
# android.services = MyService:com.example.myservice

# (str) Activity class to use for the main activity
# android.activity_class = org.kivy.android.PythonActivity

# (bool) Enable the Android TV support
# android.enable_tv_support = False

# (str) URL to the keystore for signing
# android.keystore = /path/to/keystore

# (str) Alias for the key in the keystore
# android.keyalias = my_key

# (str) Password for the keystore
# android.keystore_password = my_password

# (str) Password for the key
# android.keyalias_password = my_password

# (list) Permissions to add (already included above)
# android.permissions = RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# (list) Metadata to add
# android.meta_data = com.google.android.gms.version:@integer/google_play_services_version

# (list) Gradle dependencies to add
android.gradle_dependencies = 'com.android.support:appcompat-v7:28.0.0'

# (list) Gradle repositories to add
# android.gradle_repositories =

# (bool) Enable Java 8 features
android.enable_java8 = True

# (bool) Split the APK per architecture
# android.split_apks = False

# (str) Permission to add for the presplash
# android.presplash_permission = false

# (str) Theme to use (light or dark)
# android.theme = light

# (str) Debug mode (0 = off, 1 = on, 2 = full)
android.debug = 1

# (bool) Automatically sign the release APK
# android.release_autosign = False

# (str) Path to the private key for signing
# android.release_keystore = /path/to/keystore

# (str) Alias for the key
# android.release_keyalias = my_alias

# (str) Password for the private key
# android.release_keystore_password = my_password

# (str) Password for the alias
# android.release_keyalias_password = my_password

# (bool) Enable verbose logging for the build process
android.verbose = False

# (bool) Enable the use of the ARMv7 NEON feature
# android.neon = False

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (bool) Warn if the buildozer version is too old
warn_on_root = 1

# (bool) Avoid recompiling the python distribution
# no_compile = False

# (bool) Download the bootstrap archive with the precompiled python distribution
# download_bootstrap = True

# (bool) Rebuild the bootstrap if it exists
# rebuild_bootstrap = False

# (str) Path to the Android SDK
# android_sdk = /path/to/android-sdk

# (str) Path to the Android NDK
# android_ndk = /path/to/android-ndk

# (str) Path to the Android ANT directory
# android_ant = /path/to/android-ant

# (str) Path to the Java JDK
# android_java = /usr/lib/jvm/java-17-openjdk-amd64

# (bool) Accept the Android SDK license
android.accept_sdk_license = True

# (str) Path to the Android AVD
# android_avd = ~/.android/avd

# (bool) Force the Android build
# android_force = False

# (bool) Use the Android NDK from the one pointed by the ANDROID_NDK env var
# use_ndk_cache = False

# (bool) Use the Android SDK from the one pointed by the ANDROID_HOME env var
# use_sdk_cache = False

# (bool) Show the Android logcat output
# android_logcat = False

# (str) Filters for the Android logcat
# android_logcat_filters = *:S python:D

# (str) Custom command to run to get the Android logcat
# android_logcat_cmd = logcat

# (bool) Deploy the application to the device
# android_deploy = True

# (bool) Run the application on the device
# android_run = False

# (str) Target Android device (serial number)
# android_device = emulator-5554

# (bool) Use the Android emulator
# android_emulator = False

# (str) Path to the Android emulator
# android_emulator_path = emulator

# (str) Android emulator AVD name
# android_avd_name = test

# (str) Android emulator command line arguments
# android_emulator_args = -no-audio -no-window

# (bool) Wait for the Android emulator to start
# android_emulator_wait = True

# (int) Timeout for the Android emulator to start
# android_emulator_timeout = 300
