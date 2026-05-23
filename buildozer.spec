[app]
title = Безопасный разговор
package.name = safetalk
package.domain = com.safetalk
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav
source.include_patterns = assets/*.png,assets/*.jpg
source.exclude_exts = spec,log,pyc
source.exclude_dirs = tests,bin,.git,__pycache__,venv
version = 1.0.0

# Исправленные требования
requirements = python3==3.10.14,hostpython3==3.10.14,kivy==2.3.0,kivymd==2.0.1.dev0,requests==2.31.0,pyjnius==1.6.1,plyer==2.1

icon.filename = %(source.dir)s/assets/safetalk_icon.png

# Разрешения
android.permissions = RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

# Исправленные настройки Android API
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 23b  # Изменено с 25b на 23b

android.enable_androidx = True
android.gradle = True
android.gradle_version = 7.4.2  # Изменено с 8.2.2 на стабильную версию
android.java_jdk = 17
android.arch = arm64-v8a

# Удаляем устаревшую зависимость
# android.gradle_dependencies = 

android.enable_java8 = True
android.debug = 1
android.verbose = False

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True
