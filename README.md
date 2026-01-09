# Zec-timing
Repository for **Z**ero**E**mission**C**hallenge-Timing by Darnhofer and Maderbacher
- ZEC-API branch by Darnhofer

## Services Status
| Service               | Status         |
|-----------------------|----------------|
| User service          |done|
| Attempt service       |done|
| Score service         |calculation and refresh(acceleration) needs fixes|
| Challenge service     |done|
| Team/Driver service   |done|
| Auth service          |slight auth hardening|

## Todo
- category for challenges (close to series, advanced class, professional class)
- Attempt endpoints for energy are missing
- attempt number calculation
- fix score calculation
- use rbac at gateway level
- Upgrades for auth services regarding security
- fix tests and warnings
- add more tests to get 80% coverage

## Notes and future
- refresh tocken blacklisting could be cool
- limiter for login to "limit" :) spamming 