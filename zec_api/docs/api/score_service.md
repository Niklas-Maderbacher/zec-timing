# Scores Service

Manage scores and penalties also view leaderboards.

## Table of Contents

### Scores
- [Create Score](#create-score)
- [Update Score](#update-score)
- [Delete Score](#delete-score)
- [Delete Scores for Attempt](#delete-scores-for-attempt)
- [Get Score](#get-score)
- [Get Scores (all)](#get-scores-all)
- [Get Leaderboard](#get-leaderboard)

### Penalties
- [Create Penalty](#create-penalty)
- [Update Penalty](#update-penalty)
- [Delete Penalty](#delete-penalty)
- [Delete Penalties for Attempt](#delete-penalties-for-attempt)
- [Get Penalty](#get-penalty)
- [Get Penalties (all)](#get-penalties-all)
- [Get Penalties for Attempt](#get-penalties-for-attempt)
- [Get Penalty Types](#get-penalty-types)

## Response Schema
Response schema for score endpoints. Get endpoints return objects in this format.
```json
{
  "id": 1,
  "attempt_id": 42,
  "challenge_id": 1,
  "value": 92.0,
  "created_at": "2024-02-14T15:30:00.000000"
}
```

## Create Score
Creates a score entry for an attempt. The score value is calculated automatically based on the attempt data.

**Authorization:** Admin role required  
**Method:** `POST`  
**URL:** `http://hostname/scores/`

### Request Body
```json
{
  "attempt_id": 42
}
```

### Responses
- `200 OK`: Score created successfully
- `400 Bad Request`: Invalid attempt_id or attempt doesn't exist
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt not found
- `422 Unprocessable Entity`: Validation error

## Update Score
Manually updates a score value.

**Authorization:** Admin role required  
**Method:** `PUT`  
**URL:** `http://hostname/scores/{score_id}`

### Path Parameters
- `score_id` (int): ID of the score to update

### Request Body
```json
{
  "value": 92.0
}
```

### Responses
- `200 OK`: Score updated successfully
- `400 Bad Request`: Invalid value
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Score not found
- `422 Unprocessable Entity`: Validation error

## Delete Score
Deletes a score entry.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/scores/{score_id}`

### Path Parameters
- `score_id` (int): ID of the score to delete

### Responses
- `200 OK`: Score deleted successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Score not found

## Delete Scores for Attempt
Deletes all scores associated with a specific attempt.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/scores/attempt/{attempt_id}`

### Path Parameters
- `attempt_id` (int): ID of the attempt whose scores should be deleted

### Responses
- `200 OK`: Scores deleted successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt not found

## Get Score
Retrieves a single score by ID.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/scores/{score_id}`

### Path Parameters
- `score_id` (int): ID of the score

### Responses
- `200 OK`: Score retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Score not found

## Get Scores (all)
Retrieves all scores in the system.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/scores/`

### Responses
- `200 OK`: Scores retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

## Get Leaderboard
Retrieves the leaderboard for a specific challenge and category, showing teams ranked by their best scores.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/leaderboard/{challenge_id}/category/{category}`

### Path Parameters
- `challenge_id` (int): ID of the challenge
- `category` (string): Team category to filter by
  - `close_to_series`
  - `advanced_class`
  - `professional_class`

### Example Request
```bash
curl -X GET "http://hostname/leaderboard/1/category/advanced_class" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Responses
- `200 OK`: Leaderboard retrieved successfully
- `400 Bad Request`: Invalid category value
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Challenge not found

### Notes
- The leaderboard shows only the best score for each team in the specified category
- Teams without any valid attempts won't appear in the leaderboard
- Scores are calculated based on time, energy efficiency, and penalties

# Penalties Service

Manage penalties applied to attempts.

## Penalty Response Schema
Response schema for penalty endpoints.
```json
{
  "id": 1,
  "attempt_id": 42,
  "count": 2,
  "penalty_type_id": 1,
  "created_at": "2024-02-14T15:45:00.000000"
}
```


## Create Penalty
Creates a penalty for an attempt.

**Authorization:** Admin role required  
**Method:** `POST`  
**URL:** `http://hostname/penalties/`

### Request Body
```json
{
  "attempt_id": 42,
  "count": 2,
  "penalty_type_id": 1
}
```

### Responses
- `200 OK`: Penalty created successfully
- `400 Bad Request`: Invalid field values
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt or penalty type not found
- `422 Unprocessable Entity`: Validation error

## Update Penalty
Updates an existing penalty. Only provided fields will be updated.

**Authorization:** Team Lead or Admin role required  
**Method:** `PUT`  
**URL:** `http://hostname/penalties/{penalty_id}`

### Path Parameters
- `penalty_id` (int): ID of the penalty to update

### Request Body
All fields are optional - only include fields you want to update.
```json
{
  "count": 3,
  "penalty_type_id": 2
}
```

### Responses
- `200 OK`: Penalty updated successfully
- `400 Bad Request`: Invalid field values
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Penalty, attempt, or penalty type not found
- `422 Unprocessable Entity`: Validation error

## Delete Penalty
Deletes a penalty entry.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/penalties/{penalty_id}`

### Path Parameters
- `penalty_id` (int): ID of the penalty to delete

### Responses
- `200 OK`: Penalty deleted successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Penalty not found

## Delete Penalties for Attempt
Deletes all penalties associated with a specific attempt.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/penalties/attempt/{attempt_id}`

### Path Parameters
- `attempt_id` (int): ID of the attempt whose penalties should be deleted

### Responses
- `200 OK`: Penalties deleted successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt not found

## Get Penalty
Retrieves a single penalty by ID.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/penalties/{penalty_id}`

### Path Parameters
- `penalty_id` (int): ID of the penalty

### Responses
- `200 OK`: Penalty retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Penalty not found

## Get Penalties (all)
Retrieves all penalties in the system.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/penalties/`

### Responses
- `200 OK`: Penalties retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

## Get Penalties for Attempt
Retrieves all penalties associated with a specific attempt.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/penalties/attempt/{attempt_id}`

### Path Parameters
- `attempt_id` (int): ID of the attempt

### Responses
- `200 OK`: Penalties retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Attempt not found

## Get Penalty Types
Retrieves all available penalty types and their associated time/score penalties.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/penalties/types/`

### Responses
- `200 OK`: Penalty types retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

### Notes
- Penalty types are predefined in the system and cannot be created or modified via API
- The `amount` field represents either time added (in seconds) or points deducted, depending on scoring rules
- Multiple penalties can be applied to a single attempt
- Total penalty impact is calculated as: `count × amount` for each penalty