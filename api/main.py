import os
from email.utils import parseaddr

from dotenv import load_dotenv
from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

origins = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:4321").split(",") if origin.strip()]
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
def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)) -> dict[str, object]:
    name = name.strip()
    email = email.strip()
    message = message.strip()
    parsed_email = parseaddr(email)[1]
    if not name or len(name) > 120:
        raise HTTPException(status_code=422, detail="El nombre no es válido")
    if not parsed_email or "@" not in parsed_email or len(parsed_email) > 254:
        raise HTTPException(status_code=422, detail="El correo no es válido")
    if not message or len(message) > 5000:
        raise HTTPException(status_code=422, detail="El mensaje no es válido")

    # Punto de integración para correo, base de datos o un servicio externo.
    print(f"New contact from {name} <{email}>: {message}")
    return {"ok": True, "message": "Mensaje recibido correctamente"}
