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
