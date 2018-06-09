import json, re, os

with open('config.json') as f:
  json_str = f.read()
config = json.loads(json_str)

with open('out.json') as f:
  json_str = f.read()

email_to_path_to_output = json.loads(json_str)
email_to_loc = {
  email: sum(email_to_path_to_output[email].values()) for email in email_to_path_to_output
}

mean = sum(email_to_loc.values()) / float(len(email_to_loc))
print 'mean:', round(mean)

print 'lines of code added + deleted across all repos since {}'.format(config['since'])
print '(commits from the top quintile in each repo are excluded)'
for email, loc in sorted(email_to_loc.iteritems(), key=lambda t: -t[1]):
  print '{:<40} {:<5} {:.2}'.format(email, loc, loc / mean)
