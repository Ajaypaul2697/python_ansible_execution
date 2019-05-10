import sys, getopt
import os
import requests
from requests.auth import HTTPBasicAuth
import json
import sys

from datetime import datetime, timedelta




def main():
    username = "jenkinsuser"
    password = '5cM_NW7:z#xVp5'
    resolvergroup_value = str(sys.argv[1])
    ur11 = "https://ipcloud.tatacommunications.com/itsmv1/api/ui/v1/ticket/search/advanced?size=500&page=0&sort=id,DESC"
    N = 1
    date_N_days_ago = datetime.now() - timedelta(days=N)
    less_than =  datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    greater_than = date_N_days_ago.strftime("%Y-%m-%d %H:%M:%S")
    request = {"params":[{"field":"resolvergroup","value":resolvergroup_value,"operation":"IN"},{"field":"type","value":"1","operation":"IN"},{"field":"ticketCategory","value":"PROACTIVE","operation":"IN"},{"field":"priority","value":3,"operation":"IN"},{"field":"status","values":["NEW","ASSIGN"],"operation":"IN"},{"field":"createdTime","value":greater_than,"operation":"GREATER_THAN"},{"field":"createdTime","value":less_than,"operation":"LESS_THAN"}],"selects":["id","description","lastUpdateTime","reportedIssueType"]}
    data = json.dumps(request)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    requests2 = requests.post(ur11, headers=headers, data=data,
                              auth=HTTPBasicAuth(username, password))
    lisofticketswithdetails = []
    lisoftickets = []
    if (requests2.status_code == 200):
        lisoftickets = requests2.json().get("data").get("tickets")
        if len(lisoftickets) == 0 :
            print ("No Tickets Found")
        for i in lisoftickets:

            ticket = {}
            ticketId=str(i.get("id"))
            ticket["TicketId"] = ticketId
            ticket["Description"] =i.get("description")
            ticket["LastUpdateTime"]=i.get("lastUpdateTime")
            ticket["ReportedIssueType"]=i.get("reportedIssueType")

            url2 =  "https://ipcloud.tatacommunications.com/itsmv1/api/ui/v1/incident/details/"+ ticketId
            response2 = requests.get(url=url2  ,auth=HTTPBasicAuth(username, password))
            if (response2.status_code == 200):
                ticket["osType"]= response2.json().get("data").get("primaryCi").get("ostype")
                ticket["customerName"]=response2.json().get("data").get("customerName")
                ticket["mdba"] = response2.json().get("data").get("primaryCi").get("mdba")
                ticket["category"]=response2.json().get("data").get("primaryCi").get("category")
                lisofticketswithdetails.append(ticket)

        for j in lisofticketswithdetails:
            print ("--------------------------")
            print("customerName :" ,j["customerName"])
            print("TicketID :" ,j["TicketId"])
            print("Category :" ,j["category"])
            print("IssueType :" ,j["ReportedIssueType"])
            print("LastUpdatedTime :" ,j["LastUpdateTime"])
            print("Description :" ,j["Description"])
            print("OSType :" ,j["osType"])
            print("MDBA :" ,j["mdba"])

    else:
        print ("Error while Searching the Tickets  ")
        print ("Info : Args = resolvergroup  ")
        print (requests2.content)


if __name__ == "__main__":
    main()
