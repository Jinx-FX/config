export PATH=$HOME/.local/bin:$PATH
export EDITOR=nvim
export PATH=$PATH:/opt/homebrew/bin
export PATH=$PATH:/opt/homebrew/sbin
export PATH=$PATH:/Applications/Xcode.app/Contents/Developer/usr/bin/

# nvm config
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh" # This loads nvm
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"  # This loads nvm bash_completion

# rbenv config
export PATH="$HOME/.rbenv/shims:${PATH}"
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

# bun completions
[ -s "$HOME/.bun/_bun" ] && source "$HOME/.bun/_bun"

# bun config
export BUN_INSTALL="$HOME/.bun"
export PATH="$BUN_INSTALL/bin:$PATH"

# Mysql config
export PATH="$PATH":/usr/local/mysql/bin

# Python
for pydir in ~/Library/Python/*/bin; do
    if [ -d "$pydir" ]; then
        export PATH="$PATH:$pydir"
    fi
done

# Android
export ANDROID_HOME=~/Library/Android/sdk
export PATH=$ANDROID_HOME/platform-tools:$PATH  # 包含 adb、fastboot 等
export PATH=$ANDROID_HOME/tools:$PATH          # 包含一些旧工具（部分脚本依赖）
export PATH=$ANDROID_HOME/emulator:$PATH       # 包含模拟器命令（emulator）
export PATH=$ANDROID_HOME/cmdline-tools/latest/bin:$PATH  # 包含 sdkmanager 等新工具
