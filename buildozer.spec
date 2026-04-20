# buildozer.spec для APK
[app]

title = Voice Analyzer
package.name = safetalk
package.domain = org.safetalk

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 0.1

requirements = requirements = python3,kivy,kivymd,pillow,plyer,android

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.2.1

fullscreen = 0

android.permissions = INTERNET, RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.accept_sdk_license = True
android.ndk = 25b
android.sdk = 30
android.api = 30
android.minapi = 21

android.add_src = 

[buildozer]
log_level = 2
warn_on_root = 0
