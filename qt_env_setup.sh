#!/bin/bash

# Qt environment setup for iPhone Dev Mode Pro
export QT_PLUGIN_PATH="/home/mrkent/dev/webapp/.venv/lib/python3.12/site-packages/PyQt5/Qt5/plugins"
export QT_QPA_PLATFORM_PLUGIN_PATH="/home/mrkent/dev/webapp/.venv/lib/python3.12/site-packages/PyQt5/Qt5/plugins/platforms"
export QTWEBENGINEPROCESS_PATH="/home/mrkent/dev/webapp/.venv/lib/python3.12/site-packages/PyQt5/Qt5/libexec/QtWebEngineProcess"
export QTWEBENGINE_CHROMIUM_FLAGS="--no-sandbox"
export QT_QUICK_BACKEND=software

echo "Qt environment variables set:"
echo "QT_PLUGIN_PATH=$QT_PLUGIN_PATH"
echo "QT_QPA_PLATFORM_PLUGIN_PATH=$QT_QPA_PLATFORM_PLUGIN_PATH"
echo "QTWEBENGINEPROCESS_PATH=$QTWEBENGINEPROCESS_PATH"
echo "QTWEBENGINE_CHROMIUM_FLAGS=$QTWEBENGINE_CHROMIUM_FLAGS"