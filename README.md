# Meeting Intelligence Service - Backend

A robust, AI-powered backend service designed to process transcripts, extract grounded insights, and automate overdue action item reminders. Built for the Hintro Backend Engineering Assignment.

## Core Features
- **AI-Powered Analysis:** Integrates LangChain/LLMs to extract summaries and decisions.
- **Strict Grounding:** Every AI-generated insight includes exact timestamp citations from the original transcript.
- **Automated Scheduler:** A background `apscheduler` chron job automatically detects overdue tasks and fires real-time alerts.
- **Third-Party Integration:** Live Discord Webhook integration for task reminders.
- **Security:** Fully protected API endpoints using JWT (JSON Web Tokens) authentication.
- **Production-Ready:** Includes a global error handler, structured trace ID logging, CORS middleware, and a `/health` endpoint.

---

##  Getting Started

### Prerequisites
- Python 3.10+
- MySQL database instance

### 1. Local Setup
Clone the repository and install the dependencies in a virtual environment:
\`\`\`bash
git clone <your-repo-url>
cd backend
python -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
pip install -r requirements.txt
\`\`\`

### 2. Environment Variables
Create a `.env` file in the root directory and configure the following:
\`\`\`env
# Security
SECRET_KEY=hintro-super-secret-key
ALGORITHM=HS256

# External Integrations
WEBHOOK_URL=https://discord.com/api/webhooks/... # Your Discord Webhook URL

# Database (Update with your credentials if using MySQL locally)
# DATABASE_URL=mysql+pymysql://user:password@localhost/hintro_db
\`\`\`

### 3. Run the Server
Start the FastAPI server locally:
\`\`\`bash
uvicorn main:app --reload
\`\`\`
*The Swagger API documentation will be available at: `http://127.0.0.1:8000/docs`*

---

## Deployment Instructions

This application is configured for easy deployment on **Render**.
1. Create a new "Web Service" on [Render.com](https://render.com).
2. Connect this GitHub repository.
3. Set the Build Command to: `pip install -r requirements.txt`
4. Set the Start Command to: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Add your `.env` variables in the Render dashboard.

---

## API Usage Examples

Because the API is secured with JWT Authentication, you must retrieve a token before creating or analyzing meetings.

### 1. Authenticate (Login)
\`\`\`bash
curl -X POST "http://127.0.0.1:8000/api/auth/login" \
     -d "username=singhshubham&password=singh123"
\`\`\`
*Response:* Returns an `access_token`.

### 2. Create a Meeting
Include the token in the Authorization header to access protected routes:
\`\`\`bash
curl -X POST "http://127.0.0.1:8000/api/meetings" \
     -H "Authorization: Bearer <YOUR_ACCESS_TOKEN>" \
     -H "Content-Type: application/json" \
     -d '{
           "title": "Sprint Planning",
           "participants": ["alice@example.com"],
           "meetingDate": "2026-05-20T10:00:00Z",
           "transcript": [{"timestamp": "00:10", "speaker": "John", "text": "Launch Friday."}]
         }'
\`\`\`

---

## Project Structure
* `main.py` - Application entry point, global error handlers, and scheduler.
* `core/` - Security settings, config, and JWT logic.
* `routers/` - API route definitions (auth, meetings, action_items).
* `models/` - SQLAlchemy database schemas and Pydantic validation models.
* `services/` - AI analysis logic and Webhook notification services.

## Author

**Shubham Singh**
* **Email:** shubhams@alumni.iitgn.ac.in
* **GitHub:** [@ShubhamSingh59](https://github.com/ShubhamSingh59)
* **LinkedIn:** [@shubham-singh-96809b239](https://www.linkedin.com/in/shubham-singh-96809b239/)
