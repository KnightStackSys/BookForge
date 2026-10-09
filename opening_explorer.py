from __future__ import annotations

import argparse
import re
import random
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from book_db import BookDB, position_key
from book_types import BookMove


PLAYER_ORDER = ("Red", "Blue", "Yellow", "Green")
PLAYER_SHORT = ("R", "B", "Y", "G")


def turn_from_root(root_spec: str, ply: int) -> tuple[str, str]:
    """
    Return (long_name, short_name) for the player to move.

    startpos is Red to move.
    FEN4 roots use their first field (R/B/Y/G) as the side to move.
    """
    start_index = 0

    if root_spec.startswith("fen "):
        fen = root_spec[4:].strip()
        if fen:
            turn = fen.split("-", 1)[0].strip().upper()
            if turn in PLAYER_SHORT:
                start_index = PLAYER_SHORT.index(turn)

    idx = (start_index + ply) % 4
    return PLAYER_ORDER[idx], PLAYER_SHORT[idx]


class ManualMoveDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk,
        *,
        default_multipv: int = 1,
    ) -> None:
        super().__init__(parent)

        self.title("Add Book Move")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result: BookMove | None = None

        self.move_var = tk.StringVar()
        self.kind_var = tk.StringVar(value="cp")
        self.score_var = tk.StringVar(value="0.00")
        self.depth_var = tk.StringVar(value="0")
        self.seldepth_var = tk.StringVar(value="0")
        self.multipv_var = tk.StringVar(
            value=str(max(1, int(default_multipv)))
        )

        body = ttk.Frame(self, padding=12)
        body.pack(fill="both", expand=True)

        ttk.Label(
            body,
            text=(
                "Add a move to the currently displayed book position.\n"
                "Use the same coordinate/UCI move format as your engine."
            ),
            justify="left",
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="w",
            pady=(0, 10),
        )

        ttk.Label(body, text="Move:").grid(
            row=1,
            column=0,
            sticky="e",
            padx=(0, 8),
            pady=3,
        )

        self.move_entry = ttk.Entry(
            body,
            textvariable=self.move_var,
            width=24,
        )
        self.move_entry.grid(
            row=1,
            column=1,
            sticky="ew",
            pady=3,
        )

        ttk.Label(body, text="Score type:").grid(
            row=2,
            column=0,
            sticky="e",
            padx=(0, 8),
            pady=3,
        )

        kind = ttk.Combobox(
            body,
            textvariable=self.kind_var,
            values=("cp", "mate"),
            state="readonly",
            width=10,
        )
        kind.grid(
            row=2,
            column=1,
            sticky="w",
            pady=3,
        )

        ttk.Label(body, text="Score:").grid(
            row=3,
            column=0,
            sticky="e",
            padx=(0, 8),
            pady=3,
        )

        ttk.Entry(
            body,
            textvariable=self.score_var,
            width=14,
        ).grid(
            row=3,
            column=1,
            sticky="w",
            pady=3,
        )

        ttk.Label(
            body,
            text="For CP, enter pawns such as +0.35 or -1.20. For mate, enter 3 or -4.",
            wraplength=360,
            justify="left",
        ).grid(
            row=4,
            column=1,
            sticky="w",
            pady=(0, 6),
        )

        ttk.Label(body, text="Depth:").grid(
            row=5,
            column=0,
            sticky="e",
            padx=(0, 8),
            pady=3,
        )

        ttk.Entry(
            body,
            textvariable=self.depth_var,
            width=14,
        ).grid(
            row=5,
            column=1,
            sticky="w",
            pady=3,
        )

        ttk.Label(body, text="SelDepth:").grid(
            row=6,
            column=0,
            sticky="e",
            padx=(0, 8),
            pady=3,
        )

        ttk.Entry(
            body,
            textvariable=self.seldepth_var,
            width=14,
        ).grid(
            row=6,
            column=1,
            sticky="w",
            pady=3,
        )

        ttk.Label(body, text="MultiPV:").grid(
            row=7,
            column=0,
            sticky="e",
            padx=(0, 8),
            pady=3,
        )

        ttk.Entry(
            body,
            textvariable=self.multipv_var,
            width=14,
        ).grid(
            row=7,
            column=1,
            sticky="w",
            pady=3,
        )

        buttons = ttk.Frame(body)
        buttons.grid(
            row=8,
            column=0,
            columnspan=2,
            sticky="e",
            pady=(12, 0),
        )

        ttk.Button(
            buttons,
            text="Cancel",
            command=self.destroy,
        ).pack(side="right")

        ttk.Button(
            buttons,
            text="Add Move",
            command=self._submit,
        ).pack(
            side="right",
            padx=(0, 6),
        )

        body.columnconfigure(1, weight=1)

        self.bind("<Return>", lambda _e: self._submit())
        self.bind("<Escape>", lambda _e: self.destroy())

        self.protocol(
            "WM_DELETE_WINDOW",
            self.destroy,
        )

        self.update_idletasks()

        x = (
            parent.winfo_rootx()
            + max(
                0,
                (parent.winfo_width() - self.winfo_width()) // 2,
            )
        )

        y = (
            parent.winfo_rooty()
            + max(
                0,
                (parent.winfo_height() - self.winfo_height()) // 2,
            )
        )

        self.geometry(f"+{x}+{y}")
        self.move_entry.focus_set()

    def _submit(self) -> None:
        move = self.move_var.get().strip()

        if not move:
            messagebox.showwarning(
                "Missing move",
                "Enter a move to add.",
                parent=self,
            )
            return

        if any(ch.isspace() for ch in move):
            messagebox.showwarning(
                "Invalid move",
                "A book move cannot contain spaces.",
                parent=self,
            )
            return

        try:
            move.encode("ascii")
        except UnicodeEncodeError:
            messagebox.showwarning(
                "Invalid move",
                "The stored move must contain ASCII characters only.",
                parent=self,
            )
            return

        kind = self.kind_var.get().strip().lower()

        if kind not in ("cp", "mate"):
            messagebox.showwarning(
                "Invalid score type",
                "Score type must be cp or mate.",
                parent=self,
            )
            return

        try:
            if kind == "cp":
                # The UI accepts pawns while the book stores integer centipawns.
                score = round(
                    float(self.score_var.get().strip())
                    * 100
                )
            else:
                score = int(
                    self.score_var.get().strip()
                )

            depth = int(
                self.depth_var.get().strip()
                or "0"
            )

            seldepth = int(
                self.seldepth_var.get().strip()
                or "0"
            )

            multipv = int(
                self.multipv_var.get().strip()
                or "1"
            )

        except ValueError:
            messagebox.showwarning(
                "Invalid values",
                "Score, depth, seldepth, and MultiPV must be valid numbers.",
                parent=self,
            )
            return

        if depth < 0 or seldepth < 0:
            messagebox.showwarning(
                "Invalid depth",
                "Depth and SelDepth cannot be negative.",
                parent=self,
            )
            return

        if multipv < 1:
            messagebox.showwarning(
                "Invalid MultiPV",
                "MultiPV must be at least 1.",
                parent=self,
            )
            return

        self.result = BookMove(
            move=move,
            score_kind=kind,
            score=score,
            depth=depth,
            seldepth=seldepth,
            multipv=multipv,
        )

        self.destroy()


def _parse_uci_info_payload(
    info_line: str,
    *,
    explicit_move: str | None = None,
    invert_score: bool = False,
) -> BookMove:
    tokens = info_line.strip().split()

    if not tokens or tokens[0] != "info":
        raise ValueError(
            "UCI payload must start with 'info'."
        )

    def int_after(
        name: str,
        default: int = 0,
    ) -> int:
        try:
            i = tokens.index(name)
            return int(tokens[i + 1])
        except (ValueError, IndexError):
            return default

    try:
        score_i = tokens.index("score")
        score_kind = tokens[score_i + 1].lower()
        score = int(tokens[score_i + 2])
    except (ValueError, IndexError) as exc:
        raise ValueError(
            "Missing a valid 'score cp N' or 'score mate N' field."
        ) from exc

    if score_kind not in ("cp", "mate"):
        raise ValueError(
            f"Unsupported score type: {score_kind!r}"
        )

    if explicit_move is None:
        try:
            pv_i = tokens.index("pv")
            move = tokens[pv_i + 1]
        except (ValueError, IndexError) as exc:
            raise ValueError(
                "Missing the first PV move."
            ) from exc
    else:
        move = explicit_move.strip()

        if not move:
            raise ValueError(
                "Missing the book move before '{'."
            )

        if any(ch.isspace() for ch in move):
            raise ValueError(
                "The explicit book move cannot contain spaces."
            )

    try:
        move.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError(
            "The book move must contain ASCII characters only."
        ) from exc

    if invert_score:
        # Brace syntax means the analysis was run AFTER the book move.
        #
        # In 4PC teams, every ply changes to the opposing team:
        #   Red -> Blue -> Yellow -> Green -> Red
        #
        # So a side-to-move score from the resulting position must be
        # negated to store the move from the team that just played it.
        score = -score

    return BookMove(
        move=move,
        score_kind=score_kind,
        score=score,
        depth=max(
            0,
            int_after("depth", 0),
        ),
        seldepth=max(
            0,
            int_after("seldepth", 0),
        ),
        multipv=max(
            1,
            int_after("multipv", 1),
        ),
    )


def parse_uci_info_line(
    line: str,
) -> BookMove:
    """
    Supported formats:

    1. Analysis from the CURRENT/PARENT position:

       info depth 26 ... score cp 20 ... pv h2h3 ...

       -> move h2h3, score +0.20

    2. Analysis performed AFTER the move was played:

       h2h3 {info depth 26 ... score cp 20 ... pv a10c9 ...}

       -> move h2h3, score -0.20

    The brace form automatically negates CP and mate scores because the engine
    is now evaluating for the opposing side-to-move team.
    """
    stripped = line.strip()

    if not stripped:
        raise ValueError(
            "The line is empty."
        )

    if stripped.startswith("info "):
        return _parse_uci_info_payload(
            stripped,
            explicit_move=None,
            invert_score=False,
        )

    # Explicit post-move format:
    #   h2h3 {info depth ...}
    #
    # Be intentionally strict so malformed lines don't silently write the
    # wrong move/evaluation into the opening book.
    match = re.fullmatch(
        r"\s*(\S+)\s*\{\s*(info\b.*)\s*\}\s*",
        stripped,
    )

    if not match:
        raise ValueError(
            "Use either 'info ... pv MOVE ...' or "
            "'MOVE {info ...}' for post-move analysis."
        )

    explicit_move = match.group(1)
    info_payload = match.group(2)

    return _parse_uci_info_payload(
        info_payload,
        explicit_move=explicit_move,
        invert_score=True,
    )


def rerank_book_moves(
    moves: list[BookMove],
) -> list[BookMove]:
    ordered = sorted(
        moves,
        key=lambda move: (
            move.rated_key(),
            move.depth,
            move.seldepth,
            move.move,
        ),
        reverse=True,
    )

    return [
        BookMove(
            move=move.move,
            score_kind=move.score_kind,
            score=move.score,
            depth=move.depth,
            seldepth=move.seldepth,
            multipv=index,
        )
        for index, move in enumerate(
            ordered,
            start=1,
        )
    ]


class UCIInfoPasteDialog(tk.Toplevel):
    def __init__(
        self,
        parent: tk.Tk,
    ) -> None:
        super().__init__(parent)

        self.title("Paste UCI Info")
        self.geometry("760x390")
        self.minsize(620, 300)
        self.transient(parent)
        self.grab_set()

        self.result: list[BookMove] | None = None

        outer = ttk.Frame(
            self,
            padding=12,
        )
        outer.pack(
            fill="both",
            expand=True,
        )

        ttk.Label(
            outer,
            text=(
                "Paste one or more analyses. Use a normal 'info ... pv MOVE' "
                "line when the search was run before the move, or use "
                "'MOVE {info ...}' when the search was run after that move. "
                "Post-move scores are automatically flipped to the mover's "
                "team perspective. All book moves are then re-ranked best to worst."
            ),
            wraplength=710,
            justify="left",
        ).pack(
            fill="x",
            anchor="w",
        )

        self.text = tk.Text(
            outer,
            height=12,
            wrap="none",
            undo=True,
        )
        self.text.pack(
            fill="both",
            expand=True,
            pady=(10, 0),
        )

        xscroll = ttk.Scrollbar(
            outer,
            orient="horizontal",
            command=self.text.xview,
        )
        xscroll.pack(fill="x")
        self.text.configure(
            xscrollcommand=xscroll.set
        )

        ttk.Label(
            outer,
            text=(
                "Examples:  info ... score cp 20 ... pv h2h3 ...    |    "
                "h2h3 {info ... score cp 20 ... pv a10c9 ...}"
            ),
        ).pack(
            fill="x",
            pady=(8, 0),
        )

        buttons = ttk.Frame(outer)
        buttons.pack(
            fill="x",
            pady=(10, 0),
        )

        ttk.Button(
            buttons,
            text="Paste Clipboard",
            command=self._paste_clipboard,
        ).pack(side="left")

        ttk.Button(
            buttons,
            text="Cancel",
            command=self.destroy,
        ).pack(side="right")

        ttk.Button(
            buttons,
            text="Import",
            command=self._submit,
        ).pack(
            side="right",
            padx=(0, 6),
        )

        self.bind(
            "<Escape>",
            lambda _e: self.destroy(),
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.destroy,
        )

        try:
            clip = parent.clipboard_get()
            if (
                isinstance(clip, str)
                and "info " in clip
            ):
                self.text.insert(
                    "1.0",
                    clip.strip(),
                )
        except tk.TclError:
            pass

        self.text.focus_set()

    def _paste_clipboard(self) -> None:
        try:
            clip = self.clipboard_get()
        except tk.TclError:
            messagebox.showwarning(
                "Clipboard",
                "The clipboard does not contain text.",
                parent=self,
            )
            return

        self.text.delete(
            "1.0",
            "end",
        )
        self.text.insert(
            "1.0",
            clip,
        )

    def _submit(self) -> None:
        lines = [
            line.strip()
            for line in self.text.get(
                "1.0",
                "end",
            ).splitlines()
            if line.strip()
        ]

        if not lines:
            messagebox.showwarning(
                "No UCI info",
                "Paste at least one UCI info line.",
                parent=self,
            )
            return

        parsed: list[BookMove] = []
        errors: list[str] = []

        for number, line in enumerate(
            lines,
            start=1,
        ):
            try:
                parsed.append(
                    parse_uci_info_line(line)
                )
            except ValueError as exc:
                errors.append(
                    f"Line {number}: {exc}"
                )

        if errors:
            messagebox.showerror(
                "Could not parse UCI info",
                "\n".join(errors[:12]),
                parent=self,
            )
            return

        self.result = parsed
        self.destroy()


class OpeningExplorer:
    def __init__(self, root: tk.Tk, initial_book: str | None = None) -> None:
        self.root = root
        self.root.title("BookForge 4PC Opening Explorer")
        self.root.geometry("1120x720")
        self.root.minsize(900, 580)

        self.db: BookDB | None = None
        self.book_path: Path | None = None
        self.root_spec = "startpos"
        self.history: list[str] = []
        self.current_moves: list[BookMove] = []
        self.row_moves: dict[str, BookMove] = {}
        self.rng = random.Random()

        self._build_menu()
        self._build_ui()
        self._bind_keys()

        if initial_book:
            self.open_book(initial_book)

        self._show_window()

    def _show_window(self) -> None:
        """Center the explorer and make sure Windows actually shows it."""
        self.root.update_idletasks()

        width = max(self.root.winfo_width(), 1120)
        height = max(self.root.winfo_height(), 720)

        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        x = max(0, (screen_w - width) // 2)
        y = max(0, (screen_h - height) // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")
        self.root.deiconify()
        self.root.lift()

        # Briefly force top-most so Windows Terminal cannot hide it on startup.
        try:
            self.root.attributes("-topmost", True)
            self.root.after(
                750,
                lambda: self.root.attributes("-topmost", False),
            )
        except tk.TclError:
            pass

        try:
            self.root.focus_force()
        except tk.TclError:
            pass

    # ---------- UI construction ----------

    def _build_menu(self) -> None:
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=False)
        file_menu.add_command(
            label="New Blank Book...",
            command=self.create_blank_book,
            accelerator="Ctrl+N",
        )
        file_menu.add_command(
            label="Open Book...",
            command=self.choose_book,
            accelerator="Ctrl+O",
        )
        file_menu.add_command(
            label="Refresh",
            command=self.refresh,
            accelerator="F5",
        )
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="File", menu=file_menu)

        nav_menu = tk.Menu(menubar, tearoff=False)
        nav_menu.add_command(
            label="Play Selected",
            command=self.play_selected,
            accelerator="Enter",
        )
        nav_menu.add_command(
            label="Back",
            command=self.go_back,
            accelerator="Backspace",
        )
        nav_menu.add_command(
            label="Reset to Root",
            command=self.reset_line,
            accelerator="Home",
        )
        nav_menu.add_separator()
        nav_menu.add_command(
            label="Play Rated Move",
            command=self.play_rated,
            accelerator="B",
        )
        nav_menu.add_command(
            label="Play Random Move",
            command=self.play_random,
            accelerator="R",
        )
        menubar.add_cascade(label="Navigate", menu=nav_menu)

        tools_menu = tk.Menu(menubar, tearoff=False)
        tools_menu.add_command(
            label="Add Book Move...",
            command=self.add_manual_move,
            accelerator="Ctrl+M",
        )
        tools_menu.add_command(
            label="Paste UCI Info...",
            command=self.import_uci_info,
            accelerator="Ctrl+I",
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Delete Selected Line...",
            command=self.delete_selected_line,
            accelerator="Delete",
        )
        tools_menu.add_separator()
        tools_menu.add_command(
            label="Copy Move History",
            command=self.copy_history,
            accelerator="Ctrl+C",
        )
        tools_menu.add_command(
            label="Copy Best Continuation",
            command=self.copy_best_continuation,
        )
        menubar.add_cascade(label="Tools", menu=tools_menu)

        self.root.config(menu=menubar)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, padding=10)
        outer.pack(fill="both", expand=True)

        # Book header
        header = ttk.LabelFrame(outer, text="Book", padding=8)
        header.pack(fill="x")

        self.book_var = tk.StringVar(value="No book open")
        self.stats_var = tk.StringVar(value="")
        self.root_var = tk.StringVar(value="")

        ttk.Label(
            header,
            textvariable=self.book_var,
            font=("TkDefaultFont", 10, "bold"),
        ).grid(row=0, column=0, sticky="w")
        ttk.Button(header, text="New...", command=self.create_blank_book).grid(
            row=0, column=1, padx=(8, 0)
        )
        ttk.Button(header, text="Open...", command=self.choose_book).grid(
            row=0, column=2, padx=(6, 0)
        )
        ttk.Button(header, text="Refresh", command=self.refresh).grid(
            row=0, column=3, padx=(6, 0)
        )
        ttk.Label(header, textvariable=self.stats_var).grid(
            row=1, column=0, columnspan=4, sticky="w", pady=(4, 0)
        )
        ttk.Label(header, textvariable=self.root_var).grid(
            row=2, column=0, columnspan=4, sticky="w", pady=(2, 0)
        )
        header.columnconfigure(0, weight=1)

        # Navigation bar
        nav = ttk.LabelFrame(outer, text="Current line", padding=8)
        nav.pack(fill="x", pady=(10, 0))

        self.turn_var = tk.StringVar(value="To move: —")
        self.ply_var = tk.StringVar(value="Ply: 0")
        self.history_var = tk.StringVar(value="(root)")

        ttk.Button(nav, text="← Back", command=self.go_back).grid(
            row=0, column=0, padx=(0, 5)
        )
        ttk.Button(nav, text="Reset", command=self.reset_line).grid(
            row=0, column=1, padx=(0, 10)
        )
        ttk.Label(
            nav,
            textvariable=self.turn_var,
            font=("TkDefaultFont", 10, "bold"),
        ).grid(row=0, column=2, sticky="w")
        ttk.Label(nav, textvariable=self.ply_var).grid(
            row=0, column=3, padx=(12, 0), sticky="w"
        )
        ttk.Button(nav, text="Copy History", command=self.copy_history).grid(
            row=0, column=4, padx=(10, 0)
        )

        history_entry = ttk.Entry(
            nav,
            textvariable=self.history_var,
            state="readonly",
        )
        history_entry.grid(
            row=1, column=0, columnspan=5, sticky="ew", pady=(7, 0)
        )

        # Jump-to-line control
        ttk.Label(nav, text="Jump to moves:").grid(
            row=2, column=0, sticky="w", pady=(8, 0)
        )
        self.jump_var = tk.StringVar()
        jump = ttk.Entry(nav, textvariable=self.jump_var)
        jump.grid(
            row=2, column=1, columnspan=3, sticky="ew", pady=(8, 0), padx=(5, 5)
        )
        jump.bind("<Return>", lambda _e: self.jump_to_line())
        ttk.Button(nav, text="Go", command=self.jump_to_line).grid(
            row=2, column=4, sticky="e", pady=(8, 0)
        )
        nav.columnconfigure(1, weight=1)
        nav.columnconfigure(2, weight=1)
        nav.columnconfigure(3, weight=1)

        # Main split
        paned = ttk.Panedwindow(outer, orient=tk.HORIZONTAL)
        paned.pack(fill="both", expand=True, pady=(10, 0))

        left = ttk.Frame(paned)
        right = ttk.Frame(paned, width=340)
        paned.add(left, weight=3)
        paned.add(right, weight=1)

        # Move list
        move_box = ttk.LabelFrame(left, text="Book moves", padding=6)
        move_box.pack(fill="both", expand=True)

        columns = (
            "rank",
            "move",
            "eval",
            "depth",
            "seldepth",
            "multipv",
            "children",
        )
        self.tree = ttk.Treeview(
            move_box,
            columns=columns,
            show="headings",
            selectmode="browse",
        )

        headings = {
            "rank": "#",
            "move": "Move",
            "eval": "Eval",
            "depth": "Depth",
            "seldepth": "SelDepth",
            "multipv": "MultiPV",
            "children": "Replies",
        }
        widths = {
            "rank": 45,
            "move": 115,
            "eval": 90,
            "depth": 70,
            "seldepth": 80,
            "multipv": 75,
            "children": 75,
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            anchor = "w" if col == "move" else "center"
            self.tree.column(
                col,
                width=widths[col],
                minwidth=45,
                anchor=anchor,
                stretch=(col == "move"),
            )

        yscroll = ttk.Scrollbar(
            move_box, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=yscroll.set)
        self.tree.pack(side="left", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")

        self.tree.bind("<Double-1>", lambda _e: self.play_selected())
        self.tree.bind("<Return>", lambda _e: self.play_selected())

        # Tags use native theme where possible; foreground-only highlighting
        # keeps the UI readable across Windows light/dark themes.
        self.tree.tag_configure("best", font=("TkDefaultFont", 9, "bold"))
        self.tree.tag_configure("mate", font=("TkDefaultFont", 9, "bold"))

        action_bar = ttk.Frame(left)
        action_bar.pack(fill="x", pady=(7, 0))
        ttk.Button(
            action_bar,
            text="Play Selected",
            command=self.play_selected,
        ).pack(side="left")
        ttk.Button(
            action_bar,
            text="Play Rated/Best",
            command=self.play_rated,
        ).pack(side="left", padx=(6, 0))
        ttk.Button(
            action_bar,
            text="Play Random",
            command=self.play_random,
        ).pack(side="left", padx=(6, 0))

        ttk.Separator(
            action_bar,
            orient="vertical",
        ).pack(
            side="left",
            fill="y",
            padx=8,
        )

        ttk.Button(
            action_bar,
            text="Add Move...",
            command=self.add_manual_move,
        ).pack(side="left")

        ttk.Button(
            action_bar,
            text="Paste UCI Info...",
            command=self.import_uci_info,
        ).pack(
            side="left",
            padx=(6, 0),
        )

        ttk.Button(
            action_bar,
            text="Delete Line...",
            command=self.delete_selected_line,
        ).pack(
            side="left",
            padx=(6, 0),
        )

        self.status_var = tk.StringVar(value="Open a .nbook file to begin.")
        ttk.Label(
            left,
            textvariable=self.status_var,
            anchor="w",
        ).pack(fill="x", pady=(7, 0))

        # Right-side details
        meta_box = ttk.LabelFrame(right, text="Position", padding=8)
        meta_box.pack(fill="x")

        self.position_key_var = tk.StringVar(value="Key: —")
        self.candidate_var = tk.StringVar(value="Candidates: —")
        self.best_var = tk.StringVar(value="Rated move: —")

        ttk.Label(meta_box, textvariable=self.position_key_var).pack(
            anchor="w"
        )
        ttk.Label(meta_box, textvariable=self.candidate_var).pack(
            anchor="w", pady=(3, 0)
        )
        ttk.Label(
            meta_box,
            textvariable=self.best_var,
            font=("TkDefaultFont", 10, "bold"),
        ).pack(anchor="w", pady=(3, 0))

        preview_box = ttk.LabelFrame(
            right,
            text="Best book continuation",
            padding=8,
        )
        preview_box.pack(fill="both", expand=True, pady=(10, 0))

        ttk.Label(
            preview_box,
            text=(
                "Follows the highest-rated stored move at each book node "
                "from the current position."
            ),
            wraplength=300,
            justify="left",
        ).pack(anchor="w")

        self.preview = tk.Text(
            preview_box,
            height=18,
            wrap="word",
            state="disabled",
            borderwidth=0,
        )
        self.preview.pack(fill="both", expand=True, pady=(8, 0))

        preview_actions = ttk.Frame(preview_box)
        preview_actions.pack(fill="x", pady=(6, 0))
        ttk.Button(
            preview_actions,
            text="Copy Continuation",
            command=self.copy_best_continuation,
        ).pack(side="left")

    def _bind_keys(self) -> None:
        self.root.bind_all("<Control-n>", lambda _e: self.create_blank_book())
        self.root.bind_all("<Control-o>", lambda _e: self.choose_book())
        self.root.bind_all("<F5>", lambda _e: self.refresh())
        self.root.bind_all("<BackSpace>", lambda _e: self.go_back())
        self.root.bind_all("<Home>", lambda _e: self.reset_line())
        self.root.bind_all("<Key-b>", lambda _e: self.play_rated())
        self.root.bind_all("<Key-r>", lambda _e: self.play_random())
        self.root.bind_all("<Control-m>", lambda _e: self.add_manual_move())
        self.root.bind_all("<Control-i>", lambda _e: self.import_uci_info())
        self.root.bind_all("<Delete>", lambda _e: self.delete_selected_line())

    # ---------- book operations ----------

    def create_blank_book(self) -> None:
        """
        Create a new empty .nbook rooted at the standard 4PC start position.

        The file contains schema + metadata only. No position row is created
        until the user manually adds the first move.
        """
        path_text = filedialog.asksaveasfilename(
            title="Create Blank BookForge Opening Book",
            defaultextension=".nbook",
            filetypes=[
                ("BookForge opening books", "*.nbook"),
                ("SQLite files", "*.sqlite *.db"),
                ("All files", "*.*"),
            ],
            initialfile="new_book.nbook",
        )

        if not path_text:
            return

        path = Path(path_text)

        if path.exists():
            replace = messagebox.askyesno(
                "Replace existing book?",
                (
                    f"{path.name} already exists.\n\n"
                    "Replace it with a completely blank opening book? "
                    "This permanently deletes the existing book contents."
                ),
            )

            if not replace:
                return

        same_as_open = False

        if self.book_path is not None:
            try:
                same_as_open = (
                    self.book_path.resolve()
                    == path.resolve()
                )
            except OSError:
                same_as_open = (
                    str(self.book_path)
                    == str(path)
                )

        if same_as_open and self.db is not None:
            try:
                self.db.close()
            finally:
                self.db = None

        try:
            # Remove the main DB and stale WAL sidecars so replacing a book
            # really produces a blank SQLite file.
            for candidate in (
                path,
                Path(str(path) + "-wal"),
                Path(str(path) + "-shm"),
            ):
                if candidate.exists():
                    candidate.unlink()

            path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            with BookDB(
                path,
                readonly=False,
            ) as writer:
                writer.create_schema()
                writer.set_meta(
                    "root_spec",
                    "startpos",
                )
                writer.set_meta(
                    "score_perspective",
                    "side_to_move_team",
                )
                writer.set_meta(
                    "engine_name",
                    "Manual book",
                )
                writer.set_meta(
                    "engine_author",
                    "",
                )
                writer.set_meta(
                    "book_origin",
                    "opening_explorer_manual",
                )
                writer.commit()

        except (OSError, sqlite3.Error, RuntimeError) as exc:
            messagebox.showerror(
                "Could not create book",
                f"Could not create:\n{path}\n\n{exc}",
            )
            return

        self.open_book(path)

        if self.db is not None:
            self.status_var.set(
                "Created blank book. Use Add Move... to add the first root move."
            )

    def choose_book(self) -> None:
            path = filedialog.askopenfilename(
                title="Open BookForge Opening Book",
                filetypes=[
                    ("BookForge opening books", "*.nbook"),
                    ("SQLite files", "*.sqlite *.db"),
                    ("All files", "*.*"),
                ],
            )
            if path:
                self.open_book(path)

    def open_book(self, path: str | Path) -> None:
        path = Path(path)

        try:
            new_db = BookDB(path, readonly=True)
            root_spec = new_db.get_meta("root_spec")
            if not root_spec:
                new_db.close()
                raise ValueError("The selected database is missing book metadata.")
            # Force a schema/read check before replacing the old book.
            new_db.count_positions()
        except (OSError, sqlite3.Error, ValueError) as exc:
            messagebox.showerror(
                "Unable to open book",
                f"Could not open:\n{path}\n\n{exc}",
            )
            return

        if self.db:
            self.db.close()

        self.db = new_db
        self.book_path = path
        self.root_spec = root_spec
        self.history.clear()
        self.jump_var.set("")
        self.book_var.set(path.name)
        self._update_book_header()
        self.refresh_position()
        self.root.title(f"BookForge 4PC Opening Explorer — {path.name}")

    def _update_book_header(self) -> None:
        if not self.db or not self.book_path:
            return

        try:
            count = self.db.count_positions()
        except sqlite3.Error:
            count = 0

        engine = self.db.get_meta("engine_name", "Unknown engine") or "Unknown engine"
        author = self.db.get_meta("engine_author", "") or ""
        engine_text = f"{engine} ({author})" if author else engine

        try:
            size = self.book_path.stat().st_size
            if size >= 1024 * 1024:
                size_text = f"{size / (1024 * 1024):.2f} MiB"
            else:
                size_text = f"{size / 1024:.1f} KiB"
        except OSError:
            size_text = "size unavailable"

        self.stats_var.set(
            f"{count:,} stored positions  •  {size_text}  •  {engine_text}"
        )
        self.root_var.set(f"Root: {self.root_spec}")

    def refresh(self) -> None:
        if not self.db:
            return
        self._update_book_header()
        self.refresh_position()
        self.status_var.set("Book refreshed.")

    def _moves_for(self, history: list[str] | tuple[str, ...]) -> list[BookMove]:
        if not self.db:
            return []
        key = position_key(self.root_spec, history)
        return self.db.get_moves(key) or []

    @staticmethod
    def _sorted_moves(moves: list[BookMove]) -> list[BookMove]:
        return sorted(moves, key=lambda m: m.rated_key(), reverse=True)

    def refresh_position(self) -> None:
        self.tree.delete(*self.tree.get_children())
        self.row_moves.clear()

        if not self.db:
            self.current_moves = []
            return

        self.current_moves = self._sorted_moves(self._moves_for(self.history))
        player, short = turn_from_root(self.root_spec, len(self.history))

        self.turn_var.set(f"To move: {player} ({short})")
        self.ply_var.set(f"Ply: {len(self.history)}")
        self.history_var.set(" ".join(self.history) if self.history else "(root)")

        key = position_key(self.root_spec, self.history)
        self.position_key_var.set(f"Key: {key.hex()}")
        self.candidate_var.set(f"Candidates: {len(self.current_moves)}")

        rated = self.current_moves[0] if self.current_moves else None
        if rated:
            self.best_var.set(
                f"Rated move: {rated.move}  [{rated.display_score()}]"
            )
        else:
            self.best_var.set("Rated move: —")

        for rank, move in enumerate(self.current_moves, start=1):
            child_history = self.history + [move.move]
            replies = len(self._moves_for(child_history))

            tags: list[str] = []
            if rank == 1:
                tags.append("best")
            if move.score_kind == "mate":
                tags.append("mate")

            iid = self.tree.insert(
                "",
                "end",
                values=(
                    rank,
                    move.move,
                    move.display_score(),
                    move.depth,
                    move.seldepth,
                    move.multipv,
                    replies,
                ),
                tags=tuple(tags),
            )
            self.row_moves[iid] = move

        children = self.tree.get_children()
        if children:
            self.tree.selection_set(children[0])
            self.tree.focus(children[0])
            self.status_var.set(
                f"{len(children)} book move(s) available. "
                "Double-click a move to follow it."
            )
        else:
            self.status_var.set(
                "No stored continuation from this position (end of book line)."
            )

        self._update_preview()


    # ---------- manual editing ----------

    def _reopen_readonly_book(self) -> None:
        if not self.book_path:
            self.db = None
            return

        self.db = BookDB(
            self.book_path,
            readonly=True,
        )

        root_spec = self.db.get_meta(
            "root_spec"
        )

        if root_spec:
            self.root_spec = root_spec

    def import_uci_info(self) -> None:
        if not self.db or not self.book_path:
            messagebox.showinfo(
                "No book open",
                "Open or create a .nbook file first.",
            )
            return

        dialog = UCIInfoPasteDialog(
            self.root,
        )

        self.root.wait_window(
            dialog
        )

        imported = dialog.result

        if not imported:
            return

        imported_by_move: dict[str, BookMove] = {}

        for move in imported:
            previous = imported_by_move.get(
                move.move
            )

            if (
                previous is None
                or move.depth > previous.depth
                or (
                    move.depth == previous.depth
                    and move.seldepth >= previous.seldepth
                )
            ):
                imported_by_move[
                    move.move
                ] = move

        key = position_key(
            self.root_spec,
            self.history,
        )

        try:
            self.db.close()
        except Exception:
            pass

        self.db = None

        try:
            with BookDB(
                self.book_path,
                readonly=False,
            ) as writer:
                stored = (
                    writer.get_moves(key)
                    or []
                )

                merged_by_move = {
                    move.move: move
                    for move in stored
                }

                merged_by_move.update(
                    imported_by_move
                )

                ranked = rerank_book_moves(
                    list(
                        merged_by_move.values()
                    )
                )

                writer.put_moves(
                    key,
                    len(self.history),
                    ranked,
                )

                writer.commit()

        except Exception as exc:
            try:
                self._reopen_readonly_book()
            except Exception:
                self.db = None

            messagebox.showerror(
                "Could not import UCI info",
                (
                    "The UCI result could not be written to the book.\n\n"
                    f"{exc}\n\n"
                    "If the generator is actively writing this same .nbook, "
                    "stop it before manually editing the book."
                ),
            )

            self.refresh_position()
            return

        try:
            self._reopen_readonly_book()
        except Exception as exc:
            messagebox.showerror(
                "Imported, but refresh failed",
                (
                    "The UCI result was saved, but the explorer could not "
                    f"reopen the book:\n\n{exc}"
                ),
            )
            return

        self._update_book_header()
        self.refresh_position()

        imported_count = len(
            imported_by_move
        )

        self.status_var.set(
            f"Imported {imported_count} UCI move"
            f"{'s' if imported_count != 1 else ''}; "
            f"re-ranked {len(self.current_moves)} book move"
            f"{'s' if len(self.current_moves) != 1 else ''} "
            "best to worst."
        )

    def add_manual_move(self) -> None:
        if not self.db or not self.book_path:
            messagebox.showinfo(
                "No book open",
                "Open a .nbook file first.",
            )
            return

        next_multipv = 1

        if self.current_moves:
            next_multipv = (
                max(
                    move.multipv
                    for move in self.current_moves
                )
                + 1
            )

        dialog = ManualMoveDialog(
            self.root,
            default_multipv=next_multipv,
        )

        self.root.wait_window(dialog)

        new_move = dialog.result

        if new_move is None:
            return

        current_by_move = {
            move.move: move
            for move in self.current_moves
        }

        existing = current_by_move.get(
            new_move.move
        )

        if existing is not None:
            replace = messagebox.askyesno(
                "Move already exists",
                (
                    f"{new_move.move} is already stored at this position.\n\n"
                    f"Current: {existing.display_score()}, "
                    f"depth {existing.depth}, "
                    f"seldepth {existing.seldepth}, "
                    f"MultiPV {existing.multipv}\n\n"
                    "Replace it with the values you entered?"
                ),
            )

            if not replace:
                return

        key = position_key(
            self.root_spec,
            self.history,
        )

        # Close the explorer's read-only connection before opening the
        # temporary writer. This avoids the explorer itself contributing a
        # read lock while the row is updated.
        try:
            self.db.close()
        except Exception:
            pass

        self.db = None

        try:
            with BookDB(
                self.book_path,
                readonly=False,
            ) as writer:
                stored = (
                    writer.get_moves(key)
                    or []
                )

                replaced = False
                updated: list[BookMove] = []

                for move in stored:
                    if move.move == new_move.move:
                        updated.append(
                            new_move
                        )
                        replaced = True
                    else:
                        updated.append(
                            move
                        )

                if not replaced:
                    updated.append(
                        new_move
                    )

                writer.put_moves(
                    key,
                    len(self.history),
                    updated,
                )

                writer.commit()

        except Exception as exc:
            try:
                self._reopen_readonly_book()
            except Exception:
                self.db = None

            messagebox.showerror(
                "Could not save move",
                (
                    "The move could not be written to the book.\n\n"
                    f"{exc}\n\n"
                    "If the generator is currently writing this same .nbook, "
                    "stop it before manually editing the book."
                ),
            )

            self.refresh_position()
            return

        try:
            self._reopen_readonly_book()

        except Exception as exc:
            messagebox.showerror(
                "Move saved, but refresh failed",
                (
                    "The move was written successfully, but the explorer "
                    f"could not reopen the book:\n\n{exc}"
                ),
            )
            return

        self._update_book_header()
        self.refresh_position()

        action = (
            "Updated"
            if existing is not None
            else "Added"
        )

        self.status_var.set(
            f"{action} manual book move "
            f"{new_move.move} "
            f"[{new_move.display_score()}] "
            f"at ply {len(self.history)}."
        )

    def _collect_line_position_keys(
        self,
        start_history: list[str] | tuple[str, ...],
    ) -> list[bytes]:
        if not self.db:
            return []

        stack: list[tuple[str, ...]] = [
            tuple(start_history)
        ]

        seen: set[bytes] = set()
        stored_keys: list[bytes] = []

        while stack:
            history = stack.pop()

            key = position_key(
                self.root_spec,
                history,
            )

            if key in seen:
                continue

            seen.add(key)

            moves = self.db.get_moves(key)

            if moves is None:
                continue

            stored_keys.append(key)

            for move in moves:
                stack.append(
                    history + (move.move,)
                )

        return stored_keys

    def delete_selected_line(self) -> None:
        if not self.db or not self.book_path:
            messagebox.showinfo(
                "No book open",
                "Open or create a .nbook file first.",
            )
            return

        move = self._selected_move()

        if move is None:
            messagebox.showinfo(
                "No move selected",
                "Select a book move to delete.",
            )
            return

        parent_history = tuple(
            self.history
        )

        child_history = (
            parent_history
            + (move.move,)
        )

        descendant_keys = (
            self._collect_line_position_keys(
                child_history
            )
        )

        descendant_count = len(
            descendant_keys
        )

        if descendant_count:
            continuation_text = (
                f"This will also delete {descendant_count:,} stored "
                f"continuation position"
                f"{'s' if descendant_count != 1 else ''} below it."
            )
        else:
            continuation_text = (
                "There are no stored continuation positions below it."
            )

        confirmed = messagebox.askyesno(
            "Delete book line?",
            (
                f"Delete {move.move} "
                f"[{move.display_score()}] from this position?\n\n"
                f"{continuation_text}\n\n"
                "This cannot be undone."
            ),
        )

        if not confirmed:
            return

        parent_key = position_key(
            self.root_spec,
            parent_history,
        )

        try:
            self.db.close()
        except Exception:
            pass

        self.db = None

        try:
            with BookDB(
                self.book_path,
                readonly=False,
            ) as writer:
                parent_moves = (
                    writer.get_moves(
                        parent_key
                    )
                    or []
                )

                remaining = [
                    entry
                    for entry in parent_moves
                    if entry.move != move.move
                ]

                remaining = rerank_book_moves(
                    remaining
                )

                writer.delete_positions(
                    descendant_keys
                )

                if remaining:
                    writer.put_moves(
                        parent_key,
                        len(parent_history),
                        remaining,
                    )
                else:
                    writer.delete_position(
                        parent_key
                    )

                writer.commit()

        except Exception as exc:
            try:
                self._reopen_readonly_book()
            except Exception:
                self.db = None

            messagebox.showerror(
                "Could not delete line",
                (
                    "The selected line could not be deleted.\n\n"
                    f"{exc}\n\n"
                    "If the generator is currently writing this same .nbook, "
                    "stop it before manually editing the book."
                ),
            )

            if self.db is not None:
                self.refresh_position()

            return

        try:
            self._reopen_readonly_book()
        except Exception as exc:
            messagebox.showerror(
                "Line deleted, but refresh failed",
                (
                    "The line was deleted successfully, but the explorer "
                    f"could not reopen the book:\n\n{exc}"
                ),
            )
            return

        self._update_book_header()
        self.refresh_position()

        self.status_var.set(
            f"Deleted book line {move.move}. "
            f"Removed {descendant_count:,} continuation position"
            f"{'s' if descendant_count != 1 else ''}."
        )

    # ---------- navigation ----------

    def _selected_move(self) -> BookMove | None:
        selected = self.tree.selection()
        if not selected:
            return None
        return self.row_moves.get(selected[0])

    def play_selected(self) -> None:
        move = self._selected_move()
        if move:
            self.play_move(move)

    def play_move(self, move: BookMove) -> None:
        self.history.append(move.move)
        self.refresh_position()

    def play_rated(self) -> None:
        if self.current_moves:
            self.play_move(self.current_moves[0])

    def play_random(self) -> None:
        if self.current_moves:
            self.play_move(self.rng.choice(self.current_moves))

    def go_back(self) -> None:
        if self.history:
            self.history.pop()
            self.refresh_position()

    def reset_line(self) -> None:
        if self.history:
            self.history.clear()
            self.refresh_position()

    def jump_to_line(self) -> None:
        if not self.db:
            return

        text = self.jump_var.get().strip()
        requested = text.split() if text else []

        cursor: list[str] = []
        for index, move_text in enumerate(requested, start=1):
            available = {m.move for m in self._moves_for(cursor)}
            if move_text not in available:
                messagebox.showwarning(
                    "Line not in book",
                    f"Move {index} ({move_text}) is not a stored book move "
                    f"after:\n{' '.join(cursor) if cursor else '(root)'}",
                )
                return
            cursor.append(move_text)

        self.history = cursor
        self.refresh_position()

    # ---------- preview / clipboard ----------

    def best_continuation(self, max_plies: int = 24) -> list[BookMove]:
        if not self.db:
            return []

        cursor = list(self.history)
        result: list[BookMove] = []

        for _ in range(max_plies):
            moves = self._sorted_moves(self._moves_for(cursor))
            if not moves:
                break
            best = moves[0]
            result.append(best)
            cursor.append(best.move)

        return result

    def _update_preview(self) -> None:
        line = self.best_continuation()
        start_ply = len(self.history)

        rows: list[str] = []
        for offset, move in enumerate(line):
            ply = start_ply + offset
            player, short = turn_from_root(self.root_spec, ply)
            rows.append(
                f"{ply + 1:>2}. {short}  {move.move:<9} "
                f"{move.display_score():>9}"
            )

        if not rows:
            body = "No further rated continuation is stored."
        else:
            body = "\n".join(rows)

        self.preview.configure(state="normal")
        self.preview.delete("1.0", "end")
        self.preview.insert("1.0", body)
        self.preview.configure(state="disabled")

    def copy_history(self) -> None:
        text = " ".join(self.history)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Move history copied to clipboard.")

    def copy_best_continuation(self) -> None:
        moves = [m.move for m in self.best_continuation()]
        text = " ".join(moves)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_var.set("Best book continuation copied to clipboard.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="GUI explorer for BookForge 4PC .nbook opening books."
    )
    parser.add_argument(
        "book",
        nargs="?",
        help="Optional .nbook file to open on startup.",
    )
    args = parser.parse_args()

    print("Launching BookForge 4PC Opening Explorer...")
    root = tk.Tk()
    app = OpeningExplorer(root, args.book)

    # If no book was supplied on the command line, immediately ask for one.
    if not args.book:
        root.after(400, app.choose_book)

    root.mainloop()


if __name__ == "__main__":
    main()
