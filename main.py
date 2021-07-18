#!/usr/local/bin/python3

import os
import time
import hvac
import urllib3
from prettytable import PrettyTable
import operator

from slack_sdk import WebClient
from fpdf import FPDF

print("starting")

slack_token = os.environ["REPORTER_SLACK_BEARER"]
slack_channel = os.environ["SLACK_CHANNEL"]
slack_monitoring_channel = os.environ["SLACK_MONITORING_CHANNEL"]

slack_client = WebClient(token=slack_token)

NOTIFY_SLACK= True


def export_to_pdf(header, data, root_token):
    """
    Create a a table in PDF file from a list of row
        :param header: columns name
        :param data: List of row (a row = a list of cells)
        :param spacing=1:
    """
    pdf = FPDF()                                # New  pdf object
    pdf.set_font("Arial", size=12)


    epw = pdf.w - 0.5*pdf.l_margin                # Witdh of document
    col_width = pdf.w / 5.5                     # Column width in table
    row_height = pdf.font_size * 1.5            # Row height in table
    spacing = 1.1                             # Space in each cell

    pdf.add_page()                              # add new page

    pdf.cell(epw, 0.0, 'Active token-report: '+str(len(data)) + " tokens", align='C')   # create title cell
    if root_token > 0:
      pdf.ln(row_height * spacing)
      pdf.set_text_color(r=255, g=20, b=20)
      pdf.cell(epw, 0.0, "Active Root tokens: " + str(root_token) + " token(s) !! ", align='A')
    pdf.set_text_color(r=0)

    pdf.set_font("Arial", size=6)  # Font style
    pdf.ln(row_height*spacing)                  # Define title line style

    # Add header
    for item in header:                         # for each column
        pdf.cell(col_width, row_height*spacing, # Add a new cell
                 txt=item, border=1)
    pdf.ln(row_height*spacing)                  # New line after header

    for row in data:                            # For each row of the table
        for item in row:                        # For each cell in row
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width, row_height*spacing, # Add cell
                      txt=item, border=1)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
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
    string_x = str(x).split('\n')                               # Get a list of row
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
client.auth_kubernetes(role='$KUBERNETES_AUTH_ROLE', jwt=k8s_jwt,use_token=True, mount_point='$KUBERNETES_AUTH_MOUNTPOINT')
payload = client.list('auth/token/accessors')
keys = payload['data']['keys']
x = PrettyTable()
x.field_names = ["Display Name", "Creation Time", "Expiration Time", "Policies", "Token Accessor"]
starting=-1
ending=10000
root_token=0
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
      policies = output['data']['policies']
      accessor = key
      if "root" in policies:
          root_token=root_token+1
          print(idx, "/", len(keys), "printed")
          x.add_row([display_name, creation_date, expire_time, policies, accessor])
    except:
        print("An exception occurred")

print(type(x))
print(x)
sortedx=x.get_string(sort_key=operator.itemgetter(1, 0), sortby="expire_time")

header, data = get_data_from_prettytable(sortedx)
export_to_pdf(header, data,root_token)
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
