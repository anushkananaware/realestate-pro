RealEstate Pro - Fullstack Project (Django + React)

Structure:
- backend/: Django REST backend (api endpoints: /api/analyze/, /api/compare/, /api/upload/, /api/download/)
- frontend/: React app (chat-style UI, upload dataset, charts, download)

Quick start (Backend):
1. cd backend
2. python -m venv venv
3. source venv/bin/activate   # Windows: venv\Scripts\activate
4. pip install -r requirements.txt
5. python manage.py migrate
6. python manage.py runserver

Quick start (Frontend):
1. cd frontend
2. npm install
3. npm start

Open http://localhost:3000

Optional OpenAI integration:
- Set environment variable OPENAI_API_KEY in backend environment.
- The backend will call OpenAI for more natural summaries if key is provided.
- Model used in sample code is 'gpt-4o-mini' as placeholder. Replace with preferred model.

Deployment tips:
- Use Render/Heroku for backend (add gunicorn to requirements).
- Use Vercel/Netlify for frontend; set REACT_APP_API_BASE env var to backend URL.

