# Set editor default keymap to emacs (`-e`) or vi (`-v`)
bindkey -v

# References: https://en.wikipedia.org/wiki/ANSI_escape_code
# \e[0 q：恢复到用户设置的光标形状。
# \e[1 q：方块光标。
# \e[2 q：下划线光标。
# \e[3 q：垂直线光标（竖线）。
# \e[4 q：垂直线光标（粗竖线）。
# \e[5 q：光标形状。

function zle-keymap-select {
	if [[ ${KEYMAP} == vicmd ]] || [[ $1 = 'block' ]]; then
		echo -ne '\e[1 q'
	elif [[ ${KEYMAP} == main ]] || [[ ${KEYMAP} == viins ]] || [[ ${KEYMAP} = '' ]] || [[ $1 = 'beam' ]]; then
		echo -ne '\e[5 q'
  fi
}
zle -N zle-keymap-select

# Use beam shape cursor on startup.
echo -ne '\e[5 q'

# Use beam shape cursor for each new prompt.
preexec() {
	echo -ne '\e[5 q'
}

_fix_cursor() {
	echo -ne '\e[5 q'
}
precmd_functions+=(_fix_cursor)

KEYTIMEOUT=1
