import json
import requests
from django.conf import settings


def getembedinfo(config, accesstoken):
    """Returns Embed token and Embed Url"""

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {accesstoken}",
        }
        report_url = f"https://api.powerbi.com/v1.0/myorg/groups/{config.WORKSPACE_ID}/reports/{config.REPORT_ID}"

        apiresponse = None

        try:
            apiresponse = requests.get(report_url, headers=headers)
            if settings.DEBUG:
                print("Embed url Request ID: ", apiresponse.headers.get("RequestId"))
        except Exception as ex:
            raise Exception("Error while retrieving reports Embed url!\n")

        if not apiresponse:
            raise Exception(
                "Error while retrieving reports Embed Url\n"
                + apiresponse.reason
                + "\nRequestId: "
                + apiresponse.headers.get("RequestId")
            )

        try:
            apiresponse = json.loads(apiresponse.text)
            embed_url = apiresponse["embedUrl"]
            dataset_id = apiresponse["datasetId"]
        except Exception as ex:
            raise Exception(f"Error while extracting Embed Url from API response!\n")

        # Get embed token
        embedtoken_url = "https://api.powerbi.com/v1.0/myorg/GenerateToken"
        body = {"datasets": []}
        if dataset_id != "":
            body["datasets"].append({"id": dataset_id})

        if config.REPORT_ID != "":
            body["reports"] = []
            body["reports"].append({"id": config.REPORT_ID})

        if config.WORKSPACE_ID != "":
            body["targetWorkspaces"] = []
            body["targetWorkspaces"].append({"id": config.WORKSPACE_ID})

        apiresponse = None

        try:
            # Generate Embed token for multiple workspaces, datasets, and reports
            apiresponse = requests.post(
                embedtoken_url, data=json.dumps(body), headers=headers
            )
            if settings.DEBUG:
                print("Embed token Request ID: ", apiresponse.headers.get("RequestId"))
        except:
            raise Exception("Error while invoking Embed token REST API endpoint\n")

        if not apiresponse:
            raise Exception(
                "Error while retrieving report Embed Url\n"
                + apiresponse.reason
                + "\nRequestId: "
                + apiresponse.headers.get("RequestId")
            )

        try:
            apiresponse = json.loads(apiresponse.text)
            embedtoken = apiresponse["token"]
            embedtoken_id = apiresponse["tokenId"]
            tokenexpiry = apiresponse["expiration"]
            if settings.DEBUG:
                print("Embed token expires on: ", tokenexpiry)
                print("Embed token ID: ", embedtoken_id)
        except Exception as ex:
            raise Exception(
                "Error while extracting Embed token from API response!\n"
                + apiresponse.reason
            )

        response = {
            "accessToken": embedtoken,
            "embedUrl": embed_url,
            "tokenExpiry": tokenexpiry,
        }
        return response
    except Exception as ex:
        return {"error_message": str(ex), "status": 500}
