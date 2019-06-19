# AarhusArkivet

Decisions:
- All interfaces interact with a central APIClient
- All output from APIClient is a dict with or without an error-key and a result-key with multiple results

Bugs:
- when only one facetvalue is set, no orange remove-entry for the value is present under the given facetlisting