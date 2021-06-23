# Helper script for simulating git workflows using act
# Usage: ./act.sh <job> <action> [<github-token>]
# 
# To install act tool:
#    brew install act
# 
# To lint working copy:
#    ./act.sh lint push
#
act -s GITHUB_TOKEN=${3:-""} -j $1 $2
