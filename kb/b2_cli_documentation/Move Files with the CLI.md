The Backblaze B2 Cloud Storage command-line interface (CLI) supports the `b2 file copy-by-id` command that you can use to copy a file from one bucket to another bucket.

The context for making this call in the CLI is as follows:

The `sourceFileID` is the file ID of the file that you want to copy to the new bucket. 

There are two options to find a file ID:

-   Use the `b2 ls --long b2://<bucketName>` command in the Backblaze B2 CLI.
-   In the Backblaze web console, click the ‘i’ icon next to a file. The Fguid is the file ID for that file.

The following example shows you how to copy a file from one bucket to another bucket.

Was this article helpful?