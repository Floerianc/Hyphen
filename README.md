# LED Panel – Hyphen

A modular RGB LED panel application built for Raspberry Pi.  
Displays weather, public transport (HVV), pollen levels, Untis data, and more.

---

# Project Status

## Core Architecture ✅
- Clean project structure
- Refactored `Hyphen` into:
  - App logic
  - Canvas framework
- Fixed typing errors
- Improved documentation
- Clean error handling with proper logging levels
- Clean exit with CTRL-C + traceback support

---

# UI Redesign (In Progress)

## Completed Pages
- Weather page
- Bus line page
- Pollen page

## In Progress
- News page
- Untis integration (API clarification pending)

---

# Weather Page

## Features
- Current time & temperature
- Weather icon
- Rain icon
- Rain bar
- Rain forecast
- Temperature graph
- Precipitation graph
- Reusable `MatrixGraph` class

## Current Issue
- Weather data does not update correctly after 12am  
  - Hour index resets to 0
  - New data is fetched but indexing logic wraps incorrectly
  - Needs timestamp-based matching instead of raw index usage

---

# HVV (Public Transport)

## Migration
- Replaced Selenium with GeoFox API
- Created dataclasses:
  - `GeoFoxResponse`
  - `Departure`
  - `DepartureLine`
  - `DepartureStation`
  - `DepartureLineType`
- Implemented JSON → dataclass converter
- Added delay support
- Added fallback and visual error indicator

---

# Image System

- Replaced large pixel matrices with PNG converter
- Created `Image` dataclass
- Created `Color` dataclass
- Fixed path handling

---

# Raspberry Pi 3 Deployment

## Major Fixes
- NumPy/Pandas compilation issues
- `rgbmatrix.core` missing
- Permission issues (`.cache`)
- Font asset resolution
- Sudo / venv inconsistencies
- `idna.uts46data` error
- `pygame.rect` missing
- `numpy.full` missing
- Selenium driver problems
- urllib3 HTTP issues

## Stability Improvements
- Deployment test suite:
  - Permission checks
  - Installed packages
  - Weather cache test
  - Import test
  - rgbmatrix test
  - HVV API response test
  - Font test

---

# Performance & Stability

- Fixed heavy flickering
- Reworked Canvas rendering
- Optimized drawing logic
- Improved logging system
- Automatic log cleanup (24h + restart)
- Introduced `StopableThread`

---

# Remaining TODOs

## High Priority
- Fix weather hour index rollover (12am issue)
- Complete Untis integration
- Finish News page
- Improve real-time weather accuracy

## Medium Priority
- Add uptime monitor
- Improve UI consistency
- Refactor graph scaling logic
- Add symmetric scaling option for charts

## Optional Improvements
- Add baseline markers to graphs
- Improve animation transitions between pages
- Add system diagnostics page
- Add WiFi signal strength display
- Add CPU/RAM usage monitor
- Add configuration page

---

# Future Ideas

- Modular widget system (re-evaluate previous cancellation)
- Plugin support

---

# Versioning

Current version: `3.6.0`  
Next milestone: Stable `4.0.0` with:
- Fully stable weather system
- Completed Untis integration
- Finalized UI redesign

---

# Author

GitHub: https://github.com/Floerianc

---
