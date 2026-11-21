NAME LAB PRO V3

FRONTEND:
- Upload index.html to the root of your GitHub Pages repository, replacing the old index.html.

BACKEND ON RENDER:
1. Create a NEW public GitHub repository and upload main.py, requirements.txt, render.yaml.
2. Render Dashboard > New > Web Service > connect that repository.
3. Build command: pip install -r requirements.txt
4. Start command: uvicorn main:app --host 0.0.0.0 --port $PORT
5. Choose Free and deploy.
6. In Environment add ALLOWED_ORIGINS=https://haizaadi.github.io
7. Copy the Render URL (https://....onrender.com), paste it into NAME LAB PRO > Backend URL.

PROXY TEST:
- Supports HTTP, HTTPS, SOCKS5 proxy strings, optionally with credentials.
- Checks reachability to a fixed harmless public endpoint, not arbitrary targets.
- Maximum 300 per request; concurrency 10; timeout 7 seconds.
- Use only proxies you own or are authorized to use. Proxy credentials are sent to your own backend.
- Do not submit account passwords or tokens.
- Render free services sleep after 15 minutes idle and may take about one minute to wake. Free plan also has usage limits.
- This tool does not check Discord/TikTok username availability or automate username sniping. Username Hit/Taken status is manual.
