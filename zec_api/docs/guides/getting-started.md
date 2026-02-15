# Getting Started with ZEC-API

## Prerequisites
- Docker

## Setup Instructions

### 1. Start the Application
```bash
docker-compose up --build
```
Add `-d` to run in detached mode.

### 2. Configure Keycloak

1. Navigate to your Keycloak admin console at http://localhost:8090
   - Default credentials: `admin` / `admin`
   - **Important:** Change these default credentials immediately after first login for security purposes
2. Create a new realm by importing the configuration file:
    - Location: `zec_api/config/keycloak/realm-export.json`
3. Regenerate client secrets:
    - Switch to your newly created **zec-realm**
    - Go to clients
    - Open the **login-client** configuration
    - Navigate to the **Credentials** tab and regenerate the secret
    - Copy the new secret
    - Repeat for **user-admin-client**
4. Update your environment variables with the new client secrets in your `.env` file or Docker environment configuration

### 3. Verify Installation
Once configured, the ZEC-API should be running and ready to accept requests.

---

## What is ZEC-API?

The ZEC-API is a RESTful API for managing racing challenges, teams, drivers, attempts, scores, and penalties.

## API Documentation

- [Attempt Service](../api/attempt_service.md) - Manage race attempts
- [Auth Service](../api/auth_service.md) - Login and token management
- [Challenge Service](../api/challenge_service.md) - Challenge configuration and retrieval
- [Score Service](../api/score_service.md) - Score & Penalty tracking and leaderboards
- [Team Service](../api/team_service.md) - Team and driver management
- [User Service](../api/user_service.md) - User accounts and role management
