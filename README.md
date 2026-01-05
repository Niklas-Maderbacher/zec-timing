# Zec-timing
Repository for **Z**ero**E**mission**C**hallenge-Timing by Darnhofer and Maderbacher
- ZEC-API branch by Darnhofer

## Services Status
| Service               | Status         |
|-----------------------|----------------|
| User service          |Error Handling|
| Attempt service       |Error handling|
| Score service         |Error handling|
| Challenge service     |Error handling|
| Team/Driver service   |done|
| Auth service          |slight auth hardening|

## Todo list for before 07.01
- api endpoint documentation (user and leaderboard missing)
- change challenge get by name to use query
- adding endpoint to add roles to user
- attempt number calculation
- fix score calculation
- error handling for all
- basic tests for all the services

## Todo future
- internalise auth endpoints
- rbac at gateway level (needs more verify endpoints (depends exists))

## Notes and future
- needs 80% Test converage
- refresh tocken blacklisting could be cool
- limiter for login to "limit" :) spamming 
