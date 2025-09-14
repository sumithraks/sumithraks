import csv
import time
import os
from openai import OpenAI
api_key=<set_api_key>
client = OpenAI(api_key=api_key)

#This takes a client handle, uploads the PDF and dumps out CSV
# TODO: If the file is already in CSV, ability to skip it
def processPDF(client, filename):
# Delete if already exists need to be find tuned.
    try:
        client.files.delete(filename)
    except:
        print("File not found")        

    file = client.files.create(
        file=open(filename, "rb"),
            purpose="user_data"
    )
    prompt="This is a credit card statement. Extract all transactions as a table with columns: ['date', 'description', 'amount']. Return the transactions in plain TSV format, including the header row. Enclose all fields in double quotes"
    response = client.responses.create(
        model="gpt-5",
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": file.id,
                        },
                        {
                            "type": "input_text",
                            "text": prompt,
                        },
                    ]
                }
            ]
    )

    return response

# This uses the CSV transactions and categorizes the same
def categorize(client, content):
    prompt='''You are a helpful assistant that categorizes credit card trabsactions.Focus on the meaning and ignore account numbers or reference codes. 
Only respond with a numbered list of categories, one per line. Categorize anything from HEAVEN GREENS as Groceries.
Categorize Preply as education. Categorize Payment as credit card payments. Categorize TAJ MAHAL SUNNYVALE CA as
Groceries.

Categorize the following 20 transactions into one of these categories:
- Rent
- Utilities 
- Transport
- Groceries
- Restaurants & Cafés
- Shopping
- Books & Education 
- Subscriptions
- Insurance
- Health & Hygiene 
- Education
- Travel
- Taxes 
- Credit card payments
- Other
'''
    response = client.responses.create(
        model="gpt-5",
            input=[
                {
                    "role": "system",
                    "content": [
                        {
                            "type": "input_text",
                            "text": prompt,
                        }
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": content,
                        }
                    ]
                },

            ]
    )   
    return response

#Get the input file
utilization=dict()
while(True): 
    input_file=input("Enter the complete file path for the file to process. Enter done if no more files:")
    if input_file.lower()=='done':
        break;
#TODO: Check if file exists before sending to openai
    response=processPDF(client,input_file)
    chatgpt_response = response.output_text
    lines = chatgpt_response.strip().split('\n')
    i=0
    begin_index=None
    end_index=None

#The output contains some verbose response. The actual CSV is between ''' and '''
#Identify the chunk
    for l in (lines):
        i=i+1
        if not l.startswith("```") and begin_index is None:
            begin_index=i
            continue;
        if l.startswith("```") and begin_index is not None:
            end_index=i
            break

    field_separator = "\t";
# Get the data rows and header rows separately
    header = lines[begin_index].split(field_separator) 
    data_rows = [line.split(field_separator) for line in lines[begin_index+1:end_index]]
    print(header)
    print(data_rows)
    i=0
    chunk=list()
    amounts=list()
    report=list()

#Categorize them using openai by sending chunks of 10
    for r in data_rows:
        if (len(r) >=3):
            description = r[1];
            chunk.append(description)
            amt = r[2].strip('\"')
            isdebit=True
            amt.strip()
            if amt.endswith("Dr."):
                amt.replace("Dr.","")
                isdebit=True
            elif amt.endswith("Cr."):
                amt.replace("Cr.","")
                isdebit=False
            amt = amt.replace("$","")
            amt = amt.replace(",","")
            amt=float(amt)
            if isdebit is not True:
                amt=-1*amt
            
            amounts.append(amt)
            if (len(chunk)==10):
                separator = "\n"
                to_categorize =separator.join(chunk) 
                response = categorize(client,to_categorize)
                output_text = response.output_text
                lines = output_text.strip().split('\n')
                for i in range(len(chunk)):
                    fields = lines[i].split(" ")
                    line_item = list()
                    line_item=[chunk[i].strip('\"'),fields[1],amounts[i]]
                    report.append(line_item)
                    utilization[fields[1]]=utilization.get(fields[1],0)+amounts[i]
                chunk.clear()
                amounts.clear()

    if (len(chunk)>0):
        separator = "\n"
        to_categorize =separator.join(chunk) 
        response = categorize(client,to_categorize)
        output_text = response.output_text
        lines = output_text.strip().split('\n')
        for i in range(len(chunk)):
            fields = lines[i].split(" ")
            line_item = list()
            line_item=[chunk[i].strip('\"'),fields[1],amounts[i]]
            report.append(line_item)
            utilization[fields[1]]=utilization.get(fields[1],0)+amounts[i]


#Use the input file's base name to form two files
# Tagging each transaction into categories 
# Sum of spend in each category
    filename = os.path.basename(input_file)
    categorized_report = "categorized_report_"+filename+".csv"
    with open(categorized_report, 'w', newline='\n') as csvfile:
        writer = csv.writer(csvfile,delimiter='\t')
        writer.writerows(report)

spend_by_categories = "spend_by_categories_"+time.time()+".csv"
file = open(spend_by_categories, 'w')
for key in utilization:
    file.write(key+","+str(utilization[key])+"\n")
file.close
