#!/bin/sh
has_errored=false
find . ! -name "$(printf "*\n*")" -name '*.py' | grep -v './env' > tmp
while IFS= read -r file; do
  printf "Running flake8 on %s.... Result: " "$file"
  flake8 --count "$file"
  flake8_status="$?"
  if [ "$flake8_status" != 0 ]; then
    has_errored=true
  fi
done < tmp
rm tmp

find . ! -name "$(printf "*\n*")" -name '*.sh' | grep -v './env' > tmp
while IFS= read -r file; do
  printf "Running shellcheck on %s.... Result: " "$file"
  shellcheck "$file"
  shellcheck_status="$?"
  echo "$shellcheck_status"
  if [ "$shellcheck_status" != 0 ]; then
    has_errored=true
  fi
done < tmp
rm tmp

if [ "$has_errored" = true ]; then
  return 1
else
  return 0
fi
