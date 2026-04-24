# I Ching Hexagram Generator

An interactive I Ching hexagram generator built with pygame. Users enter a question, then reveal a randomly generated hexagram one line at a time with coin flip animations.

The original `pygame` prototype is preserved as-is, and the website now uses a root `index.html` entry point with supporting assets in `website/`.

## Features

- **Landing page** - Enter your question before consulting the I Ching
- **Interactive hexagram** - Click circles to reveal lines with coin flip animations
- **Solid and broken lines** - Randomly generated Yang (solid) and Yin (broken) lines
- **Beautiful UI** - Clean, aesthetic interface with smooth animations
- **Organized readings** - Hexagram text files live under `readings/`

## Requirements

- Python 3.8+
- pygame 2.6+

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   # or
   .venv\Scripts\activate  # On Windows
   ```
3. Install dependencies:
   ```bash
   pip install pygame
   ```

## Running the Application

```bash
python test.py
```

## Project Structure

- `test.py` - Main pygame prototype
- `fetch_hexagrams.py` - Script to build the combined reading export
- `readings/` - Individual hexagram readings plus `iching_hexagrams_texts.txt`
- `index.html` - Main website entry point
- `website/` - Website assets, scripts, styles, and bundled reading data

## Website Version

The web port is intentionally separate from the Python prototype so the current desktop version remains untouched.

### Files

- `index.html` - Web page structure for the landing screen and casting screen
- `website/style.css` - Visual system, animated background, responsive layout, and coin/line styling
- `website/app.js` - Browser state management, random hexagram generation, and three-coin casting animation logic
- `website/readings-data.js` - Bundled hexagram readings for standalone browser loading

### What Changed In The Website

- Copied the current two-page flow into a browser-based version instead of replacing `test.py`
- Recreated the atmospheric scene with a gradient sky, moon glow, stars, drifting orbs, mountain layers, and mist
- Added a dedicated landing page with the same question-first interaction as the Python app
- Ported the six-line reveal flow so each line is cast one at a time
- Rebuilt the three-coin toss animation in HTML/CSS/JavaScript for each line reveal
- Preserved the yin/yang rule from the prototype: two or three heads become a solid yang line
- Added browser buttons for `Generate New Hexagram` and `Ask Another Question`
- Preserved the `R` keyboard shortcut behavior to return to the landing page
- Added responsive styling so the website works on desktop and mobile widths
- Added a reduced-motion fallback for people who prefer less animation

### Running The Website

Open `index.html` in a browser for a quick local preview.

For the most reliable local setup, serve the project root and open the site in a browser:

```bash
python -m http.server
```

Then visit:

```text
http://localhost:8000/
```

## Usage

1. **Landing Page**: Type your question about life, decisions, or situations
2. **Submit**: Click "Submit" or press Enter to proceed
3. **Reveal Hexagram**: Click each circle (6 total) to reveal the lines
4. **Coin Flip Animation**: Watch as each coin flips to determine if it's a solid or broken line
5. **New Question**: Press 'R' to return to the landing page and ask another question

## Controls

- **Click circles** - Reveal hexagram lines
- **Enter** - Submit question on landing page
- **R** - Return to landing page to ask a new question
- **Generate New Hexagram** - Generate a new random hexagram

## Technical Details

- Built with pygame for graphics and event handling
- Uses frame-based animation for smooth coin flip effects
- Two-page interface with state management (landing page and hexagram page)
- Browser port uses plain HTML, CSS, and JavaScript with no framework dependency
