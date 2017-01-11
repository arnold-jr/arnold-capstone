import requests

def make_request(url, outfile):
  with open(outfile, "w") as f:
    with requests.Session() as s:
      resp = s.get(url, stream=True)
      for line in resp.json()['features']:
        f.write(json.dumps(line) + "\n")


if __name__ == "__main__":
  url = "http://opendata.dc.gov/datasets/" + \
        "2acc75ccdd954267acecb8713b2b800a_28.geojson"
  outfile = "DATA/resp.json"
  make_request(url, outfile)
