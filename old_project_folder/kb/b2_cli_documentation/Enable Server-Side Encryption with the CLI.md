## Enable Server-Side Encryption with the CLI

___

You can enable [server-side encryption (SSE)](https://www.backblaze.com/bb/docs/cloud-storage-server-side-encryption) on your Backblaze B2 Cloud Storage buckets using the command-line interface (CLI).

For information about how to enable SSE using the [Native API](https://www.backblaze.com/apidocs/introduction-to-the-b2-native-api), click [here](https://www.backblaze.com/bb/docs/cloud-storage-enable-server-side-encryption-with-the-native-api).

## Upload SSE-B2-Enabled Files

Even without the setting turned on at the bucket level, you can enable it on individual file uploads by using the appropriate header information.

## Upload SSE-C-Enabled Files

Use this command to upload files that are SSE-C-enabled.

## Copy SSE-C-Enabled Files Between Buckets

There are a few options to specify when you use the [b2\_copy\_file](https://www.backblaze.com/apidocs/b2-copy-file) API to copy files or parts between buckets.

Was this article helpful?