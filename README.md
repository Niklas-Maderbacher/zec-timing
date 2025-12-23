# Zec-timing
Repository for ZeroEmissionChallenge Timing by Darnhofer and Maderbacher
Web-App branch by Darnhofer

## Services Status
| Service               | Status         |
|-----------------------|----------------|
| User service          | needs cleanup  |
| Attempt service       | done           |
| Score service         | logic done needs event based running          |
| Challenge service     | done           |
| Team/Driver service   | done           |
| Auth service          | needs clean up works tho |

## Todo list
- auth service clean up (Bearer, remove error handling for now)
- user service clean up 
- score service event based 
- basic tests for all the services
- create a proper keycloak realm import file

## Notes and future
- needs 80% Test converage
- Frontend is just a html page atm 
- refrsh tocken blacklisting could be cool
- limiter for login to "limit" :) spamming 
- check if using crud in other crud limits the microservices in the future
