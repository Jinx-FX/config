export FZF_CTRL_T_OPTS='--preview "
  if [[ -d {} ]]; then
    tree -C {} | head -200;
  elif [[ -f {} ]]; then
    bat --style=numbers --color=always --line-range :500 {} ||
    cat {};
  fi"
'
export FZF_ALT_C_OPTS="--preview 'eza -a --tree --level=1 --icons --git --color=always --group-directories-first {} | head -200'"

# Set up fzf key bindings and fuzzy completion
source <(fzf --zsh)

# fzf-file-widget
# <CTRL-T> - Paste the selected files and directories onto the command-line
# fzf-history-widget
# <CTRL-R> >> <CTRL-ALT-P> - Paste the selected command from history onto the command-line
# fzf-cd-widget
# <ALT-C> >> <CTRL-G> - cd into the selected directory

bindkey '^[^P' fzf-history-widget
bindkey '^g' fzf-cd-widget

