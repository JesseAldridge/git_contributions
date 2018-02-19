import subprocess, os, json

def process_each_repo(emails, repo_paths):
  email_to_repo_path_to_output = {}

  for email in emails:
    email_to_repo_path_to_output[email] = {}
    print 'email:', email
    for repo_path in repo_paths:
      repo_path = os.path.expanduser(repo_path)
      print '  repo_path:', repo_path
      os.chdir(repo_path)
      command_list = 'bash /Users/jesse_aldridge/Dropbox/git_contributions/_git_contrib.sh'.split()
      command_list.append(email)
      proc = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
      output = proc.communicate()[0]
      email_to_repo_path_to_output[email][repo_path] = output
      print '  ', output

  return email_to_repo_path_to_output

def main():
  with open('config.json') as f:
    json_str = f.read()
  config_dict = json.loads(json_str)

  starting_dir = os.getcwd()
  try:
    email_to_repo_path_to_output = process_each_repo(
      config_dict['emails'],
      config_dict['repo_paths'],
    )
  finally:
    os.chdir(starting_dir)

  json_str = json.dumps(email_to_repo_path_to_output, indent=2)
  with open('out.json', 'w') as f:
    f.write(json_str)

main()
