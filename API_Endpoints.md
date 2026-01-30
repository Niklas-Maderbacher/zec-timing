# ZEC-API Table of Contents
### [README](#notes)
- ## 1. Attempts
  - 1.1 [Create Attempt](#create-attempt)
  - 1.2 [Update Attempt](#update-attempt)
  - 1.3 [Delete Attempt](#delete-attempt)
  - 1.4 [Get Attempt](#get-attempt)
  - 1.5 [Get Attempts (all)](#get-attempts-all)
  - 1.6 [Get Attempts per Challenge](#get-attempts-per-challenge)
  - 1.7 [Get Fastest Attempt for a Challenge](#get-fastest-attempt-for-a-challenge)
  - 1.8 [Get Fastest Attempt for a Team in a Challenge](#get-fastest-attempt-for-a-team-in-a-challenge)
  - 1.8 [Get Least Energy Attempt for a Challenge](#get-least-energy-attempt-for-a-challenge)
  - 1.9 [Get Least Energy Attempt for a Team in a Challenge](#get-least-energy-attempt-for-a-team-in-a-challenge)
- ## 2. Auth
  - 2.1 [Login](#login)
  - 2.2 [Refresh Token](#refresh-token)
- ## 3. Challenges
  - 3.1 [Update Challenge](#update-challenge)
  - 3.2 [Get Challenge by ID](#get-challenge-by-id)
  - 3.3 [Get Challenge by Name](#get-challenge-by-name)
  - 3.4 [Get Challenges (all)](#get-challenges-all)
- ## 4. Scores
  - 4.1 [Create Score](#create-score)
  - 4.2 [Update Score](#update-score)
  - 4.3 [Delete Score](#delete-score)
  - 4.4 [Delete Scores for a Attempt](#delete-scores-for-attempt)
  - 4.5 [Get Score](#get-score)
  - 4.6 [Get Scores (all)](#get-scores-all)
  - 4.7 [Get Leaderboard](#get-leaderboard)
- ## 5. Teams
  - 5.1 [Create Team](#create-team)
  - 5.2 [Update Team](#update-team)
  - 5.3 [Delete Team](#delete-team)
  - 5.4 [Get Team](#get-team)
  - 5.5 [Get Teams (all)](#get-teams-all)
  - 5.6 [Get Teams with IDs](#get-teams-with-ids)
- ## 6. Drivers
  - 6.1 [Create Driver](#create-driver)
  - 6.2 [Update Driver](#update-driver)
  - 6.3 [Delete Driver](#delete-driver)
  - 6.4 [Get Driver](#get-driver)
  - 6.5 [Get Drivers (all)](#get-drivers-all)
  - 6.6 [Get Drivers for a Team](#get-drivers-for-team)
- ## 7. Users
  - 7.1 [Create User](#create-user)
  - 7.2 [Get User by Username](#get-user-by-username)
  - 7.3 [Get User by ID](#get-user-by-id)
  - 7.4 [Get all Users](#get-all-users)
  - 7.5 [Update User](#update-user)
  - 7.6 [Delete User](#delete-user)
  - 7.7 [Assign Roles](#assign-roles)
  - 7.8 [Remove Roles](#remove-roles)
- ## 8. Penalty
  - 8.1 [Create Penalty](#create-penalty)
  - 8.2 [Update Penalty](#update-penalty)
  - 8.3 [Delete Penalty](#delete-penalty)
  - 8.4 [Delete Penalties for a Attempt](#delete-penalties-for-attempt)
  - 8.5 [Get Penalty](#get-penalty)
  - 8.6 [Get Penalties (all)](#get-penalties-all)
  - 8.7 [Get Penalties for Attempt](#get-penalties-for-attempt)
  - 8.8 [Get Penaltytypes](#get-penalty-types)
### Notes
- When talking about access_token in this document i am referring to the token gotten by [Login](#login)
- Also users with the role admin have acces to teamlead endpoints
- ZEC-API assummes the user adds the right values when creating data
### Attempt
#### Create Attempt
Needs Bearer authorization header containing `access_token` from a user with admin role  
`POST`

**URL** http://hostname/attempts/

**Request Body Format**
```json
{
  "team_id": int,
  "driver_id": int,
  "challenge_id": int,
  "is_valid": bool, (optional) if you want to create a invalid attempt
  "start_time": datetime, (with milliseconds)
  "end_time": datetime, (with milliseconds)
  "energy_used": float,
  "penalty_count": int,
  "penalty_type": int
}
```
#### Update Attempt
Needs Bearer authorization header containing `access_token` from a user with admin role  
`PUT`

**URL** http://hostname/attempts/{attempt_id}

**Request Body Format**  
All fields are optional depending on what needs to be updated.
```json
{
  "team_id": int,
  "driver_id": int,
  "challenge_id": int,
  "is_valid": bool,
  "start_time": datetime, (with milliseconds)
  "end_time": datetime, (with milliseconds)
  "energy_used": float
}
```
#### Delete Attempt
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/attempts/{attempt_id}
#### Get Attempt
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`
 
**URL** http://hostname/attempts/{attempt_id}
#### Get Attempts (all)
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`
 
**URL** http://hostname/attempts/
#### Get Attempts per Challenge
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/attempts/challenges/{challenge_id}
#### Get Fastest Attempt for a Challenge
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/attempts/fastest/{challenge_id}
#### Get Fastest Attempt for a Team in a Challenge
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`
 
**URL** http://hostname/attempts/fastest/per-team/?challenge_id={challenge_id}&team_id={team_id}

**Query Parameters**
- `challenge_id` (int): ID of the challenge  
- `team_id` (int): ID of the team
#### Get Least Energy Attempt for a Challenge
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/attempts/least-energy/{challenge_id}
#### Get Least Energy Attempt for a Team in a Challenge
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`
 
**URL** http://hostname/attempts/least-energy/per-team/?challenge_id={challenge_id}&team_id={team_id}

**Query Parameters**
- `challenge_id` (int): ID of the challenge  
- `team_id` (int): ID of the team
### Auth
#### Login
`POST`

**URL** http://hostname/auth/login

**Request Body Format**  
Content-Type: `application/x-www-form-urlencoded`
**Form Parameters**
- `username` (string, required)
- `password` (string, required)
#### Refresh Token
`POST`

**URL** http://hostname/auth/refresh

**Request Body Format**  

Content-Type: `application/x-www-form-urlencoded`

**Form Parameters**
- `refresh_token` (string, required)
### Challenge
#### Update Challenge
Needs Bearer authorization header containing `access_token` from a user with admin role  
`PUT`
 
**URL** http://hostname/challenges/{challenge_id}

**Request Body Format**  

All fields are optional depending on what needs to be updated.
```json
{
  "name": string,
  "max_attempts": int,
  "esp_mac_start1": string,
  "esp_mac_start2": string,
  "esp_mac_finish1": string,
  "esp_mac_finish2": string
}
```
#### Get Challenge by ID
`GET`
  
**URL** http://hostname/challenges/{challenge_id}
#### Get Challenge by Name
`GET`
  
**URL** http://hostname/challenges/name/{challenge_name}
#### Get Challenges (all)
`GET`

**URL** http://hostname/challenges/
### Score
#### Create Score
Needs Bearer authorization header containing `access_token` from a user with admin role  

`POST`

**URL** http://hostname/scores/

**Request Body Format**
```json
{
    "attempt_id": int
}
```
#### Update Score
Needs Bearer authorization header containing `access_token` from a user with admin role  
`PUT`

**URL** http://hostname/scores/{score_id}

**Request Body Format**
```json
{
    "value": float
}
```
#### Delete Score
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/scores/{score_id}
#### Delete Scores for Attempt
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/scores/attempt/{attempt_id}
#### Get Score
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/scores/{score_id}
#### Get Scores (all)
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/scores/
#### Get leaderboard
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/leaderboard/{challenge_id}/category{category}
### Team
#### Create Team
Needs Bearer authorization header containing `access_token` from a user with admin role  
`POST`

**URL** http://hostname/teams/

**Request Body Format**
```json
{
  "name": string,
  "mean_power": float,
  "vehicle_weight": float,
  "rfid_identifier": str,
  "category": team_category
}
```
#### Update Team
Needs Bearer authorization header containing `access_token` from a user with team_lead role  
`PUT`

**URL** http://hostname/teams/{team_id}

**Request Body Format**

Everything is optional depending on what needs to be updated
```json
{
    "name": string,
    "mean_power": float,
    "vehicle_weight": float,
    "rfid_identifier": string,
    "category": team_category
}
```
#### Delete Team
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/teams/{team_id}
#### Get Team
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/teams/{team_id}
#### Get Teams (all)
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/teams/
#### Get teams with ids
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/teams/by-ids/?team_ids=1&team_ids=2 etc..
pass ids as parameters
### Driver
#### Create Driver
Needs Bearer authorization header containing `access_token` from a user with admin role  
`POST`

**URL**http://hostname/drivers/

**Request Body Format**
```json
{
  "name": string,
  "team_id": int,
  "weight": float,
}
```
#### Update Driver
Needs Bearer authorization header containing `access_token` from a user with teamlead role  
`PUT`

**URL** http://hostname/teams/{driver_id}

**Request Body Format**

Everything is optional depending on what needs to be updated
```json
{
    "name": string,
    "team_id": int,
    "weight": float,
    "created_at": datetime
}
```
#### Delete Driver
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/drivers/{driver_id}
#### Get Driver
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/drivers/{driver_id}
#### Get Drivers (all)
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/drivers/
#### Get Drivers for Team
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/drivers/team/{team_id}
### User
#### Create User
Needs Bearer authorization header containing `access_token` from a user with admin role  
`POST`
 
**URL** http://hostname/users/

**Request Body Format**

```json
{
  "username": string,
  "password": string
}
```
#### Get User by Username
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/users/username/{username}

**Path Parameters**

- `username` (string): Username of the user
#### Get User by ID
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/users/id/{id}

**Path Parameters**
- `id` (string): Keycloak user ID
#### Get all Users
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/users/
#### Update User
Needs Bearer authorization header containing `access_token` from a user with admin role  
`PUT`

**URL** http://hostname/users/{user_id}

**Path Parameters**
- `user_id` (string): Keycloak user ID

**Request Body Format**

```json
{
  "username": string,
  "password": string
}
```
#### Delete User
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/users/{user_id}

**Path Parameters**
- `user_id` (string): Keycloak user ID
#### Assign Roles
Needs Bearer authorization header containing `access_token` 

`POST`
 
**URL** http://hostname/users/{user_id}/roles

**Path Parameters**
- `user_id` (string): Keycloak user ID

**Request Body Format**
```json
{
    "roles": [list]
}
```
#### Remove Roles
Needs Bearer authorization header containing `access_token` 

`DEL`

**URL** http://hostname/users/{user_id}/roles

**Path Parameters**
- `user_id` (string): Keycloak user ID

**Request Body Format**
```json
{
    "roles": [list]
}
```
### Penalty
#### Create Penalty
Needs Bearer authorization header containing `access_token` from a user with admin role  
`POST`

**URL**http://hostname/penalties/

**Request Body Format**
```json
{
  "attempt_id" : int,
  "count": int,
  "penalty_type_id": int
}
```
#### Update Penalty
Needs Bearer authorization header containing `access_token` from a user with teamlead role  
`PUT`

**URL** http://hostname/penalties/{penalty_id}

**Request Body Format**

Everything is optional depending on what needs to be updated
```json
{
  "attempt_id" : int,
  "count": int,
  "penalty_type_id": int
}
```
#### Delete Penalty
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/penalties/{penalty_id}
#### Delete Penalties for Attempt
Needs Bearer authorization header containing `access_token` from a user with admin role  
`DEL`

**URL** http://hostname/penalties/attempt/{attempt_id}
#### Get Penalty
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/penalties/{penalty_id}
#### Get Penalties (all)
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/penalties/
#### Get Penalties for Attempt
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/penalties/attempt/{attempt_id}

#### Get Penalty Types
Needs Bearer authorization header containing `access_token` from a user with admin role  
`GET`

**URL** http://hostname/penalties/types/
