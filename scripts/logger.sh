#!/usr/bin/env bash

declare -rA color_text=(
	[red]='\e[0;31m'
	[green]='\e[0;32m'
	[yellow]='\e[0;33m'
	[cyan]='\e[0;36m'
)

declare -r color_reset='\e[0m'

err() {
	echo -e "${color_text[red]}${*}${color_reset}"
}

die() {
	err "$*"
	exit 1
}

warn() {
	echo -e "${color_text[yellow]}${*}${color_reset}"
}

note() {
	echo -e "${color_text[cyan]}${*}${color_reset}"
}

hint() {
	echo -e "${color_text[green]}${*}${color_reset}"
}

log() {
	echo -e "${color_reset}${*}${color_reset}"
}
