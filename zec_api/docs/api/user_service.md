# Users Service

Manage user accounts and role assignments.

## Table of Contents
- [Seeded Data](#seeded-data)
- [Response Schema](#response-schema)
- [Create User](#create-user)
- [Get User by Username](#get-user-by-username)
- [Get User by ID](#get-user-by-id)
- [Get all Users](#get-all-users)
- [Update User](#update-user)
- [Delete User](#delete-user)
- [Assign Roles](#assign-roles)
- [Remove Roles](#remove-roles)

## Seeded Data

The predefined user **admin** with password **changeme** is seeded in the service.  
You can modify or extend these defaults in the following file:

`zec_api/services/user-service/app/database/seed.py`

## Response Schema
Response schema for all get endpoints
Get all endpoints return a list of objects of this
```json
{
  "id": 1,
  "team_id": 1,
  "username": "team_leader_01",
  "email": "",
  "kc_id": "a3f8b2c1-9d4e-4f5a-8b3c-1e2f3a4b5c6d",
  "created_at": "2024-02-14T09:00:00.000000"
}
```

## Create User
Creates a new user.

**Authorization:** Admin role required  
**Method:** `POST`  
**URL:** `http://hostname/users/`

### Request Body
```json
{
  "username": "team_leader_01",
  "password": "SecurePassword123!",
  "team_id": 1
}
```

### Responses
- `200 OK`: Successfully created
- `400 Bad Request`: Invalid username or password format
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `409 Conflict`: Username already exists
- `422 Unprocessable Entity`: Validation error

## Get User by Username
Gets a user by their username.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/users/username/{username}`

### Path Parameters
- `username` (string): Username of the user to retrieve

### Responses
- `200 OK`: Successfully user returned
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User not found

## Get User by ID
Retrieves a user by their Keycloak user ID.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/users/id/{id}`

### Path Parameters
- `id` (string): Keycloak user ID (UUID)

### Responses
- `200 OK`: Successfully user returned
- `400 Bad Request`: Invalid ID format
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User not found

## Get all Users
Retrieves all users in the system.

**Authorization:** Admin role required  
**Method:** `GET`  
**URL:** `http://hostname/users/`

### Responses
- `200 OK`: List of users returned
- `200 OK (empty)`: No users found
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions

## Update User
Updates an existing user's information.

**Authorization:** Admin role required  
**Method:** `PUT`  
**URL:** `http://hostname/users/{user_id}`

### Path Parameters
- `user_id` (string): Keycloak user ID (UUID)

### Request Body
All fields are optional - only include fields you want to update.
```json
{
  "username": "new_username",
  "password": "NewSecurePassword456!",
  "team_id": 1
}
```

### Responses
- `200 OK`: Successfully updated
- `400 Bad Request`: Invalid username or password format
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User not found
- `422 Unprocessable Entity`: Validation error

## Delete User
Deletes a user account and all associated data.

**Authorization:** Admin role required  
**Method:** `DELETE`  
**URL:** `http://hostname/users/{user_id}`

### Path Parameters
- `user_id` (string): Keycloak user ID (UUID)

### Responses
- `200 OK`: Successfully deleted
- `400 Bad Request`: Invalid ID format
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User not found

## Assign Roles
Assigns roles to a user.

**Authorization:** Authenticated user required  
**Method:** `POST`  
**URL:** `http://hostname/users/{user_id}/roles`

### Path Parameters
- `user_id` (string): Keycloak user ID (UUID)

### Request Body
```json
{
  "roles": ["team_lead"]
}
```

**Available Roles:**
- `admin` - Full system access
- `team_lead` - Can manage team and drivers
- `viewer` - Read-only access to analytics

### Responses
- `200 OK`: Roles successfully added
- `400 Bad Request`: Invalid role names or user ID format
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User or role not found
- `422 Unprocessable Entity`: Validation error

## Remove Roles
Removes one or more roles from a user.

**Authorization:** Authenticated user required  
**Method:** `DELETE`  
**URL:** `http://hostname/users/{user_id}/roles`

### Path Parameters
- `user_id` (string): Keycloak user ID (UUID)

### Request Body
```json
{
  "roles": ["viewer"]
}
```

### Responses
- `200 OK`: Roles successfully removed
- `400 Bad Request`: Invalid role names or user ID format
- `401 Unauthorized`: Missing or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: User or role not found
- `422 Unprocessable Entity`: Validation error