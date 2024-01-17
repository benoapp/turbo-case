#!/bin/bash

# Bump the version, build the package,
# and publish a new release to GitHub using
# semantic-release

args="$@"

semantic-release version $args
semantic-release publish
git fetch
