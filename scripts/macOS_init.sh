#!/bin/bash

if ! command -v brew &>/dev/null; then
  echo "Homebrew 未安装，正在安装 Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew 已安装"
fi

echo "使用 Homebrew 安装软件..."
brew install lazygit neovim yazi kitty fzf zoxide starship bat eza atuin fastfetch ice

echo "使用 Homebrew 安装 Node.js 和 Ruby... 包管理工具"
brew install rbenv
echo "Homebrew installation is not supported. If you have issues with homebrew-installed nvm, please brew uninstall it, and install it using the instructions below, before filing an issue."

echo "使用 Homebrew 安装 AltTab"
brew install --cask alt-tab

echo "字体Maple Mono NF CN"
brew install --cask font-maple-mono-nf-cn

echo "记得按装 *raycast* *clashX* *whistle* *vscode* ..."

