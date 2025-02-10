PROMPT_PREFIX="  Execute instruction:"

# node
NRD="npm run dev"
NRB="npm run build"
NLL="npm ls -g --depth=0 --link=true"

nrd() {
  echo "$PROMPT_PREFIX $NRD\n"
  eval $NRD
}

nrb() {
  echo "$PROMPT_PREFIX $NRB\n"
  eval $NRB
}

nll() {
  echo "$PROMPT_PREFIX $NLL\n"
  eval $NLL
}

# git
GCR="git push origin HEAD:refs/for/develop"

gcr() {
  echo "$PROMPT_PREFIX $GCR\n"
  eval $GCR
}

# other
ctags() {
    local brew_ctags="/opt/homebrew/bin/ctags"
    if [ -x "$brew_ctags" ]; then
        "$brew_ctags" "$@"
    else
        echo "Error: The ctags installed by Homebrew ($brew_ctags) is not available." >&2
        if command -v ctags > /dev/null 2>&1; then
            echo "Trying to use the system's default ctags..." >&2
            command ctags "$@"
        else
            echo "Error: No available ctags was found in the system." >&2
            return 1
        fi
    fi
}
