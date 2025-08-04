#!/bin/bash

set -e

REPO="kartavkun/osufetch"
BIN_NAME="osufetch"
ARCH="$(uname -m)"
INSTALL_DIR="/usr/local/bin"

# Преобразуем архитектуру
case "$ARCH" in
x86_64) ARCH="x86_64" ;;
aarch64) ARCH="aarch64" ;;
*)
  echo "Unsupported architecture: $ARCH"
  exit 1
  ;;
esac

# Получаем последнюю версию
TAG=$(curl -s "https://api.github.com/repos/${REPO}/releases/latest" | grep '"tag_name":' | cut -d '"' -f 4)

echo "📦 Installing $BIN_NAME version $TAG for $ARCH..."

# Формируем URL
BIN_URL="https://github.com/${REPO}/releases/download/${TAG}/${BIN_NAME}-${ARCH}"

# Качаем бинарник во временную директорию
TMP_DIR=$(mktemp -d)
curl -L "$BIN_URL" -o "$TMP_DIR/$BIN_NAME"
chmod +x "$TMP_DIR/$BIN_NAME"

# Перемещаем в /usr/local/bin (может потребовать sudo)
if [ "$EUID" -ne 0 ]; then
  echo "⚠️  Root privileges required to install to $INSTALL_DIR"
  sudo mv "$TMP_DIR/$BIN_NAME" "$INSTALL_DIR/$BIN_NAME"
else
  mv "$TMP_DIR/$BIN_NAME" "$INSTALL_DIR/$BIN_NAME"
fi

echo "✅ $BIN_NAME installed to $INSTALL_DIR/$BIN_NAME"
echo "👉 Run with: $BIN_NAME"
