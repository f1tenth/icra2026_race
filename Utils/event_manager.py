#!/usr/bin/env python3
"""
Roboracer Event Manager - GUI tool for managing race event configurations.

This tool allows organizers to:
- Configure event details (conference name, venue, dates, etc.)
- Automatically calculate timeline dates from the race day
- Update all HTML/MD files with new event information
- Import registrants from Excel files
- Generate registrant HTML tables

Run with: uv run python Utils/event_manager.py
"""

import io
import json
import os
import re
import tkinter as tk
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any

import cairosvg
import pandas as pd
from PIL import Image
from tkcalendar import Calendar
from ttkthemes import ThemedTk

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
CONFIG_FILE = SCRIPT_DIR / "event_config.json"


def load_config() -> dict:
    """Load event configuration from JSON file."""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return get_default_config()


def save_config(config: dict) -> None:
    """Save event configuration to JSON file."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=4)


def get_default_config() -> dict:
    """Return default configuration template."""
    return {
        "event": {
            "conference_name": "ICRA",
            "conference_full_name": "IEEE Conference on Robotics and Automation",
            "race_number": "25TH",
            "year": "2026",
            "venue_name": "Venue Name",
            "location": "City, State, Country",
            "venue_url": "https://venue-website.com",
            "conference_url": "https://conference-website.com",
            "conference_logo": "images/ICRA2026.png",
            "contact_email": "roboracer@email.com",
            "cname": "icra2026-race.roboracer.ai",
            "conference_dates_display": "Month Day - Day",
        },
        "dates": {
            "race_day": datetime.now().strftime("%Y-%m-%d"),
            "offsets": {
                "qualification": -1,
                "team_training": -2,
                "track_setup": -3,
                "orientation_2": -38,
                "registration_closes": -40,
                "orientation_1": -66,
                "registration_open": -113,
            },
        },
        "orientation_1": {
            "time_display": "11:00AM - 12:00PM ET",
            "zoom_link": "",
            "slides_link": "",
            "video_link": "",
        },
        "orientation_2": {
            "time_display": "11:00AM - 12:00PM ET",
            "zoom_link": "",
            "slides_link": "",
            "video_link": "",
        },
        "registration": {
            "status": "closed",
            "form_link": "",
            "hide_participants": False,
        },
        "results": {
            "time_trial_sheet_link": "",
            "bracket_link": "",
            "twitch_parent_domains": ["localhost"],
            "youtube_stream_id": "",
            "show_stream_placeholder": True,
            "stream_placeholder_text": "Live stream will appear here during the event.",
            "show_results_placeholder": True,
            "results_placeholder_text": "Results will be posted after the competition.",
        },
        "sim_racing": {
            "enabled": True,
            "edition": "3rd",
            "website_url": "",
            "registration_url": "",
            "timeline_url": "",
        },
    }


def calculate_dates(race_day: str, offsets: dict) -> dict:
    """Calculate all event dates based on race day and offsets."""
    race_date = datetime.strptime(race_day, "%Y-%m-%d")
    dates = {"race": race_date}

    for event_name, offset in offsets.items():
        dates[event_name] = race_date + timedelta(days=offset)

    return dates


def format_date_display(date: datetime, include_ordinal: bool = True) -> str:
    """Format date for display (e.g., 'May 22nd')."""
    day = date.day
    if include_ordinal:
        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        return f"{date.strftime('%B')} {day}{suffix}"
    return f"{date.strftime('%B')} {day}"


class ScaleDialog:
    """Dialog to get a scale factor from the user."""

    def __init__(self, parent, title: str, message: str, default_value: float = 1.0):
        self.result = None

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Dark theme styling
        self.dialog.configure(bg="#1e1e2e")

        # Center the dialog
        self.dialog.geometry("400x200")
        self.dialog.resizable(False, False)

        # Message label
        msg_label = tk.Label(
            self.dialog,
            text=message,
            bg="#1e1e2e",
            fg="#cdd6f4",
            font=("Ubuntu", 10),
            justify="left"
        )
        msg_label.pack(padx=20, pady=(20, 10))

        # Scale entry
        entry_frame = tk.Frame(self.dialog, bg="#1e1e2e")
        entry_frame.pack(pady=10)

        tk.Label(
            entry_frame,
            text="Scale factor:",
            bg="#1e1e2e",
            fg="#cdd6f4",
            font=("Ubuntu", 10)
        ).pack(side="left", padx=(0, 10))

        self.scale_entry = tk.Entry(
            entry_frame,
            width=10,
            bg="#3c3c3c",
            fg="white",
            insertbackground="white",
            font=("Ubuntu", 10)
        )
        self.scale_entry.pack(side="left")
        self.scale_entry.insert(0, str(default_value))
        self.scale_entry.select_range(0, tk.END)
        self.scale_entry.focus_set()

        # Buttons
        btn_frame = tk.Frame(self.dialog, bg="#1e1e2e")
        btn_frame.pack(pady=20)

        ok_btn = tk.Button(
            btn_frame,
            text="OK",
            command=self.on_ok,
            bg="#45475a",
            fg="#cdd6f4",
            font=("Ubuntu", 10),
            width=10
        )
        ok_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.on_cancel,
            bg="#45475a",
            fg="#cdd6f4",
            font=("Ubuntu", 10),
            width=10
        )
        cancel_btn.pack(side="left", padx=5)

        # Bind Enter key
        self.scale_entry.bind("<Return>", lambda e: self.on_ok())
        self.dialog.bind("<Escape>", lambda e: self.on_cancel())

        # Wait for dialog to close
        parent.wait_window(self.dialog)

    def on_ok(self):
        try:
            self.result = float(self.scale_entry.get())
            if self.result <= 0:
                raise ValueError("Scale must be positive")
            self.dialog.destroy()
        except ValueError:
            tk.messagebox.showerror(
                "Invalid Input",
                "Please enter a valid positive number."
            )

    def on_cancel(self):
        self.result = None
        self.dialog.destroy()


class EventManagerApp:
    """Main application class for the Event Manager GUI."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Roboracer Event Manager")
        self.root.geometry("1000x850")
        self.root.minsize(900, 750)

        # Configure custom styles
        self.setup_styles()

        # Load configuration
        self.config = load_config()

        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create tabs
        self.create_event_tab()
        self.create_dates_tab()
        self.create_orientations_tab()
        self.create_registration_tab()
        self.create_results_tab()
        self.create_registrants_tab()

        # Create bottom button frame
        self.create_button_frame()

        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_styles(self) -> None:
        """Configure custom styles for the application."""
        style = ttk.Style()

        # Use 'clam' as base theme - it's the most customizable
        style.theme_use("clam")

        # Dark theme colors
        bg_dark = "#1e1e2e"  # Dark background
        bg_surface = "#2a2a3c"  # Surface/card background
        bg_hover = "#3a3a4c"  # Hover state
        text_primary = "#cdd6f4"  # Primary text
        text_secondary = "#a6adc8"  # Secondary text
        accent = "#89b4fa"  # Blue accent
        accent_hover = "#b4befe"  # Lighter blue
        success = "#a6e3a1"  # Green
        border = "#45475a"  # Border color

        # Font - using commonly available fonts on Linux
        main_font = ("Ubuntu", 10)
        main_font_bold = ("Ubuntu", 10, "bold")
        header_font = ("Ubuntu", 12, "bold")
        mono_font = ("Ubuntu Mono", 10)

        # Configure notebook tab styling
        style.configure(
            "TNotebook",
            background=bg_dark,
            borderwidth=0,
            tabmargins=[8, 8, 8, 0],
        )
        style.configure(
            "TNotebook.Tab",
            background=bg_surface,
            foreground=text_secondary,
            padding=[16, 8],
            font=main_font,
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", "#00bcd4"), ("active", bg_hover)],
            foreground=[("selected", "#1e1e2e"), ("active", text_primary)],
            padding=[("selected", [18, 12])],
            expand=[("selected", [0, 2, 0, 0])],
        )

        # Configure frame background
        style.configure("TFrame", background=bg_dark)

        # Configure labels
        style.configure(
            "TLabel",
            background=bg_dark,
            foreground=text_primary,
            font=main_font,
        )
        style.configure(
            "Header.TLabel",
            background=bg_dark,
            foreground=accent,
            font=header_font,
        )

        # Configure entry fields
        style.configure(
            "TEntry",
            fieldbackground=bg_surface,
            foreground=text_primary,
            insertcolor=text_primary,
            padding=8,
            font=main_font,
        )

        # Configure buttons
        style.configure(
            "TButton",
            background=bg_surface,
            foreground=text_primary,
            padding=[14, 8],
            font=main_font,
            borderwidth=1,
        )
        style.map(
            "TButton",
            background=[("active", bg_hover), ("pressed", accent)],
            foreground=[("pressed", bg_dark)],
        )

        style.configure(
            "Accent.TButton",
            background=accent,
            foreground=bg_dark,
            padding=[14, 8],
            font=main_font_bold,
        )
        style.map(
            "Accent.TButton",
            background=[("active", accent_hover)],
        )

        # Configure checkbuttons and radiobuttons
        style.configure(
            "TCheckbutton",
            background=bg_dark,
            foreground=text_primary,
            font=main_font,
        )
        style.configure(
            "TRadiobutton",
            background=bg_dark,
            foreground=text_primary,
            font=main_font,
        )

        # Configure separators
        style.configure("TSeparator", background=border)

        # Configure text widget colors (for preview areas)
        self.text_bg = bg_surface
        self.text_fg = text_primary

        # Set root background
        self.root.configure(bg=bg_dark)

    def create_labeled_entry(
        self, parent: tk.Widget, label: str, row: int, default: str = ""
    ) -> tk.Entry:
        """Create a labeled entry field with dark theme styling."""
        ttk.Label(parent, text=label).grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        entry = tk.Entry(
            parent,
            width=60,
            bg="#2a2a3c",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
            font=("Ubuntu", 10),
            highlightthickness=1,
            highlightcolor="#89b4fa",
            highlightbackground="#45475a",
        )
        entry.grid(row=row, column=1, sticky=tk.EW, padx=5, pady=5, ipady=5)
        entry.insert(0, default)
        return entry

    def create_event_tab(self) -> None:
        """Create the Event Details tab."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Event Details")

        # Configure grid
        frame.columnconfigure(1, weight=1)

        event = self.config.get("event", {})

        row = 0
        self.conference_name_entry = self.create_labeled_entry(
            frame, "Conference Acronym (e.g., ICRA):", row, event.get("conference_name", "")
        )
        row += 1
        self.conference_full_name_entry = self.create_labeled_entry(
            frame, "Conference Full Name (no year):", row, event.get("conference_full_name", "")
        )
        row += 1
        self.race_number_entry = self.create_labeled_entry(
            frame, "Race Number (e.g., 24TH):", row, event.get("race_number", "")
        )
        row += 1
        self.year_entry = self.create_labeled_entry(
            frame, "Year:", row, event.get("year", "")
        )
        row += 1
        self.venue_name_entry = self.create_labeled_entry(
            frame, "Venue Name:", row, event.get("venue_name", "")
        )
        row += 1
        self.location_entry = self.create_labeled_entry(
            frame, "Location:", row, event.get("location", "")
        )
        row += 1
        self.venue_url_entry = self.create_labeled_entry(
            frame, "Venue URL:", row, event.get("venue_url", "")
        )
        row += 1
        self.conference_url_entry = self.create_labeled_entry(
            frame, "Conference URL:", row, event.get("conference_url", "")
        )
        row += 1
        # Conference logo with file picker
        ttk.Label(frame, text="Conference Logo:").grid(
            row=row, column=0, sticky="w", padx=5, pady=2
        )
        logo_frame = ttk.Frame(frame)
        logo_frame.grid(row=row, column=1, sticky="ew", padx=5, pady=2)
        self.conference_logo_entry = tk.Entry(logo_frame, width=40, bg="#3c3c3c", fg="white", insertbackground="white")
        self.conference_logo_entry.pack(side="left", fill="x", expand=True)
        self.conference_logo_entry.insert(0, event.get("conference_logo", ""))
        browse_btn = ttk.Button(
            logo_frame, text="Browse...", command=self.browse_conference_logo, style="Accent.TButton"
        )
        browse_btn.pack(side="left", padx=(5, 0))
        row += 1
        self.contact_email_entry = self.create_labeled_entry(
            frame, "Contact Email:", row, event.get("contact_email", "")
        )
        row += 1
        self.cname_entry = self.create_labeled_entry(
            frame, "CNAME (domain):", row, event.get("cname", "")
        )
        row += 1
        self.conference_dates_display_entry = self.create_labeled_entry(
            frame,
            "Conference Dates (no year, e.g., May 19th - 23rd):",
            row,
            event.get("conference_dates_display", ""),
        )

    def create_dates_tab(self) -> None:
        """Create the Dates/Timeline tab."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Dates & Timeline")

        frame.columnconfigure(1, weight=1)

        dates = self.config.get("dates", {})
        offsets = dates.get("offsets", {})

        row = 0
        ttk.Label(
            frame, text="Set the Race Day and offsets to calculate all dates:"
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10)

        row += 1
        ttk.Label(frame, text="Race Day:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )

        # Date picker frame with entry and button
        date_frame = ttk.Frame(frame)
        date_frame.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        self.race_day_var = tk.StringVar(value=dates.get("race_day", ""))
        self.race_day_entry = tk.Entry(
            date_frame,
            textvariable=self.race_day_var,
            width=15,
            bg="#2a2a3c",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
            font=("Ubuntu", 10),
            highlightthickness=1,
            highlightcolor="#89b4fa",
            highlightbackground="#45475a",
        )
        self.race_day_entry.pack(side=tk.LEFT, padx=(0, 5), ipady=5)

        ttk.Button(date_frame, text="Pick Date...", command=self.open_calendar_dialog).pack(
            side=tk.LEFT
        )

        row += 1
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=tk.EW, pady=10
        )

        row += 1
        ttk.Label(frame, text="Day Offsets (relative to race day):").grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5
        )

        self.offset_entries = {}
        offset_labels = {
            "qualification": "Qualification (day before race)",
            "team_training": "Team Training",
            "track_setup": "Track Setup",
            "orientation_2": "Orientation 2",
            "registration_closes": "Registration Closes",
            "orientation_1": "Orientation 1",
            "registration_open": "Registration Opens",
        }

        for name, label in offset_labels.items():
            row += 1
            ttk.Label(frame, text=f"{label}:").grid(
                row=row, column=0, sticky=tk.W, padx=5, pady=4
            )
            entry = tk.Entry(
                frame,
                width=10,
                bg="#2a2a3c",
                fg="#cdd6f4",
                insertbackground="#cdd6f4",
                relief=tk.FLAT,
                font=("Ubuntu", 10),
                highlightthickness=1,
                highlightcolor="#89b4fa",
                highlightbackground="#45475a",
            )
            entry.grid(row=row, column=1, sticky=tk.W, padx=5, pady=4, ipady=3)
            entry.insert(0, str(offsets.get(name, 0)))
            self.offset_entries[name] = entry

        row += 1
        ttk.Button(frame, text="Calculate & Preview Dates", command=self.preview_dates).grid(
            row=row, column=0, columnspan=2, pady=20
        )

        row += 1
        self.dates_preview = tk.Text(
            frame,
            height=12,
            width=60,
            state=tk.DISABLED,
            bg="#2a2a3c",
            fg="#cdd6f4",
            font=("Ubuntu Mono", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.dates_preview.grid(
            row=row, column=0, columnspan=2, sticky=tk.EW, padx=5, pady=5
        )

    def create_orientations_tab(self) -> None:
        """Create the Orientations tab."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Orientations")

        frame.columnconfigure(1, weight=1)

        # Info label
        row = 0
        ttk.Label(
            frame,
            text="Dates are calculated from the Dates & Timeline tab. Only enter the time.",
            foreground="#a6adc8",
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        # Orientation 1
        row += 1
        ttk.Label(frame, text="Orientation 1", font=("Ubuntu", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10
        )

        o1 = self.config.get("orientation_1", {})

        row += 1
        ttk.Label(frame, text="Date (calculated):").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.o1_date_label = ttk.Label(frame, text="(click 'Calculate Dates' in Dates tab)", foreground="#00bcd4")
        self.o1_date_label.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        row += 1
        self.o1_time_entry = self.create_labeled_entry(
            frame, "Time (e.g., 11:00AM - 12:00PM ET):", row, o1.get("time_display", "")
        )
        row += 1
        self.o1_zoom_entry = self.create_labeled_entry(
            frame, "Zoom Link:", row, o1.get("zoom_link", "")
        )
        row += 1
        self.o1_slides_entry = self.create_labeled_entry(
            frame, "Slides Link:", row, o1.get("slides_link", "")
        )
        row += 1
        self.o1_video_entry = self.create_labeled_entry(
            frame, "Video Link:", row, o1.get("video_link", "")
        )

        # Orientation 2
        row += 1
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=tk.EW, pady=15
        )
        row += 1
        ttk.Label(frame, text="Orientation 2", font=("Ubuntu", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10
        )

        o2 = self.config.get("orientation_2", {})

        row += 1
        ttk.Label(frame, text="Date (calculated):").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.o2_date_label = ttk.Label(frame, text="(click 'Calculate Dates' in Dates tab)", foreground="#00bcd4")
        self.o2_date_label.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)

        row += 1
        self.o2_time_entry = self.create_labeled_entry(
            frame, "Time (e.g., 11:00AM - 12:00PM ET):", row, o2.get("time_display", "")
        )
        row += 1
        self.o2_zoom_entry = self.create_labeled_entry(
            frame, "Zoom Link:", row, o2.get("zoom_link", "")
        )
        row += 1
        self.o2_slides_entry = self.create_labeled_entry(
            frame, "Slides Link:", row, o2.get("slides_link", "")
        )
        row += 1
        self.o2_video_entry = self.create_labeled_entry(
            frame, "Video Link:", row, o2.get("video_link", "")
        )

        # Update orientation dates on load
        self.update_orientation_dates()

    def create_registration_tab(self) -> None:
        """Create the Registration tab."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Registration")

        frame.columnconfigure(1, weight=1)

        reg = self.config.get("registration", {})

        row = 0
        ttk.Label(frame, text="Registration Status:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.reg_status_var = tk.StringVar(value=reg.get("status", "closed"))
        status_frame = ttk.Frame(frame)
        status_frame.grid(row=row, column=1, sticky=tk.W, padx=5, pady=5)
        ttk.Radiobutton(
            status_frame, text="Open", variable=self.reg_status_var, value="open"
        ).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(
            status_frame, text="Closed", variable=self.reg_status_var, value="closed"
        ).pack(side=tk.LEFT, padx=5)

        row += 1
        self.reg_form_entry = self.create_labeled_entry(
            frame, "Registration Form Link:", row, reg.get("form_link", "")
        )

        # Participants section
        row += 1
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=tk.EW, pady=15
        )
        row += 1
        ttk.Label(frame, text="Participants List", font=("Ubuntu", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10
        )

        row += 1
        self.hide_participants_var = tk.BooleanVar(value=reg.get("hide_participants", False))
        ttk.Checkbutton(
            frame, text="Hide participants section on registration page", variable=self.hide_participants_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        row += 1
        participants_btn_frame = ttk.Frame(frame)
        participants_btn_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)
        ttk.Button(
            participants_btn_frame, text="Clear Participants", command=self.clear_participants
        ).pack(side=tk.LEFT, padx=5)

        # Sim Racing section
        row += 1
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=tk.EW, pady=15
        )
        row += 1
        ttk.Label(frame, text="Sim Racing League", font=("Ubuntu", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10
        )

        sim = self.config.get("sim_racing", {})
        row += 1
        self.sim_enabled_var = tk.BooleanVar(value=sim.get("enabled", True))
        ttk.Checkbutton(
            frame, text="Enable Sim Racing Section", variable=self.sim_enabled_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        row += 1
        self.sim_edition_entry = self.create_labeled_entry(
            frame, "Edition (e.g., 3rd):", row, sim.get("edition", "")
        )
        row += 1
        self.sim_website_entry = self.create_labeled_entry(
            frame, "Website URL:", row, sim.get("website_url", "")
        )
        row += 1
        self.sim_registration_entry = self.create_labeled_entry(
            frame, "Registration URL:", row, sim.get("registration_url", "")
        )
        row += 1
        self.sim_timeline_entry = self.create_labeled_entry(
            frame, "Timeline URL:", row, sim.get("timeline_url", "")
        )

    def create_results_tab(self) -> None:
        """Create the Results/Stream tab."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Results & Stream")

        frame.columnconfigure(1, weight=1)

        results = self.config.get("results", {})

        # Stream section
        row = 0
        ttk.Label(frame, text="Live Stream", font=("Ubuntu", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10
        )

        row += 1
        self.youtube_stream_entry = self.create_labeled_entry(
            frame, "YouTube Stream ID:", row, results.get("youtube_stream_id", "")
        )
        row += 1
        self.twitch_domains_entry = self.create_labeled_entry(
            frame,
            "Twitch Parent Domains (comma-separated):",
            row,
            ", ".join(results.get("twitch_parent_domains", [])),
        )

        row += 1
        self.show_stream_placeholder_var = tk.BooleanVar(value=results.get("show_stream_placeholder", True))
        ttk.Checkbutton(
            frame, text="Show placeholder text if stream not configured", variable=self.show_stream_placeholder_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        row += 1
        self.stream_placeholder_entry = self.create_labeled_entry(
            frame, "Stream Placeholder Text:", row, results.get("stream_placeholder_text", "Live stream will appear here during the event.")
        )

        # Results section
        row += 1
        ttk.Separator(frame, orient=tk.HORIZONTAL).grid(
            row=row, column=0, columnspan=2, sticky=tk.EW, pady=15
        )
        row += 1
        ttk.Label(frame, text="Results", font=("Ubuntu", 12, "bold")).grid(
            row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=10
        )

        row += 1
        self.time_trial_entry = self.create_labeled_entry(
            frame, "Time Trial Sheet Link:", row, results.get("time_trial_sheet_link", "")
        )
        row += 1
        ttk.Label(frame, text="", foreground="#a6adc8").grid(row=row, column=0, sticky=tk.W, padx=5)
        self.hide_time_trial_info = ttk.Label(frame, text="(Leave empty to hide this section)", foreground="#a6adc8")
        self.hide_time_trial_info.grid(row=row, column=1, sticky=tk.W, padx=5)

        row += 1
        self.bracket_entry = self.create_labeled_entry(
            frame, "Head-to-Head Bracket Link:", row, results.get("bracket_link", "")
        )
        row += 1
        ttk.Label(frame, text="", foreground="#a6adc8").grid(row=row, column=0, sticky=tk.W, padx=5)
        self.hide_bracket_info = ttk.Label(frame, text="(Leave empty to hide this section)", foreground="#a6adc8")
        self.hide_bracket_info.grid(row=row, column=1, sticky=tk.W, padx=5)

        row += 1
        self.show_results_placeholder_var = tk.BooleanVar(value=results.get("show_results_placeholder", True))
        ttk.Checkbutton(
            frame, text="Show placeholder text for results section", variable=self.show_results_placeholder_var
        ).grid(row=row, column=0, columnspan=2, sticky=tk.W, padx=5, pady=5)

        row += 1
        self.results_placeholder_entry = self.create_labeled_entry(
            frame, "Results Placeholder Text:", row, results.get("results_placeholder_text", "Results will be posted after the competition.")
        )

    def create_registrants_tab(self) -> None:
        """Create the Registrants tab."""
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="Registrants")

        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(3, weight=1)

        row = 0
        ttk.Label(
            frame,
            text="Import registrants from Video Demo Checklist Excel file:",
            font=("", 10),
        ).grid(row=row, column=0, sticky=tk.W, padx=5, pady=10)

        row += 1
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)

        ttk.Button(
            btn_frame, text="Select Excel File", command=self.select_registrants_file
        ).pack(side=tk.LEFT, padx=5)
        ttk.Button(
            btn_frame, text="Generate Registrants Table", command=self.generate_registrants_table
        ).pack(side=tk.LEFT, padx=5)

        row += 1
        self.registrants_file_label = ttk.Label(frame, text="No file selected")
        self.registrants_file_label.grid(row=row, column=0, sticky=tk.W, padx=5, pady=5)

        row += 1
        ttk.Label(frame, text="Preview:").grid(
            row=row, column=0, sticky=tk.W, padx=5, pady=5
        )
        row += 1
        self.registrants_preview = tk.Text(
            frame,
            height=15,
            width=80,
            bg="#2a2a3c",
            fg="#cdd6f4",
            font=("Ubuntu Mono", 10),
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.registrants_preview.grid(
            row=row, column=0, sticky=tk.NSEW, padx=5, pady=5
        )

        scrollbar = ttk.Scrollbar(frame, command=self.registrants_preview.yview)
        scrollbar.grid(row=row, column=1, sticky=tk.NS)
        self.registrants_preview.config(yscrollcommand=scrollbar.set)

        self.registrants_file_path = None

    def create_button_frame(self) -> None:
        """Create the bottom button frame."""
        frame = ttk.Frame(self.root)
        frame.pack(fill=tk.X, padx=10, pady=15)

        # Left side - main actions
        left_frame = tk.Frame(frame, bg="#1e1e2e")
        left_frame.pack(side=tk.LEFT)

        # Save Configuration - subtle teal
        tk.Button(
            left_frame,
            text="Save Configuration",
            command=self.save_config,
            bg="#2d4a4a",
            fg="#a6e3a1",
            activebackground="#3d5a5a",
            activeforeground="#a6e3a1",
            font=("Ubuntu", 10),
            relief=tk.FLAT,
            padx=16,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        # Apply to Repository - accent teal (matching selected tab)
        tk.Button(
            left_frame,
            text="Apply to Repository",
            command=self.apply_to_repo,
            bg="#00838f",
            fg="#e0f7fa",
            activebackground="#00acc1",
            activeforeground="#ffffff",
            font=("Ubuntu", 10, "bold"),
            relief=tk.FLAT,
            padx=16,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        # Reset to Defaults - muted red/rose
        tk.Button(
            left_frame,
            text="Reset to Defaults",
            command=self.reset_config,
            bg="#4a2d2d",
            fg="#f38ba8",
            activebackground="#5a3d3d",
            activeforeground="#f38ba8",
            font=("Ubuntu", 10),
            relief=tk.FLAT,
            padx=16,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.LEFT, padx=5)

        # Right side - exit (neutral)
        tk.Button(
            frame,
            text="Exit",
            command=self.on_close,
            bg="#2a2a3c",
            fg="#cdd6f4",
            activebackground="#3a3a4c",
            activeforeground="#cdd6f4",
            font=("Ubuntu", 10),
            relief=tk.FLAT,
            padx=16,
            pady=8,
            cursor="hand2",
        ).pack(side=tk.RIGHT, padx=5)

    def browse_conference_logo(self) -> None:
        """Open file picker to select conference logo image."""
        # Start in images directory
        initial_dir = PROJECT_ROOT / "images"
        if not initial_dir.exists():
            initial_dir = PROJECT_ROOT

        filepath = filedialog.askopenfilename(
            title="Select Conference Logo",
            initialdir=initial_dir,
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.webp *.gif"),
                ("PNG files", "*.png"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("WebP files", "*.webp"),
                ("All files", "*.*"),
            ],
        )

        if filepath:
            # Convert to relative path from project root
            try:
                rel_path = Path(filepath).relative_to(PROJECT_ROOT)
                self.conference_logo_entry.delete(0, tk.END)
                self.conference_logo_entry.insert(0, str(rel_path))

                # Ask if user wants to regenerate the banner
                if messagebox.askyesno(
                    "Generate Banner",
                    "Would you like to regenerate BackGroundProject.png with this logo?"
                ):
                    self.generate_banner_image(str(rel_path))
            except ValueError:
                # File is outside project root - copy it to images folder
                messagebox.showwarning(
                    "File Location",
                    "Please select an image from within the project directory, "
                    "or copy the image to the 'images' folder first."
                )

    def generate_banner_image(self, logo_path: str) -> None:
        """Generate BackGroundProject.png with roboracer icon and conference logo on base image."""
        try:
            offset = 100
            svg_scale = 8  # Scale for roboracer icon

            # Load the base background image
            base_path = PROJECT_ROOT / "images" / "Main_Image_Backup.jpg"
            if not base_path.exists():
                messagebox.showerror(
                    "Error",
                    "Main_Image_Backup.jpg not found in images folder.\n"
                    "This file is required as the base background."
                )
                return

            banner = Image.open(base_path).convert("RGBA")
            banner_width, banner_height = banner.size

            # Load and render roboracer_icon.svg
            roboracer_icon = None
            roboracer_height = 50 * svg_scale  # Default height
            svg_path = PROJECT_ROOT / "images" / "roboracer_icon.svg"
            if svg_path.exists():
                # Render SVG to PNG at a larger size for the banner
                png_data = cairosvg.svg2png(
                    url=str(svg_path),
                    output_width=81 * svg_scale,
                    output_height=50 * svg_scale
                )
                roboracer_icon = Image.open(io.BytesIO(png_data)).convert("RGBA")
                roboracer_height = roboracer_icon.height

                # Position at top-right with offset
                icon_x = banner_width - roboracer_icon.width - offset
                icon_y = offset
                banner.paste(roboracer_icon, (icon_x, icon_y), roboracer_icon)

            # Ask user for scale factor
            scale_dialog = ScaleDialog(
                self.root,
                "Logo Scale",
                f"The Roboracer icon is {roboracer_height}px tall.\n\n"
                "Enter a scale factor for the conference logo:\n"
                "• 1.0 = same height as Roboracer icon\n"
                "• 0.5 = half the height\n"
                "• 2.0 = double the height",
                default_value=1.0
            )
            if scale_dialog.result is None:
                return  # User cancelled

            logo_scale = scale_dialog.result

            # Load conference logo
            conf_logo_path = PROJECT_ROOT / logo_path
            if conf_logo_path.exists():
                conf_logo = Image.open(conf_logo_path).convert("RGBA")

                # Scale conference logo based on user input (relative to roboracer height)
                target_height = int(roboracer_height * logo_scale)
                ratio = target_height / conf_logo.height
                new_width = int(conf_logo.width * ratio)
                conf_logo = conf_logo.resize((new_width, target_height), Image.Resampling.LANCZOS)

                # Position at top-left with offset
                banner.paste(conf_logo, (offset, offset), conf_logo)

            # Save the banner as PNG
            output_path = PROJECT_ROOT / "images" / "BackGroundProject.png"
            banner.save(output_path, "PNG")

            messagebox.showinfo(
                "Success",
                f"Banner image generated successfully!\n\n"
                f"Conference logo scaled to {logo_scale}x Roboracer icon height.\n"
                f"Saved to: {output_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate banner: {e}")

    def clear_participants(self) -> None:
        """Clear the participants table in registration.html."""
        if messagebox.askyesno(
            "Confirm Clear",
            "This will remove all participants from registration.html. Continue?"
        ):
            try:
                reg_path = PROJECT_ROOT / "registration.html"
                with open(reg_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Clear the tbody content using placeholder
                content = RepositoryUpdater.replace_placeholder(content, "PARTICIPANTS_TBODY", "")

                with open(reg_path, "w", encoding="utf-8") as f:
                    f.write(content)

                messagebox.showinfo("Success", "Participants list cleared!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear participants: {e}")

    def update_orientation_dates(self) -> None:
        """Update orientation date labels based on calculated dates."""
        try:
            race_day = self.race_day_var.get().strip()
            if not race_day:
                return

            offsets = {}
            for name, entry in self.offset_entries.items():
                offsets[name] = int(entry.get().strip())

            dates = calculate_dates(race_day, offsets)

            if "orientation_1" in dates:
                self.o1_date_label.config(text=format_date_display(dates["orientation_1"]))
            if "orientation_2" in dates:
                self.o2_date_label.config(text=format_date_display(dates["orientation_2"]))
        except Exception:
            pass  # Silently ignore errors during initial load

    def open_calendar_dialog(self) -> None:
        """Open a calendar dialog to pick the race day."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Select Race Day")
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.configure(bg="#1e1e2e")

        # Parse current date or use today
        try:
            current_date = datetime.strptime(self.race_day_var.get(), "%Y-%m-%d")
        except ValueError:
            current_date = datetime.now()

        cal = Calendar(
            dialog,
            selectmode="day",
            year=current_date.year,
            month=current_date.month,
            day=current_date.day,
            date_pattern="yyyy-mm-dd",
            background="#1e1e2e",
            foreground="#cdd6f4",
            headersbackground="#2a2a3c",
            headersforeground="#89b4fa",
            selectbackground="#89b4fa",
            selectforeground="#1e1e2e",
            normalbackground="#2a2a3c",
            normalforeground="#cdd6f4",
            weekendbackground="#2a2a3c",
            weekendforeground="#f5c2e7",
            othermonthbackground="#1e1e2e",
            othermonthforeground="#45475a",
            othermonthwebackground="#1e1e2e",
            othermonthweforeground="#45475a",
            bordercolor="#45475a",
            font=("Ubuntu", 11),
        )
        cal.pack(padx=15, pady=15)

        def on_select():
            self.race_day_var.set(cal.get_date())
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg="#1e1e2e")
        btn_frame.pack(pady=15)

        select_btn = tk.Button(
            btn_frame,
            text="Select",
            command=on_select,
            bg="#89b4fa",
            fg="#1e1e2e",
            font=("Ubuntu", 10, "bold"),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
        )
        select_btn.pack(side=tk.LEFT, padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=dialog.destroy,
            bg="#2a2a3c",
            fg="#cdd6f4",
            font=("Ubuntu", 10),
            relief=tk.FLAT,
            padx=20,
            pady=8,
            cursor="hand2",
        )
        cancel_btn.pack(side=tk.LEFT, padx=5)

        # Center the dialog
        dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (dialog.winfo_height() // 2)
        dialog.geometry(f"+{x}+{y}")

        dialog.wait_window()

    def preview_dates(self) -> None:
        """Preview calculated dates."""
        try:
            race_day = self.race_day_var.get().strip()
            offsets = {}
            for name, entry in self.offset_entries.items():
                offsets[name] = int(entry.get().strip())

            dates = calculate_dates(race_day, offsets)

            preview_text = "Calculated Timeline:\n" + "=" * 40 + "\n\n"
            preview_text += f"Registration Opens: {format_date_display(dates['registration_open'])}\n"
            preview_text += f"Orientation 1: {format_date_display(dates['orientation_1'])}\n"
            preview_text += f"Registration Closes: {format_date_display(dates['registration_closes'])}\n"
            preview_text += f"Orientation 2: {format_date_display(dates['orientation_2'])}\n"
            preview_text += f"Track Setup: {format_date_display(dates['track_setup'])}\n"
            preview_text += f"Team Training: {format_date_display(dates['team_training'])}\n"
            preview_text += f"Qualification: {format_date_display(dates['qualification'])}\n"
            preview_text += f"Race Day: {format_date_display(dates['race'])}\n"

            self.dates_preview.config(state=tk.NORMAL)
            self.dates_preview.delete("1.0", tk.END)
            self.dates_preview.insert("1.0", preview_text)
            self.dates_preview.config(state=tk.DISABLED)

            # Also update orientation date labels
            self.update_orientation_dates()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to calculate dates: {e}")

    def select_registrants_file(self) -> None:
        """Open file dialog to select registrants Excel file."""
        filename = filedialog.askopenfilename(
            title="Select Video Demo Checklist Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")],
            initialdir=SCRIPT_DIR,
        )
        if filename:
            self.registrants_file_path = filename
            self.registrants_file_label.config(text=f"Selected: {Path(filename).name}")

    def generate_registrants_table(self) -> None:
        """Generate registrants HTML table from Excel file."""
        if not self.registrants_file_path:
            messagebox.showwarning("Warning", "Please select an Excel file first.")
            return

        try:
            # Read the Excel file
            df = pd.read_excel(
                self.registrants_file_path, sheet_name="Data", header=1, usecols="B:G"
            )

            # Filter rows where "Video Demo Submitted?" is True
            submitted_teams = df[df["Video Demo Submitted?"] == True]

            # Build HTML table
            html_table = """
<table>
    <thead>
        <tr>
            <th style="text-align: left">TEAM NAME</th>
            <th style="text-align: left">AFFILIATION</th>
            <th style="text-align: left">TEAM MEMBERS</th>
        </tr>
    </thead>
    <tbody>
"""
            for _, row in submitted_teams.iterrows():
                team_name = row["Team Name"]
                affiliation = row["Affiliation"]
                team_members = row["Team Names"]

                if pd.isna(team_members):
                    team_members = "N/A"

                # Clean up team members string
                match = re.search(r":\s*(.+)", str(team_members))
                if match:
                    team_members = match.group(1).strip()

                # Remove email addresses
                team_members = re.sub(r"\S+@\S+", "", str(team_members))
                team_members = re.sub(r"\([^)]*\S+@\S+[^)]*\)", "", team_members)
                team_members = re.sub(r"^\s*\d+\)\s*", "", team_members)

                # Split into individual names
                names = team_members.strip().split()
                members = [" ".join(names[i : i + 2]) for i in range(0, len(names), 2)]
                team_members_html = "<br>".join(members)

                html_table += f"""
        <tr>
            <td style="text-align: left">{team_name}</td>
            <td style="text-align: left">{affiliation}</td>
            <td style="text-align: left">{team_members_html}</td>
        </tr>
"""

            html_table += """
    </tbody>
</table>
"""

            # Show preview
            self.registrants_preview.delete("1.0", tk.END)
            self.registrants_preview.insert("1.0", html_table)

            # Save to file
            output_path = PROJECT_ROOT / "registrants_table.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html_table)

            messagebox.showinfo(
                "Success", f"Registrants table generated and saved to:\n{output_path}"
            )
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate table: {e}")

    def collect_config(self) -> dict:
        """Collect all configuration from GUI fields."""
        # Parse twitch domains
        twitch_domains = [
            d.strip()
            for d in self.twitch_domains_entry.get().split(",")
            if d.strip()
        ]

        # Collect offsets
        offsets = {}
        for name, entry in self.offset_entries.items():
            try:
                offsets[name] = int(entry.get().strip())
            except ValueError:
                offsets[name] = 0

        return {
            "event": {
                "conference_name": self.conference_name_entry.get().strip(),
                "conference_full_name": self.conference_full_name_entry.get().strip(),
                "race_number": self.race_number_entry.get().strip(),
                "year": self.year_entry.get().strip(),
                "venue_name": self.venue_name_entry.get().strip(),
                "location": self.location_entry.get().strip(),
                "venue_url": self.venue_url_entry.get().strip(),
                "conference_url": self.conference_url_entry.get().strip(),
                "conference_logo": self.conference_logo_entry.get().strip(),
                "contact_email": self.contact_email_entry.get().strip(),
                "cname": self.cname_entry.get().strip(),
                "conference_dates_display": self.conference_dates_display_entry.get().strip(),
            },
            "dates": {
                "race_day": self.race_day_var.get().strip(),
                "offsets": offsets,
            },
            "orientation_1": {
                "time_display": self.o1_time_entry.get().strip(),
                "zoom_link": self.o1_zoom_entry.get().strip(),
                "slides_link": self.o1_slides_entry.get().strip(),
                "video_link": self.o1_video_entry.get().strip(),
            },
            "orientation_2": {
                "time_display": self.o2_time_entry.get().strip(),
                "zoom_link": self.o2_zoom_entry.get().strip(),
                "slides_link": self.o2_slides_entry.get().strip(),
                "video_link": self.o2_video_entry.get().strip(),
            },
            "registration": {
                "status": self.reg_status_var.get(),
                "form_link": self.reg_form_entry.get().strip(),
                "hide_participants": self.hide_participants_var.get(),
            },
            "results": {
                "time_trial_sheet_link": self.time_trial_entry.get().strip(),
                "bracket_link": self.bracket_entry.get().strip(),
                "youtube_stream_id": self.youtube_stream_entry.get().strip(),
                "twitch_parent_domains": twitch_domains,
                "show_stream_placeholder": self.show_stream_placeholder_var.get(),
                "stream_placeholder_text": self.stream_placeholder_entry.get().strip(),
                "show_results_placeholder": self.show_results_placeholder_var.get(),
                "results_placeholder_text": self.results_placeholder_entry.get().strip(),
            },
            "sim_racing": {
                "enabled": self.sim_enabled_var.get(),
                "edition": self.sim_edition_entry.get().strip(),
                "website_url": self.sim_website_entry.get().strip(),
                "registration_url": self.sim_registration_entry.get().strip(),
                "timeline_url": self.sim_timeline_entry.get().strip(),
            },
        }

    def save_config(self) -> None:
        """Save current configuration to file."""
        try:
            self.config = self.collect_config()
            save_config(self.config)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save configuration: {e}")

    def reset_config(self) -> None:
        """Reset configuration to defaults."""
        if messagebox.askyesno(
            "Confirm Reset", "Are you sure you want to reset to default configuration?"
        ):
            self.config = get_default_config()
            save_config(self.config)
            # Reload the application
            self.root.destroy()
            main()

    def apply_to_repo(self) -> None:
        """Apply configuration to all repository files."""
        try:
            self.config = self.collect_config()
            save_config(self.config)

            updater = RepositoryUpdater(self.config, PROJECT_ROOT)
            results = updater.update_all()

            # Show results
            result_text = "Repository Update Results:\n" + "=" * 40 + "\n\n"
            for filename, status in results.items():
                result_text += f"{filename}: {status}\n"

            messagebox.showinfo("Update Complete", result_text)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply configuration: {e}")

    def on_close(self) -> None:
        """Handle window close event."""
        if messagebox.askyesno("Exit", "Do you want to save configuration before exiting?"):
            self.save_config()
        self.root.destroy()


class RepositoryUpdater:
    """Updates repository files with configuration values."""

    def __init__(self, config: dict, project_root: Path):
        self.config = config
        self.project_root = project_root
        self.event = config.get("event", {})
        self.dates_config = config.get("dates", {})
        self.o1 = config.get("orientation_1", {})
        self.o2 = config.get("orientation_2", {})
        self.reg = config.get("registration", {})
        self.results = config.get("results", {})
        self.sim = config.get("sim_racing", {})

        # Calculate dates
        self.dates = calculate_dates(
            self.dates_config.get("race_day", ""),
            self.dates_config.get("offsets", {}),
        )

        # Pre-compute combined names with year
        self.year = self.event.get("year", "")
        self.conf_acronym = self.event.get("conference_name", "")
        self.conf_full_base = self.event.get("conference_full_name", "")

    @staticmethod
    def replace_placeholder(content: str, name: str, value: str) -> str:
        """Replace content between <!-- NAME --> and <!-- /NAME --> markers."""
        pattern = rf'<!-- {name} -->.*?<!-- /{name} -->'
        replacement = f'<!-- {name} -->{value}<!-- /{name} -->'
        return re.sub(pattern, replacement, content, flags=re.DOTALL)

    @property
    def conf_with_year(self) -> str:
        """Conference acronym with year (e.g., 'ICRA 2025')."""
        return f"{self.conf_acronym} {self.year}"

    @property
    def conf_full_with_year(self) -> str:
        """Full conference name with year (e.g., '2025 IEEE Conference on Robotics and Automation')."""
        return f"{self.year} {self.conf_full_base}"

    @property
    def conf_dates_with_year(self) -> str:
        """Conference dates with year (e.g., 'May 19th - 23rd 2025')."""
        return f"{self.event.get('conference_dates_display', '')} {self.year}"

    def update_all(self) -> dict[str, str]:
        """Update all repository files. Returns dict of filename -> status."""
        results = {}

        # Update CNAME
        results["CNAME"] = self.update_cname()

        # Update HTML files
        html_files = [
            "index.html",
            "timeline.html",
            "registration.html",
            "results.html",
            "roboracer_resources.html",
            "orientation_1.html",
            "orientation_2.html",
        ]

        for filename in html_files:
            filepath = self.project_root / filename
            if filepath.exists():
                results[filename] = self.update_html_file(filepath)
            else:
                results[filename] = "File not found"

        # Update markdown files
        md_files = ["race_resources.md", "stream.md"]
        for filename in md_files:
            filepath = self.project_root / filename
            if filepath.exists():
                results[filename] = self.update_md_file(filepath)
            else:
                results[filename] = "File not found"

        return results

    def update_cname(self) -> str:
        """Update CNAME file."""
        try:
            cname_path = self.project_root / "CNAME"
            with open(cname_path, "w", encoding="utf-8") as f:
                f.write(self.event.get("cname", ""))
            return "Updated"
        except Exception as e:
            return f"Error: {e}"

    def update_html_file(self, filepath: Path) -> str:
        """Update an HTML file with configuration values."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Common placeholders for all HTML files
            # Page title - wrap entire element
            page_title = f"<title>Roboracer {self.conf_with_year}</title>"
            content = self.replace_placeholder(content, "PAGE_TITLE", page_title)
            content = self.replace_placeholder(content, "CONF_WITH_YEAR", self.conf_with_year)

            # Nav email link - wrap entire element
            contact_email = self.event.get("contact_email", "")
            nav_email_html = f'''<li><a href="mailto:{contact_email}" class="icon solid solo fa-envelope"><span
						class="label">Email</span></a></li>'''
            content = self.replace_placeholder(content, "NAV_EMAIL_LINK", nav_email_html)

            # File-specific updates
            if filepath.name == "index.html":
                content = self._update_index_html(content)
            elif filepath.name == "timeline.html":
                content = self._update_timeline_html(content)
            elif filepath.name == "registration.html":
                content = self._update_registration_html(content)
            elif filepath.name == "results.html":
                content = self._update_results_html(content)
            elif filepath.name == "orientation_1.html":
                content = self._update_orientation1_html(content)
            elif filepath.name == "orientation_2.html":
                content = self._update_orientation2_html(content)

            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                return "Updated"
            return "No changes needed"
        except Exception as e:
            return f"Error: {e}"

    def _update_index_html(self, content: str) -> str:
        """Update index.html using placeholder markers."""
        race_num = self.event.get("race_number", "")
        venue = self.event.get("venue_name", "")
        location = self.event.get("location", "")
        venue_url = self.event.get("venue_url", "")
        conf_url = self.event.get("conference_url", "")
        conf_logo = self.event.get("conference_logo", "")

        # Update race number placeholder (replaces all occurrences)
        content = self.replace_placeholder(content, "RACE_NUMBER", race_num)

        # Update conference info (replaces all occurrences)
        content = self.replace_placeholder(content, "CONF_FULL_WITH_YEAR", self.conf_full_with_year)
        content = self.replace_placeholder(content, "CONF_DATES_WITH_YEAR", self.conf_dates_with_year)

        # Venue link - full element
        venue_link = f'<a href="{venue_url}" class="icon solid solo fa-globe-europe"><span class="label">Location</span></a> {venue}, {location}'
        content = self.replace_placeholder(content, "VENUE_LINK", venue_link)

        # Conference logo link - full element
        conf_logo_link = f'<a href="{conf_url}" class="image main"><img src="{conf_logo}" style="width: 30vw" alt="" /></a>'
        content = self.replace_placeholder(content, "CONF_LOGO_LINK", conf_logo_link)

        # Sim racing paragraph - full element
        if self.sim.get("enabled"):
            edition = self.sim.get("edition", "3rd")
            sim_url = self.sim.get("website_url", "")
            sim_paragraph = f'''<p>
							The {edition} Roboracer Sim Racing League is a virtual benchmark competition where teams can
							participate remotely. The teams will be provided with a simulator environment and a
							standardized car model. The teams will have to write software for their car to fulfill the
							objectives for the competition: Don't crash and minimize laptime. The teams will submit
							their
							software to the organizers, who will run the software on the simulator and evaluate the
							performance of the software. The teams will be ranked based on their performance in the
							simulator. The Sim Racing League is a great opportunity for teams to participate in the
							competition without the need to build a physical car and travel to the competition. For
							more information on the {edition} Roboracer Sim Racing League, please visit the <a
								href="{sim_url}">{edition}
								Sim Racing League website</a>.
						</p>'''
            content = self.replace_placeholder(content, "SIM_RACING_PARAGRAPH", sim_paragraph)

        return content

    def _update_timeline_html(self, content: str) -> str:
        """Update timeline.html using placeholder markers."""
        race_num = self.event.get("race_number", "")

        # Update race number placeholder
        content = self.replace_placeholder(content, "TL_RACE_NUMBER", race_num)

        # Update date cells with calculated dates
        if self.dates:
            # Registration Opens
            if "registration_open" in self.dates:
                reg_open = format_date_display(self.dates["registration_open"])
                content = self.replace_placeholder(content, "TL_REG_OPEN_DATE", reg_open)

            # Orientation 1 row - full element
            o1_date = format_date_display(self.dates.get("orientation_1", "")) if "orientation_1" in self.dates else ""
            o1_time = self.o1.get("time_display", "")
            o1_zoom = self.o1.get("zoom_link", "")
            o1_slides = self.o1.get("slides_link", "")
            o1_video = self.o1.get("video_link", "")
            o1_row = f'''<tr>
							<td class="tg-1vzr"><span
									style="font-weight:400;font-style:normal;text-decoration:none;color:#000;background-color:transparent">{o1_date}, {o1_time}</span>
							</td>
							<td class="tg-j1gp"><a
									href="{o1_zoom}"><span
										style="font-weight:inherit;font-style:inherit">Roboracer Orientation 1 (
										Competition Rules overview )</span></a><br>
								<span
									style="font-weight:400;font-style:normal;text-decoration:none;color:#000;background-color:transparent">
									<a
										href="{o1_slides}">Slide</a>
									<a
										href="{o1_video}">Video</a></span>
							</td>
						</tr>'''
            content = self.replace_placeholder(content, "TL_O1_ROW", o1_row)

            # Registration Closes
            if "registration_closes" in self.dates:
                reg_close = format_date_display(self.dates["registration_closes"])
                content = self.replace_placeholder(content, "TL_REG_CLOSE_DATE", reg_close)

            # Orientation 2 row - full element
            o2_date = format_date_display(self.dates.get("orientation_2", "")) if "orientation_2" in self.dates else ""
            o2_time = self.o2.get("time_display", "")
            o2_zoom = self.o2.get("zoom_link", "")
            o2_slides = self.o2.get("slides_link", "")
            o2_video = self.o2.get("video_link", "")
            o2_row = f'''<tr>
							<td class="tg-tbri"><span
									style="font-weight:400;font-style:normal;text-decoration:none;color:#000;background-color:transparent">{o2_date}, {o2_time}</span></td>
							<td class="tg-npj4"><a
									href="{o2_zoom}"><span
										style="font-weight:400;font-style:normal">Roboracer Orientation 2 ( Track set
										up, Track overview for in-person competition, Teams Training )</span></a><br>
								<span
									style="font-weight:400;font-style:normal;text-decoration:none;color:#000;background-color:transparent">
									<a
										href="{o2_slides}">Slide</a>
									<a
										href="{o2_video}">Video</a></span>
							</td>
						</tr>'''
            content = self.replace_placeholder(content, "TL_O2_ROW", o2_row)

            # Track Setup
            if "track_setup" in self.dates:
                track_setup = format_date_display(self.dates["track_setup"])
                content = self.replace_placeholder(content, "TL_TRACK_SETUP_DATE", track_setup)

            # Team Training
            if "team_training" in self.dates:
                training = format_date_display(self.dates["team_training"])
                content = self.replace_placeholder(content, "TL_TRAINING_DATE", training)

            # Qualification
            if "qualification" in self.dates:
                qual = format_date_display(self.dates["qualification"])
                content = self.replace_placeholder(content, "TL_QUAL_DATE", qual)

            # Race Day
            if "race" in self.dates:
                race = format_date_display(self.dates["race"])
                content = self.replace_placeholder(content, "TL_RACE_DATE", race)

        # Sim Racing timeline paragraph - full element
        sim_timeline_url = self.sim.get("timeline_url", "")
        sim_paragraph = f'''<p>For a detailed timeline of the virtual competition, please refer to the <a
					href="{sim_timeline_url}">virtual
					competition website</a>. </p>'''
        content = self.replace_placeholder(content, "TL_SIM_PARAGRAPH", sim_paragraph)

        return content

    def _update_registration_html(self, content: str) -> str:
        """Update registration.html using placeholder markers."""
        reg_status = self.reg.get("status", "closed")
        form_link = self.reg.get("form_link", "")
        hide_participants = self.reg.get("hide_participants", False)
        contact_email = self.event.get("contact_email", "")

        # Registration info paragraph - full element
        sim_edition = self.sim.get("edition", "3rd")
        sim_reg_url = self.sim.get("registration_url", "")
        reg_info = f'''<p>This competition is open for everyone of all levels, everyone is welcome to participate in this
					competition.
					A team can consist of multiple teammates. Teams with only one person are also allowed.
					Teams that take part in the in-person competition need to provide and build an Roboracer car by
					themselves.
					To register in the {sim_edition} Roboracer Sim Racing League, please refer to the <a
						href="{sim_reg_url}">Sim
						Racing Registration page</a>.
					<br>
					The following Google form is only for preliminary registration and for orientation and information
					sessions. Registration to {self.conf_with_year} is expected for all competitors.
				</p>'''
        content = self.replace_placeholder(content, "REG_INFO_PARAGRAPH", reg_info)

        # Update registration button based on status
        if reg_status == "open" and form_link:
            button_html = f'<a href="{form_link}" class="button">Registration Open</a>'
        else:
            button_html = '<a class="button" style="pointer-events: none; opacity: 0.5;">Registration Closed</a>'
        content = self.replace_placeholder(content, "REG_BUTTON", button_html)

        # Handle hide participants section
        if hide_participants:
            # Replace participants section with hidden version
            hidden_section = '''
				<hr style="display:none;">
				<h3 id="participants" style="display:none;">Participants</h3>
				<p style="display:none;">
					If you have registered for participation but the list below is not updated, please contact us at
					<a href="mailto:''' + contact_email + '''"><span
							class="label">''' + contact_email + '''</span></a>. <br>
					Register the modified information under the same team name, and we will update it accordingly.
				</p>
				<table style="display:none;">
					<thead>
						<tr>
							<th style="text-align: left">TEAM NAME</th>
							<th style="text-align: left">AFFILIATION</th>
							<th style="text-align: left">TEAM MEMBERS</th>
						</tr>
					</thead>
					<tbody>
					</tbody>
				</table>
				'''
            content = self.replace_placeholder(content, "PARTICIPANTS_SECTION", hidden_section)
        else:
            # Show participants section
            visible_section = '''
				<hr>
				<h3 id="participants">Participants</h3>
				<p>
					If you have registered for participation but the list below is not updated, please contact us at
					<a href="mailto:''' + contact_email + '''"><span
							class="label">''' + contact_email + '''</span></a>. <br>
					Register the modified information under the same team name, and we will update it accordingly.
				</p>
				<table>
					<thead>
						<tr>
							<th style="text-align: left">TEAM NAME</th>
							<th style="text-align: left">AFFILIATION</th>
							<th style="text-align: left">TEAM MEMBERS</th>
						</tr>
					</thead>
					<tbody>
					</tbody>
				</table>
				'''
            content = self.replace_placeholder(content, "PARTICIPANTS_SECTION", visible_section)

        return content

    def _update_results_html(self, content: str) -> str:
        """Update results.html using placeholder markers."""
        # Update Twitch parent domains
        domains = self.results.get("twitch_parent_domains", [])
        if domains:
            domains_str = json.dumps(domains)
            content = self.replace_placeholder(content, "TWITCH_PARENTS", domains_str)

        # Get placeholder settings
        show_stream_placeholder = self.results.get("show_stream_placeholder", True)
        stream_placeholder_text = self.results.get("stream_placeholder_text", "Live stream will appear here during the event.")
        show_results_placeholder = self.results.get("show_results_placeholder", True)
        results_placeholder_text = self.results.get("results_placeholder_text", "Results will be posted after the competition.")

        # Update stream placeholder
        if show_stream_placeholder:
            stream_html = f'<p style="color: #888; font-style: italic;">{stream_placeholder_text}</p>'
        else:
            stream_html = ''
        content = self.replace_placeholder(content, "STREAM_PLACEHOLDER", stream_html)

        # Update results placeholder
        if show_results_placeholder:
            results_html = f'<p style="color: #888; font-style: italic;">{results_placeholder_text}</p>'
        else:
            results_html = ''
        content = self.replace_placeholder(content, "RESULTS_PLACEHOLDER", results_html)

        # Update time trial section - hide if no link
        tt_link = self.results.get("time_trial_sheet_link", "")
        if tt_link:
            tt_section = f'''<br>
						<h3 style="text-align: left;">TIME TRIAL</h3>
						<a href="{tt_link}" class="button">Mapping Schedule, Qualification</a>'''
        else:
            tt_section = ''  # Hide entire section
        content = self.replace_placeholder(content, "TIME_TRIAL_SECTION", tt_section)

        # Update bracket section - hide if no link
        bracket_link = self.results.get("bracket_link", "")
        if bracket_link:
            bracket_section = f'''<br>
						<br>
						<h3 style="text-align: left;">HEAD TO HEAD RACE BRACKET</h3>
						<a href="{bracket_link}" class="button">TOURNAMENT</a>'''
        else:
            bracket_section = ''  # Hide entire section
        content = self.replace_placeholder(content, "BRACKET_SECTION", bracket_section)

        return content

    def _update_orientation1_html(self, content: str) -> str:
        """Update orientation_1.html using placeholder markers."""
        slides_link = self.o1.get("slides_link", "")
        video_link = self.o1.get("video_link", "")

        # Generate full content block
        o1_content = f'''<h3> Orientation 1 Slides </h3>
						<iframe src="{slides_link}" frameborder="0" width="960" height="569" allowfullscreen="true" mozallowfullscreen="true"
							webkitallowfullscreen="true"></iframe>

						<h3> Orientation 1 Video Recording</h3>
						<iframe src="{video_link}" width="640" height="480" allow="autoplay"></iframe>'''
        content = self.replace_placeholder(content, "O1_CONTENT", o1_content)

        return content

    def _update_orientation2_html(self, content: str) -> str:
        """Update orientation_2.html using placeholder markers."""
        # The CONF_WITH_YEAR placeholder is already handled in the common section
        # O2_CONTENT can be updated when slides/video are available
        return content

    def update_md_file(self, filepath: Path) -> str:
        """Update a markdown file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

            original_content = content

            # Update title in YAML front matter (simple text replacement)
            content = re.sub(
                r"title: Roboracer \w+ \d+ Race Resources",
                f"title: Roboracer {self.conf_with_year} Race Resources",
                content,
            )

            # Build orientation links - only include links that have URLs
            orientation_lines = []
            o1_slides = self.o1.get("slides_link", "")
            o1_video = self.o1.get("video_link", "")
            o2_slides = self.o2.get("slides_link", "")
            o2_video = self.o2.get("video_link", "")

            if o1_slides:
                orientation_lines.append(f"- [Orientation 1 Meeting Slides]({o1_slides})")
            if o1_video:
                orientation_lines.append(f"- [Orientation 1 Recording]({o1_video})")
            if o2_slides:
                orientation_lines.append(f"- [Orientation 2 Meeting Slides]({o2_slides})")
            if o2_video:
                orientation_lines.append(f"- [Orientation 2 Recording]({o2_video})")

            orientation_content = "\n".join(orientation_lines)
            content = self.replace_placeholder(content, "ORIENTATION_LINKS", orientation_content)

            if content != original_content:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(content)
                return "Updated"
            return "No changes needed"
        except Exception as e:
            return f"Error: {e}"


def main():
    """Main entry point."""
    # Use regular Tk with custom dark styling
    root = tk.Tk()
    app = EventManagerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

