#!/usr/bin/env python3
import argparse
import json
import requests
import csv

class RestfulClient:
    BASE_URL = "https://jsonplaceholder.typicode.com"

    def __init__(self, method, endpoint, outfile):
        self.method = method
        self.endpoint = endpoint
        self.outfile = outfile

    def make_request(self):
        url = f"{self.BASE_URL}{self.endpoint}"
        response = None

        if self.method.lower() == 'get':
            response = requests.get(url)
        elif self.method.lower() == 'post':
            # For simplicity, let's just send an empty JSON payload for POST
            response = requests.post(url, json={})

        return response

    def process_response(self, response):
        print(f"HTTP Status Code: {response.status_code}")

        if not response.ok:
            print(f"Error: {response.text}")
            exit(1)

        if self.outfile:
            if self.outfile.endswith('.json'):
                with open(self.outfile, 'w') as json_file:
                    json.dump(response.json(), json_file, indent=2)
            elif self.outfile.endswith('.csv'):
                # For simplicity, let's just write the response as a CSV row
                with open(self.outfile, 'w', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(response.json().values())
        else:
            print(json.dumps(response.json(), indent=2))

def main():
    parser = argparse.ArgumentParser(description="Simple REST client for JSONPlaceholder.")
    parser.add_argument("METHOD", choices=["get", "post"], help="HTTP method (get or post)")
    parser.add_argument("ENDPOINT", help="URI fragment, e.g., /posts/1")
    parser.add_argument("--OUTFILE", help="Output file (JSON or CSV)")

    args = parser.parse_args()
    rest_client = RestfulClient(args.METHOD, args.ENDPOINT, args.OUTFILE)
    response = rest_client.make_request()
    rest_client.process_response(response)

if __name__ == "__main__":
    main()
