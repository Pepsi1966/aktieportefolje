# Aktieportefølje Web-App — Deployment Guide

## Hvad du har brug for
- En gratis GitHub-konto (github.com)
- En gratis Render-konto (render.com)
- De 3 filer i denne mappe: app.py, requirements.txt, Procfile + mappen static/

---

## Trin 1: Upload koden til GitHub

1. Gå til **github.com** og log ind (eller opret konto)
2. Klik på **"New repository"** (grøn knap øverst til højre)
3. Navngiv den f.eks. `aktieportefolje`
4. Vælg **Public** og klik **Create repository**
5. Klik på **"uploading an existing file"** linket på den nye side
6. Træk ALLE filerne ind (app.py, requirements.txt, Procfile, og static/index.html)
7. Klik **Commit changes**

---

## Trin 2: Deploy på Render (gratis)

1. Gå til **render.com** og log ind med din GitHub-konto
2. Klik **"New +"** → **"Web Service"**
3. Vælg dit `aktieportefolje` repository
4. Udfyld indstillingerne:
   - **Name**: aktieportefolje (eller hvad du vil)
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: Free
5. Klik **"Create Web Service"**

Render bygger og starter din app automatisk. Det tager 2-3 minutter.

---

## Trin 3: Åbn din app

Render giver dig en URL som:
`https://aktieportefolje-xxxx.onrender.com`

Den URL virker fra alle enheder — telefon, tablet, computer.

---

## Vigtigt om gratis plan
- Render's gratis plan "sover" efter 15 min inaktivitet
- Første besøg efter søvn tager ~30 sekunder at vågne op
- Herefter er den hurtig som normalt
- Du kan opgradere til $7/md for at undgå dette

---

## Opdater kurserne
Klik bare **"Opdater kurser"** i appen — den henter automatisk
live kurser fra Yahoo Finance via din server.
