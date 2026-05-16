[app]
title = Безопасный разговор
package.name = safetalk
package.domain = org.safetalk
icon.filename = %(source.dir)s/assets/safetalk_icon.png

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 0.1

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.2.1

fullscreen = 0

requirements = python3,kivy==2.1.0,kivymd,requests,plyer,jnius,android

android.permissions = INTERNET,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 23b

[buildozer]
log_level = 2
warn_on_root = 0
