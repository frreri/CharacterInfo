import requests

pts_url = "http://api.pts.se/PTSNumberService/Pts_Number_Service.svc/json/"


def op_search(msisdn):
    number = str(msisdn)
    if number.startswith("46"):
        pts_number = number[2:][:2] + "-" + number[2:]
    elif number[:3] in ["070", "072", "073", "076", "079"]:
        pts_number = number[:3][1:] + "-" + number[3:]
    else:
        return "Fel format!"
    r = requests.get(pts_url + "SearchByNumber?number=" + pts_number)
    resultat = r.json()
    return resultat["d"]["Name"]
