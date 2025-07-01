#!/bin/sh

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

RESULTES_DIR="/usr/share/dotpusher"
BIN_FILE="/usr/bin/dotpusher"

sleep_and_echo "${BLUE}🗑️ Starting dotpusher uninstall process...${RESET}"

if [ -d "$RESULTES_DIR" ]; then
    sleep_and_echo "${YELLOW}🧹 Removing directory $RESULTES_DIR${RESET}"
    rm -rf "$RESULTES_DIR"
    sleep_and_echo "${GREEN}✅ Directory removed: $RESULTES_DIR${RESET}"
else
    sleep_and_echo "${BLUE}ℹ️ Directory not found: $RESULTES_DIR${RESET}"
fi

if [ -f "$BIN_FILE" ]; then
    sleep_and_echo "${YELLOW}🧹 Removing binary $BIN_FILE${RESET}"
    rm -f "$BIN_FILE"
    sleep_and_echo "${GREEN}✅ Binary removed: $BIN_FILE${RESET}"
else
    sleep_and_echo "${BLUE}ℹ️ Binary not found: $BIN_FILE${RESET}"
fi

sleep_and_echo "${GREEN}🎉 dotpusher successfully uninstalled!${RESET}"

