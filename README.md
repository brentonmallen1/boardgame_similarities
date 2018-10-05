# Boardgame Similarity Engine

This web app is meant to provide a list of similar
board games from an user-input BoardGameGeek ID number using
Locality Sensitive Hashing.

The app can be accessed
[here](https://nqluu8bsoi.execute-api.us-east-1.amazonaws.com/dev/)


### Credit
This would not have been possible without data gathering
assistance and rubber ducking from
[@gallamine](https://twitter.com/gallamine) and
[@notthatdsw](https://twitter.com/notthatdsw)
as well as the following main dependencies:

- [BoardGameGeek](https://boardgamegeek.com) API
- [BoardGameGeek v2](https://github.com/lcosmin/boardgamegeek)
- [Zappa](https://github.com/Miserlou/Zappa)
- [datasketch](https://github.com/ekzhu/datasketch)

## Working with the library
#### Build the Environment
`make init`

#### Gather the Data
This library is built on a data file that contains a pandas
dataframe of the top ~6000 board games (as of 2018-06-27).  This
data file is not included as I don't own that data but it can be
built using the boardgamegeekv2 library.

#### Building the Locality Sensitive Hash Table


##### Run Local via Flask
`make start`

##### Stop or Restart Local
`make stop` or `make restart`

### Deployment
This system is deployed to AWS's serverless architecture using Zappa.
The following commands can be used to interact with the deployment:

##### Initial deploy
`make deploy`

##### Update a previous deployment
`make redeploy`

##### Tear down a deployment
`make remove`

##### Get Logs
If there is an issue with the system after deployment, the aws logs can be
observed using
`make logs`

### Tests
There is limited testing at the moment but tests can be run using
`make test`



