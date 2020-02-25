import boto3

MTURK_SANDBOX = 'https://mturk-requester-sandbox.us-east-1.amazonaws.com' #Must change out if real run is needed, instructions at bottom
mturk = boto3.client('mturk',
   aws_access_key_id = "INSERT", #INSERT
   aws_secret_access_key = "INSERT", #INSERT
   region_name='us-east-1',
   endpoint_url = MTURK_SANDBOX #Must comment out if real run is needed
)
print("I have $" + mturk.get_account_balance()['AvailableBalance'] + " in my Sandbox account")

question = open(file='questions.xml',mode='r').read()
new_hit = mturk.create_hit(
    Title = 'Rate newsworthiness of sentences',
    Description = 'Recording the newsworthiness of statements in the US Congressional Record',
    Keywords = 'news, newsworthy, United States, fact checking',
    Reward = '0.3',
    MaxAssignments = 3,
    LifetimeInSeconds = 86400,
    AssignmentDurationInSeconds = 900,
    AutoApprovalDelayInSeconds = 259200,
    Question = question,
)
print("A new HIT has been created. You can preview it here:")
print("https://workersandbox.mturk.com/mturk/preview?groupId=" + new_hit['HIT']['HITGroupId'])
print("HITID = " + new_hit['HIT']['HITId'] + " (Use to Get Results)")
# Remember to modify the URL above when you're publishing
# HITs to the live marketplace.
# Use: https://worker.mturk.com/mturk/preview?groupId=
