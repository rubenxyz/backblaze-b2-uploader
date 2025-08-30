## Upload Files with the CLI

___

Now that you have a bucket to put files in, you are ready to upload a file.

List buckets will show you the bucket ID you need to upload files:

```
$ b2 bucket list
10f72c8d00b1ea614ceb0319 allPublic KittenPhotos
$
```

If you have a local file on your computer called "kitten.jpg" and you want to upload this file to your "KittenPhotos" bucket into a folder named "fluffy," you would do it like this:

```
$ b2 file upload KittenPhotos kitten.jpg fluffy/kitten.jpg
URL by file name: https://f004.backblazeb2.com/file/KittenPhotos/fluffy/kitten.jpg
URL by fileId: https://f004.backblazeb2.com/b2api/v3/b2_download_file_by_id?fileId=4_ze1256f0973908bfc71ed0c1z_f10072d5b729d51d1_d20150731_m214727_c100_v0009990_t0004
{
    "accountId": "12f634bf3cbz", 
    "action": "upload", 
    "bucketId": "e1256f0973908bfc71ed0c1z", 
    "contentMd5": "7958b9fxc5748f70e53f62ec163478zb", 
    "contentSha1": "3a16e5f24a9a4e8a47438f39141ec33a79bd97bc", 
    "contentType": "text/jpeg", 
    "fileId": "4_ze1256f0973908bfc71ed0c1z_f10072d5b729d51d1_d20150731_m214727_c100_v0009990_t0004", 
    "fileInfo": {}, 
    "fileName": "fluffy/kitten.jpg"
}
$
```

The ls command will show the files in your bucket:

```
$ b2 ls b2://KittenPhotos
fluffy/kitten.jpg
```

See [`b2_download_file_by_id`](https://www.backblaze.com/apidocs/b2-download-file-by-id) and [`b2_download_file_by_name`](https://www.backblaze.com/apidocs/b2-download-file-by-name) for information about downloading files.

Warning

Do not include Protected Health Information (PHI) or Personally Identifiable Information (PII) in bucket names; object, file, or folder names; or other metadata. This metadata is not encrypted in a way that meets Health Insurance Portability and Accountability Act (HIPAA) protection requirements for PHI/PII data, and it is not generally encrypted in client-side encryption architectures.

Was this article helpful?