[app]
title = Безопасный разговор
package.name = safetalk
package.domain = org.safetalk
icon.filename = %(source.dir)s/assets/safetalk_icon.png

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 0.1

requirements = python3,kivy==2.2.1,kivymd==1.1.1,plyer,requests,pyjnius==1.6.0

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.2.1

fullscreen = 0

android.permissions = RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE, INTERNET

android.accept_sdk_license = True
android.ndk = 25b
android.sdk = 30
android.api = 30
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 0
