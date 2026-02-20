PROMPT_PREFIX="  Execute instruction:"

# json
alias checkjson='find . -name "*.json" -not -path "*/node_modules/*" -exec sh -c "python3 -m json.tool {} > /dev/null || echo \"❌ 错误文件: {}\"" \;'

# yazi
function y() {
	local tmp="$(mktemp -t "yazi-cwd.XXXXXX")" cwd
	yazi "$@" --cwd-file="$tmp"
	if cwd="$(command cat -- "$tmp")" && [ -n "$cwd" ] && [ "$cwd" != "$PWD" ]; then
		builtin cd -- "$cwd"
	fi
	rm -f -- "$tmp"
}

# node
NRD="npm run dev"
NRB="npm run build"
NLL="npm ls -g --depth=0 --link=true"

nrd() {
  echo -e "$PROMPT_PREFIX $NRD\n"
  eval "$NRD"
}

nrb() {
  echo -e "$PROMPT_PREFIX $NRB\n"
  eval "$NRB"
}

nll() {
  echo -e "$PROMPT_PREFIX $NLL\n"
  eval "$NLL"
}

# Web -> live server

# Use: live 8080
live() {
  local port=${1:-5500}

  # 循环检测端口是否被占用
  # lsof -i :$port 用于检查端口是否有进程在监听
  while lsof -Pi :$port -sTCP:LISTEN -t >/dev/null ; do
    echo "⚠️  Port $port is already occupied, try the next one..."
    port=$((port + 1))
  done

  echo "🚀 Port ready！Starting Five Server (Port: $port)..."
  
  # 执行启动命令
  # --open: 自动打开浏览器
  # --port: 指定最终确定的空闲端口
  bunx five-server . --port=$port --open
}

# git
alias gl="lazygit"

gcr() {
  local branch=${1:-develop}
  local GCR="git push origin HEAD:refs/for/$branch"
  echo -e "$PROMPT_PREFIX $GCR\n"
  eval "$GCR"
}

# cd git root dir
gr() {
  local git_root
  git_root=$(git rev-parse --show-toplevel 2>/dev/null)
  if [[ $? -eq 0 && -d $git_root ]]; then
    cd "$git_root"
  else
    echo "Not in a git repository or could not find the git root."
  fi
}

# make sure use homebrew ctags first or use system default
# https://github.com/universal-ctags/ctags
# Use: ctags -R .
# 生成一个 tags 索引文件 -> 编辑器读取该文件实现秒速跳转
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
