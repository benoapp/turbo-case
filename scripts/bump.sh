#!/bin/bash

# Bump the version, build the package,
# and publish a new release to GitHub using
# semantic-release

semantic-release version
semantic-release publish
git fetch
