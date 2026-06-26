import os
from datetime import datetime

from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# --- Site basics ---
NAME = "thomas lenh"
TAGLINE = "first year @ uwaterloo · into consumer tech"

# Pages shown in the dynamic navigation bar. Add a route + an entry
# here and it automatically appears in the menu.
PAGES = [
    {"name": "home", "endpoint": "index"},
    {"name": "hobbies", "endpoint": "hobbies"},
    {"name": "week 1", "endpoint": "week1"},
]

# Social links shown next to the hero heading.
SOCIALS = [
    {"label": "GitHub", "href": "https://github.com/forkiron", "icon": "github"},
    {"label": "Twitter", "href": "https://x.com/forkyron", "icon": "twitter"},
    {"label": "LinkedIn", "href": "https://www.linkedin.com/in/thomas-lenh", "icon": "linkedin"},
    {"label": "Email", "href": "mailto:thomaslenh@gmail.com", "icon": "mail"},
]

# Short bio lines. The first is the lead; the rest render as ↳ sub-lines.
BIO = {
    "lead": "first-year student based in waterloo.",
    "lines": [
        "i like consumer tech and building cool things.",
    ],
}

WORK_EXPERIENCES = [
    {
        "company": "viggle (a16z)",
        "role": "member of technical staff",
        "note": "systems + infra for 40 million users",
        "period": "summer 2026",
        "logo": "vigglenew.webp",
        "href": "https://viggle.ai/",
    },
    {
        "company": "plots (a16z)",
        "role": "software engineer",
        "note": "internal tooling for 500k users",
        "period": "jan 2026 - april 2026",
        "logo": "plots_new.png",
        "href": "https://plots.events",
        "dark_logo": True,
    },
    {
        "company": "keywa newcomers",
        "role": "software engineer",
        "note": "cursor for international students",
        "period": "nov 2025 - dec 2025",
        "logo": "keywa_logo.jpg",
        "href": "https://www.keywacanada.com/",
    },
]

# Side projects — image, a short stat badge, blurb, and links. Pulled from
# thomaslenh-v2 (one still image each, no hover-zoom).
PROJECTS = [
    {
        "name": "vit",
        "image": "vit.jpeg",
        "stat": "2m views",
        "description": "git for video editing. 700+ stars and 2 million views.",
        "href": "https://vit-editor.vercel.app/",
        "links": [
            {"icon": "github", "href": "https://github.com/LucasHJin/vit"},
            {"icon": "youtube", "href": "https://www.youtube.com/watch?v=phS28hhJSP8"},
            {"icon": "external", "href": "https://vit-editor.vercel.app/"},
        ],
    },
    {
        "name": "anterno",
        "image": "anternomain.png",
        "stat": "won $30k",
        "description": "cursor for intern onboarding. national finalist @ spark, backed by dmz ventures & rhf.",
        "href": "https://ingeniousplus.ca/spark-investments/",
        "links": [
            {"icon": "newspaper", "href": "https://ingeniousplus.ca/spark-investments/"},
            {"icon": "external", "href": "https://anterno.com"},
        ],
    },
    {
        "name": "pindex",
        "image": "pindex.png",
        "stat": "won nexhacks",
        "description": "agentic index funds that automatically diversify risk across related prediction markets.",
        "href": "https://pindex.tech",
        "links": [
            {"icon": "github", "href": "https://github.com/danielp1218/Pindex"},
            {"icon": "external", "href": "https://pindex.tech"},
        ],
    },
    {
        "name": "donair",
        "image": "donairshow.png",
        "stat": "acquired",
        "description": "instant agentic crowdfunding. won twice @ conuhacks, acquired by talsom.",
        "href": "https://donair.tech",
        "links": [
            {"icon": "newspaper", "href": "https://www.talsom.com/insights/talsom-et-la-maison-du-pere-du-design-thinking-a-laction-contre-litinerance/"},
            {"icon": "external", "href": "https://donair.tech"},
        ],
    },
]

EDUCATION = [
    {
        "school": "university of waterloo",
        "degree": "bachelor of mathematics, computer science",
        "period": "2025 — present",
        "logo": "uwaterloo.webp",
        "href": "https://uwaterloo.ca",
    },
]

# Places I've been. Each entry carries lat/lng so it can be plotted as a
# marker on the interactive Leaflet map (see index.html).
PLACES = [
    {"flag": "🇺🇸", "city": "san francisco", "country": "usa", "lat": 37.7749, "lng": -122.4194},
    {"flag": "🇺🇸", "city": "los angeles", "country": "usa", "lat": 34.0522, "lng": -118.2437},
    {"flag": "🇻🇳", "city": "vietnam", "country": "", "lat": 16.0471, "lng": 108.2068},
    {"flag": "🇹🇼", "city": "taiwan", "country": "", "lat": 23.6978, "lng": 120.9605},
]

SKILLS = [
    {"group": "languages", "skills": ["python", "java", "c", "c++", "javascript", "typescript", "sql", "bash", "swift"]},
    {"group": "frameworks", "skills": ["react", "react native", "next.js", "express", "flask", "fastapi", "tailwind"]},
    {"group": "infrastructure", "skills": ["docker", "kubernetes", "linux", "ci/cd"]},
    {"group": "databases & data", "skills": ["postgresql", "mysql", "mongodb", "redis", "influxdb", "pandas", "opencv"]},
    {"group": "developer tools", "skills": ["git", "github actions", "gcp", "aws", "digitalocean", "supabase", "vercel", "figma"]},
]

HOBBIES = [
    {
        "section": "hackathons",
        "hobbies": [
            {"name": "", "description": "building projects under pressure — easily the most fun i have.", "image": "vit.jpeg"},
        ],
    },
]

# Week 1 recap — kept short and nonchalant, one line per thing.
WEEK1 = {
    "intro": "orientation + first taste of linux and servers. super hands-on week.",
    "learnings": [
        "spun up my first digitalocean droplet running centos stream 9.",
        "ran cat /etc/centos-release to check the os — kinda cool.",
        "generated ssh keys to get into the box securely.",
        "deployed this flask site straight onto the vps.",
        "used tmux so flask keeps running after i log out.",
        "pointed a duckdns domain at the server's ip.",
        "deploy off a branch so main stays clean for friends to fork.",
    ],
}


@app.context_processor
def inject_globals():
    """Make these available to every template (powers the dynamic nav)."""
    return {
        "pages": PAGES,
        "name": NAME,
        "socials": SOCIALS,
        "url": os.getenv("URL"),
        "year": datetime.now().year,
    }


@app.route("/")
def index():
    return render_template(
        "index.html",
        title=f"{NAME} · portfolio",
        tagline=TAGLINE,
        bio=BIO,
        skills=SKILLS,
        work_experiences=WORK_EXPERIENCES,
        education=EDUCATION,
        places=PLACES,
    )


@app.route("/hobbies")
def hobbies():
    return render_template(
        "hobbies.html",
        title=f"hobbies · {NAME}",
        hobbies=HOBBIES,
        projects=PROJECTS,
    )


@app.route("/week1")
def week1():
    return render_template(
        "week1.html",
        title=f"week 1 · {NAME}",
        week1=WEEK1,
    )
