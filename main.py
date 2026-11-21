import asyncio, ipaddress, os, time
from urllib.parse import urlparse
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="NAME LAB Proxy Health API")
origins = [x.strip() for x in os.getenv("ALLOWED_ORIGINS", "https://haizaadi.github.io").split(",") if x.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"], allow_headers=["Content-Type"])

class RequestBody(BaseModel):
    proxies: list[str] = Field(min_length=1, max_length=300)

def validate_proxy(raw: str) -> str:
    value = raw.strip()
    if "://" not in value:
        value = "http://" + value
    parsed = urlparse(value)
    if parsed.scheme not in ("http", "https", "socks5"):
        raise ValueError("Only HTTP/HTTPS/SOCKS5 supported")
    if not parsed.hostname or not parsed.port or not 1 <= parsed.port <= 65535:
        raise ValueError("Invalid host or port")
    try:
        addr = ipaddress.ip_address(parsed.hostname)
        if not addr.is_global:
            raise ValueError("Private/reserved IP blocked")
    except ValueError as exc:
        if "blocked" in str(exc):
            raise
    return value

async def test_one(raw: str, sem: asyncio.Semaphore):
    try:
        proxy = validate_proxy(raw)
    except Exception as exc:
        return {"proxy": raw, "live": False, "latency_ms": None, "detail": str(exc)}
    async with sem:
        started = time.perf_counter()
        try:
            timeout = httpx.Timeout(7.0, connect=4.0)
            async with httpx.AsyncClient(proxy=proxy, timeout=timeout, follow_redirects=True) as client:
                # Fixed harmless destination; users cannot supply arbitrary scan targets.
                response = await client.get("https://www.example.com/")
            latency = round((time.perf_counter() - started) * 1000)
            live = 200 <= response.status_code < 500
            return {"proxy": raw, "live": live, "latency_ms": latency, "detail": f"HTTP {response.status_code}"}
        except Exception as exc:
            return {"proxy": raw, "live": False, "latency_ms": None, "detail": type(exc).__name__}

@app.get("/")
async def root():
    return {"service": "NAME LAB Proxy Health API", "status": "ok"}

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/api/check-proxies")
async def check_proxies(body: RequestBody):
    semaphore = asyncio.Semaphore(10)
    results = await asyncio.gather(*(test_one(item, semaphore) for item in body.proxies))
    return {"results": results}
