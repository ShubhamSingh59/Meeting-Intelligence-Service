# Testing Strategy

This document outlines the testing approach used to validate the Meeting Intelligence API, ensuring functional correctness, security, and edge-case handling.

---

## 1. Automated Unit Testing (pytest)
A suite of automated tests was implemented using `pytest` and FastAPI's `TestClient` to verify core API behavior without requiring a live database connection.

**Test Scenarios Executed:**
* `test_health_check`: Verified the `/health` endpoint returns a `200 OK` and correctly formats the JSON response to indicate database connectivity.
* `test_evaluation_endpoint`: Verified the `/api/evaluation` route correctly returns the candidate details and feature array.
* `test_login_success`: Verified that submitting valid credentials to `/api/auth/login` successfully generates and returns a valid JWT Bearer token.
* `test_login_failure`: Verified that submitting invalid credentials correctly triggers the global error handler and returns a `400 Bad Request`.
* `test_protected_route_without_token`: Verified that attempting to hit the `POST /api/meetings` endpoint without a JWT token is successfully blocked, returning a `401 Unauthorized` error.

---

## 2. Edge Cases Considered & Handled
* **Malformed JSON / Missing Fields:** If a user submits a meeting creation request missing the required `title` or `meetingDate`, FastAPI's Pydantic validation intercepts the request before it hits the database. The global error handler shapes this into the required unified `VALIDATION_ERROR` response format.
* **Empty Transcripts:** If a user requests AI analysis on a meeting that has no transcript data, the API gracefully catches the empty array and returns a `BAD_REQUEST` rather than crashing the LLM prompt chain.
* **Missing Webhook URLs:** If the environment variable for the Discord webhook is missing, the `apscheduler` checks for this before attempting to post, safely logging a skipped execution rather than crashing the background thread.

---

## 3. Limitations Discovered
* **Scheduler Execution in Serverless Environments:** The background `apscheduler` task relies on the FastAPI event loop staying alive. If this API is deployed to a strictly serverless environment (like Vercel) where the container sleeps between requests, the webhook reminder chron job will not trigger reliably. To mitigate this limitation, deployment on a containerized, always-on platform (like Render or Railway) is strongly recommended.