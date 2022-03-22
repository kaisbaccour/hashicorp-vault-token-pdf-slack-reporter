#!/usr/local/bin/python3

from datetime import date
import os
import time
import hvac
import urllib3
from prettytable import PrettyTable
import operator
from datetime import datetime

from slack_sdk import WebClient
from fpdf import FPDF

print("starting")

slack_token = os.environ["REPORTER_SLACK_BEARER"]
slack_channel = os.environ["SLACK_CHANNEL"]
slack_monitoring_channel = os.environ["SLACK_MONITORING_CHANNEL"]
kubernetes_auth_mountpoint = os.environ["KUBERNETES_AUTH_MOUNTPOINT"]
kubernetes_auth_role = os.environ["KUBERNETES_AUTH_ROLE"]

slack_client = WebClient(token=slack_token)

NOTIFY_SLACK= True
HUMAN_ROLES = ["developer", "admin", "root", "devops"]
NUMBER_OF_DAYS_FOR_A_TOKEN_BE_CONSIDERED_LONG_LIVED=7
WORK_DAYS=[0,1,2,3,4]
WORK_HOURS=[8,9,10,11,12,13,14,15,16,17,18]



def export_to_pdf(header1, table1, header2, table2, header3, table3,header4, table4, root_token):
    """
    Create a a table in PDF file from a list of row
        :param header: columns name
        :param data: List of row (a row = a list of cells)
        :param spacing=1:
    """
    
    pdf = FPDF()                                # New  pdf object
    pdf.set_font("Courier", size=12)
    pdf.set_fill_color(r=210,g=-1,b=-1)


    epw = pdf.w - 0.5*pdf.l_margin                # Witdh of document
    col_width = pdf.w / 5.5                     # Column width in table
    row_height = pdf.font_size * 1.5            # Row height in table
    spacing = 1.1                             # Space in each cell

    pdf.add_page()                              # add new page

    pdf.cell(epw, 0.0, 'Hashicorp Vault Token Report', align='C')   # create title cell
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, str(datetime.now().strftime("%A %d. %B %Y")), align='C')   # create title cell
    pdf.ln(row_height * spacing*3)
    pdf.set_font("Courier", size=10)

    pdf.cell(epw, 0.0, 'Total active tokens: '+str(len(table1)+len(table2)), align='A')   # create title cell
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Human tokens: '+str(len(table1)), align='A') 
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Processes tokens: '+str(len(table2)), align='A') 
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Long lived tokens: '+str(len(table3)), align='A') 
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Outside working hour tokens: '+str(len(table4)), align='A') 

    
    if root_token > 0:
      pdf.ln(row_height * spacing)
      pdf.set_text_color(r=255, g=20, b=20)
      pdf.cell(epw, 0.0, "Active Root tokens: " + str(root_token) + " token(s) !! ", align='A')
      pdf.ln(row_height * spacing)
    pdf.set_text_color(r=0)

    pdf.set_font("Courier", size=6)  # Font style
    pdf.ln(row_height*spacing)                  # Define title line style

####################OUTSIDE_WORKING_HOURS_TOKENS#################
    pdf.ln(h="aa")
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'Outside working hours tokens', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    for item in header4:                         # for each column
        pdf.cell(col_width, row_height*spacing, # Add a new cell
                 txt=item, border=1)
    pdf.ln(row_height*spacing)                  # New line after header

    for row in table4:                            # For each row of the table
        for item in row:                        # For each cell in row
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width, row_height*spacing, # Add cell
                      txt=item, border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
########################HUMAN_TOKENS##########

    pdf.ln(h="aa")
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'Human tokens', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")

    # Add header
    pdf.ln(row_height*spacing) 
    for item in header1:                         # for each column
        pdf.cell(col_width, row_height*spacing, # Add a new cell
                 txt=item, border=1)
    pdf.ln(row_height*spacing)                  # New line after header

    for row in table1:                            # For each row of the table
        for item in row:                        # For each cell in row
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width, row_height*spacing, # Add cell
                      txt=item, border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row

####################LONG_LIVED_TOKENS#################
    pdf.ln(h="aa")
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'Long lived tokens(+' +str(NUMBER_OF_DAYS_FOR_A_TOKEN_BE_CONSIDERED_LONG_LIVED)+"days)", align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    for item in header3:                         # for each column
        pdf.cell(col_width, row_height*spacing, # Add a new cell
                 txt=item, border=1)
    pdf.ln(row_height*spacing)                  # New line after header

    for row in table3:                            # For each row of the table
        for item in row:                        # For each cell in row
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width, row_height*spacing, # Add cell
                      txt=item, border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
########################



####################PROCESS_TOKENS#################
    pdf.ln(h="aa")
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'Processes tokens ', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    for item in header2:                         # for each column
        pdf.cell(col_width, row_height*spacing, # Add a new cell
                 txt=item, border=1)
    pdf.ln(row_height*spacing)                  # New line after header

    for row in table2:                            # For each row of the table
        for item in row:                        # For each cell in row
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width, row_height*spacing, # Add cell
                      txt=item, border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
########################




#Footer
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font(style="U", family="", size=9)
    pdf.cell(epw, 0.0,"https://github.com/kaisbaccour/hashicorp-vault-token-pdf-slack-reporter" , align='C') 
#######


    pdf.output('token-report.pdf')               # Create pdf file
    pdf.close()                                 # Close file
def get_data_from_prettytable(data):
    """
    Get a list of list from pretty_data table
    Arguments:
        :param data: data table to process
        :type data: PrettyTable
    """

    def remove_space(liste):
        """
        Remove space for each word in a list
        Arguments:
            :param liste: list of strings
        """
        list_without_space = []
        for mot in liste:                                       # For each word in list
            word_without_space = mot.replace(' ', '')           # word without space
            list_without_space.append(word_without_space)       # list of word without space
        return list_without_space

    # Get each row of the table
    string_x = str(data).split('\n')                               # Get a list of row
    header = string_x[1].split('|')[1: -1]                      # Columns names
    rows = string_x[3:len(string_x) - 1]                        # List of rows

    list_word_per_row = []
    for row in rows:                                            # For each word in a row
        row_resize = row.split('|')[1:-1]                       # Remove first and last arguments
        list_word_per_row.append(remove_space(row_resize))      # Remove spaces

    return header, list_word_per_row

urllib3.disable_warnings()

try:
    os.environ["VAULT_ADDR"]
except Exception:
    print("The VAULT_ADDR environment must be set.")
    os._exit(1)

#try:
#    os.environ["VAULT_TOKEN"]
#except Exception:
#    print("The VAULT_TOKEN environment must be set.")
#    os._exit(1)

with open('/var/run/secrets/kubernetes.io/serviceaccount/token', 'r') as file:
    k8s_jwt = file.read().replace('\n', '')

client = hvac.Client(url=os.environ['VAULT_ADDR'])
client.auth_kubernetes(role=kubernetes_auth_role, jwt=k8s_jwt,use_token=True, mount_point=kubernetes_auth_mountpoint)
payload = client.list('auth/token/accessors')
keys = payload['data']['keys']
processes_table = PrettyTable()
humans_table = PrettyTable()
long_lived_table = PrettyTable()
outside_hours_table = PrettyTable()
processes_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
humans_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
long_lived_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
outside_hours_table.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
starting=-1
ending=10000
root_token=0
now=datetime.now()
for idx,key in enumerate(keys):
    if idx == ending:
        break
    if idx < starting:
        continue
    try:
      output = client.lookup_token(key, accessor=True)
      if output['data']['display_name'] is not None:
        if len(output['data']['display_name']) > 34:
          display_name = output['data']['display_name'][ 0 : 33 ]
        else:
            display_name = output['data']['display_name']
      else:
          display_name = "undefined"
      creation_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(output['data']['creation_time']))
      if output['data']['expire_time'] is not None:
        if len(output['data']['expire_time']) > 24:
          expire_time = output['data']['expire_time'][ 0 : 23 ]
        else:
            expire_time = output['data']['expire_time']
      else:
          expire_time = "undefined"
      policies = str(output['data']['policies']).replace('\'default\'','').replace(',','+').replace('[+','').replace(']+','').replace('[','').replace(']','').replace('\'','').replace('++','')
      accessor = key
      try:
        expire_time_date_type = datetime.strptime(expire_time, '%Y-%m-%dT%H:%M:%S.%f')
        creation_time_date_type = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
      except:
          print("time parser error")
      will_expire_in=expire_time_date_type-now
      date_display_format="%A_%d_%B_%Y-%H:%M:%S"
      
      if "root" in policies:
          root_token=root_token+1
      if will_expire_in.days > NUMBER_OF_DAYS_FOR_A_TOKEN_BE_CONSIDERED_LONG_LIVED:
          long_lived_table.add_row([display_name, creation_time_date_type.strftime(date_display_format), expire_time_date_type.strftime(date_display_format), policies, accessor])
      if any(role in policies for role in HUMAN_ROLES):
          humans_table.add_row([display_name, creation_time_date_type.strftime(date_display_format), expire_time_date_type.strftime(date_display_format), policies, accessor])
          if (creation_time_date_type.weekday() not in WORK_DAYS) or (creation_time_date_type.hour not in WORK_HOURS):
              outside_hours_table.add_row([display_name, creation_time_date_type.strftime(date_display_format), expire_time_date_type.strftime(date_display_format), policies, accessor])
      else:
          processes_table.add_row([display_name, creation_time_date_type.strftime("%A %d %B %Y-%H:%M:%S"), expire_time_date_type.strftime(date_display_format), policies, accessor])
    except:
        print("An exception occurred")
        print(display_name)

print(humans_table)
print(processes_table)
print(long_lived_table)
print(outside_hours_table)
#sortedx=x.get_string(sort_key=operator.itemgetter(1, 0), sortby="expire_time")

header1, table1 = get_data_from_prettytable(humans_table)
header2, table2 = get_data_from_prettytable(processes_table)
header3, table3 = get_data_from_prettytable(long_lived_table)
header4, table4 = get_data_from_prettytable(outside_hours_table)
export_to_pdf(header1, table1, header2, table2, header3, table3, header4, table4, root_token)
payload = {"channels": "kibana_reports"}

headers = {"Authorization": "Bearer:$REPORTER_SLACK_BEARER"}

if NOTIFY_SLACK==True:
  response = slack_client.files_upload(
          channels=slack_channel,
          headers=headers,
          file="token-report.pdf",
          title="root-token-report"
         )
  if root_token>0:
    response_mon = slack_client.chat_postMessage(
            channel=slack_monitoring_channel,
            headers=headers,
            text="I found "+str(root_token)+" root active token(s) !",
           )

