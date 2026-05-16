[app]

title = Безопасный разговор
package.name = safetalk
package.domain = org.safetalk
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,wav,mp3,json
version = 1.0.0

requirements = python3,kivy,kivymd,requests,plyer,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

android.api = 30
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.accept_sdk_license = True

log_level = 2

[buildozer]

log_level = 2
android = True
android.accept_sdk_license = True
android.arch = arm64-v8a
android.debug_keystore = True
