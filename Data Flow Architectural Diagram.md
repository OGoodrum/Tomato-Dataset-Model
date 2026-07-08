## How the Data Flows (Pi ➡️ Cloud ➡️ Website)

```mermaid
graph TD
    subgraph Edge ["Raspberry Pi"]
        Camera[Webcam] --> Inference["YOLO Detection"]
        LocalStorage[("Local SSD/SD")]
        Inference -->|Save image locally| LocalStorage
    end

    subgraph CloudServices ["Cloud Infrastructure"]
        CloudStorage["Cloudflare R2 Storage"]
        CloudBackend["Cloudflare Tunnel"]
        DB[("Supabase DB")]
    end

    subgraph User ["Web Browser"]
        Website["Netlify Frontend"]
    end

    %% Cross-subgraph connections
    Inference -->|Upload image file| CloudStorage
    Inference -->|Expose Live Video| CloudBackend
    Website -->|Fetch charts & logs| DB
    Website -->|Request historical image| CloudStorage
    CloudBackend -->|Retrieve Live Video| Website
```