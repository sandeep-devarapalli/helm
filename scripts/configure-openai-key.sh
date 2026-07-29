#!/bin/zsh

set -eu

repo_root="${0:A:h:h}"
env_file="${repo_root}/.env"
example_file="${repo_root}/.env.example"

umask 077

if [[ ! -f "${env_file}" ]]; then
  cp "${example_file}" "${env_file}"
fi

chmod 600 "${env_file}"
read -r -s "api_key?Paste the OpenAI API key (input hidden): "
print

if [[ -z "${api_key}" ]]; then
  print -u2 "No key entered. Nothing changed."
  exit 1
fi

temp_file="$(mktemp "${env_file}.tmp.XXXXXX")"
trap 'rm -f "${temp_file}"' EXIT INT TERM
found=0

while IFS= read -r line || [[ -n "${line}" ]]; do
  if [[ "${line}" == OPENAI_API_KEY=* ]]; then
    print -r -- "OPENAI_API_KEY=${api_key}" >> "${temp_file}"
    found=1
  else
    print -r -- "${line}" >> "${temp_file}"
  fi
done < "${env_file}"

if (( found == 0 )); then
  print -r -- "OPENAI_API_KEY=${api_key}" >> "${temp_file}"
fi

mv "${temp_file}" "${env_file}"
chmod 600 "${env_file}"
trap - EXIT INT TERM
unset api_key

print "OpenAI API key saved to the ignored local .env file."
