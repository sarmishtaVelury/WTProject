from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import AddItemProperty, SetItemValues, AddPurchase
from recombee_api_client.api_requests import ItemBasedRecommendation, Batch, ResetDatabase
import random
import csv

PROBABILITY_PURCHASED = 0.1

client = RecombeeClient('wt-proj', 'gVEMJ5zdYOleXwlX4MyCtExwaa8MgAFgejz0W7TPa8kB1Qebtp1t0OvESDDdwrmO')

#Clear the entire database
client.send(ResetDatabase())

# We will use courses as items
# Courses have three properties
#   - domain (string)
#   - title (string)
#   - description (string)

# Add properties of items
client.send(AddItemProperty('domain', 'string'))
client.send(AddItemProperty('title', 'string'))
client.send(AddItemProperty('description', 'string'))

# Prepare requests for setting a catalog of courses

with open('courseCatalog.csv') as csvfile:
  csvreader = csv.reader(csvfile)
  for row in csvreader:
    requests = [SetItemValues(
      "course-%s" % row[0], #itemId
      #values:
      {
        'domain':row[1],
        'title':row[2],
        'description':row[3],
      },
      cascade_create=True   # Use cascadeCreate for creating item
                            # with given itemId if it doesn't exist
    )]

# Send catalog to the recommender system
client.send(Batch(requests))

# Prepare some purchases of items by users
requests = []


with open('purchase.csv') as csvfile:
  csvreader = csv.reader(csvfile)
  for row in csvreader:
    items = ["course-%s" % row[1]]
    users = ["user-%s" % row[0]]

for item_id in items:
    #Use cascadeCreate to create unexisting users
    purchasing_users = [user_id for user_id in users if random.random() < PROBABILITY_PURCHASED]
    requests += [AddPurchase(user_id, item_id, cascade_create=True) for user_id in purchasing_users]

# Send purchases to the recommender system
client.send(Batch(requests))

# Get 5 recommendations for user-42, who is currently viewing course-101
recommended = client.send(ItemBasedRecommendation('101', 5, target_user_id='user-42'))
print("Recommended items: %s" % recommended)
