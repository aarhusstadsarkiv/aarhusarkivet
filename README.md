# AarhusArkivet

Decisions:
- All interfaces interact with a central APIClient
- All output from APIClient is a dict with error or result
- All "result"-keys are either a dict or an array