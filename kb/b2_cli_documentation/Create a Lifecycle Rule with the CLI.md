## Create a Lifecycle Rule with the CLI

___

Lifecycle Rules enable the Backblaze B2 Cloud Storage service to automatically hide and delete older versions of your files that are stored in Backblaze B2. Each Backblaze B2 bucket can have its own Lifecycle Rules, and you can apply Lifecycle Rules to some or all of the files in your bucket.

To use Lifecycle Rules with the Backblaze B2 Cloud Storage command-line interface (CLI), you need to run version 0.7.0 of the Backblaze B2 [command-line tool](https://www.backblaze.com/bb/docs/cloud-storage-command-line-tools).

Use the following commands to create and manage Lifecycle Rules in the CLI.

The B2 `bucket get` command returns all of the variables for the named bucket.

Was this article helpful?