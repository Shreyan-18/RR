# 🏏 SupeRR Selector Web Application

An interactive sports analytics platform designed for the **Rajasthan Royals (SupeRR Selector Season 2 - Round 1)**.

Built with **Next.js (App Router)**, **React**, **Tailwind CSS**, and **Lucide Icons**.

---

## 🌟 Features Included

1. **Top 10 Pressure Leaderboards**:
   - High-resolution player headshots with graceful fallback avatars.
   - Comprehensive metrics: High-Pressure Strike Rate, Economy, Boundary %, and Post-Boundary Composure.
   - Expandable **Tactical Scouting Reports** detailing player pressure mechanics.
2. **The 4-Quadrant Archetypes Model**:
   - Visual breakdown across *Clutch Giants*, *Crisis Specialists*, *Front-Runners*, and *Strugglers*.
3. **The Pressure-Proof World XI Tactical Pitch**:
   - Position-optimized batting spine (Slots 1 to 7) and bowling phase specialists (Powerplay, Middle, Death).
4. **Live Match Pressure Simulator**:
   - Real-time interactive sliders (RRR, Balls Remaining, Wickets Fallen, Macro Stakes, Hostile Fortress).
   - Dynamic continuous pressure formula: $P_{\text{ball}} = 0.40 \times C_{\text{macro}} + 0.60 \times S_{\text{micro}}$.
5. **Interactive Methodology Reference**:
   - Complete breakdown of weights, tiers, and momentum indicators.

---

## ⚡ Instant Standalone Preview (Zero Install Required)

You can preview the platform right now without installing any Node modules:

* Simply open **`web/index.html`** in any web browser (Chrome, Edge, Safari, Firefox).
* It contains the full application powered by Tailwind CSS CDN and Chart.js!

---

## 🚀 Running the Next.js App Locally

```bash
cd web
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to view the development server.

---

## ☁️ Deploying to Vercel (1-Click)

When you are ready to deploy:

1. Push your repository to GitHub:
   ```bash
   git add .
   git commit -m "Add SupeRR Selector Next.js web application"
   git push origin main
   ```
2. Go to **[vercel.com](https://vercel.com)** and log in.
3. Click **"Add New..."** $\to$ **"Project"**.
4. Import your repository: **`Shreyan-18/RR`**.
5. Under **Root Directory**, click **Edit** and select **`web`**.
6. Click **Deploy**. Vercel will build and deploy the application in under 60 seconds with a free public `.vercel.app` domain!
