#!/bin/sh

# Цвета для вывода
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
RESET="\033[0m"

sleep_and_echo() {
    echo -e "$1"
    sleep 0.5
}

if [ "$(id -u)" -ne 0 ]; then
    echo -e "${RED}❌ This script must be run as root (use sudo)${RESET}"
    exit 1
fi

CURRENT_DIR="$(cd "$(dirname "$0")" && pwd)"

CORE_DIR="$CURRENT_DIR/core"
MODULES_DIR="$CURRENT_DIR/modules"

RESULTES_DIR="/usr/share/dotpusher"
INDEX_FILE="$CURRENT_DIR/index.py"

sleep_and_echo "${BLUE}🚀 Starting dotpusher installation...${RESET}"

# prepare destination
if [ ! -d "$RESULTES_DIR" ]; then
    sleep_and_echo "${GREEN}📁 Creating directory $RESULTES_DIR${RESET}"
    mkdir -p "$RESULTES_DIR"
else
    sleep_and_echo "${YELLOW}🗑️  Cleaning existing directory $RESULTES_DIR${RESET}"
    rm -rf "$RESULTES_DIR"
    sleep_and_echo "${GREEN}📁 Recreating directory $RESULTES_DIR${RESET}"
    mkdir -p "$RESULTES_DIR"
fi

# copy core
if [ -d "$CORE_DIR" ]; then
    sleep_and_echo "${GREEN}📂 Copying CORE to $RESULTES_DIR${RESET}"
    cp -r "$CORE_DIR" "$RESULTES_DIR"
else
    sleep_and_echo "${RED}❌ Not found: $CORE_DIR${RESET}"
fi

# copy modules
if [ -d "$MODULES_DIR" ]; then
    sleep_and_echo "${GREEN}📂 Copying MODULES to $RESULTES_DIR${RESET}"
    cp -r "$MODULES_DIR" "$RESULTES_DIR"
else
    sleep_and_echo "${RED}❌ Not found: $MODULES_DIR${RESET}"
fi

# install binary
if [ ! -f "/usr/bin/dotpusher" ]; then
    sleep_and_echo "${YELLOW}⚙️  dotpusher not found in /usr/bin, installing...${RESET}"
    cp "$INDEX_FILE" /usr/bin/dotpusher
    chmod +x /usr/bin/dotpusher
    sleep_and_echo "${GREEN}✅ Installed dotpusher to /usr/bin/dotpusher${RESET}"
else
    sleep_and_echo "${YELLOW}⚠️ dotpusher already installed at /usr/bin/dotpusher${RESET}"
    printf "${BLUE}❓ Do you want to replace it? [y/N]: ${RESET}"
    read -r replace
    case "$replace" in
        [yY][eE][sS]|[yY])
            sleep_and_echo "${YELLOW}♻️ Replacing existing dotpusher...${RESET}"
            rm -f /usr/bin/dotpusher
            cp "$INDEX_FILE" /usr/bin/dotpusher
            chmod +x /usr/bin/dotpusher
            sleep_and_echo "${GREEN}✅ dotpusher replaced successfully.${RESET}"
            ;;
        *)
            sleep_and_echo "${BLUE}ℹ️ Skipped replacing dotpusher.${RESET}"
            ;;
    esac
fi

sleep_and_echo "${GREEN}🎉 Installation complete!${RESET}"

