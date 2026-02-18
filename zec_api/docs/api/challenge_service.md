# Challenges Service

Manage racing challenges and their configuration.

## Table of Contents
- [Seeded Data](#seeded-data)
- [Response Schema](#response-schema)
- [Update Challenge](#update-challenge)
- [Get Challenge by ID](#get-challenge-by-id)
- [Get Challenge by Name](#get-challenge-by-name)
- [Get Challenges (all)](#get-challenges-all)

## Seeded Data

The predefined challenges **Skidpad**, **Slalom**, **Acceleration**, and **Endurance** are seeded in the service.  
You can modify or extend these defaults in the following file:

`zec_api/services/challenge-service/app/database/seed.py`

## Response Schema
Response schema for all get endpoints
Get all endpoints return a list of objects of this
```json
{
  "id": 1,
  "name": "Speed Challenge 2024",
  "max_attempts": 5,
  "esp_mac_start1": "AA:BB:CC:DD:EE:01",
  "esp_mac_start2": "AA:BB:CC:DD:EE:02",
  "esp_mac_finish1": "AA:BB:CC:DD:EE:03",
  "esp_mac_finish2": "AA:BB:CC:DD:EE:04",
  "created_at": "2024-01-15T10:00:00.000000"
}
```

## Update Challenge
Updates an existing challenge. Only provided fields will be updated.

**Authorization:** Admin role required  
**Method:** `PUT`  
**URL:** `http://hostname/challenges/{challenge_id}`

### Path Parameters
- `challenge_id` (int): ID of the challenge to update

### Request Body
All fields are optional - only include fields you want to update.
```json
{
  "name": "Speed Challenge 2024",
  "max_attempts": 5,
  "esp_mac_start1": "AA:BB:CC:DD:EE:01",
  "esp_mac_start2": "AA:BB:CC:DD:EE:02",
  "esp_mac_finish1": "AA:BB:CC:DD:EE:03",
  "esp_mac_finish2": "AA:BB:CC:DD:EE:04"
}
```
### Responses
- `200 OK`: Successfully updated
- `404 Not Found`: Challenge not found
- `422 Unprocessable Entity`: Invalid request schema

## Get Challenge by ID
Retrieves a single challenge by its ID.

**Authorization:** None required  
**Method:** `GET`  
**URL:** `http://hostname/challenges/{challenge_id}`

### Path Parameters
- `challenge_id` (int): ID of the challenge

### Responses
- `200 OK`: Challenge returned
- `404 Not Found`: Challenge not found

## Get Challenge by Name
Retrieves a single challenge by its name.

**Authorization:** None required  
**Method:** `GET`  
**URL:** `http://hostname/challenges/name/{challenge_name}`

### Path Parameters
- `challenge_name` (string): Name of the challenge

### Responses
- `200 OK`: Challenge returned
- `404 Not Found`: Challenge not found

## Get Challenges (all)
Retrieves all challenges in the system.

**Authorization:** None required  
**Method:** `GET`  
**URL:** `http://hostname/challenges/`

### Responses
- `200 OK`: List of challenges returned
- `200 OK (empty)`: No challenges found
