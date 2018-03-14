#!/usr/bin/python
# -*- coding: utf-8 -*-
#

DOCUMENTATION = '''
---
'''

from ansible.module_utils.basic import *
import requests
import os

def main():

  # http://192.168.56.23:8080/manager/text/deploy?path=/samplewar&update=true
  module = AnsibleModule(
    argument_spec = dict(
      url       = dict(required=True, type='str'),
      username  = dict(required=True, type='str'),
      password  = dict(required=True, type='str'),
      context   = dict(required=True, type='str'),
      src       = dict(required=True, type='str')
    )
  )

  result = dict(
      msg='',
      changed=False,
      context='',
      application_url='',
      src=''
  )

  if module.check_mode:
    return result

  url = module.params["url"]
  username = module.params["username"]
  password = module.params["password"]
  context = module.params["context"]
  src = module.params["src"]

  files = {'file': (os.path.basename(src), open(src, 'rb'))}
  deploy_url = "{}/manager/text/deploy?path={}&update=true".format(url, context)

  r = requests.put(url=deploy_url, auth=(username, password), files=files)

  if r.status_code == 200:
    result['msg'] = "OK - Deployed application at context path [{}]".format(context)
    result['changed'] = True
    result['context'] = context
    result['application_url'] = "{}{}".format(url, context)
    result['src'] = src
  else:
    module.fail_json(msg='FAIL - Deployment Failed at context path [{}]'.format(context), **result)

  module.exit_json(**result)
  
# include magic from lib/ansible/module_common.py
#<<INCLUDE_ANSIBLE_MODULE_COMMON>>
main()
