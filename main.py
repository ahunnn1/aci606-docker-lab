from pathlib import Path
import os
import socket
from fastapi import FastAPI

app = FastAPI(title="ACI606 Container Lab", version="1.0")
DATA_DIR = Path(os.getenv("DATA_DIR", "/data"))
DATA_DIR.mkdir(parents=True, exist_ok=True)
COUNTER_FILE = (DATA_DIR / "counter.txt")


def read_counter() -> int:
    if not COUNTER_FILE.exists():
        return 0
    try:
        return int(COUNTER_FILE.read_text().strip())
    except Exception:
        return 0

def write_counter(value: int) -> None:
    COUNTER_FILE.write_text(str(value))


@app.get("/")
def root():
    return {
        "service": "ACI606 Container Lab",
        "version": os.getenv("APP_VERSION", "v1"),
        "message": os.getenv("APP_MESSAGE", "Hello from a container"),
        "hostname": socket.gethostname(),
    }


@app.get("/health")
def health():
    return {"status": "ok", "hostname": socket.gethostname()}

@app.post("/visit")
def visit():
    value = read_counter() + 1
    write_counter(value)
    return {"visits": value, "hostname": socket.gethostname(),
            "data_dir": str(DATA_DIR)}


@app.get("/visit")
def get_visit():
    return {"visits": read_counter(), "hostname": socket.gethostname(),
            "data_dir": str(DATA_DIR)}
