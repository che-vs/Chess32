# Chess32

A beginner-friendly chess platform built for A-Level Computer Science NEA. Chess32 provides a clean, distraction-free environment for learning and playing chess, featuring 8 progressive AI difficulty levels and 8 structured lessons.

[Python](3.8+)
[Pygame](2.0+)
[License](Educational)

---

## Overview

Chess32 was designed to solve a real problem: existing chess platforms overwhelm beginners with cluttered interfaces, aggressive monetisation, and advanced features. This project delivers a minimalistic, ad-free platform focused entirely on helping new players learn chess at their own pace.

### Key Features

- **Clean 800×800 Interface** — Consistent layout across all screens with no distractions
- **8 AI Difficulty Levels** — From random moves (Level 1) to iterative deepening with quiescence search (Level 8)
- **8 Structured Lessons** — Step-by-step tutorials covering rules, tactics, and strategy
- **Visual Feedback System** — Green highlights for legal moves, red for check, gold for last move
- **Keyboard Navigation** — Full keyboard shortcuts (ESC, B, R, U, Arrow keys)
- **Two-Player Mode** — Local multiplayer with full chess rule enforcement
- **No Ads, No Paywalls, No Accounts** — Completely free and private

---

## Screenshots

| Main Menu | Bot Selection | Game Board |
|-----------|---------------|------------|
| *(Blurred chessboard background with logo and 4 buttons)* | *(8 bot portraits in 2×4 grid)* | *(Chess board with green legal move highlights)* |

---

## Installation

### Prerequisites

- **Python 3.8+**
- **Windows** (primary target OS)
- **4GB RAM** minimum

### Dependencies

```bash
pip install pygame python-chess pillow numpy
```

Or install from `requirements.txt`:
```bash
pip install -r requirements.txt
```

### Running the Game

```bash
python Chess32.py
```

### Building Executable (Optional)

```bash
python setup.py build
```

---

## Project Structure

```
Chess32/
├── Chess32.py              # State manager — central controller
├── menu.py                 # Main menu (State 1)
├── twoplayer.py            # Two-player game (State 2)
├── lessonmenu.py           # Lesson selection menu (State 3)
├── botmenu.py              # Bot difficulty menu (State 4)
├── baseplate.py            # Bot game engine (State 5)
├── credit.py               # Credits page (State 6)
├── baseplate2.py           # Lesson launcher (State 7)
├── setup.py                # cx_Freeze build configuration
│
├── bots/                   # AI engine package
│   ├── bot1.py             # Level 1: Random moves
│   ├── bot2.py             # Level 2: Minimax (depth 3)
│   ├── bot3.py             # Level 3: Alpha-beta pruning
│   ├── bot4.py             # Level 4: Piece-square tables
│   ├── bot5.py             # Level 5: MVVLVA move ordering
│   ├── bot6.py             # Level 6: King safety + development
│   ├── bot7.py             # Level 7: Opening book (polyglot)
│   └── bot8.py             # Level 8: Iterative deepening + quiescence
│
├── lessons/                # Educational content
│   ├── lesson1.py          # Introduction & disclaimer
│   ├── lesson2.py          # Piece movement basics
│   ├── lesson3.py          # Capturing & special moves
│   ├── lesson4.py          # Check, checkmate & stalemate
│   ├── lesson5.py          # Opening principles
│   ├── lesson6.py          # Tactics introduction
│   ├── lesson7.py          # Endgame fundamentals
│   └── lesson8.py          # Improvement strategies
│
├── images/                 # Game assets
│   ├── board.png           # Chess board background
│   ├── logo.png            # Application icon
│   ├── white/              # White piece sprites (P, R, N, B, Q, K)
│   ├── black/              # Black piece sprites (p, r, n, b, q, k)
│   ├── botpfp/             # Bot avatars (1.png – 8.png)
│   ├── menuassets/         # Menu buttons
│   ├── gameover/           # End-game screens
│   └── lessons/images/     # Tutorial illustrations
│
└── codekiddy.bin           # Polyglot opening book database
```

---

## AI Difficulty Levels

| Level | Algorithm | Description | Avg. Response |
|-------|-----------|-------------|---------------|
| **1** | Random | Chooses any legal move | <5ms |
| **2** | Minimax | Game tree search, material-only eval | ~2s |
| **3** | Alpha-Beta | Pruned minimax (depth 3) | ~2s |
| **4** | PST | Adds piece-square tables for positional play | ~2s |
| **5** | MVVLVA | Capture-prioritised move ordering | ~2s |
| **6** | Development | King safety + piece development bonuses | ~2s |
| **7** | Opening Book | Polyglot book + fallback to Level 6 | ~2s |
| **8** | Full Engine | Iterative deepening, aspiration windows, quiescence search, transposition tables | 0–15s |

---

## Controls

| Key | Action | Context |
|-----|--------|---------|
| `ESC` | Quit application | Global |
| `B` | Back to menu | Global |
| `R` | Reset game | Game screens |
| `U` | Undo move(s) | Game screens |
| `← →` | Page navigation | Lessons, Credits |
| **Mouse** | Select & move pieces | Game screens |

---

## Technical Highlights

### Algorithms Implemented
- **Minimax** with depth-limited search
- **Alpha-Beta Pruning** for performance optimisation
- **Piece-Square Tables** for positional evaluation
- **MVVLVA** (Most Valuable Victim, Least Valuable Aggressor) move ordering
- **Iterative Deepening** with time management
- **Aspiration Windows** for search efficiency
- **Quiescence Search** to mitigate horizon effect
- **Transposition Tables** (FEN-based caching, 10,000 entry limit)
- **Polyglot Opening Book** integration

### Architecture
- **State Manager Pattern** — `Chess32.py` dispatches between 7 independent modules
- **Threading** — AI calculations run on separate threads to maintain UI responsiveness
- **Config Dictionary** — Clean parameter passing between states (replaced file-based config)
- **python-chess Library** — Robust move validation and game state management

---

## Research & Methodology

This project was grounded in primary research (125 survey respondents) and secondary research (Reddit discussions, platform reviews). Key findings:

- **60%** of beginners found existing platforms difficult to understand
- **35%** felt overwhelmed by information density
- **73%** preferred a simpler, beginner-friendly platform
- **68%** reported ads/paywalls negatively affected learning

These insights directly shaped Chess32's design philosophy: minimalism, gradual progression, and zero barriers to entry.

---

## Testing

| Category | Tests | Passed | Failed |
|----------|-------|--------|--------|
| Core Game Mechanics | 5 | 5 | 0 |
| Special Moves | 6 | 6 | 0 |
| Draw Conditions | 5 | 5 | 0 |
| Navigation & Controls | 6 | 6 | 0 |
| AI Performance | 24 | 23 | 1 |

Full testing documentation covers functional testing, usability testing with stakeholders, AI benchmarking (including a game vs. Chess.com's Magnus Carlsen bot), and boundary/edge-case testing.

---

## Future Improvements

- **GPU Acceleration** — Parallelise position evaluation for deeper search
- **Zobrist Hashing** — Replace FEN-based transposition tables for memory efficiency
- **Endgame Tablebases** — Perfect play in simplified positions
- **Interactive Lessons** — Replace static text with playable puzzles
- **Move Hints / AI Coach** — Suggest improvements after each game
- **Cross-Platform Support** — macOS, Linux, and WebAssembly builds

---

## Acknowledgements

- **Chess Programming Wiki** — Algorithm references and pseudocode
- **SimplyInDev (YouTube)** — Chess engine architecture tutorials
- **python-chess** — Move validation and board state management
- **Pygame** — Rendering and event handling framework

---

## License

This project was created for educational purposes as part of A-Level Computer Science coursework. Assets sourced from Chess.com, Lichess.org, and other credited sources are used under their respective licenses for educational use.

---

*Built with ❤️ for beginners who just want to play chess.*
