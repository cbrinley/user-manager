import subprocess
import pwd
import os


def shell_out(cmd):
  if type(cmd) is unicode: cmd = str(cmd)
  if type(cmd) is str: cmd = cmd.split()
  if type(cmd) is not list: raise Exception("Invalid arguments to shell_out(%s)" % cmd)
  p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  if p.wait() != 0:
    msg = "Error:\n"
    so = p.stdout.read()
    if so: msg += so + "\n"
    se = p.stderr.read()
    if se: msg += se
    print msg
  else: 
    msg = p.stdout.read()
    if msg: print msg
  return p.returncode


def add(arguments):
  cmd = ["useradd"] + arguments
  return shell_out(cmd)


def ls_help():
  print '''
  Usage: user-manager ls
  Doc: displays a list of users in the following form
  Example:
    Username\tUser ID\tComment
    root\t0\tThis is root user
    ...
  '''
  return 1

def ssh_help(msg=''):
  if msg: print msg
  print '''
  Usage: user-manager ssh <user> <public_key>
  Doc: adds a new ssh key to the authorized_keys file if it does not already exist
  Example:
    user-manager ssh myuser "`cat mykey.pub`"
  '''
  return 1

def display_table(lines):
  '''impl from https://stackoverflow.com/questions/9989334/create-nice-column-output-in-python
  '''
  col_width = max(len(word) for row in lines for word in row) + 2  # padding
  for row in lines:
    print "".join(word.ljust(col_width) for word in row)

def ls(arguments):
  '''returns: username user_id comments'''
  if arguments: return ls_help()
  header = ["username","User ID", "Comment"]
  lines = [header]
  for user in pwd.getpwall(): 
    line = map(str, [user.pw_name,user.pw_uid,user.pw_gecos])
    lines.append( line )
  display_table(lines)
  return 0

def rm(arguments):
  cmd = ["userdel"] + arguments
  return shell_out(cmd)


def ssh(arguments):
  '''adds ssh pub key to authorized_keys if not present.
     #1 ensure permissions are correct on dir 700
     #2 ensure premissions are correct on authorized_keys file 600
     #3 ordering here matters so dont try to open file to parent dir exists
  '''
  if arguments[0] == "--help" or arguments[0] == "-h": return ssh_help()
  if len(arguments) != 2: return ssh_help("invalid argument count. be sure to put quotes around public key. see example below.")
  user_name = arguments[0]
  pub_key = arguments[1].strip()
  home_dir = os.path.expanduser('~%s' % user_name)
  ssh_dir = os.path.join(home_dir,".ssh")
  auth_keys = os.path.join(ssh_dir,"authorized_keys")
  if not os.path.isdir(ssh_dir): os.mkdir(ssh_dir)
  if shell_out("chmod 700 %s" % ssh_dir) != 0:    #1
    print "Could not set permissions on %s. Please check that you have appropriate rights." % ssh_dir
    return 1
  auth_keys_file = open(auth_keys,"a") #3
  if shell_out("chmod 600 %s" % auth_keys) != 0:    #2
    print "Could not set permissions on %s. Please check that you have appropriate rights." % auth_keys
    return 1
  if shell_out("chown -R %s:%s %s" % (user_name,user_name,ssh_dir)) != 0:
    print "Could not set owner on %s. Please check that you have appropriate rights." % ssh_dir
    return 1
  for line in open(auth_keys):
    if line.strip() == pub_key: return 0
  auth_keys_file.write(pub_key + '\n')
  auth_keys_file.close()
  return 0


