''' example filter doc 
    Arg1 = dict to act on
    ArgN = keys to add to output dictionary

    example:
      - name: setup a dictionary
        set_fact:
          input_dict:
            k1: some value
            another_key: does not matter

      - name: use filter
        set_fact:
          output_dict: "{{ input_dict | example('a','b') }}"

      - name: display it
        debug:
	  var: output_dict
'''
def example(*args):
  if type(args[0]) is dict: out = args[0]
  else: out = {}
  i = 0
  for k in args[1:]:
    out[i] = i
    i += 1
  return out 

class FilterModule(object):
  def filters(self):
    return { "example": example}
