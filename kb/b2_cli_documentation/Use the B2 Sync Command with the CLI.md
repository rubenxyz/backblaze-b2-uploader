You can use the B2 Sync command to sync a local directory with a Backblaze B2 Cloud Storage destination. You can upload or download files between a local folder and a bucket path, or you can copy files between bucket path and another bucket path in the same account.

The B2 Sync command is used within the Backblaze B2 command-line tool (install [here](https://www.backblaze.com/bb/docs/cloud-storage-command-line-interface)).

The following example shows the basic parameter structure for the B2 Sync call:

Enter the following command to initially upload a source directory to a Backblaze B2 bucket destination:

The direction of b2 sync can be from

-   A local path to a B2 bucket path, or
-   A B2 bucket path to a local path, or
-   A B2 bucket path to another B2 bucket path in the same account

Use `b2://<bucketName>/<prefix>` for Backblaze B2 paths, for example, `b2://my-bucket-name/a/path/prefix/`.

File uploads are done in parallel in multiple threads.

The default number of threads is 10. Progress is displayed on the console unless `--no-progress` is specified. A list of actions taken is always printed. There is no set amount of threads that work best in every scenario or for every user. Backblaze recommends that you start with the default 10 threads and watch your system activity. If you max out your CPU, RAM, disk, or network usage, decrease the number of threads. If you do not max out, increase the number of threads until you see performance dip. It is a trial and error process to find the right number of threads for your use case.

Now that your directory is uploaded to Backblaze B2, if you make changes to the directory files locally (for example, update your files and keep the same names), you may run into the following scenarios.

## Upload Local Changes

**You want to upload local changes to all files and keep previous versions.**

Call `b2 sync <source file location> <B2 bucket destination>`. The older versions of your files remain, and you will upload new copies on top of the originals. Please note, you are charged for storing multiple versions of files. If your original file is 5 GB and your updated file of the same name is 5.3 GB, you are charged for 10.3 GB of storage.

## Upload New File Versions

**You want to upload only new file versions for the files that you updated.**

If you have files that are the same and have not changed, you will not upload a new file version. Files are considered to be the same if they have the same name and modification time. However, this behavior can be changed using the `--compare-versions` option. The following values are possible:

-   **none**: Comparison using only the file name
-   **modTime**: Comparison using the modification time (default)
-   **size**: Comparison using the file size

You can specify `--exclude-regex` to selectively ignore files that match the given pattern. Ignored files will not copy during the sync operation. The pattern is a regular expression that is tested against the full path of each file.

## Upload Changes to All Files

**You want to upload changes to all files and keep previous versions for a set number of days.**

For example, to make the destination match the source, but retain previous versions for 30 days, call `b2 sync --keep-days 30 --replace-newer <source file location> <B2 bucket destination>`. You will still upload new file versions. However the older versions are set to be removed in 30 days.

## Destination Files

**Files are present in the Backblaze B2 bucket, but they are not in the source bucket.**

When a destination file is present that is not in the source, the default is to leave it there. Specifying `--delete` means to delete destination files that are not in the source. This deletes older versions of updated files, as well.

Files at the source that have a newer modification time are always copied to the destination. If the destination file is newer, the default is to report an error and stop. But if you set `--skip-newer`, those files are skipped. If you set `--replace-newer`, the old file from the source replaces the newer one in the destination.

If you run into any issues or have any suggestions or feature requests while using the B2 Sync command, submit them to our [Github page](https://github.com/Backblaze/B2_Command_Line_Tool/issues).

## Download Snapshots or Large Files

Large files can be difficult to retrieve over https and other single-click download methods.

If you have a large file or a Snapshot that is multiple GBs or even in the TBs, you can use the B2 Sync command and the following syntax to download data:

You use the `--threads` argument and omit the other options for the command. The threads argument needs a recommended value between 1 and 99, with the default value being 10.

To see all of the options for the B2 Sync command, enter `b2 sync` in the command line.

### Download Files from a Bucket

To download all of the files from a bucket or a Snapshot, enter the following command:

This command looks for all of the files in the Backblaze B2 bucket, `MyBucket`, and it downloads all of the files to the current working directory of the CLI.

If you want to designate a location, like a Music folder, use the following command:

This uses 25 threads to transfer all of the data from the bucket: `MyBucket` to the Users Music folder.

On a Mac, the following command is the equivalent example:

This allows you to bolster your download speed with the addition of multiple threads.

If you need to find the names of your buckets, you can run the [b2\_list\_buckets call](https://www.backblaze.com/apidocs/b2-list-buckets).

### Download a Single Large File

To download a single file from a bucket, add the argument `[--include-regex <regex>]` and `[--exclude-regex <regex>]` as well.

Scenario:

You have a large image file in a bucket, but there are 700,000 files in the bucket and you do not want to download all of the data and just one file that is name test/TestEnvironment.img.

The command to download the file is as follows:

The --exclude-regex "." is a wildcard, so this command excludes everything except the file that is included.