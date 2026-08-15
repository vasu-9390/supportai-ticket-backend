🤖 SupportAI Desk — Django Backend

AI-powered customer support ticket management backend built with Python, Django, Django REST Framework, JWT Authentication, PostgreSQL, and Google Gemini AI.

The backend provides secure REST APIs for authentication, ticket management, AI ticket analysis, agent assignment, duplicate detection, AI-generated responses, comments, and support insights.

🚀 Features
🔐 Authentication
User registration
User login
JWT access and refresh tokens
Protected REST APIs
Authentication-based API access
User roles for support agents and administrators
🎫 Ticket Management
Create support tickets
View all tickets
View individual tickets
Update tickets
Delete tickets
Search tickets
Filter tickets by:
Status
Priority
Category
Assigned agent
Ticket comments and conversation history
🤖 AI Ticket Analysis

Google Gemini AI analyzes incoming tickets and identifies:

Ticket category
Priority
Customer sentiment
Sentiment score
Required support skills
AI confidence score
Suggested customer response

Example:

Customer Issue
      ↓
Gemini AI
      ↓
Category → PAYMENT
Priority → HIGH
Sentiment → NEGATIVE
Skills → Payment Support
      ↓
Recommended Agent
👨‍💻 Intelligent Agent Assignment

The system matches tickets with suitable support agents based on:

Required skills
Agent availability
Agent workload
Technical expertise
✨ AI Suggested Responses

The backend generates professional responses for customer support tickets.

Agents can use the generated response as a starting point before sending it to customers.

🔍 Duplicate Ticket Detection

The AI engine can identify potentially duplicate tickets based on:

Subject
Description
Existing ticket information
📊 AI Insights

Provides support analytics including:

Classification accuracy
Agent assignment accuracy
Suggested response statistics
Duplicate ticket detection
Support trend insights
AI recommendations
🛠️ Tech Stack
Technology	Purpose
Python	Backend programming
Django	Web framework
Django REST Framework	REST APIs
Simple JWT	Authentication
PostgreSQL	Database
Google Gemini AI	AI analysis
Django Filters	Filtering
Axios	Frontend API communication
CORS	Frontend-backend communication
📁 Project Structure
backend/
│
├── manage.py
│
├── backend/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── users/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── tickets/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── customers/
│   ├── models.py
│   └── ...
│
├── agents/
│   ├── models.py
│   └── ...
│
├── ai_engine/
│   ├── views.py
│   ├── urls.py
│   │
│   └── services/
│       ├── gemini_service.py
│       ├── ticket_analyzer.py
│       ├── response_generator.py
│       ├── agent_matcher.py
│       └── duplicate_detector.py
│
├── requirements.txt
├── .env
└── README.md
🔗 API Endpoints
Authentication
POST /api/auth/register/
POST /api/auth/login/
POST /api/auth/refresh/
Login
POST /api/auth/login/

Example:

{
  "email": "user@example.com",
  "password": "your_password"
}
🎫 Ticket APIs
Get Tickets
GET /api/tickets/
Get Single Ticket
GET /api/tickets/{ticket_id}/
Create Ticket
POST /api/tickets/

Example:

{
  "customerName": "John Smith",
  "customerEmail": "john@example.com",
  "subject": "Payment failed",
  "description": "My payment failed but the amount was deducted from my account.",
  "category": "Auto Detect",
  "priority": "Auto Detect"
}
Update Ticket
PATCH /api/tickets/{ticket_id}/
Delete Ticket
DELETE /api/tickets/{ticket_id}/
Ticket Comments
GET /api/tickets/{ticket_id}/comments/
POST /api/tickets/{ticket_id}/comments/
🤖 AI APIs
Analyze Ticket
POST /api/ai/analyze-ticket/

Example:

{
  "subject": "Payment failed",
  "description": "I tried to make a payment three times but every attempt failed."
}

Example response:

{
  "category": "PAYMENT",
  "priority": "HIGH",
  "sentiment": "NEGATIVE",
  "sentiment_score": -0.78,
  "confidence": 0.94,
  "required_skills": [
    "Payment Support",
    "Transaction Support",
    "Stripe API"
  ],
  "suggested_response": "Hello, we are sorry..."
}
AI Suggested Response
POST /api/ai/suggest-response/
AI Agent Assignment
POST /api/ai/assign-agent/
Duplicate Detection
POST /api/ai/check-duplicate/
AI Insights
GET /api/ai/insights/
🔐 JWT Authentication

Protected APIs require a JWT access token.

Send the token using:
