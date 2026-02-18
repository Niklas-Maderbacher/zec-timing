# Attempts Service

Manage race attempts and retrieve performance data.

## Table of Contents
- [Create Attempt](#create-attempt)
- [Update Attempt](#update-attempt)
- [Delete Attempt](#delete-attempt)
- [Get Attempt](#get-attempt)
- [Get Attempts (all)](#get-attempts-all)
- [Get Attempts per Challenge](#get-attempts-per-challenge)
- [Get Attempts per Challenge (valid)](#get-attempts-per-challenge-valid)
- [Get Fastest Attempt for a Challenge](#get-fastest-attempt-for-a-challenge)
- [Get Fastest Attempt for a Team in a Challenge](#get-fastest-attempt-for-a-team-in-a-challenge)
- [Get Least Energy Attempt for a Challenge](#get-least-energy-attempt-for-a-challenge)
- [Get Least Energy Attempt for a Team in a Challenge](#get-least-energy-attempt-for-a-team-in-a-challenge)
- [Get Attempts per Team](#get-attempts-per-team)
- [Get Attempts per Driver](#get-attempts-per-driver)

## Response Schema
Response schema for all get endpoints
Get all endpoints return a list of objects of this
```json
{
  "id": 42,
  "team_id": 1,
  "driver_id": 1,
  "challenge_id": 1,
  "is_valid": true,
  "start_time": "2024-02-14T14:30:45.123456",
  "end_time": "2024-02-14T14:35:20.654321",
  "energy_used": 15.75,
  "created_at": "2024-02-14T14:35:21.000000"
}
```

## Create Attempt
Creates a new attempt for a team/driver in a challenge.

**Authorization:** Admin role required  
**Method:** `POST`  
**URL:** `http://hostname/attempts/`

### Request Body
Penalty-related fields are optional. If provided, a corresponding penalty record will be created.  
Additionally, a score entry is automatically generated upon attempt creation.
```json
{
  "team_id": 1,
  "driver_id": 1,
  "challenge_id": 1,
  "is_valid": true,
  "start_time": "2024-02-14T14:30:45.123456",
  "end_time": "2024-02-14T14:35:20.654321",
  "energy_used": 15.75,
  "penalty_count": 0,
  "penalty_type": null
}
```

### Responses
- `200 OK`: Attempt created
- `400 Bad Request`: Invalid datetime format or missing required fields
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `422 Unprocessable Entity`: Validation error

## Update Attempt
Updates an existing attempt. Only provided fields will be updated.

**Authorization:** Admin role required  
**Method:** `PUT`  
**URL:** `http://hostname/attempts/{attempt_id}`

### Path Parameters
- `attempt_id` (int): ID of the attempt to update

### Request Body
All fields are optional - only include fields you want to update.
```json
{
  "team_id": 2,
  "driver_id": 3,
  "is_valid": false,
  "energy_used": 16.25
}
```

### Responses
- `200 OK`: Attempt updated
- `400 Bad Request`: Invalid datetime format
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt not found
- `422 Unprocessable Entity`: Validation error

## Delete Attempt
Deletes an attempt and all associated data.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/attempts/{attempt_id}`

### Path Parameters
- `attempt_id` (int): ID of the attempt to delete

### Responses
- `200 OK`: Attempt succesfully deleted
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt not found

## Get Attempt
Gets a single attempt by ID.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/{attempt_id}`

### Path Parameters
- `attempt_id` (int): ID of the attempt to get

### Responses
- `200 OK`: Attempt returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt not found

## Get Attempts (all)
Gets all attempts in the system.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/`

### Responses
- `200 OK`: List of attempts returned
- `200 OK (empty)`: No attempts found
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

## Get Attempts per Challenge
Gets all attempts for a specific challenge.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/challenges/{challenge_id}`

### Path Parameters
- `challenge_id` (int): ID of the challenge

### Responses
- `200 OK`: List of attempts returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Challenge not found

## Get Attempts per Challenge (valid)
Gets only valid attempts for a specific challenge.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/challenges/valid/{challenge_id}`

### Path Parameters
- `challenge_id` (int): ID of the challenge

### Responses
- `200 OK`: List of attempts returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Challenge not found

## Get Fastest Attempt for a Challenge
Gets the attempt with the shortest time for a challenge.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/fastest/{challenge_id}`

### Path Parameters
- `challenge_id` (int): ID of the challenge

### Responses
- `200 OK`: Attempt returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Challenge not found or no attempts exist

## Get Fastest Attempt for a Team in a Challenge
Gets the fastest attempt for a specific team in a challenge.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/fastest/per-team/?challenge_id={challenge_id}&team_id={team_id}`

### Query Parameters
- `challenge_id` (int): ID of the challenge
- `team_id` (int): ID of the team

### Responses
- `200 OK`: Attempt returned
- `400 Bad Request`: Missing required query parameters
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: No matching attempt found

## Get Least Energy Attempt for a Challenge
Gets the attempt with the lowest energy consumption for a challenge.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/least-energy/{challenge_id}`

### Path Parameters
- `challenge_id` (int): ID of the challenge

### Responses
- `200 OK`: Attempt returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Challenge not found or no attempts exist

## Get Least Energy Attempt for a Team in a Challenge
Gets the most energy-efficient attempt for a specific team in a challenge.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/least-energy/per-team/?challenge_id={challenge_id}&team_id={team_id}`

### Query Parameters
- `challenge_id` (int): ID of the challenge
- `team_id` (int): ID of the team

### Responses
- `200 OK`: Attempt returned
- `400 Bad Request`: Missing required query parameters
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: No matching attempt found

## 1.12 Get Attempts per Team
Gets all attempts made by a specific team.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/per-team/{team_id}`

### Path Parameters
- `team_id` (int): ID of the team

### Responses
- `200 OK`: List of attempts returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Team not found

## 1.13 Get Attempts per Driver
Gets all attempts made by a specific driver.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/attempts/per-driver/{driver_id}`

### Path Parameters
- `driver_id` (int): ID of the driver

### Responses
- `200 OK`: List of attempts returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Driver not found