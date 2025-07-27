You can use the Backblaze B2 Cloud Storage command-line interface (CLI) to implement cross-origin resource sharing (CORS) rules.

## Access Arguments

Use the following command to access the arguments to set the CORS rules:

## Add CORS Rules with a JSON File (MacOS and Linux)

The easiest way to add the rules is with a JSON file that contains the rule set.

1.  Copy the following example, and save the JSON block locally.
2.  After you validate the JSON file with your rule set, add the rule set to your bucket. In the following example, the JSON file is named `rules.json` and it is located in the current working directory.
3.  Run the following command to add the rule set to your bucket. You can use this example after you have a validated JSON file of rules, but the command will make the specified bucket "public."The following example shows a possible output:

### Failures

The failures that can occur are typically based around an invalid JSON file. Backblaze recommends that you use a validation tool like **_jq_** on the file if you encounter issues.

## Add CORS Rules without a File (MacOS and Linux)

To use the CORS rules through the CLI without a file, escape all of the double quotes around the key pairs or use single quotes around the JSON block, as in the following example:

The command applies the same values and the method of calling the JSON through a file.

Use double-quotes (") to surround the JSON key pairs, this set of double-quotes is not escaped. These are the first and last double quotes in the code block above.

## Add CORS Rules without a File (Windows Command Prompt)

The Windows CLI does not respond appropriately with the above command-line string. This is due to the way Windows handles the single quote.

To correct this issue, replace the leading and tailing single-quote with a double quote and escape any double-quotes with a backslash “ \\ ” inside of the JSON block:

## Add CORS Rules without a File (Windows PowerShell)

Similar to Command Prompt, double-quotes must use an escape character. However, with PowerShell you must use a backtick “ \` ” within the JSON block. 

Note

Windows PowerShell uses “backticks” rather than “backslashes” as an escape character.

## Add CORS Rules using PowerShell with a JSON File

1.  Create a `rules.json` file.
2.  Verify that PowerShell correctly interprets the file using the following command:
3.  Create a PowerShell Object using the file `rules.json`:
4.  Use the Object to set CORS rules.  
    

Was this article helpful?