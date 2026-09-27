# Mizan Qist — Investor Pitch

Seed-round pitch deck for Mizan Qist, a digital agency built in Abuja serving clients in the UK, the Gulf, the US and Nigeria. Raising ₦35m to scale toward a $1m annual revenue run-rate in 18 months.

## View the deck

Open `index.html` in any browser. Use ← → (or click either side of the screen) to move between slides, and press F for fullscreen. Add `#n` to the URL to jump to slide n. Print to PDF from the browser to get one slide per page.

## What's in here

| Path | Contents |
|---|---|
| `index.html` | The full 18-slide presentation, built from the files below |
| `slides/` | One HTML file per slide (speaker notes are in each slide's `<aside>`) |
| `deck.json` | Slide order, sections and fonts |
| `build.py` | Rebuilds `index.html` from `deck.json` and `slides/` — run `python3 build.py` |
| `model/model.py` | 18-month financial model behind the projections. `python3 model/model.py 1` runs the target plan; `python3 model/model.py 0.5` runs the half-speed case |

## Key assumptions (model)

- ₦1,330 per US dollar, held flat
- International retainers average $2,000/month; Nigerian retainers ₦600,000/month
- Two developers at ₦250,000/month each to start; later hires paid from revenue
- Costs include 12% own marketing, 10% sales commission on international deals, 12% freelancers, 3% payment fees and 5% bad debt
- Figures are before tax

Market data sources are listed on the final slide.
