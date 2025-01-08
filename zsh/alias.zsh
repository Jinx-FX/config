PROMPT_PREFIX="  Execute instruction:"

# node
alias nrd='echo "$PROMPT_PREFIX npm run dev\n"; npm run dev'
alias nrb='echo "$PROMPT_PREFIX npm run build\n"; npm run build'
alias nll='echo "$PROMPT_PREFIX npm ls -g --depth=0 --link=true\n";npm ls -g --depth=0 --link=true'

# git
alias gcr='echo "$PROMPT_PREFIX git push origin HEAD:refs/for/develop\n"; git push origin HEAD:refs/for/develop'