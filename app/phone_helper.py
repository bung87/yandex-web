import os
import requests
import sys

ONLINE_SIM_API_KEY = os.environ.get("ONLINE_SIM_API_KEY","37532098140606ca3b549463c3a7d3dd")

def get_operations():
    url = "https://onlinesim.ru/api/getOperations.php"
    rep = requests.get(url,params= {"apikey":ONLINE_SIM_API_KEY})
    rep = rep.json()
    if isinstance(rep,dict):
        # rep["response"] == "ERROR_NO_OPERATIONS"
        return None
    elif isinstance(rep,list):
        return rep

def get_state(tzid):
    url = "https://onlinesim.ru/api/getState.php"
    rep = requests.get(url,params= {"apikey":ONLINE_SIM_API_KEY,"tzid":tzid,"message_to_code":1,"msg_list":1})
    rep = rep.json()
    return rep

def get_code(phone):
    operations = get_operations()
    phone_operations = filter( lambda x:x["number"] == phone,operations )
    phone_completed = filter(lambda x:x["response"] == "TZ_NUM_ANSWER",phone_operations)
    service = "Yandex" # "yandex"
    phone_service_completed = filter(lambda x:x["service"] == service,phone_completed)
    phone_service_completed = list(phone_service_completed)
    tzid  = phone_service_completed[0]["tzid"]
    status = get_state(tzid)
    code_list = list( filter(lambda x:x["service"] == service,status[len(status) - 1]["msg"] ) )
    code = code_list[len(code_list) - 1 ]["msg"]
    return code

if __name__ == "__main__":
    code = get_code(sys.argv[1])
    print(code)
