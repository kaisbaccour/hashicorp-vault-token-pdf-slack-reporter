#!/usr/local/bin/python3

import time
import hvac
import urllib3
from prettytable import PrettyTable
import operator
from datetime import datetime,date
from utils import *
import config

print("starting")

urllib3.disable_warnings()
with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
    k8s_jwt = file.read().replace('\n', '')

client = hvac.Client(url=VAULT_ADDR)
client.auth_kubernetes(role=KUBERNETES_AUTH_ROLE, jwt=k8s_jwt,use_token=True, mount_point=KUBERNETES_AUTH_MOUNTPOINT)
payload = client.list('auth/token/accessors')
keys = payload['data']['keys']

unique_auth_type_dict =dict()
unique_identities_dict =dict()
unique_roles_dict =dict() 

unique_auth_type_table = PrettyTable()
unique_roles_table = PrettyTable()
unique_identities_table = PrettyTable()
processes_table = PrettyTable()
humans_table = PrettyTable()
long_lived_table = PrettyTable()
outside_hours_table = PrettyTable()
long_lived_expiring_table = PrettyTable()

unique_auth_type_table.field_names = ["Auth type", "Occurence"]
unique_identities_table.field_names = ["Display Name", "Occurence"]
unique_roles_table.field_names = ["Role Name", "Occurence"]
processes_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
humans_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
long_lived_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
outside_hours_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
long_lived_expiring_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
multiple_tokens_with_same_id=0
multiple_tokens_with_same_id_example=""
starting=-1
ending=10000
root_token=0
now=datetime.now()
for idx,key in sorted(enumerate(keys)):
    if idx == ending:
        break
    if idx < starting:
        continue
    try:
      try:
         output = client.lookup_token(key, accessor=True)
      except:
          print("failed looking up token by accessor")
      if output['data']['display_name'] is not None:
          display_name = output['data']['display_name']
      else:
          display_name = "undefined"
      try:
          creation_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(output['data']['creation_time']))
      except:
          print("creation_date exception")
      try:
          if output['data']['expire_time'] is not None:
            if len(output['data']['expire_time']) > 24:
              expire_time = output['data']['expire_time'][0:len(str(output['data']['expire_time']))-9]
            else:
                expire_time = output['data']['expire_time']
                print (expire_time)
                print ("expire time too short")
          else:
              expire_time = "undefined"
              print(expire_time)
      except:
          print("expire_time exception")
      #role
      try:
          if output['data']['meta'] is None: 
              role="None"
          else:
              role= output['data']['meta']['role']
      except:
          print("getting_role_exception")
          print("role exception_raw_data: ", output['data'])
      #auth_type
      try:
          if output['data']['path'] is None: 
              auth_type="None"
          else:
              auth_type= str(output['data']['path']).replace('auth/','').replace('/login','').replace('/create','')
      except:
          print("getting_auth_type_exception")
          print("auth exception_raw_data: ", output['data'])
          print("auth exception_raw_data: ", output['data']['path'])
          
      try:
          policies = str(output['data']['policies']).replace('\'default\'','').replace(',','+').replace('[+','').replace(']+','').replace('[','').replace(']','').replace('\'','').replace('++','')
      except:
          print("policies fetching error")
      
      try:
          accessor = key
      except:
          print("assigning accessor key error. how strange!")

      try:
        expire_time_date_type = datetime.strptime(expire_time, '%Y-%m-%dT%H:%M:%S.%f')
        creation_time_date_type = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
      except:
          print("time parser error")
      try:
          will_expire_in=expire_time_date_type-now
          life_span=expire_time_date_type-creation_time_date_type
      except:
          print("time diff issue")

      
      try:
          date_display_format="%A_%d_%B_%Y-%H:%M:%S"
      except:
          print("date_display_format error. how strange!")

      try:
          #unique_display_name
          if display_name not in unique_identities_dict:
              unique_identities_dict.update({display_name: 1})
          else:
              occ=unique_identities_dict.get(display_name)
              unique_identities_dict.update({display_name: occ+1})
              if occ>multiple_tokens_with_same_id:
                  multiple_tokens_with_same_id=occ
                  multiple_tokens_with_same_id_example=display_name
          #unique_role_name
          if role not in unique_roles_dict:
              unique_roles_dict.update({role: 1})
          else:
              occ=unique_roles_dict.get(role)
              unique_roles_dict.update({role: occ+1})
          #unique_auth_name
          if auth_type not in unique_auth_type_dict:
              unique_auth_type_dict.update({auth_type: 1})
          else:
              occ=unique_auth_type_dict.get(auth_type)
              unique_auth_type_dict.update({auth_type: occ+1})
      except:
          print("unique_block exception")
      try:
          if "root" in policies:
              root_token=root_token+1
      except:
          print("checking root policy exception")
      try: 
          #print("life_span: ", life_span)
          #print("life_span.days: ", life_span.days)
          if life_span.days > NUMBER_OF_DAYS_FOR_A_TOKEN_BE_CONSIDERED_LONG_LIVED:
              long_lived_table.add_row([display_name, creation_time_date_type.strftime(date_display_format), expire_time_date_type.strftime(date_display_format), policies, accessor])
              if will_expire_in.days < NUMBER_OF_DAYS_FOR_A_LONG_LIVED_TOKEN_TO_NOTICE_EXPIRATION:
                  print("will_expire_in.days: ", will_expire_in.days)
                  long_lived_expiring_table.add_row([display_name, creation_time_date_type.strftime(date_display_format), expire_time_date_type.strftime(date_display_format), policies, accessor])
      except:
          print("long lived tokens block issue")
      try:
          if any(role in policies for role in HUMAN_ROLES):
              humans_table.add_row([display_name, creation_time_date_type.strftime(date_display_format), expire_time_date_type.strftime(date_display_format), policies, accessor])
              if (creation_time_date_type.weekday() not in WORK_DAYS) or (creation_time_date_type.hour not in WORK_HOURS):
                  outside_hours_table.add_row([display_name, creation_time_date_type.strftime(date_display_format), expire_time_date_type.strftime(date_display_format), policies, accessor])
          else:
              processes_table.add_row([display_name, creation_time_date_type.strftime("%A %d %B %Y-%H:%M:%S"), expire_time_date_type.strftime(date_display_format), policies, accessor])
      except:
          print("grouping tokens by policies. block exception")
    except:
        print("An exception occurred")
        try:
          print("raw_data: ", output['data'])
        except:
            print("couldnt show details of exception")
    #print("raw_data: ", output['data'])

for id in sorted(unique_identities_dict.keys()):
    unique_identities_table.add_row([id,unique_identities_dict.get(id)])
for role in sorted(unique_roles_dict.keys()):
    unique_roles_table.add_row([role,unique_roles_dict.get(role)])
for auth_type in sorted(unique_auth_type_dict.keys()):
    unique_auth_type_table.add_row([auth_type,unique_auth_type_dict.get(auth_type)])

#print(long_lived_expiring_table)
#print(humans_table)
#print(processes_table)
#print(long_lived_table)
#print(outside_hours_table)
#sortedx=x.get_string(sort_key=operator.itemgetter(1, 0), sortby="expire_time")

header1, table1 = get_data_from_prettytable(humans_table)
header2, table2 = get_data_from_prettytable(processes_table)
header3, table3 = get_data_from_prettytable(long_lived_table)
header4, table4 = get_data_from_prettytable(outside_hours_table)
header5, table5 = get_data_from_prettytable(unique_identities_table)
header6, table6 = get_data_from_prettytable(unique_roles_table)
header7, table7 = get_data_from_prettytable(unique_auth_type_table)
header8, table8 = get_data_from_prettytable(long_lived_expiring_table)

export_to_pdf(header1, table1,
              header2, table2,
              header3, table3, 
              header4, table4, 
              header5, table5, 
              header6, table6, 
              header7, table7,
              header8, table8,
              root_token)

report_and_monitor_to_slack(root_token,len(table8),multiple_tokens_with_same_id,str(multiple_tokens_with_same_id_example))
