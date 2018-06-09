import subprocess, re, os, json

def process_each_repo(emails, repo_paths, since_date_str):
  email_to_repo_path_to_output = {}

  for email in emails:
    email_to_repo_path_to_output[email] = {}
    print 'email:', email
    total_loc = 0
    for repo_path in repo_paths:
      repo_path = os.path.expanduser(repo_path)
      print '  repo_path:', repo_path
      os.chdir(repo_path)
      commits = process_repo(repo_path, email)
      commits.sort(key=lambda commit: commit.added + commit.removed)
      normal_commits = commits[:int(len(commits) * .8)]
      locs = [commit.added + commit.removed for commit in normal_commits]
      email_to_repo_path_to_output[email][repo_path] = sum(locs)

  return email_to_repo_path_to_output

def process_repo(repo_path, email):
  class Commit:
    def __init__(self):
      self.added = 0
      self.removed = 0

    def __repr__(self):
      return '({}, {})'.format(self.added, self.removed)

  os.chdir(repo_path)
  cmd_arr = ['git', 'log', '--author={}'.format(email), '--since=2017-01-01', '--numstat']
  proc = subprocess.Popen(cmd_arr, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  output = proc.communicate()[0]

  # Parse git log.  Sample output:
  '''
  commit 9e2ed981742f1065fac35f70d546bf11b2d00b56
  Author: Jesse Aldridge <jesse.aldridge@airbnb.com>
  Date:   Fri Feb 23 21:40:23 2018 -0800

      relative to mean

  4 1 parse_output.py

  commit b5eecf54f298a91538bea44647d48bd82f32437b
  Author: Jesse Aldridge <jesse.aldridge@airbnb.com>
  Date:   Mon Feb 19 03:25:03 2018 -0800

      add since

  1 1 _git_contrib.sh
  3 2 git_contributions.py
  '''

  if not output.strip():
    return []
  lines = output.splitlines()

  commits = []
  i = 0
  while True:
    while not re.match('^[0-9]', lines[i]):
      i += 1
      if i >= len(lines):
        return commits
    commits.append(Commit())
    commit = commits[-1]
    while re.match('^[0-9]', lines[i]):
      split = lines[i].split()
      file_added, file_removed = [int(x) for x in split[0], split[1]]
      commit.added += file_added
      commit.removed += file_removed
      i += 1
      if i >= len(lines):
        return commits

def main():
  with open('config.json') as f:
    json_str = f.read()
  config_dict = json.loads(json_str)

  starting_dir = os.getcwd()
  try:
    email_to_repo_path_to_output = process_each_repo(
      config_dict['emails'],
      config_dict['repo_paths'],
      config_dict['since'],
    )
  finally:
    os.chdir(starting_dir)

  json_str = json.dumps(email_to_repo_path_to_output, indent=2)
  with open('out.json', 'w') as f:
    f.write(json_str)

if __name__ == '__main__':
  main()
