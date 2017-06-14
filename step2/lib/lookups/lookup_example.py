from ansible.plugins.lookup import LookupBase

'''
Example lookup module which acts on some static yaml/json/dict input
Usage:

set_fact:
  data:
    super_secret_key: 1234
    ignored_key: yep

set_fact:
  output_data: "{{lookup('lookup_example',data)}}

debug: var=output_data
'''

class LookupModule(LookupBase):
  def run(self, terms, variables):
    data = terms[0] # multiple inputs may be given using "{{ term0 | example(term1,...) }}"
    for k,v in data.items():
      if k == "super_secret_key": return [v] #You must return a list else string is treated as a list.
    return ['']  

