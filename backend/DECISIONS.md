# Technical Decisions

This document outlines the core architectural and technical decisions made during the development of the Meeting Intelligence API, including the rationale, alternatives, and accepted trade-offs.

---

## 1. Database Choice: Relational (SQLAlchemy / MySQL)

* **Why it was chosen:** The data model for this application is inherently relational. A `Meeting` has a strict one-to-many relationship with `ActionItems`. Using a SQL database ensures data integrity, strict schemas, and ACID compliance, which is critical when tracking the exact status of overdue tasks. 
* **Alternatives considered:** MongoDB (NoSQL).
* **Trade-offs:** A NoSQL database would have allowed for slightly faster initial development, especially when dumping unstructured JSON transcripts. However, the trade-off was accepted because tracking relational state changes (like marking specific action items as COMPLETED) is much safer and more efficient with relational foreign keys.

---

## 2. Authentication Strategy: JWT (JSON Web Tokens)

* **Why it was chosen:** JWT is the industry standard for securing REST APIs. It is stateless, meaning the backend does not need to query a database or manage session memory to verify a user's identity on every single request. It integrates natively with FastAPI's `OAuth2PasswordBearer`, providing high security with minimal overhead.
* **Alternatives considered:** Session-Based Authentication (Cookies).
* **Trade-offs:** The main trade-off with JWTs is that they cannot be easily revoked before they expire unless you build a complex token-blacklist database. We accepted this trade-off by keeping the token expiration time short (1 hour), prioritizing API speed and scalability over immediate manual revocation.

---

## 3. External Integration: Discord Webhook API

* **Why it was chosen:** The assignment required a real third-party integration for the background scheduler to send overdue task reminders. Discord webhooks were chosen because they are lightweight, instantaneous, and extremely reliable for server-to-server alerts. It only requires a simple HTTP POST request without heavy SDKs.
* **Alternatives considered:** Slack API, SendGrid (Email).
* **Trade-offs:** Slack is more standard for corporate environments, but its API requires OAuth approval processes and complex bot setups. Email via SendGrid introduces formatting overhead and potential spam-filtering delays. Discord provided the fastest, most reliable proof-of-concept for real-time background task execution.

---

## 4. Project Structure: Modular Layered Architecture

* **Why it was chosen:** The codebase was structured into distinct domains (`routers/`, `models/`, `core/`, `services/`). This separation of concerns ensures that the AI logic (LangChain) doesn't tangle with the database logic (SQLAlchemy) or the API routing (FastAPI). 
* **Alternatives considered:** A monolithic structure (putting all code inside a single `main.py` file).
* **Trade-offs:** A modular structure requires slightly more boilerplate code and import management upfront compared to a single-file script. However, this trade-off was happily accepted because it makes the application infinitely more readable, testable, and scalable for future engineers.

---

## 5. Background Task Execution: APScheduler

* **Why it was chosen:** We needed a way to autonomously check the database for overdue tasks every minute. `apscheduler` was chosen because it runs concurrently within the FastAPI event loop without blocking standard API requests. 
* **Alternatives considered:** Celery + Redis, native `node-cron` (Node.js equivalent).
* **Trade-offs:** Celery is the enterprise standard for background tasks, but it requires spinning up a separate Redis message broker and a separate worker process. For a lightweight scheduling requirement, the infrastructure overhead of Celery was too high. `apscheduler` keeps the deployment simple (a single container) while still perfectly executing the webhook requirements.