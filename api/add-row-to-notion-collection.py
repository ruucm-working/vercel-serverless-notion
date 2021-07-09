from http.server import BaseHTTPRequestHandler
from notion.client import NotionClient
import json


class JsonPage:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class handler(BaseHTTPRequestHandler):

    def do_POST(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET,OPTIONS,PATCH,DELETE,POST,PUT')
        self.send_header('Access-Control-Allow-Headers',
                         'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version')
        self.end_headers()

        post_body = self.rfile.read(int(self.headers['content-length']))
        bodyStr = post_body.decode("utf-8")
        dic = json.loads(bodyStr)

        client = NotionClient(dic['notion']['token_v2'])
        cv = client.get_collection_view(dic['notion']['collectionUrl'])

        row = cv.collection.add_row()

        for key, item in dic["properties"].items():
            setattr(row, key,  item["value"])

        return
