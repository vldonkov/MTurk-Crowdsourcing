Required files:

1) 200623_Assignment_Part1_Code
2) HITLayout
3) Data_HIT_TextRelatedness
4) QualificationType_Question
5) QualificationType_AnswerKey


General instructions for creating tasks:

1) Please open 200623_Assignment_Part1_Code. The comments contain detailed explanations for the creation of the tasks
2) Make sure that you have an Amazon access key and have accounts for Amazon Mechanical Turk's Sandbox (both Worker and Requester websites)
3) Please enter the Access Key ID and the Secret Access Key in variables aws_access_key_id and aws_secret_access_key, respectively
4) You need to create a project containing the html code in HITLayout. You should put it in the Design Layout of the project. For more
	information please check https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_HITLayoutArticle.html
5) You need to enter the Layout ID (otained as shown in 
	https://docs.aws.amazon.com/AWSMechTurk/latest/AWSMturkAPI/ApiReference_HITLayoutArticle.html) in variable HITLayoutId
6) You need to read-in Data_HIT_TextRelatedness in variable df
7) You need to read-in QualificationType_Question in variable qual_question
8) You need to read-in QualificationType_AnswerKey in variable qual_answer
9) You need to read-in your Worker ID from the Worker's Sandbox website in variable WorkerID (for more info please check:
	https://blog.mturk.com/get-to-know-the-new-worker-site-4a69967d90c3#:~:text=You%20can%20always%20find%20your,to%20provide%20your%20Worker%20ID)
	You can ignore this step, if you also want to test the Master Task Qualification Test
10) Plase make sure that you have read-in the input for all the following variables:
	- aws_access_key_id
	- aws_secret_access_key
	- HITLayoutId
	- df
	- qual_question
	- qual_answer
	- (WorkerID)
11) You can now execute the whole code contained in 200623_Assignment_Part1_Code
