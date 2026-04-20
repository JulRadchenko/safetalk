# buildozer.spec для APK
[app]

title = Voice Analyzer
package.name = voiceanalyzer
package.domain = com.yourcompany.voiceanalyzer

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf

version = 0.1

requirements = python3,kivy==2.2.1,kivymd==1.1.1,requests==2.31.0,plyer==2.1,pyjnius==1.5.0,android==1.0

orientation = portrait

osx.python_version = 3
osx.kivy_version = 2.2.1

fullscreen = 0

android.permissions = INTERNET, RECORD_AUDIO, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

android.api = 30
android.minapi = 21
android.ndk = 25b
android.sdk = 30

android.add_src = 

[buildozer]
log_level = 2
warn_on_root = 0
