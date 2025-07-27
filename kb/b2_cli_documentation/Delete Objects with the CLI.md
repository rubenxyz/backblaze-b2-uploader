## Delete Objects with the CLI

___

You can delete all of the files in a bucket using the command-line interface (CLI). This task assumes that you are using the Python version of the CLI.

1.  [Download and install the CLI](https://www.backblaze.com/bb/docs/cloud-storage-command-line-tools).
2.  Open a Terminal window.
3.  Run this command: `b2 account authorize [<KeyID>] [<ApplicationKey>]`
4.  Run this command:  `b2 rm --versions --recursive b2://<bucketName>` where `<bucketName>` is the name of the bucket you want to empty.

Warning

Step #4 will delete all files, file versions, and subfolders in the bucket. 

Note

If there are still unfinished large files in the bucket, this method by itself will not remove those unfinished listings. The bucket may still report as not empty.

To remove unfinished large files, call `b2 cancel-all-unfinished-large-files <bucketName>` and delete the bucket again.

Was this article helpful?