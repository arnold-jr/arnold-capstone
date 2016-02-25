import simplejson as json
from requests import Session, Request
import re

def get_zip_and_lat_lng(google_api_key, q_address):
  ''' Given an unformatted query_address, return the zipcode
  and lat_lng string for the geocoded address'''

  q_address = q_address + ", Washington, DC"
  f_address = re.sub(r'\s+',r'+',q_address.strip()) 

  print f_address
  with Session() as s:
    r = s.get("https://maps.googleapis.com/maps/api/geocode/json",
            params={"key":google_api_key,"address":f_address}
        )
  
  if r.json()['status'] == "OK":
    res = r.json()['results'][0]

    out_address = res["formatted_address"]
    zipcode = out_address[-10:-5] 
    lat_lng = ",".join((str(x) for x in res["geometry"]["location"].values()))

  else:
    print json.dumps(r.json(), indent=4)
    out_address = "Invalid Address Specified"
    zipcode = "-42"
    lat_lng = "-42"
    
  return lat_lng, zipcode, out_address 

if __name__ == "__main__":
  address = "3801 Connecticut Ave NW, Washington DC"
  print get_zip_and_lat_lng(address)
  
  address = "a;lsdkfj;alkjs;"
  print get_zip_and_lat_lng(address)
