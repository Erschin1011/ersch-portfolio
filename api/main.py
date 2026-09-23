import os
import re
import time
from email.utils import parseaddr
from collections import defaultdict, deque

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:4321").split(",") if origin.strip()]
rate_limit_window = 15 * 60
rate_limit_max = 5
requests_by_ip: dict[str, deque[float]] = defaultdict(deque)
email_pattern = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")
spam_pattern = re.compile(r"(?:https?://|www\.|<script|\[url|viagra|casino|crypto)", re.IGNORECASE)
app = FastAPI(title="ErsCh.dev Contact API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/contact")
def contact(request: Request, name: str = Form(...), email: str = Form(...), message: str = Form(...), website: str = Form("")) -> dict[str, object]:
    # The honeypot is invisible to people but commonly filled by basic bots.
    if website.strip():
        raise HTTPException(status_code=400, detail="Solicitud no válida")

    now = time.monotonic()
    client_ip = request.client.host if request.client else "unknown"
    recent_requests = requests_by_ip[client_ip]
    while recent_requests and now - recent_requests[0] > rate_limit_window:
        recent_requests.popleft()
    if len(recent_requests) >= rate_limit_max:
        raise HTTPException(status_code=429, detail="Demasiados intentos. Intenta más tarde.")
    recent_requests.append(now)

    name = name.strip()
    email = email.strip()
    message = message.strip()
    parsed_email = parseaddr(email)[1]
    if not name or len(name) > 120 or any(ord(char) < 32 for char in name):
        raise HTTPException(status_code=422, detail="El nombre no es válido")
    if not parsed_email or not email_pattern.fullmatch(parsed_email) or len(parsed_email) > 254:
        raise HTTPException(status_code=422, detail="El correo no es válido")
    if not message or len(message) < 10 or len(message) > 5000 or any(ord(char) < 9 for char in message):
        raise HTTPException(status_code=422, detail="El mensaje no es válido")
    if spam_pattern.search(message) or len(set(message)) < 5:
        raise HTTPException(status_code=422, detail="El mensaje no parece válido")

    # Punto de integración para correo, base de datos o un servicio externo.
    print(f"New contact from {name} <{email}>")
    return {"ok": True, "message": "Mensaje recibido correctamente"}
