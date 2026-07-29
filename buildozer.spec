
[app]

# (str) Title of your application
title = Aviator App

# (str) Package name
package.name = aviatorapp

# (str) Package domain (needed for android packaging)
package.domain = org.aviator

# (str) Source directory where the main.py file is located
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Version of the application
version = 0.1

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientations
orientation = portrait

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license automatically
android.accept_sdk_license = True

# (list) Permissions
android.permissions = INTERNET

# (list) Architectures to build for
android.archs = arm64-v8a

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
