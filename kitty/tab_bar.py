from typing import Callable
from kitty.fast_data_types import Screen, add_timer, get_boss, get_options
from kitty.tab_bar import DrawData, TabBarData, ExtraData, TabAccessor, as_rgb
from kitty.utils import color_as_int
import os
import datetime
import random
from pathlib import Path

opts = get_options()

BG = as_rgb(color_as_int(opts.color8))
FG = as_rgb(color_as_int(opts.color7))
COLOR_1 = as_rgb(color_as_int(opts.color2))
COLOR_2 = as_rgb(color_as_int(opts.color5))
COLOR_3 = as_rgb(color_as_int(opts.color4))
COLOR_4 = as_rgb(color_as_int(opts.color4))

REFRESH_TIME = 3
MAX_LENGTH_PATH = 3

FOLDER_ICON = " "
TIME_ICON = "󰥔 "
SESSION_ICON = " "

ICONS = [
    " ",
    " ",
    "󰝱 ",
    "󰋄 ",
    "󰋅 ",
    " ",
    "󰁨 ",
    "󰈸 ",
    "󱕣 ",
    "󰣙 ",
    " ",
    " ",
    " ",
    "󰌽 ",
    "󰲄 ",
]


active_tab = None
timer_id = None

_TAB_ICON_CACHE = {}
_TAB_WD_CACHE = {}


class Cell:
    def __init__(
        self,
        icon: str,
        text_fn: Callable[[int, TabBarData], str | None],
        tab: TabBarData = None,
        bg: str = BG,
        fg: str = FG,
        color: int = COLOR_1,
        separator: str = "",
        border: tuple[str, str] = ("", ""),
    ) -> None:

        self.tab: TabBarData = tab
        self.fg: str = fg
        self.bg: str = bg
        self.color: int = color
        self.icon: str = icon
        self.text_fn: Callable[[int, TabBarData], str | None] = text_fn
        self.border: tuple[str, str] = border
        self.separator: str = separator
        self.text_length_overhead = (
            len(self.border[0] + self.border[1] + self.separator + self.icon) + 1
        )

    def draw(self, screen: Screen, max_size: int) -> None:
        text = self.text_fn(max_size - self.text_length_overhead, self.tab)

        if text is None:
            return

        screen.cursor.dim = False
        screen.cursor.bold = False
        screen.cursor.italic = False

        screen.cursor.bg = 0
        screen.cursor.fg = self.color
        screen.draw(self.border[0])

        screen.cursor.bg = self.color
        screen.cursor.fg = self.bg
        screen.cursor.bold = True
        screen.draw(self.icon)
        screen.cursor.bold = False

        if text == "":
            screen.cursor.bg = 0
            screen.cursor.fg = self.color
            screen.draw(self.border[1])
        else:
            screen.cursor.bg = self.bg
            screen.cursor.fg = self.color
            screen.draw(self.separator)

            screen.cursor.fg = self.fg
            screen.draw(f" {text}")

            screen.cursor.fg = self.bg
            screen.cursor.bg = 0
            screen.draw(self.border[1])

        return screen.cursor.x

    def length(self, max_size: int) -> int:
        text = self.text_fn(max_size - self.text_length_overhead, self.tab)

        if text is None:
            return 0
        elif text == "":
            return len(self.icon + self.border[0] + self.border[1])
        else:
            return len(text) + self.text_length_overhead


def get_wd(max_size: int, tab: TabBarData):
    if tab is None:
        return "~"

    accessor = TabAccessor(tab.tab_id)
    raw_wd = accessor.active_wd

    if raw_wd and raw_wd != "":
        _TAB_WD_CACHE[tab.tab_id] = raw_wd
    else:
        if tab.title and (tab.title.startswith("/") or tab.title.startswith("~")):
            raw_wd = tab.title
        else:
            raw_wd = _TAB_WD_CACHE.get(tab.tab_id)

        if not raw_wd:
            raw_wd = tab.title if tab.title else "busy"

    if str(raw_wd).startswith("~"):
        home_dir = os.getenv("HOME", "/")
        raw_wd = str(raw_wd).replace("~", home_dir, 1)

    wd = Path(raw_wd)
    home = Path(os.getenv("HOME", "/"))

    try:
        if wd.is_relative_to(home):
            if wd == home:
                wd = Path("~")
            else:
                wd = Path("~") / wd.relative_to(home)
    except (ValueError, AttributeError):
        pass

    parts = list(wd.parts)
    compressed = False
    if len(parts) > MAX_LENGTH_PATH:
        compressed = True
        parts = [parts[0], ".."] + parts[-MAX_LENGTH_PATH:]

    parts_cnt = 1 + compressed
    while parts_cnt != len(parts):
        wd_str = "/".join(parts[0 : 1 + compressed] + parts[parts_cnt:])
        if len(wd_str) <= max_size:
            return wd_str
        parts_cnt += 1

    if parts and len(parts[-1]) <= max_size:
        return parts[-1]

    return "..."


def get_time(max_size: int, tab: TabBarData) -> str | None:
    if max_size < 5:
        return None
    else:
        return datetime.datetime.now().strftime("%H:%M")


def get_tab(max_size: int, tab: TabBarData) -> str | None:
    if tab is None:
        return "tab"

    accessor = TabAccessor(tab.tab_id)
    text = ""

    if tab.title and tab.title[0] == "#":
        text = tab.title[1:]
    else:
        try:
            text = str(accessor.active_exe)
        except Exception:
            text = ""

        if not text or text == "None":
            text = tab.title or f"tab:{tab.tab_id}"

    if max_size <= len(text):
        return ""
    else:
        return text


def get_session(max_size: int, tab: TabBarData) -> str | None:
    text = tab.session_name
    if text == "":
        text = "none"
    if len(text) <= max_size:
        return text
    elif max_size >= 3:
        return text[:3]
    else:
        return None


def get_tab_cell(tab: TabBarData) -> Cell:
    color = COLOR_2 if tab.is_active else COLOR_1
    icon = str(tab.tab_id)

    if tab.tab_id in _TAB_ICON_CACHE:
        icon = _TAB_ICON_CACHE[tab.tab_id]
    else:
        if ICONS:
            last_icon = list(_TAB_ICON_CACHE.values())[-1] if _TAB_ICON_CACHE else None

            if last_icon in ICONS:
                candidates = [i for i in ICONS if i != last_icon]
            else:
                candidates = ICONS

            new_icon = random.choice(candidates) if candidates else random.choice(ICONS)

            _TAB_ICON_CACHE[tab.tab_id] = new_icon
            icon = new_icon
        else:
            icon = str(tab.tab_id)

    return Cell(icon, text_fn=get_tab, tab=tab, color=color)


def _redraw_tab_bar(_):
    tm = get_boss().active_tab_manager
    if tm is not None:
        tm.mark_tab_bar_dirty()


def _draw_left(screen: Screen, max_length: int):
    cell = Cell(FOLDER_ICON, get_wd, active_tab, color=COLOR_4)
    cell.draw(screen, max_length)


def _draw_right(screen: Screen):
    max_size = screen.columns - screen.cursor.x
    time_cell = Cell(TIME_ICON, get_time, color=COLOR_3)
    session_cell = Cell(SESSION_ICON, get_session, active_tab, color=COLOR_3)

    total_length = time_cell.length(max_size)
    session_length = session_cell.length(max_size - total_length - 1)

    if session_length != 0:
        total_length += 1 + session_length

    offset_length = max_size - total_length
    screen.draw(" " * offset_length)

    if session_length != 0:
        session_cell.draw(screen, session_length)
        screen.draw(" ")

    time_cell.draw(screen, max_size)


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_title_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    global active_tab, timer_id

    if timer_id is None:
        timer_id = add_timer(_redraw_tab_bar, REFRESH_TIME, True)

    if active_tab is None or tab.is_active:
        active_tab = tab

    screen.cursor.x = before

    if index == 1 and not extra_data.for_layout:
        _draw_left(screen, max(0, screen.columns - screen.cursor.x))
        screen.draw(" ")

    end = get_tab_cell(tab).draw(screen, max_title_length)
    screen.draw(" ")

    if is_last and not extra_data.for_layout:
        _draw_right(screen)
    return end
