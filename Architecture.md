## Architectural Diagram

```mermaid
graph TD
    subgraph Edge ["Raspberry Pi (Edge Device)"]
        Camera["Webcam / Pi Camera"]
        PiService["Edge Service (pi_service.py)"]
        DBLogger["DB Logger Thread"]
        StreamServer["MJPEG Streamer (Port 8080)"]

        Camera --> PiService
        PiService --> DBLogger
        PiService --> StreamServer
    end

    subgraph CloudServices ["Cloud Infrastructure"]
        Storage["Cloudflare R2 Storage"]
        Supabase[("Supabase DB")]
    end

    subgraph Server ["Central Flask Server"]
        FlaskServer["Flask App (src/routes_server.py)"]
    end

    subgraph Client ["Web Client"]
        Browser["User Browser"]
    end

    DBLogger -->|1. Upload snapshot| Storage
    DBLogger -->|2. Insert detection metadata| Supabase
    StreamServer -->|3. Serve MJPEG frames when requested| FlaskServer
    FlaskServer -->|5. Streams frames| Browser
    FlaskServer -->|6. Queries logs| Supabase
    FlaskServer -->|6. Queries images| Storage
```