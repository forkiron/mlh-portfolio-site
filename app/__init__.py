import os
from datetime import datetime

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- Site basics (placeholders — personalize these later) ---
NAME = "Enter Name"
TAGLINE = "Enter Role"
PHOTO = "logo.jpg"  #

# Pages shown in the dynamic navigation bar. Add a route + an entry
# here and it automatically appears in the menu.
PAGES = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
]

ABOUT = (
    "Hi, I'm [Enter Name]. I am currently pursuing [Enter Major] at [Enter University] "
    "and my background is in [xyz]. I am currently interested in [abc]."
)

EDUCATION = [
    {
        "school": "Enter University",
        "degree": "B.S. in Enter Program",
        "period": "20XX — 20XX",
    },
]

# Places I've traveled to. Each entry carries lat/lng so it can be
# plotted as a marker on the interactive Leaflet map (see index.html).
PLACES = [
    {"flag": "🇺🇸", "city": "San Francisco", "country": "USA", "lat": 37.7749, "lng": -122.4194},
    {"flag": "🇯🇵", "city": "Tokyo", "country": "Japan", "lat": 35.6762, "lng": 139.6503},
    {"flag": "🇫🇷", "city": "Paris", "country": "France", "lat": 48.8566, "lng": 2.3522},
    {"flag": "🇨🇦", "city": "Toronto", "country": "Canada", "lat": 43.6532, "lng": -79.3832},
]

HOBBIES = [
    {
        "section": "Outdoor",
        "hobbies": [
            {"name": "Hiking", "description": "Exploring trails and nature.", "icon": "🥾"},
            {"name": "Cycling", "description": "Long rides through the city and countryside.", "icon": "🚴"},
        ],
    },
    {
        "section": "Creative",
        "hobbies": [
            {"name": "Photography", "description": "Capturing moments and places.", "icon": "📷"},
            {"name": "Sketching", "description": "Drawing portraits and landscapes.", "icon": "✏️"},
        ],
    },
    {
        "section": "Tech & Gaming",
        "hobbies": [
            {"name": "Hackathons", "description": "Building projects under pressure.", "image": "vit.jpeg"},
            {"name": "Gaming", "description": "Strategy and indie games.", "icon": "🎮"},
        ],
    },
]

SKILLS = [
    {
        "group": "Languages",
        "skills": ["Language#1", "Language#2", "Language#3", "Language#4"],
    },
    {
        "group": "Frameworks",
        "skills": ["Framework#1", "Framework#2", "Framework#3", "Framework#4"],
    },
    {
        "group": "Tools",
        "skills": ["Tool#1", "Tool#2", "Tool#3", "Tool#4"],
    },
]

WORK_EXPERIENCES = [
    {
        "role": "Enter Role",
        "company": "Enter Company",
        "period": "20XX-20XX",
        "description": "Enter what you worked on.",
    },
    {
        "role": "Enter Role",
        "company": "Enter Company",
        "period": "20XX-20XX",
        "description": "Enter what you worked on."
    },
    {
        "role": "Enter Role",
        "company": "Enter Company",
        "period": "20XX-20XX",
        "description": "Enter what you worked on."
    },
]

@app.context_processor
def inject_globals():
    """Make these available to every template (powers the dynamic nav)."""
    return {
        "pages": PAGES,
        "name": NAME,
        "url": os.getenv("URL"),
        "year": datetime.now().year,
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=f"{NAME} · Portfolio",
        tagline=TAGLINE,
        photo=PHOTO,
        about=ABOUT,
        skills=SKILLS,
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
        places=PLACES,
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title=f"Hobbies · {NAME}",
        hobbies=HOBBIES,
    )
