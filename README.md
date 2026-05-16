# Synaply AI

## Overview
Synaply AI is an AI-powered study platform that allows users to upload study documents and generate intelligent learning resources automatically.

---

## Tech Stack

### Frontend
- React
- TypeScript
- Vite
- TailwindCSS
- React Router
- Axios
- WebSockets

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Ollama
- JWT Authentication

---

## Main Features

### Authentication
- User registration
- User login
- Protected routes with JWT

### Documents
- Upload PDF files
- Extract text from PDFs
- Store documents in database
- Chunk document content for AI processing

### AI Features
- AI-generated summaries
- AI-generated flashcards
- AI-generated quizzes
- AI-powered document chat
- Streaming responses with WebSockets

### Dashboard
- Dynamic analytics
- Real activity tracking
- Quiz and flashcard statistics
- Activity chart

### Quiz System
- Generate quizzes from uploaded documents
- Multiple choice questions
- Quiz scoring system
- Quiz library

---

## AI Models
Currently using:
- Ollama
- phi3

Future improvement:
- OpenAI API integration

---

## Project Architecture

### Frontend Structure
- Pages
- Components
- Services
- Hooks
- Types
- Layouts

### Backend Structure
- API routes
- Services
- Database models
- Authentication
- WebSocket manager

---

## Current Status
MVP Completed ✅

The platform is fully functional and supports:
- PDF processing
- AI study tools
- Real-time AI chat
- Quiz generation
- Flashcard generation
- Dashboard analytics

---

## Possible Future Improvements
- PostgreSQL migration
- OpenAI integration
- File deletion
- User settings
- Better AI models
- Cloud deployment
- Mobile responsive improvements
- RAG optimization

---

## Deployment Plan
- Frontend: Vercel
- Backend: Railway
- Database: PostgreSQL
- AI Provider: OpenAI API