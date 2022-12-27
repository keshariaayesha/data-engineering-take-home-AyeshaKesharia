# FetchRewardsTest

## Implementation Steps
I created a python file to process the json data files. I performed the below steps in this file:
1) Flattened the JSON data file and stored the processed data in a dataframe
2) Masked 'device_id' and 'ip' columns in such a way where it is easy for data analysts to identify duplicate values in those fields
3) The transformed dataframe is then stored in a postgresql table called user_logins using python script

## Implementation Procedure
We can read messages from the queue using boto3 client function. This helps us to connect to the AWS account and create a queue and pull the json file. I masked the columns using label encoder. I used this method because this is an excellent way to also identify duplicate values from the masked the data. The unmasking process is also easy, just use inverse_transform function at the receiver side and the data is decrypted back to its original form. 
The application will run on the AWS server since the SQS data queue is hosted on AWS. 


## Future scope
1) How would you deploy this application in production?

--> While deploying the application in production one should endure that the database is configured. Security is configured to avoid data breach issues. The application should be pushed to a package.

2) What other components would you want to add to make this production ready?

--> We can do automation testing on the application to ensure that the application is robust enough and does not break down more often. We can also add a user friendly website or dashboard where he/she can start and stop the entire ETL process or we can automate the entire process to run at regular intervals (daily/weekly,etc.) and the user can just invade in the process when there is an error in the process. 
There should also be a CI framework where new code can be integrated easily without much changes and user can also keep a track of the commit changes done to the framework. 

3) How can this application scale with a growing data set.

--> By using load balancers we can balance out the data. This would help scale the data and also avoid overloading issues when the dataset grows in size. Also, in order to avoid server downtime issues, we can use web proxy servers.

4) How can PII be recovered later on?

--> We can recover back the masked data using inverse_tranform function present in sklearn library.

