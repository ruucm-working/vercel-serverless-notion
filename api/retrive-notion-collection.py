from http.server import BaseHTTPRequestHandler
from notion.client import NotionClient
from urllib import parse
import json


class JsonPage:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class handler(BaseHTTPRequestHandler):

    def do_GET(self):

        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.send_header('Access-Control-Allow-Credentials', 'true')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET,OPTIONS,PATCH,DELETE,POST,PUT')
        self.send_header('Access-Control-Allow-Headers',
                         'X-CSRF-Token, X-Requested-With, Accept, Accept-Version, Content-Length, Content-MD5, Content-Type, Date, X-Api-Version')
        self.end_headers()

        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

        client = NotionClient(
            token_v2=dic["token_v2"])
        cv = client.get_collection_view(dic["collectionUrl"])

        collectionTitle = cv.collection.name
        collection_default = cv.default_query().execute()

        resultList = []

        for idx, page in enumerate(collection_default):
            jsonPage = JsonPage()
            jsonPage.title = page.title
            jsonPage.email = page.email
            jsonPage.profileImage = page.profileImage
            jsonStr = jsonPage.toJSON()

            resultList.append(jsonStr)

        resultListStr = "[" + ','.join(resultList) + "]"
        self.wfile.write(resultListStr.encode())
        return
