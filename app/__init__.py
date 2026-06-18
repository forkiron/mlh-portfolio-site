import os
from datetime import datetime

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- Site basics (placeholders — personalize these later) ---
NAME = "Enter Name"
TAGLINE = "Enter role"
PHOTO = "logo.jpg"  # 

# Pages shown in the dynamic navigation bar. Add a route + an entry
# here and it automatically appears in the menu.
PAGES = [
    {"name": "Home", "endpoint": "index"},
    {"name": "Hobbies", "endpoint": "hobbies"},
]

ABOUT = (
    "Enter About Me section. "
    )

EDUCATION = [
    {
        "school": "Enter University",
        "degree": "Enter Degree",
        "period": "Enter Period",
    },
]

# Simple list-style "travel map" for now — we'll upgrade to an
# interactive map later.
PLACES = [
    {"flag": "flag emoji", "city": "City", "country": "Country"}
    
]

HOBBIES = [
    {
        "name": "Name",
        "description": "Description.",
        "image": "vit.jpeg",
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
