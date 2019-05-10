

import sys, getopt
import os
import requests
from requests.auth import HTTPBasicAuth
import json
import sys

def main():
    # ticketId = "3641988"
    # ticketId = "2439461"
    username = "jenkinsuser"
    password = '5cM_NW7:z#xVp5'

    ticketId = str(sys.argv[1])
    resolutionTypeId = str(sys.argv[2])
    issueTypeId = str(sys.argv[3])
    resolutionSummary = str(sys.argv[4])

    ur11 = "https://ipcloud.tatacommunications.com/itsmv1/api/ui/v1/incident/details/" + ticketId
    ur12 = "https://ipcloud.tatacommunications.com/itsmv1/api/ui/v1/incident/" + ticketId+"/resolve"

    response = requests.get(url=ur11  ,auth=HTTPBasicAuth(username, password))
    if (response.status_code == 200):
        response_etag = response.headers["ETag"]
        request = {"resolutionTypeId":resolutionTypeId,"resolutionSummary":resolutionSummary,"issueTypeId":issueTypeId,"slaBreachReason":"","slaBreachComments":"","problemId":None ,"createdBy":"admin"}
        headers = {'Content-type': 'application/json', 'Accept': 'application/json', 'If-None-Match': response_etag}
        # {"requestId":"edbdc7a5-fc39-424a-aa02-9489f4d5f518compilers1.PNG","containerId":1,"fileName":"compilers1.PNG"}
        requests3 = requests.post(ur12, headers=headers, data=json.dumps(request),
                                  auth=HTTPBasicAuth(username, password))
        if (requests3.status_code == 200):
            print (requests3.json().get('message'))

    else:
        print ("Error while Fetching the Ticket Details  ")
        print ("Info : Args = TicketId  resolutionTypeId  issueTypeId  resolutionSummary")


if __name__ == "__main__":
    main()
