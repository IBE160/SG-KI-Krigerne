# SG-KI-Krigerne
Repository for SG-KI-Krigerne - IBE160 Programmering med KI.
Instrukser for å starte og for å bruke appen:

**HiMolde Study Friend**
En liten web-basert chatbot som hjelper himolde studenter om å finne informasjon rundt emner. Denne informasjonen finner chatbotten via en kunnskapsbase som består av alle emner som undervises på engelsk i følgende semester høst 2025 og vår 2026

På maskinen din trenger du: 
Python 3.10+
Node.js 18+
Og det anbefales sterkt å bruke en gemini api key (kan fåes og brukes gratis)
    Funker uten, men svarene er mer begrenset

**Starte backend**
1. Åpne terminalen og gå til backend mappen (Vi har brukt powershell)
    - cd sg-ki-krigerne\backend
2. Lag og aktiver et virituelt miljø
    - python -m venv .venv
    - .venv\Scripts\activate
3. Installere python dependencies
    - pip install -r requirements.txt
4. Konfigurere en Gemini API key (må ikke gjøres, men anbefales)
    - pip install google-generativeai
    - pip install google-genai
    - $env:GEMINI_API_KEY = "Sett inn api key her"
5. Kjør FastAPI appen med uvicorn
    - cd sg-ki-krigerne
    - uvicorn backend.main:app --reload


**Starte Frontend**
1. Åpne en ny terminal og gå til himolde-study-friend mappen
    - cd sg-ki-krigerne\himolde-study-friend
2. Installer Node Dependencies
    - npm install
3. Start Serveren
    - npm run dev
4. Vite printer en url (localhost:5000 eller lignende)
    - Åpne URLen i browser


**Bruk av appen**
Quick prompts i toppen funker til kjappe spørsmål

Ellers kan man stille direkte spørsmål, som for eksempel:
    - What is the exam format for IBE320?
    - How many mandatory assignments for IDR210?

Spørsmål bør stilles på engelsk, hvis man har api key kan man spørre på norsk også, gemini modellen oversetter automatisk. 

Prosjektet bruker gemini modellen: gemini-2.5-flash-lite
Hvis du har free tier med gemini er det inkludert 10 Requests Per Minute, 250 000 Tokens Per minute og 20 Requests Per Day

