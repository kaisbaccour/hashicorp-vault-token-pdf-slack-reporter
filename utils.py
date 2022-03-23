from config import *
def export_to_pdf(header1, table1, 
                  header2, table2, 
                  header3, table3, 
                  header4, table4, 
                  header5, table5, 
                  header6, table6, 
                  header7, table7,
                  header8, table8,
                  root_token):
    from fpdf import FPDF
    from datetime import datetime,date
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
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Unique identities: '+str(len(table5)), align='A') 
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Unique roles: '+str(len(table6)), align='A') 
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Unique auth types: '+str(len(table7)), align='A') 
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Expiring long lived tokens: '+str(len(table8)), align='A')
    pdf.ln(row_height * spacing)
    pdf.cell(epw, 0.0, 'Root tokens: '+str(root_token), align='A')

    pdf.add_page()

    
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
    pdf.cell(epw, 0.0, 'Outside working hour tokens (humans)', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    for item in header4:                         # for each column
        pdf.cell(col_width, row_height*spacing, # Add a new cell
                 txt=item, border=1, align='C')
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
                      txt=item[ 0 : 33 ], border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
##################################


####################EXPIRING_TOKENS#################
    pdf.ln(h="aa")
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'Expiring Long lived tokens(expire in less than '+str(NUMBER_OF_DAYS_FOR_A_LONG_LIVED_TOKEN_TO_NOTICE_EXPIRATION)+'days)', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    for item in header8:                         # for each column
        pdf.cell(col_width, row_height*spacing, # Add a new cell
                 txt=item, border=1, align='C')
    pdf.ln(row_height*spacing)                  # New line after header

    for row in table8:                            # For each row of the table
        for item in row:                        # For each cell in row
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width, row_height*spacing, # Add cell
                      txt=item[ 0 : 33 ], border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
##################################


####################UNIQUE_TOKENS#################
    pdf.ln(h="aa") 
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'aggregate tokens', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    pdf.cell(col_width*3.5, row_height*spacing,txt=header5[0], border=1)
    pdf.cell(col_width*0.5, row_height*spacing,txt=header5[1], border=1)
    pdf.ln(row_height*spacing)                  

    for row in table5:                            # For each row of the table
        col=0
        for item in row:                        # For each cell in row
            if col==0:
                col_witdh_ratio=3.5
                col=1
            elif col==1:
                col_witdh_ratio=0.5
                col=0
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width*col_witdh_ratio, row_height*spacing, # Add cell
                      txt=item, border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
##################################

####################UNIQUE_AUTH_TYPES#################
    pdf.ln(h="aa") 
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'aggregate auth types', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    pdf.cell(col_width*3.5, row_height*spacing,txt=header7[0], border=1)
    pdf.cell(col_width*0.5, row_height*spacing,txt=header7[1], border=1)
    pdf.ln(row_height*spacing)                  

    for row in table7:                            # For each row of the table
        col=0
        for item in row:                        # For each cell in row
            if col==0:
                col_witdh_ratio=3.5
                col=1
            elif col==1:
                col_witdh_ratio=0.5
                col=0
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width*col_witdh_ratio, row_height*spacing, # Add cell
                      txt=item, border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
##################################

####################UNIQUE_ROLES#################
    pdf.ln(h="aa") 
    pdf.set_text_color(r=0, g=0, b=255)
    pdf.set_font("Courier", size=12,style="B")
    pdf.cell(epw, 0.0, 'aggregate roles', align='C') 
    pdf.set_text_color(r=0)
    pdf.set_font("Courier", size=6,style="")
    # Add header
    pdf.ln(row_height*spacing)  
    pdf.cell(col_width*3.5, row_height*spacing,txt=header6[0], border=1)
    pdf.cell(col_width*0.5, row_height*spacing,txt=header6[1], border=1)
    pdf.ln(row_height*spacing)                  

    for row in table6:                            # For each row of the table
        col=0
        for item in row:                        # For each cell in row
            if col==0:
                col_witdh_ratio=3.5
                col=1
            elif col==1:
                col_witdh_ratio=0.5
                col=0
            if "developer" in item:
              pdf.set_text_color(r=0, g=0, b=255)
            if "admin" in item:
              pdf.set_text_color(r=0, g=255, b=0)
            if "root" in item:
              pdf.set_text_color(r=255, g=0, b=0)
              pdf.set_font(style="B", family="", size=9)
            pdf.cell(col_width*col_witdh_ratio, row_height*spacing, # Add cell
                      txt=item, border=1,fill=True)
            pdf.set_text_color(r=0)
            pdf.set_font(style="", family="",size=6)
        pdf.ln(row_height*spacing)              # Add line at the end of row
    pdf.ln(h="aa")
#############################################


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
                 txt=item, border=1, align='C')
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

####################################################


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
                 txt=item, border=1, align='C')
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
                 txt=item, border=1, align='C')
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

def report_and_monitor_to_slack(root_token_number,expiring_long_lived_token,multiple_tokens_with_same_id,multiple_tokens_with_same_id_example):
    from slack_sdk import WebClient
    headers = {"Authorization": "Bearer:$REPORTER_SLACK_BEARER"}
    slack_client = WebClient(token=SLACK_TOKEN)
    if NOTIFY_SLACK==True:
      response = slack_client.files_upload(
              channels=SLACK_REPORT_CHANNEL,
              headers=headers,
              file="token-report.pdf",
              title="root-token-report"
             )
      if root_token_number>0:
        response_mon = slack_client.chat_postMessage(
                channel=SLACK_MONITORING_CHANNEL,
                headers=headers,
                text="I found "+str(root_token_number)+" root active token(s) !",
               )
      if expiring_long_lived_token>0:
        response_mon = slack_client.chat_postMessage(
                channel=SLACK_MONITORING_CHANNEL,
                headers=headers,
                text="I found "+str(expiring_long_lived_token)+" expiring long lived token(s) !",
               )
      if multiple_tokens_with_same_id>ALERT_THRESHOLD_ON_SAME_ID_HAVING_MANY_TOKENS:
        response_mon = slack_client.chat_postMessage(
                channel=SLACK_MONITORING_CHANNEL,
                headers=headers,
                text="I found "+
                str(multiple_tokens_with_same_id)+
                " tokens with the same id. Example: "+
                multiple_tokens_with_same_id_example+
                ". There might me more of them so check the generated report !"
               )
    