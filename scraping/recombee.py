from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
import csv

client = RecombeeClient('wt', '0IHcpVHDwnsQHZBytn9x77SobNPSsepNFbDdC6iSyLmoYLc7CfBK9uAJo37DhNpm')

# purchases = []

# with open('purchaseRecord.csv') as csvfile:
# 	csvreader = csv.reader(csvfile)
# 	for row in csvreader:
# 		user_id = row[0]
# 		item_id = row[1]
# 		r = AddPurchase(user_id, item_id)
# 		purchases.append(r)

# br = Batch(purchases)
# client.send(br)

recommended = client.send(UserBasedRecommendation('user-0', 5))
print(recommended)