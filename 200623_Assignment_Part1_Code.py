import boto3
import pandas as pd

# Access key information for connecting to Amazon Mechanical Turk (MTurk). Instructions for obtaining an access key and
# connecting to MTurk can be found here: https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMechanicalTurkGettingStartedGuide/SetUp.html
aws_access_key_id = 'xxx'
aws_secret_access_key = 'xxx'

# All HITs in this code are being created in the free-to-use Sandbox. To manage the HITs as a requester, you can access the
# the Sandbox requester website: https://requestersandbox.mturk.com/mturk/manageHITs. To work on the created HITs, you can
# go to the Sandbox worker website: https://workersandbox.mturk.com/mturk/preview
create_hits_in_live = False

environments = {
        "live": {
            "endpoint": "https://mturk-requester.us-east-1.amazonaws.com",
            "preview": "https://www.mturk.com/mturk/preview",
            "manage": "https://requester.mturk.com/mturk/manageHITs",
            "reward": "0.00"
        },
        "sandbox": {
            "endpoint": "https://mturk-requester-sandbox.us-east-1.amazonaws.com",
            "preview": "https://workersandbox.mturk.com/mturk/preview",
            "manage": "https://requestersandbox.mturk.com/mturk/manageHITs",
            "reward": "0.05"
        },
}
mturk_environment = environments["live"] if create_hits_in_live else environments["sandbox"]

# Create a session to MTurk
session = boto3.Session()
client = session.client(
    service_name='mturk',
    region_name='us-east-1',
    endpoint_url=mturk_environment['endpoint'],
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
)

# Test that you can connect to the API by checking your account balance. The account balance in the Sandbox should always
# be 10000.00
user_balance = client.get_account_balance()
print ("Your account balance is {}".format(user_balance['AvailableBalance']))

# Description of the text relatedness HITs
description_tr= "A simple text relatedness task that asks you to evaluate whether one text/sentence describes anoter. " \
                "Completing all tasks in the batch will allow you to see the origin of the texts used in the task. " \
                "Please use the Chrome browser if possible."

# You need to create a HITLayoutID to generate HITs. For that, please check:
# https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_HITLayoutArticle.html
# The HTML code for the HIT Layout is contained in HITLayout.html

# Requirements for discovering, previewing and accepting the text relatedness HITs. The requirements are:
# a. The worker has had at least 80% of submitted assignments approved
# b. The worker has had more than 50 submitted assignments approved
# c. The worker is based in the USA
# b. and c. have been disabled in the code, in order to be able to access and test the created HITs.
worker_requirements_hit = [
    {
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [80],
    'ActionsGuarded': 'DiscoverPreviewAndAccept',
}
#     ,
#     {
#     'QualificationTypeId': '00000000000000000040',
#     'Comparator': 'GreaterThan',
#     'IntegerValues': [50],
#     'ActionsGuarded': 'DiscoverPreviewAndAccept',
# }
#     ,
#     {
#     'QualificationTypeId': '00000000000000000071',
#     'Comparator': 'EqualTo',
#     'LocaleValue': {'Country':'US'},
#     'ActionsGuarded': 'DiscoverPreviewAndAccept',
# }
]

# Read-in input data for the text relatedness HITs batch (contained in Data_HIT_TextRelatedness)
df = pd.read_csv("xxx)

# Store created batch of HIT IDs in an array (for future reference, if needed)
hit_id_arr=[]

# Create text relatedness HITs batch
i=0
while i < len(df.index):
    response = client.create_hit(
        MaxAssignments=9,
        LifetimeInSeconds=7200,
        AssignmentDurationInSeconds=150,
        Reward=mturk_environment['reward'],
        Title='Text relatedness',
        Keywords='text, relatedness, emotion, sentiment, easy',
        Description=description_tr,
        HITLayoutId='xxx',
        HITLayoutParameters=[{'Name': 'Text1','Value': df.Text1[i]},
                             {'Name': 'Text2','Value': df.Text2[i]},
                             {'Name': 'Hint','Value': str(df.Hint[i])},],
        QualificationRequirements=worker_requirements_hit,
    )
    hit_id = response['HIT']['HITId']
    print("\nCreated HIT: {}".format(hit_id))
    hit_id_arr.append(hit_id)
    i+=1

# Access the created HITs and manage the results
hit_type_id = response['HIT']['HITTypeId']
print ("\nYou can work the HITs here:")
print (mturk_environment['preview'] + "?groupId={}".format(hit_type_id))

print ("\nAnd see results here:")
print (mturk_environment['manage'])

# Description of qualification type
description_qt = "Answering the question in this Qualification Test correctly will allow you to access the Extra Task and " \
                 "find out the name of the social platform from the text relatedness tasks. You can repeat the Test in 10 " \
                 "minutes, if you have submitted a wrong answer."

# Read-in input data for the question in the qualification type. The question is based on the collected
# number keys (data field "Hint") from the previously created text relatedness HITs
qual_question = open("xxx","r").read()

# Read-in input data for the answer key of the question. Answering the question correctly ("100") will
# give you the qualification and allow you to see the name of the social platform in the Extra Task HIT
qual_answer = open("xxx","r").read()

# Create qualification type
qual_response = client.create_qualification_type(
    Name='Extra Task Qualification',
    Keywords='text relatedness, popular social platform, Extra Task',
    Description=description_qt,
    QualificationTypeStatus='Active',
    RetryDelayInSeconds=600,
    Test=qual_question,
    AnswerKey=qual_answer,
    TestDurationInSeconds=90
)

# # Grant yourself the qualification. To do that, you need to put in your unique "WorkerID". You can find it at the top left
# # of the Worker's site: https://workersandbox.mturk.com/mturk/preview. For more information see here:
# # https://blog.mturk.com/get-to-know-the-new-worker-site-4a69967d90c3#:~:text=You%20can%20always%20find%20your,to%20provide%20your%20Worker%20ID
# client.associate_qualification_with_worker(
#     QualificationTypeId = qual_response['QualificationType']['QualificationTypeId'],
#     WorkerId = "xxx",
#     IntegerValue = 1,
#     SendNotification = False
# )

# Description of the Extra Task
description_ET= "This task contains the answer to the voluntary question from the text relatedness tasks. You need to pass " \
                "the Extra Task Qualification in order to access the task."

# Creating the HIT Layout for the Extra Task
html ="""
<script src="https://assets.crowd.aws/crowd-html-elements.js"></script>

<crowd-form answer-format="flatten-objects">

    <p>
      The sentences were taken from:
    </p>
    
    <p>
        <strong>Twitter!</strong>
    </p>

    <p><img src="https://praxistipps-images.chip.de/MniEw17MQa7NmiQEYdGjZASiJgw=/0x0/filters:format(jpeg):fill(fff,true):no_upscale()/praxistipps.s3.amazonaws.com%2Ftwitter-das-logo_2d8e3b65.png" 
    style="max-width: 100%; max-height: 250px" /></p>
    
    <p>
      Thank you very much for completing all text relatedness tasks!!!
    </p>

</crowd-form>"""

HITLayout_XML = """
<HTMLQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2011-11-11/HTMLQuestion.xsd">
   <HTMLContent>
        <![CDATA[<!DOCTYPE html>""" + html + """]]>
   </HTMLContent>
   <FrameHeight>0</FrameHeight>
</HTMLQuestion>"""

# Requirements for previewing and accepting the Extra Task and seing the answer. The requirements are the same as for the
# text relatedness tasks, plus the successful completion of the Extra Task Qualification Test.
worker_requirements_hit_ET = [
    {
    'QualificationTypeId': '000000000000000000L0',
    'Comparator': 'GreaterThanOrEqualTo',
    'IntegerValues': [80],
    'ActionsGuarded': 'DiscoverPreviewAndAccept',
}
#     ,
#     {
#     'QualificationTypeId': '00000000000000000040',
#     'Comparator': 'GreaterThan',
#     'IntegerValues': [50],
#     'ActionsGuarded': 'DiscoverPreviewAndAccept',
# }
#     ,
#     {
#     'QualificationTypeId': '00000000000000000071',
#     'Comparator': 'EqualTo',
#     'LocaleValue': {'Country':'US'},
#     'ActionsGuarded': 'DiscoverPreviewAndAccept',
# }
,
{
    'QualificationTypeId': qual_response['QualificationType']['QualificationTypeId'],
    'Comparator': 'EqualTo',
    'IntegerValues': [1],
    'ActionsGuarded': 'PreviewAndAccept',
}
]

# Create Extra Task
response_ET = client.create_hit(
    MaxAssignments=9,
    LifetimeInSeconds=7200,
    AssignmentDurationInSeconds=60,
    Reward='0.00',
    Title='Extra Task',
    Keywords='text relatedness, social platform, Extra Task, answer',
    Description=description_ET,
    Question=HITLayout_XML,
    QualificationRequirements=worker_requirements_hit_ET,
)

# Access the created HIT
hit_id_ET = response_ET['HIT']['HITId']
print("\nCreated HIT: {}".format(hit_id_ET))

hit_type_id_ET = response_ET['HIT']['HITTypeId']
print ("\nYou can access the HIT here:")
print (mturk_environment['preview'] + "?groupId={}".format(hit_type_id_ET))