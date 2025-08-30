## Create a Bucket with the CLI

___

Now that you have installed the command-line tool, you're ready to start using Backblaze B2 Cloud Storage.

The first step is to tell the command-line tool how to access your account. You'll need the application key ID that you got when you [created your account](https://www.backblaze.com/docs/cloud-storage-get-started-with-the-ui). Use the `b2 account authorize` command:

```
$ b2 account authorize
Backblaze application key: 
$
```

If you want to know what happened here, the command-line tool called the B2 service over a secure connection to validate your password and get an authorization token. The auth token is stored in the file `.b2_account_info` in your home directory if you want to take a look at it.

Now you can list the existing buckets in your account. If you're new to b2, there won't be any yet.

```
$ b2 bucket list
$
```

Creating a bucket is easy. You provide the bucket name, and whether the access should be "allPublic" or "allPrivate". When the bucket is created, it will print the ID of the new bucket.

```
$ b2 bucket create KittenPhotos allPublic
10f72c8d00b1ea614ceb0319
$
```

Now that the bucket has been created, `b2 bucket list` will show its ID and name.

```
$ b2 bucket list
10f72c8d00b1ea614ceb0319 allPublic KittenPhotos
$
```

Now you are ready to [upload a file](https://www.backblaze.com/bb/docs/en/cloud-storage-upload-files-with-the-cli).

Warning

Do not include Protected Health Information (PHI) or Personally Identifiable Information (PII) in bucket names; object, file, or folder names; or other metadata. This metadata is not encrypted in a way that meets Health Insurance Portability and Accountability Act (HIPAA) protection requirements for PHI/PII data, and it is not generally encrypted in client-side encryption architectures.

Was this article helpful?