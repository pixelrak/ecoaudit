# 🌿 EcoAudit — Community Waste Logger

> A location-verified waste logging platform built to make community disposal data trustworthy and transparent.

**Live Demo:** `https://ecoaudit.vercel.app` *(replace with your deployed URL)*  
**API Backend:** `https://ecoaudit-api.onrender.com` *(replace with your Render URL)*

---

## What is EcoAudit?

EcoAudit is a full-stack web application where users can log waste they've disposed of, with their **GPS location captured automatically** to prevent fraudulent entries. All logs appear on a live map alongside a dashboard showing total waste by category.

The idea: good environmental data requires trust. By using the browser's native Geolocation API instead of a manual text field, every entry is tied to a real physical location.

---

## Features

### MVP
- **Waste Entry Form** — Select category (Plastic, E-Waste, Organic, Metal, Paper, Other) and enter weight in kg
- **Validated Geolocation** — Location is captured via `navigator.geolocation`, no manual text input allowed
- **Audit Dashboard** — Live feed of all submitted entries with coordinates, category, and timestamp
- **Live Totaling** — Real-time aggregated stats per category and grand total, updated after every submission

### Bonus Features Implemented
- **Map Visualization** — Leaflet.js renders a dark-themed map with a custom pin for every log entry
- **Location Error Handling** — Graceful UI messages for denied permission, GPS unavailability, and timeout

---

## Tech Stack

| Layer      | Technology                        | Why                                              |
|------------|-----------------------------------|--------------------------------------------------|
| Frontend   | HTML, CSS, Vanilla JavaScript     | No unnecessary build complexity for an MVP       |
| Map        | Leaflet.js                        | Open-source, no API key required                 |
| Backend    | Python + Flask                    | Lightweight REST API, matches my Python skillset |
| Database   | Supabase (PostgreSQL)             | Managed DB with a generous free tier             |
| Deployment | Vercel (frontend), Render (API)   | Both have free tiers and auto-deploy from GitHub |

---

## Project Structure

```
ecoaudit/
├── frontend/
│   └── index.html          # Single-page app (HTML + CSS + JS)
├── backend/
│   ├── app.py              # Flask REST API
│   ├── requirements.txt    # Python dependencies
│   ├── render.yaml         # Render deployment config
│   └── .env.example        # Environment variable template
├── supabase_schema.sql     # Database schema (run once in Supabase SQL editor)
├── vercel.json             # Vercel frontend deployment config
└── README.md
```

---

## API Endpoints

| Method | Endpoint      | Description                          |
|--------|---------------|--------------------------------------|
| GET    | `/api/logs`   | Fetch all waste log entries           |
| POST   | `/api/logs`   | Submit a new waste log entry          |
| GET    | `/api/stats`  | Get aggregated totals by category     |
| GET    | `/`           | Health check                          |

### POST `/api/logs` — Request Body
```json
{
  "category":   "Plastic",
  "weight_kg":  2.5,
  "latitude":   12.9716,
  "longitude":  77.5946,
  "notes":      "Collected from roadside cleanup"
}
```

---

## Running Locally

### Prerequisites
- Python 3.10+
- A free [Supabase](https://supabase.com) account

### 1. Clone the repository
```bash
git clone https://github.com/pixelrak/ecoaudit.git
cd ecoaudit
```

### 2. Set up the database
1. Create a new project on [Supabase](https://supabase.com)
2. Go to **SQL Editor → New Query**
3. Paste and run the contents of `supabase_schema.sql`
4. Go to **Project Settings → API** and copy your Project URL and `anon` key

### 3. Configure the backend
```bash
cd backend
cp .env.example .env
# Edit .env and paste your Supabase URL and key
```

### 4. Install dependencies and run Flask
```bash
pip install -r requirements.txt
python app.py
```
The API runs at `http://localhost:5000`

### 5. Open the frontend
In `frontend/index.html`, change the `API_BASE` constant at the top of the `<script>` section:
```js
const API_BASE = "http://localhost:5000";
```
Then open `frontend/index.html` directly in your browser (or use VS Code Live Server).

> **Note:** Geolocation requires HTTPS in production. Locally, `localhost` is exempt.

---

## Deployment

### Backend (Render)
1. Push repo to GitHub
2. Go to [render.com](https://render.com) → New Web Service → Connect your GitHub repo
3. Set root directory to `backend/`
4. Add environment variables: `SUPABASE_URL` and `SUPABASE_KEY`
5. Render auto-detects `render.yaml` and builds from there

### Frontend (Vercel)
1. Go to [vercel.com](https://vercel.com) → New Project → Import your GitHub repo
2. No build command needed — it's a static site
3. After deploy, update `API_BASE` in `index.html` to your Render URL, then redeploy

---

## What I Learned Building This

Coming into this project, I was comfortable with Python and basic web (HTML/CSS/JS). Building EcoAudit pushed me to:

- **Build a REST API with Flask** — learned how to structure routes, handle request bodies, and return proper HTTP status codes
- **Work with Supabase** — first time using a managed database; understanding Row Level Security policies was a new challenge
- **Use the Browser Geolocation API** — learned the async permission model and how to handle the three error states gracefully
- **Integrate Leaflet.js** — customised map tiles and built dynamic icon markers from scratch
- **Deploy a full-stack app** — wiring together Vercel + Render + Supabase with environment variables across services

---

## Author

**Rakshandoss M**  
BTech CSE (AI & ML), VIT Chennai  
[github.com/pixelrak](https://github.com/pixelrak) · [linkedin.com/in/rakshandossm](https://linkedin.com/in/rakshandossm)
