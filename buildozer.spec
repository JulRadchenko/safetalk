[app]
title = Voice Analyzer
package.name = voiceanalyzer
package.domain = org.example

source.dir = .
source.include_exts = py,png,jpg,kv,json,ttf,otf,wav,mp3,ogg

version = 1.0

requirements = python3,kivy,kivymd,requests,plyer,pyjnius

android.permissions = RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET,MODIFY_AUDIO_SETTINGS

android.api = 33
android.minapi = 21
android.ndk = 25b
android.sdk = 33

android.archs = arm64-v8a,armeabi-v7a

android.allow_backup = True
android.private_storage = True

log_level = 2
warn_on_root = 1
