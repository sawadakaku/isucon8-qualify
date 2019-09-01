#!/bin/bash

function main() {
  set -eu

  cd /home/isucon/torb/bench/

  local readonly RESULT_JSON="bench-result_$(date "+%Y-%m-%d_%H-%M-%S").json"
  bin/bench -remotes=127.0.0.1 -output ${RESULT_JSON}

  local readonly SCORE="$(cat ${RESULT_JSON} | jq .score)"
  local readonly SCORES_LOG="scores.log"
  echo "$(date) | Score: ${SCORE}" >> ${SCORES_LOG}
  echo
  echo "Score: ${SCORE}"
  echo "Updated $(pwd)/${SCORES_LOG}"
}

main
