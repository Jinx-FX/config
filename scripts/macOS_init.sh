#!/bin/bash

if ! command -v brew &> /dev/null
then
    echo "Homebrew 未安装，正在安装 Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "Homebrew 已安装"
fi

echo "使用 Homebrew 安装软件..."
brew install lazygit neovim yazi kitty fzf zoxide starship bat eza atuin fastfetch ice

echo "使用 Homebrew 安装 Node.js 和 Ruby... 包管理工具"
brew install nvm rbenv

echo "记得按装 *raycast* *AltTab* *clashX* *whistle* *vscode* ..."
