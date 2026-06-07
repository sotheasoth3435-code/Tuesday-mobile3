[app]
title           = TUESDAY
package.name    = tuesday
package.domain  = com.albe

source.dir      = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,json,ttf,env

version         = 1.0.0

# ── Requirements ──────────────────────────────────────────────────────────────
# FIXES:
#   - kivymd pinned to 2.0.1 (latest stable, matches kivy 2.3.0)
#   - openai pinned to 1.35.0 (stable, works on Android)
#   - pyjnius (NOT jnius — was wrong package name, caused build failure)
#   - certifi + charset-normalizer added (required by openai for SSL on Android)
#   - httpx added (openai async client dependency)
#   - python-dotenv added
requirements = \
    python3,\
    kivy==2.3.0,\
    kivymd==2.0.1,\
    openai==1.35.0,\
    python-dotenv==1.0.1,\
    requests==2.32.3,\
    pillow,\
    pyjnius,\
    certifi,\
    charset-normalizer,\
    httpx,\
    android

# ── Orientation ───────────────────────────────────────────────────────────────
orientation = portrait

# ── Android permissions ───────────────────────────────────────────────────────
android.permissions = \
    INTERNET,\
    RECORD_AUDIO,\
    READ_CONTACTS,\
    SEND_SMS,\
    READ_CALENDAR,\
    WRITE_CALENDAR,\
    RECEIVE_SMS,\
    CHANGE_WIFI_STATE,\
    ACCESS_WIFI_STATE,\
    MODIFY_AUDIO_SETTINGS,\
    VIBRATE,\
    RECEIVE_BOOT_COMPLETED

# ── Android SDK/NDK ───────────────────────────────────────────────────────────
# FIXES:
#   - api and sdk now both = 34 (was 35 vs 34 mismatch, caused build conflict)
#   - minapi lowered to 26 (Android 8+) — was 31 which blocked Android 10/11
#   - ndk stays 25b (most compatible with p4a and Kivy)
android.api             = 34
android.minapi          = 26
android.ndk             = 25b
android.sdk             = 34
android.ndk_api         = 21
android.archs           = arm64-v8a

# ── AndroidX ─────────────────────────────────────────────────────────────────
android.enable_androidx = True
android.gradle_dependencies = com.google.android.material:material:1.11.0

# ── App icon & presplash ──────────────────────────────────────────────────────
# Uncomment and add your icon file to use a custom icon:
# icon.filename      = %(source.dir)s/tuesday_icon.png
# presplash.filename = %(source.dir)s/tuesday_splash.png

# ── p4a bootstrap ─────────────────────────────────────────────────────────────
p4a.bootstrap = sdl2

[buildozer]
log_level    = 2
warn_on_root = 1
