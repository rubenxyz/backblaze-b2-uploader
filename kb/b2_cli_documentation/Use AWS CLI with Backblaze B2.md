## Use the AWS CLI with Backblaze B2

___

Backblaze B2 Cloud Storage has S3 endpoints that you can use in conjunction with the AWS Command Line Interface (CLI) to communicate with and update your Backblaze B2 buckets. After configuration, you can use this tool to transfer data between an S3 bucket and Backblaze B2.

## Enable Backblaze B2

**Before you begin:** You must have a [Backblaze B2 Cloud Storage account](https://www.backblaze.com/docs/cloud-storage-enable-backblaze-b2#create-a-backblaze-b2-account). If you already have a Backblaze account and the left navigation menu contains a **B2 Cloud Storage** section, your account is already enabled for Backblaze B2.

1.  [Sign in](https://secure.backblaze.com/user_signin.htm) to the Backblaze web console.
2.  In the user menu in the upper-right corner of the page, select **My Settings**.
3.  Under **Enabled Products**, select the checkbox to enable **B2 Cloud Storage**.
4.  Review the Terms and Conditions, and click **OK** to accept them. 

## Create an Application Key

1.  [Sign in](https://secure.backblaze.com/user_signin.htm) to the Backblaze web console.
2.  In the left navigation menu under B2 Cloud Storage, click **Application Keys**.
3.  Click **Add a New Application Key**, and enter an app key name.  
    _You cannot search an app key by this name; therefore, app key names are not required to be globally unique. Key names are limited to 100 characters and can contain letters, numbers, and "-", but not I18N characters, such as é, à, and ü._
4.  Select **All** or select a specific bucket in the **Allow Access to Bucket(s)** menu.
5.  Optionally, select your access type (**Read** **and Write**, **Read Only**, or **Write Only**).
6.  Optionally, select **Allow List All Bucket Names**.  
    _This option is required for the B2 Native API [b2\_list\_buckets](https://www.backblaze.com/apidocs/b2-list-buckets) and the S3-Compatible API [S3 List Buckets](https://www.backblaze.com/apidocs/s3-list-buckets) operations_.
7.  Optionally, enter a file name prefix to restrict application key access only to files with that prefix.  
    _Depending on what you selected in step #4, this limits application key access to files with the specified prefix for all buckets or just the selected bucket._
8.  Optionally, enter a positive integer to limit the time, in seconds, before the application key expires.  
    _The value must be less than 1000 days (in seconds)._
9.  Click **Create New Key**, and note the resulting _keyID_ and _applicationKey_ values.

Note

When you create a new app key, the response contains the actual key string, for example **N2Zug0evLcHDlh\_L0Z0AJhiGGdY**. You can always find the keyID on this page, but for security, the applicationKey appears only once. Make sure you copy and securely save this value elsewhere.

## Configure the AWS CLI to Interface With Backblaze B2

**Before you begin**: [Install the AWS CLI](https://aws.amazon.com/cli/). Use the command `aws --version` to verify that the CLI is installed.

1.  Use the command `aws configure` to begin the configuration process.  
    _You are prompted for several pieces of information that you can find in the **App Key** section of your Backblaze account._
2.  When AWS prompts you for your **AWS Access Key ID**, provide your Backblaze `keyID`.
3.  When AWS prompts you for your **AWS Secret Access Key**, provide your Backblaze `applicationKey`.
    
    Note
    
    Your master application key will not work with the Backblaze S3 Compatible API. You must create a new key that is eligible for use. For more information, see [this article](https://www.backblaze.com/bb/docs/cloud-storage-application-keys).
    
4.  Leave the **Default region name** and **Default output format** fields blank.
5.  Test the integration by entering the following command to list the buckets in your account: `aws s3 ls --endpoint-url=<S3 Endpoint URL>`, for example:

## Use the AWS CLI to Transfer Data to Backblaze B2

**Before you begin**: If your data comes from an AWS S3 bucket, add your S3 buckets using the configuration tool.

1.  Copy files to a local directory using the following command:
2.  Transfer files directly to Backblaze B2 using the following command:

## Create Pre-Signed URLs from the AWS CLI

You can use the AWS CLI to create a pre-signed URL for sharing an object from a bucket. 

Enter the following command to generate a pre-signed URL on a file in a bucket that expires in 3,600 seconds (the default value):

A pre-signed URL is returned:

### Pre-Signed URL Example Usage

Note

Depending on how you use the pre-signed URL, you may need to enclose it in quotes.

1.  Use a pre-signed URL to get the contents of a file:  
    Example output:
2.   Use a pre-signed URL to save the contents of a file locally (the local file in this example is named “dlTest.txt”):  
    

Note

Uploads are possible using pre-signed URLs but they must be generated with one of our [S3 Compatible SDKs](https://www.backblaze.com/docs/cloud-storage-s3-compatible-sdks).

Was this article helpful?