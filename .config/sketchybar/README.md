# SketchyBar Setup

> Fork https://github.com/FelixKratz/dotfiles/tree/master/.config/sketchybar

- Dependencies(sf-symbols, jq, github-cli, switchaudio-osx, sketchybar-app-font):

```sh
brew install --cask sf-symbols
brew install jq
brew install gh
brew install switchaudio-osx
curl -L https://github.com/kvndrsslr/sketchybar-app-font/releases/download/v1.0.16/sketchybar-app-font.ttf -o $HOME/Library/Fonts/sketchybar-app-font.ttf
```

- (optional) gh auth login for GitHub notifications
- (optional) If you don't use yabai you can safely remove the yabai item from items/yabai.sh or sketchybarrc
- (optional; needed for yabai window state) yabai event:

```sh
https://github.com/FelixKratz/dotfiles/tree/master/.config/sketchybar
```

- (optional; needed for yabai window state) skhd shortcuts should trigger the sketchybar event, e.g.:

```sh
lalt - space : yabai -m window --toggle float; sketchybar --trigger window_focus
shift + lalt - f : yabai -m window --toggle zoom-fullscreen; sketchybar --trigger window_focus
lalt - f : yabai -m window --toggle zoom-parent; sketchybar --trigger window_focus
```

- (optional) update outdated packages after running brew commands (add to .zshrc):

```sh
function brew() {
  command brew "$@" 

  if [[ $* =~ "upgrade" ]] || [[ $* =~ "update" ]] || [[ $* =~ "outdated" ]]; then
    sketchybar --trigger brew_update
  fi
}
```

NOTE: The helper C program is included here only to show off this specific functionality of sketchybar and is not needed generally. It provides the data for the cpu graph. Using a mach_helper provides a much lower overhead solution for performance sensitive tasks, since the helper talks directly to sketchybar via kernel level messages. For most tasks (including those listed above) this difference in performance does not matter at all.
