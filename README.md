## AarhusArkivet
### Set up
- .env files are in OneDrive. Copy aarhusarkivet-dev.env to .env and place it in the root of the repository.
- Current Heroku runtime is 3.9.9. Pipfile only specifies version "3"

### Local dev
- run "python application.py" from root. Runs on port 3000.

### Decisions
- All interfaces interact with a central API-Client
- All output from the client is a dict with an "errors"-key OR either a "result"-key with multiple results or varying keys in the root when single result
