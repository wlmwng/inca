# Initialize INCA
import datetime
import os
from pprint import pprint

from inca import Inca

os.getcwd()
os.chdir("./inca")

myinca = Inca()  # get an instance of INCA
print(myinca.database.list_apps())  # see which apps already exist

# one time: create an app and add credentials
# myinca.clients.twitter2_remove_app("usright")
myinca.clients.twitter2_create_app()  # create a Twitter API v2 app
myinca.clients.twitter2_create_credentials(appname="usrightmedia")
# myinca.database.delete_doctype("tweets2")
myinca.clients.twitter2_timeline(
    app="usrightmedia",
    screen_name="LeaderMcConnell",
    start_time=datetime.datetime(2016, 1, 1, 0, 0, 0, 0, datetime.timezone.utc),
    end_time=datetime.datetime(2016, 2, 1, 0, 0, 0, 0, datetime.timezone.utc),
)
pprint(myinca.database.doctype_first("tweets2"))

# curl http://localhost:9200/_cat/indices?v
# curl -X DELETE "localhost:9200/inca?pretty"
# curl -X DELETE "localhost:9200/.credentials?pretty"
# curl -X DELETE "localhost:9200/.apps?pretty"
