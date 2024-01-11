# starship config see : https://github.com/starship/starship
eval "$(starship init zsh)"

# atuin config
eval "$(atuin init zsh)"

# joshuto config
alias joshuto='joshuto --output-file /tmp/joshutodir; LASTDIR=`cat /tmp/joshutodir`; cd "$LASTDIR"'

# yazi config
# just use ya<enter>
function ya() {
    tmp="$(mktemp -t "yazi-cwd.XXXXX")"
    yazi --cwd-file="$tmp"
    if cwd="$(cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then
        cd -- "$cwd"
    fi
    rm -f -- "$tmp"
}
# Convert this function to alias
# alias yazi='tmp="$(mktemp -t "yazi-cwd.XXXXX")"; yazi --cwd-file="$tmp"; if cwd="$(cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then cd -- "$cwd"; fi; rm -f -- "$tmp"'
