#!/usr/bin/env python

import requests
import json

DOCUMENTATION = '''
---
module: example_module 
author: Your Name (your.name@hyatt.com)
version_added: '2.1'
short_description: short description here 
description:
  - longer description here.

options:
  state:
    required: no
    choices: ['present', 'absent']
    default: 'present'
    description:
      - declares if this item should be present of absent 

  other_item:
    requred: true
    description:
      - continue options here 

'''

EXAMPLES = '''
- name: be nice add some examples 
  example_module:
    state: present
    other_item: value 

'''

RETURN = '''
key: value
stdout: <text of standard out>
'''

class Helper(object):
  def __init__(self,module):
    self.module = module
    self.changed = False

  def __getattr__(self,key):
      return self.module.params.get(key,'')

  def update(self):
    import random
    self.changed = random.choice([True,False])
    if self.changed: self.exit("Update: All done")
    else: self.fail("Update: I failed.")

  def rm(self):
    import random
    self.changed = random.choice([True,False])
    if self.changed: self.exit("Remove: All done")
    else: self.fail("Remove: I failed.")

  @property 
  def update_required(self):
    import random
    return random.choice([True,False])

  def fail(self,msg,**kwargs):
    self.module.fail_json(msg=msg,changed=False,traceback=traceback.format_exc(), **kwargs)

  def exit(self,msg='',**kwargs):
    if not msg: msg = "OK"
    self.module.exit_json(changed=self.changed,stdout=msg,**kwargs)



def main():
  module = AnsibleModule(
    argument_spec=dict(
      state=dict(type='str', required=False,default='present'),
      other_item=dict(type='str',required=True)
    ),
    supports_check_mode=False,
  )

  try: helper = Helper(module)
  except Exception, exc: module.fail_json(msg="Error creating internal class Helper. Contact development")
  allowed_states = ["absent","present"]
  if helper.state not in allowed_states: helper.fail("Invalid state selected: %s" % helper.state,allowed_states=allowed_states)

  if not helper.update_required: helper.exit("no action required")
  if helper.state == 'present': helper.do_it()
  else: helper.rm()

# this is magic, see lib/ansible/module_common.py
from ansible.module_utils.basic import *
if __name__ == '__main__':
    main()
