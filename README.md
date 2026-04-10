# I Ching Hexagram Generator

An interactive I Ching hexagram generator built with pygame. Users enter a question, then reveal a randomly generated hexagram one line at a time with coin flip animations.

## Features

- **Landing page** - Enter your question before consulting the I Ching
- **Interactive hexagram** - Click circles to reveal lines with coin flip animations
- **Solid and broken lines** - Randomly generated Yang (solid) and Yin (broken) lines
- **Beautiful UI** - Clean, aesthetic interface with smooth animations

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
