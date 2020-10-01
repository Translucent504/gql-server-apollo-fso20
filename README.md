# GraphQL Backends with Client

This Repo contains both the Backend and the Frontend code.

## Backend
There are 2 backends implemented that expose a GraphQL API.
  1. A NodeJS (apollo-server) backend
  2. A Python (graphene + FastAPI) backend

Both are fully interchangeable.

### NodeJS (apollo-server)
This is written using a **Schema-first** approach where we define the types using a gql template string.
Then we define resolvers for all Queries and Mutations that were defined in that string as needed.
  
### Python (graphene + FastAPI)
This is written using a **Code-first** approach where all the types and queries are defined as actual separate python classes.
The resolvers for each field are as methods for the class to which they belong.

**Note:** The NodeJS approach felt easier and less cumbersome but that is probably due to the fact that I learnt that first and
I have been programming mostly in javascript (React) recently.

## Frontend
The frontend is written in React (apollo-client). Where we only need to change the uri in the index.js file where we define the apollo client
to switch the backends.
