from __future__ import annotations

import datetime
import os
import random
from pathlib import Path
from typing import Callable, Optional

from kitty.fast_data_types import Screen, add_timer, get_boss, get_options
from kitty.tab_bar import DrawData, ExtraData, TabAccessor, TabBarData, as_rgb
from kitty.utils import color_as_int

try:
    from kitty.fast_data_types import wcswidth as _wcswidth
except ImportError:
    try:
        from kitty.tab_bar import wcswidth as _wcswidth
    except ImportError:
        _wcswidth = None

opts = get_options()

BG = as_rgb(color_as_int(opts.color8))
FG = as_rgb(color_as_int(opts.color7))
COLOR_1 = as_rgb(color_as_int(opts.color2))
COLOR_2 = as_rgb(color_as_int(opts.color5))
COLOR_3 = as_rgb(color_as_int(opts.color4))
COLOR_4 = as_rgb(color_as_int(opts.color4))
COLOR_ATTN = as_rgb(color_as_int(opts.color1))

REFRESH_TIME = 3
MAX_LENGTH_PATH = 3
MAX_SESSION_LENGTH = 12
LEFT_MAX = 30
TAB_GAP = 1
MIN_TAB_WIDTH = 4
NATURAL = 512

FOLDER_ICON = "\uf07b "
TIME_ICON = "\U000f0954 "
SESSION_ICON = "\uf489 "

ICONS = [
    "\uef4e ",
    "\ue24a ",
    "\U000f0771 ",
    "\U000f02c4 ",
    "\U000f02c5 ",
    "\uf1d8 ",
    "\U000f0068 ",
    "\U000f0238 ",
    "\U000f1563 ",
    "\U000f08d9 ",
    "\ue370 ",
    "\ue796 ",
    "\ue23a ",
    "\U000f033d ",
    "\U000f0c84 ",
]

SEPARATOR = "\ue0b4"
BORDER_LEFT = "\ue0b6"
BORDER_RIGHT = "\ue0b4"


def _dw(s: str) -> int:
    if not s:
        return 0
    if _wcswidth is not None:
        try:
            w = _wcswidth(s)
        except Exception:
            w = -1
        if w >= 0:
            return w
    return len(s)


def _trunc(s: str, max_cells: int) -> str:
    if max_cells < 1:
        return ""
    if _dw(s) <= max_cells:
        return s
    if max_cells == 1:
        return "…"
    used = 0
    out = []
    for ch in s:
        w = _dw(ch)
        if w < 1:
            w = 1
        if used + w > max_cells - 1:
            break
        out.append(ch)
        used += w
    return "".join(out) + "…"


timer_id: Optional[int] = None
_pass_budget = 0
_pass_right_w = 0
_pass_layout_default = 0
_pass_layout_n = 0

_TAB_ICON_CACHE: dict = {}
_TAB_WD_CACHE: dict = {}
_NUM_TABS_CACHE: dict = {}
_ACTIVE_TAB_CACHE: dict = {}


class Cell:
    def __init__(
        self,
        icon: str,
        text_fn: Callable[[int, Optional[TabBarData]], Optional[str]],
        tab: Optional[TabBarData] = None,
        bg: int = BG,
        fg: int = FG,
        color: int = COLOR_1,
        separator: str = SEPARATOR,
        border: tuple = (BORDER_LEFT, BORDER_RIGHT),
    ) -> None:
        self.tab: Optional[TabBarData] = tab
        self.fg: int = fg
        self.bg: int = bg
        self.color: int = color
        self.icon: str = icon
        self.text_fn: Callable[[int, Optional[TabBarData]], Optional[str]] = text_fn
        self.border: tuple = border
        self.separator: str = separator
        self.icon_w: int = _dw(icon)
        self.border_w: int = _dw(border[0]) + _dw(border[1])
        self.sep_w: int = _dw(separator)
        self.empty_w: int = self.border_w + self.icon_w
        self.text_length_overhead: int = self.empty_w + self.sep_w + 1

    def _clamp(self, text: str, max_size: int) -> str:
        room = max_size - self.text_length_overhead
        if room < 1:
            return ""
        if _dw(text) <= room:
            return text
        return _trunc(text, room)

    def draw(self, screen: Screen, max_size: int) -> int:
        text = self.text_fn(max_size - self.text_length_overhead, self.tab)

        if text is None:
            return screen.cursor.x
        text = self._clamp(text, max_size)

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
        text = self._clamp(text, max_size)
        if text == "":
            return self.empty_w
        return self.text_length_overhead + _dw(text)


def get_wd(max_size: int, tab: Optional[TabBarData]) -> str:
    if max_size < 1:
        return ""
    if tab is None:
        return "~"

    raw_wd = ""
    try:
        raw_wd = TabAccessor(tab.tab_id).active_wd or ""
    except Exception:
        pass

    if raw_wd:
        _TAB_WD_CACHE[tab.tab_id] = raw_wd
    elif tab.title and (tab.title.startswith("/") or tab.title.startswith("~")):
        raw_wd = tab.title
    else:
        raw_wd = _TAB_WD_CACHE.get(tab.tab_id, "")

    if not raw_wd:
        raw_wd = tab.title or "busy"

    try:
        wd = Path(str(raw_wd))
        home = Path(os.getenv("HOME", "/"))
        if wd.is_relative_to(home):
            wd = Path("~") if wd == home else Path("~") / wd.relative_to(home)
        parts = list(wd.parts)
    except Exception:
        parts = [str(raw_wd)]

    candidates = ["/".join(parts)]
    if len(parts) > MAX_LENGTH_PATH + 1:
        candidates.append("/".join([parts[0], ".."] + parts[-MAX_LENGTH_PATH:]))
    if len(parts) > 2:
        candidates.append(f"{parts[0]}/../{parts[-1]}")
    if len(parts) > 1:
        candidates.append(parts[-1])

    for c in candidates:
        if _dw(c) <= max_size:
            return c

    return _trunc(parts[-1] if parts else str(raw_wd), max_size)


def get_time(max_size: int, tab: Optional[TabBarData]) -> Optional[str]:
    if max_size < 5:
        return None
    return datetime.datetime.now().strftime("%H:%M")


def get_tab(max_size: int, tab: Optional[TabBarData]) -> str:
    if tab is None:
        text = "tab"
    elif tab.title and tab.title[0] == "#":
        text = tab.title[1:]
    else:
        try:
            text = str(TabAccessor(tab.tab_id).active_exe)
        except Exception:
            text = ""
        if not text or text == "None":
            text = tab.title or f"tab:{tab.tab_id}"

    if max_size < 1:
        return ""
    if _dw(text) <= max_size:
        return text
    return _trunc(text, max_size)


def get_session(max_size: int, tab: Optional[TabBarData]) -> Optional[str]:
    text = tab.session_name if (tab is not None and tab.session_name) else "none"
    text = _trunc(text, MAX_SESSION_LENGTH)
    if max_size < 1:
        return None
    if _dw(text) <= max_size:
        return text
    if max_size == 1:
        return "…"
    return _trunc(text, max_size)


def _tab_icon(tab_id: int) -> str:
    icon = _TAB_ICON_CACHE.get(tab_id)
    if icon is None:
        last = list(_TAB_ICON_CACHE.values())[-1] if _TAB_ICON_CACHE else None
        candidates = [i for i in ICONS if i != last] if last in ICONS else ICONS
        icon = random.choice(candidates) if candidates else (ICONS[0] if ICONS else str(tab_id))
        _TAB_ICON_CACHE[tab_id] = icon
    return icon


def get_tab_cell(tab: TabBarData) -> Cell:
    if tab.needs_attention:
        color = COLOR_ATTN
    elif tab.is_active:
        color = COLOR_2
    else:
        color = COLOR_1
    return Cell(_tab_icon(tab.tab_id), text_fn=get_tab, tab=tab, color=color)


def _redraw_tab_bar(_) -> None:
    tm = get_boss().active_tab_manager
    if tm is not None:
        tm.mark_tab_bar_dirty()


def _count_tabs_for_window(wid: int) -> Optional[int]:
    try:
        boss = get_boss()
        try:
            for tm in boss.all_tab_managers:
                if getattr(tm, "os_window_id", None) == wid:
                    return len(tm.tabs)
        except Exception:
            pass
        try:
            atm = boss.active_tab_manager
            if atm is not None and getattr(atm, "os_window_id", None) == wid:
                return len(atm.tabs)
        except Exception:
            pass
    except Exception:
        pass
    return None


def _estimate_num_tabs(tab: TabBarData, index: int, mtl: int, cols: int) -> int:
    n = max(1, index)
    cached = _NUM_TABS_CACHE.get(tab.os_window_id, 0)
    if cached > n:
        n = cached
    if mtl and mtl > 0:
        derived = cols // (mtl + 1)
        if derived > n:
            n = derived
    exact = _count_tabs_for_window(tab.os_window_id)
    if exact is not None and exact >= 1:
        n = exact
    return n


def _plan_pass(cols: int, x: int, n: int, tab: Optional[TabBarData], mtl: int) -> tuple:
    time_len = Cell(TIME_ICON, get_time, color=COLOR_3).length(NATURAL)
    sess_len = Cell(SESSION_ICON, get_session, tab, color=COLOR_3).length(NATURAL)
    right_full = time_len + (TAB_GAP + sess_len if sess_len else 0)
    plans = (
        (LEFT_MAX, right_full),
        (LEFT_MAX, time_len),
        (18, time_len),
        (10, time_len),
        (0, time_len),
        (0, 0),
    )

    default = max(1, cols // n - 1) if n > 0 else max(1, cols - 1)
    # layout pass 可能用过期 tab 数 → kitty 分配的 mtl 可能偏大, 按最坏情况预留
    mtl_wc = max(default, _pass_layout_default)

    def budget_of(left_b: int, right_w: int) -> int:
        avail = cols - x - left_b - (TAB_GAP if left_b else 0)
        b = (avail - right_w - n * TAB_GAP) // n
        # kitty cut 阈值 = cols - mtl_next (≥ cols - mtl_wc)
        # 保证 left + (n-1)(b+gap) <= cols - mtl_wc
        if n > 1:
            nocut = (cols - mtl_wc - left_b - TAB_GAP) // (n - 1) - TAB_GAP
            b = min(b, nocut)
        if mtl > 0:
            b = min(b, mtl)
        return b

    for thr in (9, 6, MIN_TAB_WIDTH):
        for plan in plans:
            b = budget_of(*plan)
            if b >= thr:
                return plan[0], plan[1], b

    return 0, 0, MIN_TAB_WIDTH


def _draw_right(screen: Screen, tab: Optional[TabBarData]) -> None:
    cols = screen.columns
    max_size = cols - screen.cursor.x
    if max_size <= 0:
        return

    time_cell = Cell(TIME_ICON, get_time, color=COLOR_3)
    session_cell = Cell(SESSION_ICON, get_session, tab, color=COLOR_3)

    t_len = time_cell.length(max_size)
    s_len = session_cell.length(max_size - t_len - TAB_GAP) if t_len else 0

    total = t_len + (s_len + TAB_GAP if s_len else 0)
    if total > max_size:
        s_len = 0
        total = t_len
    if total > max_size:
        return

    screen.cursor.bg = 0
    screen.cursor.fg = 0
    screen.draw(" " * (max_size - total))

    if s_len:
        session_cell.draw(screen, s_len)
        screen.draw(" " * TAB_GAP)
    if t_len:
        time_cell.draw(screen, t_len)


def draw_tab(
    draw_data: DrawData,
    screen: Screen,
    tab: TabBarData,
    before: int,
    max_tab_length: int,
    index: int,
    is_last: bool,
    extra_data: ExtraData,
) -> int:
    global timer_id, _pass_budget, _pass_right_w, _pass_layout_default, _pass_layout_n

    if timer_id is None:
        timer_id = add_timer(_redraw_tab_bar, REFRESH_TIME, True)

    if tab.is_active:
        _ACTIVE_TAB_CACHE[tab.os_window_id] = tab
    cur = _ACTIVE_TAB_CACHE.get(tab.os_window_id) or tab

    screen.cursor.x = before
    cols = screen.columns

    if index == 1:
        if extra_data.for_layout:
            _pass_right_w = 0
            n = _estimate_num_tabs(tab, index, 0, cols)
            _pass_layout_n = n
            default = max(1, cols // n - 1) if n > 0 else max(1, cols - 1)
            _pass_layout_default = default
            base = max_tab_length if max_tab_length > 0 else max(MIN_TAB_WIDTH, (cols - before) // 2)
            _pass_budget = min(base, default)
        else:
            n = _estimate_num_tabs(tab, index, max_tab_length, cols)
            left_b, right_w, _pass_budget = _plan_pass(cols, before, n, cur, max_tab_length)
            _pass_right_w = right_w
            if left_b > 0 and before + left_b + 2 * TAB_GAP + MIN_TAB_WIDTH <= cols:
                left_cell = Cell(FOLDER_ICON, get_wd, cur, color=COLOR_4)
                if left_cell.length(left_b) > 0:
                    left_cell.draw(screen, left_b)
                    if screen.cursor.x < cols:
                        screen.draw(" ")
    elif extra_data.for_layout and index > _pass_layout_n:
        # layout 中途发现 tab 数超过估计 → 收紧后续理想宽度 (决定 kitty 的 mtl)
        _pass_layout_n = index
        d = max(1, cols // index - 1)
        base = max_tab_length if max_tab_length > 0 else cols
        _pass_budget = min(base, d)

    if not extra_data.for_layout:
        wid = tab.os_window_id
        if index > _NUM_TABS_CACHE.get(wid, 0):
            _NUM_TABS_CACHE[wid] = index

    if _pass_budget <= 0:
        _pass_budget = max(MIN_TAB_WIDTH, min(max_tab_length if max_tab_length > 0 else 40, 40))

    room = cols - screen.cursor.x
    if not extra_data.for_layout and _pass_right_w > 0:
        room -= _pass_right_w + TAB_GAP
    if not is_last:
        room -= MIN_TAB_WIDTH + TAB_GAP

    budget = _pass_budget
    if max_tab_length > 0 and max_tab_length < budget:
        budget = max_tab_length
    if budget > room:
        budget = room

    if budget >= MIN_TAB_WIDTH:
        get_tab_cell(tab).draw(screen, budget)
        if screen.cursor.x < cols:
            screen.draw(" ")

    if is_last:
        _NUM_TABS_CACHE[tab.os_window_id] = index
        if not extra_data.for_layout:
            _draw_right(screen, cur)
            pad = cols - screen.cursor.x
            if pad > 0:
                screen.cursor.bg = 0
                screen.cursor.fg = 0
                screen.draw(" " * pad)

    return screen.cursor.x
