# Team Service

Manage racing teams and their drivers.

## Table of Contents

### Teams
- [Create Team](#create-team)
- [Update Team](#update-team)
- [Delete Team](#delete-team)
- [Get Team](#get-team)
- [Get Teams (all)](#get-teams-all)
- [Get Teams with IDs](#get-teams-with-ids)

### Drivers
- [Create Driver](#create-driver)
- [Update Driver](#update-driver)
- [Delete Driver](#delete-driver)
- [Get Driver](#get-driver)
- [Get Drivers (all)](#get-drivers-all)
- [Get Drivers for Team](#get-drivers-for-team)

## Response Schema
Response schema for team endpoints and driver endpoints.
Team example:
```json
{
  "id": 1,
  "name": "Racing Team Alpha",
  "mean_power": 75.5,
  "vehicle_weight": 250.0,
  "rfid_identifier": "RFID-12345",
  "category": "advanced_class",
  "created_at": "2024-02-14T10:30:00.000000"
}
```

Driver example:
```json
{
  "id": 1,
  "name": "John A. Smith",
  "team_id": 1,
  "weight": 76.0,
  "created_at": "2024-02-14T13:45:00.000000"
}
```

## Teams

### Create Team
Creates a new racing team.

**Authorization:** Admin role required  
**Method:** `POST`  
**URL:** `http://hostname/teams/`

#### Request Body
```json
{
  "name": "Racing Team Alpha",
  "mean_power": 75.5,
  "vehicle_weight": 250.0,
  "rfid_identifier": "RFID-12345",
  "category": "advanced_class"
}
```

#### Responses
- `200 OK`: Team created successfully
- `400 Bad Request`: Invalid category or field values
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `422 Unprocessable Entity`: Validation error

### Update Team
Updates an existing team. Only provided fields will be updated.

**Authorization:** Team Lead or Admin role required  
**Method:** `PUT`  
**URL:** `http://hostname/teams/{team_id}`

#### Path Parameters
- `team_id` (int): ID of the team to update

#### Request Body
All fields are optional - only include fields you want to update.
```json
{
  "name": "Racing Team Alpha",
  "mean_power": 75.5,
  "vehicle_weight": 250.0,
  "rfid_identifier": "RFID-12345",
  "category": "advanced_class"
}
```

#### Responses
- `200 OK`: Team updated successfully
- `400 Bad Request`: Invalid field values
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Team not found
- `422 Unprocessable Entity`: Validation error

### Delete Team
Deletes a team and all associated data.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/teams/{team_id}`

#### Path Parameters
- `team_id` (int): ID of the team to delete

#### Responses
- `200 OK`: Team deleted successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Team not found

### Get Team
Retrieves a single team by ID.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/teams/{team_id}`

#### Path Parameters
- `team_id` (int): ID of the team

#### Responses
- `200 OK`: Team retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Team not found

### Get Teams (all)
Retrieves all teams in the system.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/teams/`

#### Responses
- `200 OK`: Teams retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

### Get Teams with IDs
Retrieves multiple specific teams by their IDs.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/teams/by-ids/?team_ids=1&team_ids=2&team_ids=3`

#### Query Parameters
- `team_ids` (int, repeatable): Team IDs to retrieve (can be repeated multiple times)

#### Responses
- `200 OK`: Teams retrieved successfully
- `400 Bad Request`: No team_ids provided
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

---

## Drivers

### Create Driver
Creates a new driver for a team.

**Authorization:** Admin role required  
**Method:** `POST`  
**URL:** `http://hostname/drivers/`

#### Request Body
```json
{
  "name": "John Smith",
  "team_id": 1,
  "weight": 75.5
}
```

#### Responses
- `200 OK`: Driver created successfully
- `400 Bad Request`: Invalid field values
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Team not found
- `422 Unprocessable Entity`: Validation error

### Update Driver
Updates an existing driver. Only provided fields will be updated.

**Authorization:** Team Lead or Admin role required  
**Method:** `PUT`  
**URL:** `http://hostname/drivers/{driver_id}`

#### Path Parameters
- `driver_id` (int): ID of the driver to update

#### Request Body
All fields are optional - only include fields you want to update.
```json
{
  "name": "John Smith",
  "team_id": 1,
  "weight": 75.5
}
```

#### Responses
- `200 OK`: Driver updated successfully
- `400 Bad Request`: Invalid field values
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Driver or team not found
- `422 Unprocessable Entity`: Validation error

### Delete Driver
Deletes a driver and all associated data.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/drivers/{driver_id}`

#### Path Parameters
- `driver_id` (int): ID of the driver to delete

#### Responses
- `200 OK`: Driver deleted successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Driver not found

### Get Driver
Retrieves a single driver by ID.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/drivers/{driver_id}`

#### Path Parameters
- `driver_id` (int): ID of the driver

#### Responses
- `200 OK`: Driver retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Driver not found

### Get Drivers (all)
Retrieves all drivers in the system.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/drivers/`

#### Responses
- `200 OK`: Drivers retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

### Get Drivers for Team
Retrieves all drivers belonging to a specific team.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/drivers/team/{team_id}`

#### Path Parameters
- `team_id` (int): ID of the team

#### Responses
- `200 OK`: Drivers retrieved successfully
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Team not found