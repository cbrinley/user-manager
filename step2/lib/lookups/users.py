from ansible.plugins.lookup import LookupBase
import pwd

'''
Lookup user module which acts on some static yaml/json/dict input


Usage:
second parameter is any valid username or "*" to capture all users.

set_fact:
  output_data: "{{lookup('users','*')}}"

debug: var=output_data
'''

class LookupModule(LookupBase):
  def run(self, terms, variables):
    match = str(terms[0]) # multiple inputs may be given using "{{ term0 | example(term1,...) }}"
    ret = []
    for user in pwd.getpwall():
      if match != "*" and match != user.pw_name: continue
      ret.append( {
        "name" : user.pw_name,
        "uid" : user.pw_uid,
        "comment" : user.pw_gecos
      })
    return ret

