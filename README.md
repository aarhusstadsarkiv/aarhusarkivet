# AarhusArkivet

Git remotes
origin  https://github.com/aarhusstadsarkiv/aarhusarkivet.git (fetch)
origin  https://github.com/aarhusstadsarkiv/aarhusarkivet.git (push)
production      https://git.heroku.com/aarhusarkivet.git (fetch)
production      https://git.heroku.com/aarhusarkivet.git (push)
staging https://git.heroku.com/aarhusarkivet-staging.git (fetch)
staging https://git.heroku.com/aarhusarkivet-staging.git (push)

Decisions:
- All interfaces interact with a central APIClient
- All output from APIClient is a dict with an "errors"-key OR either a "result"-key with multiple results or varying keys in the root when single result

Bugs:
- when only one facetvalue is set, no orange remove-entry for the value is present under the given facetlisting