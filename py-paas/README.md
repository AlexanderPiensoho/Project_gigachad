# Py-PaaS - Er Egen Mini-Heroku/Netlify 🚀

En webbportal byggd med Flask som låter er driftsätta små webbprojekt direkt från GitHub - precis som Heroku eller Netlify, fast er egen!

![Py-PaaS](../assets/project_gigachad.jpg)

## 🎯 Vad är Py-PaaS?

Py-PaaS är en Platform-as-a-Service (PaaS) som ni kan använda för att:
- Driftsätta Flask-appar från GitHub med ett knapptryck
- Automatiskt bygga Docker-containers
- Hantera flera appar samtidigt
- Stoppa, starta om och ta bort deployade appar via ett snyggt webb-UI

## ✨ Funktioner

- **Dashboard** - Se alla deployade appar på ett ställe
- **Deploy från GitHub** - Klistra in en GitHub-länk och driftsätt direkt
- **Docker-integration** - Automatisk byggning och körning av containers
- **App-hantering** - Stoppa, starta om eller ta bort appar
- **SQLite-databas** - Håller koll på alla deployade appar
- **Snyggt UI** - Bootstrap-baserat gränssnitt

## 🛠️ Teknisk Stack

- **Backend:** Python, Flask
- **Databas:** SQLite
- **Container:** Docker
- **Frontend:** HTML, Bootstrap 5, Bootstrap Icons
- **Version Control:** Git

## 📋 Förutsättningar

Innan ni börjar, se till att ni har följande installerat:

- Python 3.8+ ([Ladda ner här](https://www.python.org/downloads/))
- Docker (se installationsinstruktioner nedan)
- Git ([Ladda ner här](https://git-scm.com/downloads))

### 🐳 Installera Docker

**För Linux (Ubuntu/Linux Mint/Debian):**

Docker Desktop behövs inte på Linux - installera Docker Engine istället:

```bash
# Update package index
sudo apt update

# Install prerequisites
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

# Add Docker's official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Add Docker repository (for Linux Mint, use Ubuntu base)
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu jammy stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Update package index again
sudo apt update

# Install Docker Engine
sudo apt install -y docker-ce docker-ce-cli containerd.io

# Add your user to the docker group (so you don't need sudo)
sudo usermod -aG docker $USER

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Apply group changes (or log out and back in)
newgrp docker

# Verify installation
docker --version
docker run hello-world
```

**För Windows/Mac:**

Ladda ner och installera Docker Desktop från [docker.com](https://www.docker.com/products/docker-desktop/)

## 🚀 Snabbstart

### 1. Klona projektet

```bash
cd py-paas
```

### 2. Skapa och aktivera en virtuell miljö

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Installera dependencies

```bash
pip install -r requirements.txt
```

### 4. Starta Docker

**Linux:**
Docker Engine körs som en systemtjänst och startar automatiskt. Verifiera att den körs:
```bash
sudo systemctl status docker
```

**Windows/Mac:**
Se till att Docker Desktop körs på er dator innan ni startar appen.

### 5. Kör appen

```bash
python app.py
```

Öppna sedan webbläsaren och gå till: **http://localhost:5000**

## 📖 Hur fungerar det?

### Deployment-processen:

1. **Klistra in GitHub-länk** - Ange URL:en till ett repo med en Dockerfile
2. **Kloning** - Repot klonas till servern
3. **Byggning** - Docker bygger en image från Dockerfile
4. **Körning** - En container startas på en ledig port (8001-8100)
5. **Live!** - Din app är nu tillgänglig via `http://localhost:[port]`

### Krav för era appar:

För att en app ska kunna driftsättas måste den:
- Vara ett publikt GitHub-repo (eller ha access)
- Innehålla en `Dockerfile`
- Köra på port 5000 (standard för Flask-appar)

## 📁 Projektstruktur

```
py-paas/
├── app.py                 # Huvudapplikationen (Flask-routes)
├── database.py            # Databashantering (SQLite)
├── docker_manager.py      # Docker-operationer (build, run, stop)
├── requirements.txt       # Python-dependencies
├── templates/             # HTML-templates
│   ├── dashboard.html     # Dashboard-sida
│   └── deploy.html        # Deploy-formulär
├── static/                # CSS, JS, bilder (framtida)
├── app-deploys/           # Klonade repos sparas här
└── py-paas.db            # SQLite-databas (skapas automatiskt)
```

## 🎨 Användargränssnitt

### Dashboard
- Lista över alla deployade appar
- Status för varje app (Körs, Stoppad, Fel)
- Direktlänkar till era live-appar
- Knappar för att hantera appar

### Deploy-sida
- Enkelt formulär för GitHub URL
- Tydliga instruktioner
- Validering av input

## 🔧 API Endpoints

| Route | Metod | Beskrivning |
|-------|-------|-------------|
| `/` | GET | Dashboard - visa alla appar |
| `/deploy` | GET/POST | Formulär för att driftsätta ny app |
| `/stop/<app_id>` | GET | Stoppa en körande app |
| `/restart/<app_id>` | GET | Starta om en app |
| `/delete/<app_id>` | GET | Ta bort en app helt |

## 💾 Databasschema

**Tabell: `deployed_apps`**

| Kolumn | Typ | Beskrivning |
|--------|-----|-------------|
| id | INTEGER | Primary key |
| app_name | TEXT | Namnet på appen |
| github_url | TEXT | GitHub-repo URL |
| status | TEXT | Status (Körs, Stoppad, etc.) |
| port | INTEGER | Port som appen körs på |
| container_id | TEXT | Docker container ID |
| created_at | TIMESTAMP | När appen deployades |

## 🧪 Testa med en exempelapp

Vill ni testa Py-PaaS? Skapa en enkel Flask-app med Dockerfile:

**app.py:**
```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return '<h1>Hello from Py-PaaS!</h1>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Dockerfile:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install flask
EXPOSE 5000
CMD ["python", "app.py"]
```

Pusha till GitHub och driftsätt via Py-PaaS!

## 🐛 Felsökning

### Docker-fel
- **Linux:** Se till att Docker Engine körs: `sudo systemctl status docker`
- **Windows/Mac:** Se till att Docker Desktop körs
- Kontrollera att ni har rättigheter att köra Docker-kommandon
- **Linux:** Om du får "permission denied", se till att du är med i docker-gruppen: `groups` (ska visa "docker")

### Port redan upptagen
- Py-PaaS använder portar 8001-8100
- Om en port är upptagen, väljs nästa lediga automatiskt

### Git clone-fel
- Kontrollera att GitHub-URL:en är korrekt
- För privata repos, behöver ni konfigurera SSH-nycklar

## 🔮 Framtida förbättringar

- [ ] Stöd för privata GitHub-repos (SSH)
- [ ] Loggvisning för varje app
- [ ] Miljövariabler för appar
- [ ] Multi-port support (inte bara port 5000)
- [ ] Auto-redeploy vid GitHub push (webhooks)
- [ ] HTTPS-stöd med SSL-certifikat
- [ ] Användarautentisering
- [ ] Resource limits (CPU, minne)

## 👥 Team

**Project Gigachad:**
- Alexander
- Anton  
- Vincent

## 📄 Licens

© Project_gigachad Alexander, Anton & Vincent.

Se [LICENSE](../LICENSE) för mer information.

## 🙏 Tack till

- Flask community
- Docker community
- Bootstrap för det snygga UI-ramverket

---

**Lycka till med er Py-PaaS! 🚀**
