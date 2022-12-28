# AWS IoT Incident Response Automation Example #

This example code, deployed as an AWS Serverless Application Model (SAM) template, demonstrates how to automate the response to security incidents for AWS IoT managed devices using AWS IoT Device Defender and AWS Systems Manager (SSM) Incident Manager, as described in the associated [AWS IoT Blog Post](https://aws.amazon.com/blogs/iot/enable-compliance-and-mitigate-iot-risks-with-automated-incident-response/). 

## Deployment Steps for Automated Solution ##

This section reviews the steps to implement the example solution using AWS CloudFormation.

### Setup AWS Systems Manager (SSM) Incident Manager ###

Suppose this is the first time using SSM Incident Manager in the account you will be deploying this solution. In that case, you must follow these steps to [configure the service](https://docs.aws.amazon.com/incident-manager/latest/userguide/disaster-recovery-resiliency.html).

1. Open the [Incident Manager console](https://console.aws.amazon.com/systems-manager/incidents/home)
2. On the Incident Manager service homepage, select **Get prepared**.
3. Choose **General settings**.
4. Read the onboarding acknowledgment. If you agree to Incident Manager's terms and conditions, check the **I have read and agree to the AWS Systems Manager Incident Manager terms and conditions** checkbox. Then select **Next**.
5. Set up the replication using either an AWS Owned or a Customer Managed AWS Key Management Service (AWS KMS) key. All Incident Manager resources are encrypted. To learn more about how your data is encrypted, see Data Protection in Incident Manager. See Using the Incident Manager replication set for more information about your replication set.
 - If you want to use the AWS Owned key, choose **Use AWS owned key**, and then choose **Create**.
 - If you want to use a Customer Managed AWS KMS key, choose **Choose a different AWS KMS key (advanced)**.
    - Your current Region appears as the first Region in your replication set. Search for an AWS key in our account. If you have not created a key or need to create a new one, select the **Create an AWS KMS key** button.
    - To add more Regions to your replication set, choose **Add Region**.
6. Select the Create button to create your replication set and contacts. To learn more about replication sets and resiliency, see Resilience in AWS Systems Manager Incident Manager.

### Create an AWS Simple Systems Manager (SSM) Contact ###

1. After logging into an AWS account with the appropriate permissions, go to the [AWS Systems Manager Incident Manager console](https://console.aws.amazon.com/systems-manager/incidents/home)
2. Select **Contacts**, and then select **Create contact**
    - Choose the **Create Contact** button.
    - Type the full name of the contact and provide a unique and identifiable alias.
    - Define a **Contact channel**. We recommend having two or more different types of contact channels.
        - Choose the type: email, SMS, or voice.
        - Enter an identifiable name for the contact channel.
        - Provide the contact channel details, such as email
    - Define the **Engagement Plan**
        - In the Contact channel name drop down, select one of the contact channels from step e, then add the Engagement time in minutes this contact should be notified after stage start
        - Click **Add engagement** to optionally select any other contact channel from step e, along with the Engagement time
        - Click **Create** to create the contact. The contact channel(s) will need to be activated through confirmation email/SMS/voice to be fully functional.
3. Copy the ARN of the contact you created for use when launching the SAM application

### Create an IoT Thing Group for Quarantined Things ###

1. Go to the [AWS IoT console](https://console.aws.amazon.com/iot/home) and select **Manage > Thing Groups**.
2. Under [Create Thing Group](https://console.aws.amazon.com/iot/home?#/create/thing-group-options), select **Create a static thing group**, then click **Next**.
3. Enter the name QUARANTINED for the **Thing group name**, and leave other options in the default state.
4. Select the **Create thing group** button.

### Prerequisites for Launching the CloudFormation Stack ###

The code in GitHub provides a working example of the solution using AWS Serverless Application Module (SAM). Ensure you have met the following prerequisites to deploy the solution using SAM:

- An AWS Account
- AWS Command Line Interface (AWS CLI) installed and configured. User guide [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html).
- AWS Serverless Application Model (SAM) installed. Overview and user guide [here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html).
- An Amazon S3 Bucket for storing SAM-generated packaged templates. Overview [here](https://docs.aws.amazon.com/AmazonS3/latest/userguide/create-bucket-overview.html).

### Launching the CloudFormation Stack ###

1. Initialize the SAM project from the GitHub source repo

```
sam init --location gh:aws-samples/aws-iot-incident-response-automation
```

2. In the file **samconfig.toml**, modify the **ssmEngagementContact** field with the ARN of the contact you created in previous step(s)

3. Package the SAM application

```
sam package \
--template-file template.yaml \
--s3-bucket <S3_BUCKET_NAME> \
--output-template-file packaged-template.yaml
```

4. Deploy the SAM application

```
sam deploy \
--template-file packaged-template.yaml \
--stack-name aws-iot-incident-mgmt \
--capabilities CAPABILITY_IAM
```

After launching the product, it can take from 3 to 5 minutes to deploy. When the product is deployed, it creates a new CloudFormation stack with a status of **CREATE_COMPLETE** as part of the provisioned product in the AWS CloudFormation console.







## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

