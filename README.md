# S&S Property Services — Website

A single-file static website for S&S Property Services: lawn care, pressure
washing, landscaping and window washing in and around Kingston, Ontario.

## Files

| File | What it is |
|---|---|
| `index.html` | The whole website — HTML, CSS and JS in one file. |
| `thank-you.html` | Where visitors land after submitting a form. |
| `netlify.toml` | Netlify deploy config (publish root, no build step). |
| `design-options.pdf` | 42 design options: 32 colour schemes (each shown applied to the real site) + 10 page layouts. |
| `design/schemes.json` | The colour scheme definitions used by both scripts below. |
| `design/render_scheme_previews.js` | Renders a screenshot of the site in every scheme (`npm i playwright-core`, then `node render_scheme_previews.js previews`). |
| `design/generate_design_options.py` | Builds the PDF from those previews (`pip install reportlab pillow`, then `python3 generate_design_options.py previews`). |

## Changing the colour scheme

Every scheme in the PDF lists five hex codes. Open `index.html`, find the
`:root{...}` block at the top of the `<style>` section, and paste the five
codes over the existing ones — same order, same labels
(`--primary`, `--dark`, `--accent`, `--light`, `--ink`). That's it.

## Before going live — TODO list

1. **Form notifications** — both forms submit through Netlify Forms
   (`quote-request` and `general-inquiry`). After the first deploy, in the
   Netlify dashboard go to **Forms → Form notifications** and add an email
   notification pointing at the real inbox. No code changes needed.
2. **Photos & videos** — the gallery and video section use stock media
   stored locally in `assets/` (see credits below). Replace them with
   your own job photos/clips when you have them — same filenames, or
   update the `src`/`poster` attributes in `index.html`.
   No free stock video of pressure washing could be found; that service
   is covered by a photo only for now.
3. **Testimonials** — the four quotes are placeholder examples. Swap them
   for real customer feedback as it comes in.
4. **Phone number** — none is listed yet; add one to the footer/hero if
   you want calls.

## Stock media credits

Videos and three photos are from [Mixkit](https://mixkit.co) and
[Unsplash](https://unsplash.com) (free licenses, no attribution required).
Three photos are **CC BY 2.0** from Flickr and require this attribution
(keep this section, or credit them in the site footer, while they're in use):

- `assets/img/pressure-washing.jpg` — "Pressure Washing Driveway – Lima OH"
  by [Decorative Concrete Kingdom](https://www.flickr.com/photos/38041294@N05/6215666345), CC BY 2.0
- `assets/img/mowing.jpg` — "First Leaf Mowing of the Season"
  by [byzantiumbooks](https://www.flickr.com/photos/10688882@N00/15598694757), CC BY 2.0
- `assets/img/windows.jpg` — "a window washer soaps up a window"
  by [aqua.mech](https://www.flickr.com/photos/137169575@N04/24441624384), CC BY 2.0

## Hosting — Netlify (push = deploy)

The site deploys automatically via Netlify: every push to `main` publishes
the repo root (configured in `netlify.toml` — keep it in sync with the
Netlify UI settings).

| Detail | Value |
|---|---|
| Netlify site name | _TBD — fill in after connecting in the Netlify UI_ |
| Netlify site ID | _TBD_ |
| Live URL | _TBD — e.g. https://ss-property-services.netlify.app_ |

### Day-to-day workflow (every change — this IS the deploy)

1. Edit the site files.
2. Open `index.html` in a browser to eyeball it locally.
3. Commit, then `git push origin main`.
4. Netlify auto-builds; the change is live in ~30–60 s. Pushing is the
   deploy — there is no manual publish step.
5. Verify it reached **ready** under Netlify → Deploys.

Small content edits can go straight to `main`; use a branch + PR for
anything non-trivial. Never commit secrets (use Netlify env vars if ever
needed), and check with the owner before touching a custom domain or DNS.
