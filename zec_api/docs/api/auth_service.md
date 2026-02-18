# Auth Service

Authentication and token management endpoints.

## Table of Contents
- [Login](#login)
- [Refresh Token](#refresh-token)

## Login
Authenticates a user and returns access and refresh tokens.

**Authorization:** None required  
**Method:** `POST`  
**URL:** `http://hostname/auth/login`  
**Content-Type:** `application/x-www-form-urlencoded`

### Form Parameters
- `username` (string): User's username
- `password` (string): User's password

### Response
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJxxx...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJyyy...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "token_type": "Bearer"
}
```
- `400 Bad Request`: Missing username or password
- `401 Unauthorized`: Invalid credentials

## Refresh Token
Obtains a new access token using a valid refresh token.

**Authorization:** None required  
**Method:** `POST`  
**URL:** `http://hostname/auth/refresh`  
**Content-Type:** `application/x-www-form-urlencoded`

### Form Parameters
- `refresh_token` (string): The refresh token from login response

### Response
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJxxx...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJyyy...",
  "expires_in": 300,
  "refresh_expires_in": 1800,
  "token_type": "Bearer"
}
```
- `400 Bad Request`: Missing refresh token
- `401 Unauthorized`: Invalid or expired refresh token
