#!/bin/bash
export LIBGL_ALWAYS_SOFTWARE=1
export MESA_GL_VERSION_OVERRIDE=3.3
export QT_X11_NO_MITSHM=1
export QTWEBENGINE_CHROMIUM_FLAGS="--disable-gpu --no-sandbox"
freecad "$@"
