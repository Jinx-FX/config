export EDITOR=nvim

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

# nvm config
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion
export PATH="/Users/didi/.rbenv/shims:${PATH}"
export RBENV_SHELL=sh
command rbenv rehash 2>/dev/null
rbenv() {
  local command
  command="${1:-}"
  if [ "$#" -gt 0 ]; then
    shift
  fi

  case "$command" in
  rehash|shell)
    eval "$(rbenv "sh-$command" "$@")";;
  *)
    command rbenv "$command" "$@";;
  esac
}

# flutter config
export PATH="$PATH:$HOME/development/flutter/bin"

# bun completions
[ -s "/Users/didi/.bun/_bun" ] && source "/Users/didi/.bun/_bun"

# bun config
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# Mysql config
export PATH="$PATH":/usr/local/mysql/bin

