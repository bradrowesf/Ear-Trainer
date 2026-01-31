# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A Python CLI ear training application for guitar players. It plays MIDI notes/intervals via the `scamp` library and scores the user's response time to develop interval recognition skills.

## Commands

**Run the application:**
```bash
python main.py
```

**Run all tests:**
```bash
python -m unittest discover tests/
```

**Run a single test file:**
```bash
python -m unittest tests/test_midiutilities.py
```

**Build executable (PyInstaller):**
```bash
pyinstaller main.spec
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

## Architecture

### Core Flow

`main.py` wires everything together: loads a `Config`, creates an `Application`, `Player`, and `Scoreboard`, registers all 14 exercises, then runs the menu loop. Scores are saved to `scores.json` on exit.

### Key Classes

- **`Config`** (`src/config.py`) — Loads an optional `config.json` file for per-exercise and application setting overrides. Validates `key_centers` and `intervalics` values against `MidiUtil` at load time. See [Configuration](#configuration) below.

- **`Application`** (`src/application.py`) — Menu system that registers exercises and provides run modes: single exercise, random, mixer (timed mixed session), or run-all. Accepts a `Config` instance and applies it to exercises during registration.

- **`Exercise`** (`src/exercise.py`) — Abstract base class using the Template Method pattern. Each subclass configures its own trial generation parameters (key centers, intervalics, trial counts, note ranges). There are 14 concrete exercise types spanning one-string, one-octave, one-position, chord tone, audiation, interval singing, and pure interval exercises at varying difficulty levels.

- **`Player`** (`src/player.py`) — Manages a `scamp.Session` for MIDI playback. Executes trials dispatched by exercise type (`INTERVAL`, `SERIES`, `SERIES_HOLD_ON_ONE`). Handles timing measurement for scoring.

- **`ExercisePackage`** (`src/exercisepackage.py`) — Immutable configuration container passed to `Player` for each exercise. Contains exercise type (`ExerciseType` enum), pause durations (`PauseDuration` enum), repeat settings, and scoring flags.

- **`Scoreboard`** (`src/scoreboard.py`) / **`ScoreHistory`** (`src/scorehistory.py`) — Time-based scoring. Keeps the last 30 scores per element. Averages below 3.5s promote; above 7.5s demote. Active scores persist in `scores.json`; all scores append to `scorehistory.csv`.

- **`MidiUtil`** (`src/midiutilities.py`) — MIDI note array (index = MIDI value, value = note name like "C#4"), interval patterns for scales/modes/chords, and note-to-index lookups.

- **`GuitarUtil`** (`src/guitarutilities.py`) — Maps MIDI notes to guitar strings and frets (6-string standard tuning, configurable to 20, 22, or 24 frets). Lookup tables always extend to fret 24 internally; `max_frets` acts as a logical cap.

### Exercise Type Enum

Defined in `ExercisePackage`, controls how `Player` executes a trial:
- `INTERVAL` — Two notes played with timing-based scoring measured between them.
- `SERIES` — Sequence of notes with optional repeat.
- `SERIES_HOLD_ON_ONE` — Sequence emphasizing the first note (held 4x longer).

### Configuration

An optional `config.json` file in the project root allows overriding per-exercise settings and the mixer duration. If the file is missing, all exercises use their hardcoded defaults.

```json
{
    "guitar_type": "Guitar22",
    "mixer_duration": 1200,
    "exercises": {
        "OneOctaveEasy": {
            "exercise_duration": 300,
            "key_centers": ["C", "G", "F"],
            "intervalics": ["Major", "Minor", "Ionian"]
        }
    }
}
```

- **`guitar_type`** — Guitar fret count: `"Guitar20"`, `"Guitar22"`, or `"Guitar24"` (default: `"Guitar22"`). Controls the fret range used by exercises for note generation and string/fret lookups.
- **`mixer_duration`** — Duration in seconds for the mixer session (default: 1200).
- **`exercise_duration`** — Duration in seconds for the exercise.
- **`key_centers`** — List of note names (e.g., `"C"`, `"F#"`). Replaces the exercise's default key centers entirely.
- **`intervalics`** — List of scale/chord names (e.g., `"Ionian"`, `"Major Seventh"`, `"ii7"`). Replaces the exercise's default intervalics entirely.

Exercises are keyed by class name: `OneString`, `OneOctaveEasy`, `OneOctaveMedium`, `OneOctaveHard`, `OnePositionEasy`, `OnePositionMedium`, `OnePositionHard`, `ChordTones`, `AudiationEasy`, `AudiationHard`, `JustTheIntervals`, `SingTheIntervalsEasy`, `SingTheIntervalsMedium`, `SingTheIntervalsHard`.

All settings are optional. Invalid `key_centers` or `intervalics` values are logged as warnings and filtered out; if no valid values remain, the hardcoded defaults are preserved. Valid values are derived from `MidiUtil.note_names` and `MidiUtil.interval_pattern` at load time.

### Data Files

- `config.json` — Optional user configuration for exercise overrides (not checked into the repo).
- `scores.json` — Active score dictionary, loaded on startup, saved on exit.
- `scorehistory.csv` — Append-only log with timestamps for long-term tracking.
- `eartrainer.log` — Debug log, overwritten each run.

## Dependencies

- `scamp` — MIDI session and playback (uses a bundled Merlin.sf2 soundfont in the PyInstaller build).
- `keyboard` — Low-level keyboard input for real-time key press detection.
- `pandas` — Score history CSV handling.
