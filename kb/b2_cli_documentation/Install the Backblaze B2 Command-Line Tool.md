If you [created an account](https://www.backblaze.com/docs/cloud-storage-get-started-with-the-ui), you are ready to get the command-line tool that gives easy access to all of the capabilities of Backblaze B2 Cloud Storage.

The command-line tool is available in four options. Backblaze offers an easy-to-use self-contained download for Windows and Linux users, a Homebrew formula for Mac users, a Python version from the Python Package Index (PyPI), and Github sources.

## Self-Contained Download

The self-contained download is the easiest way to get up and running; no installation or Python needed. Simply download the version for your operating system and run it from a command window. For detailed documentation, visit our [B2 CLI page](https://b2-command-line-tool.readthedocs.io/en/master/).

-   [Windows](https://github.com/Backblaze/B2_Command_Line_Tool/releases/download/v4.1.0/b2-windows.exe)
-   [Linux](https://github.com/Backblaze/B2_Command_Line_Tool/releases/latest/download/b2-linux)

For Mac users, Backblaze recommends Homebrew as the quickest way to get set up. Mac users may also use the Python version or Github sources, if preferred.

After you download the self-contained tool, you can learn how to use the command-line tool below. Prior to running the tool, run the following command:

```
chmod +x &lt;tool filename&gt;
```

## Homebrew

[Homebrew](https://brew.sh/) is widely used in the Mac community, particularly amongst developers. We recommend using the [B2 CLI Homebrew](https://formulae.brew.sh/formula/b2-tools) formula as the quickest setup method for Mac users:

```
brew install b2-tools
```

## Python Version

If you want to run the Python version of the command-line tool, it has been packaged in Python modules and published on the Python Package Index (PyPI). The easiest way to get the Python version of the command-line tool is using the standard Python `pip3` installation tool.

Your first step is to make sure that you have Python 3 (3.7 or later) installed.

### Python Installation on Mac (OSX)

To install Python3, `pip3`, and the B2 command-line tool on Mac OSX:

1.  Go to [Python Releases for Mac OS X](https://www.python.org/downloads/mac-osx/), select the "Latest Python 3 Release", and scroll to the bottom.
2.  Download and run the "macOS 64-bit installer"
3.  Open a new Terminal window and type `pip3 install --upgrade b2`

If you see a message like this, it is because Apple installs a really old version of one of the Python libraries that B2 uses:

```
OSError: [Errno 1] Operation not permitted: '/tmp/pip-BMa2Su-uninstall/System/Library/Frameworks/Python.framework/Versions/2.7/Extras/lib/python/six-1.4.1-py2.7.egg-info'
```

You can work around this with the `--ignore-installed option`:

```
sudo pip3 install --upgrade --ignore-installed b2
```

### Python Installation on Windows

To install Python3, `pip3`, and the command-line tool on Windows:

1.  Click [Python Releases for Windows](https://www.python.org/downloads/windows/), select the "Latest Python 3 Release", and scroll to the bottom.
2.  Download the "Windows x86-64 executable installer". For older 32-bit windows, download the "Windows x86 executable installer".
3.  Run the installer. By default it will install Python to your Users directory.
4.  Check the "Add Python 3.x to PATH" box to enable you to use Python from any directory.
5.  Open a Command Prompt window and type `pip3 install --upgrade b2`

## Github Sources

This version of the command-line tool is useful for Python developers who wish to work with the command-line tool source code. The sources for the command-line tool are available from Github in the [B2\_Command\_Line\_Tool](https://github.com/Backblaze/B2_Command_Line_Tool) project.

The first step is make sure that you have Python3 installed and then download the latest version of the source code from Github:

```
git clone https://github.com/Backblaze/B2_Command_Line_Tool.git
```

The [Developer Info](https://github.com/Backblaze/B2_Command_Line_Tool#developer-info) section of the project's [README.md](https://github.com/Backblaze/B2_Command_Line_Tool#b2-command-line-tool) file has all the info needed to build and contribute to the project.

## Usage

Once you have the B2 command-line tool installed, you can view all of the options by running:

```
b2 --help
```

Click [here](https://github.com/Backblaze/B2_Command_Line_Tool?tab=readme-ov-file#usage) for a complete list of commands.

The environment variable `B2_ACCOUNT_INFO` specifies the SQLite file to use for caching authentication information. The default file to use is: `~/.b2_account_info`.

To get more details on a specific command, run:

```
b2 &lt;command&gt; --help
```

When authorizing with application keys, this tool requires that the key have the `listBuckets` capability so that it can take the bucket names that you provide on the command line and translate them into bucket IDs for the Backblaze B2 service. Each command may require additional capabilities. You can find the details for each command in the help for that command.

If you see a message like `b2: Permission denied` on OSX or Linux, set the executable bit on the file with the command:

```
chmod +x b2
```

For more information about the calls that can be made in the B2 CLI, see our [B2 CLI page](https://b2-command-line-tool.readthedocs.io/en/master/) or the downloadable [B2 CLI Guide](https://f000.backblazeb2.com/file/jsonwaterfalls/B2%20CLI%20Guide.pdf).

Now that you have the command-line tool, you are ready to [make a bucket](https://www.backblaze.com/bb/docs/en/cloud-storage-create-a-bucket-with-the-cli) to hold your files.

The `ls` command may time out when used on directories containing several million hidden files.

Was this article helpful?