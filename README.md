## AarhusArkivet

Local dev:
- 

Decisions:
- All interfaces interact with a central API-Client
- All output from the client is a dict with an "errors"-key OR either a "result"-key with multiple results or varying keys in the root when single result
