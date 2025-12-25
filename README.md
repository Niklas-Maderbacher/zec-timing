# Zec-timing
Repository for ZeroEmissionChallenge Timing by Darnhofer and Maderbacher
ZEC-API branch by Darnhofer

## Services Status
| Service               | Status         |
|-----------------------|----------------|
| User service          | Error Handling|
| Attempt service       | Error handling|
| Score service         | logic done needs event based running & Error handling|
| Challenge service     | Error handling|
| Team/Driver service   | Error handling|
| Auth service          | Error handling|

## Todo list
- Split into services
- score service event based 
- Api gateway
- basic tests for all the services
- create a proper keycloak realm import file

## Notes and future
- needs 80% Test converage
- Frontend is just a html page atm 
- refrsh tocken blacklisting could be cool
- limiter for login to "limit" :) spamming 
- check if using crud in other crud limits the microservices in the future --> yes it does
