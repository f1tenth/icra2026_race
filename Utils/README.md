# Roboracer Event Management Utilities

This folder contains utilities for managing the Roboracer race event website.

## Event Manager GUI

The **Event Manager** is a GUI-based tool that allows organizers to easily configure and update the race website for new events.

### Running the Event Manager

```bash
# From the project root directory
uv run python Utils/event_manager.py
```

### Features

1. **Event Details Tab** - Configure:
   - Conference acronym (e.g., "ICRA") - year is added automatically
   - Full conference name (without year, e.g., "IEEE Conference on Robotics and Automation")
   - Race number (e.g., "25TH")
   - Year - combined with conference name automatically
   - Venue name and location
   - Conference URL and logo
   - Conference dates (without year, e.g., "May 19th - 23rd")
   - Contact email
   - CNAME (domain)

2. **Dates & Timeline Tab** - Automatically calculate event dates:
   - Set the Race Day (before-last day of conference)
   - All other dates are calculated using configurable offsets
   - Preview calculated dates before applying

3. **Orientations Tab** - Configure orientation meeting links:
   - Zoom meeting links
   - Slides links (Google Presentations)
   - Video recording links (Google Drive)

4. **Registration Tab** - Manage registration status:
   - Toggle registration open/closed
   - Set registration form link
   - Configure Sim Racing League settings

5. **Results & Stream Tab** - Configure results and streaming:
   - Time trial sheet link
   - Head-to-head bracket link
   - YouTube/Twitch streaming settings

6. **Registrants Tab** - Import participants:
   - Import from Video Demo Checklist Excel file
   - Generate HTML table for the website
   - Preview before applying

### Configuration File

All settings are stored in `Utils/event_config.json`. This file can be:
- Edited manually if needed
- Backed up for different events
- Version controlled

### Applying Changes

Click **"Apply to Repository"** to update all HTML and Markdown files with the new configuration. The tool will:
- Update page titles
- Update conference names and dates
- Update venue information
- Update registration status and links
- Update orientation links
- Update result/stream links
- Update CNAME file

### Date Calculation

The date calculator replaces the old Excel-based AutoDateCalculator. It uses these default offsets from race day:

| Event | Offset (days) |
|-------|---------------|
| Qualification | -1 |
| Team Training | -2 |
| Track Setup | -3 |
| Orientation 2 | -38 |
| Registration Closes | -40 |
| Orientation 1 | -66 |
| Registration Opens | -113 |

Adjust these offsets in the Dates & Timeline tab as needed.

## Files

- `event_config.json` - Current event configuration (JSON)
- `event_manager.py` - Main GUI application
- `RegisteredList.xlsx` - Output from extract_final_registrants.py
- `Video Demo Checklist.xlsx` - Input file for registrant processing

