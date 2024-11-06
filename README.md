# travel-assistant

# Steps to run code: - Jad, Ruben

- **Setup spaCy Language Model**: 
    - `python -m spacy download en_core_web_sm`

- **Setup Database**
    - **Install MongoDB**: https://www.mongodb.com/try/download/community
    - Create default connection. 

- **Setup Backend**
    - `cd backend`
    - **Create virtual environment**: `python -m venv venv`
    - **Activate virtual environment**: 
    - macOS/Linux: `source venv/bin/activate`
    - Windows: `venv\Scripts\activate`
    - **Install dependencies**: `pip install -r requirements.txt`    

- **Setting up Frontend**:
    - `cd frontend`
    - `npm install`

- **Running Backend**: 
    - `cd backend`
    - `uvicorn app.main:app --reload`

- **Running Frontend**:
    - `cd frontend`
    - `npm start`
