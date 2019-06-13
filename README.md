# AarhusArkivet

Decisions:
- All interfaces interact with a central APIClient
- All output from APIClient is a dict with or without an error-key and sometimes a result-key
