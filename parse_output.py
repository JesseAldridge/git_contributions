import json, re, os

with open('out.json') as f:
  json_str = f.read()

email_to_path_to_output = json.loads(json_str)
email_to_loc = {}

for email in email_to_path_to_output:
  path_to_output = email_to_path_to_output[email]
  sum_ = 0
  for path, output in path_to_output.iteritems():
    counts = re.findall(': ([0-9]*?),|\n', output)
    if not counts:
      continue
    counts = [(int(s) if s else 0) for s in counts]
    added, deleted, _ = counts
    sum_ += added + deleted
  email_to_loc[email] = sum_

for email, loc in sorted(email_to_loc.iteritems(), key=lambda t: -t[1]):
  print email, loc
