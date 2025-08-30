# Sync Failure Report
**Date**: 2025-08-30 08:52:40
**Operation**: sync

## Summary
- **Failed Files**: 1

## Failed Files
### sync_operation
- **Error**: Traceback (most recent call last):
  File "/opt/homebrew/bin/b2", line 3, in <module>
    from b2._internal.b2v4.__main__ import main
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2/_internal/b2v4/__main__.py", line 13, in <module>
    main()
    ~~~~^^
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2/_internal/console_tool.py", line 5623, in main
    exit_status = ct.run_command(sys.argv)
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2/_internal/console_tool.py", line 5487, in run_command
    return command.run(args)
           ~~~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2/_internal/console_tool.py", line 1083, in run
    return self._run(args)
           ~~~~~~~~~^^^^^^
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2/_internal/console_tool.py", line 3198, in _run
    destination = parse_folder(args.destination, self.console_tool.api)
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2sdk/_internal/scan/folder_parser.py", line 35, in parse_folder
    return _parse_bucket_and_folder(folder_name[5:], api, b2_folder_class)
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2sdk/_internal/scan/folder_parser.py", line 55, in _parse_bucket_and_folder
    return b2_folder_class(bucket_name, folder_name, api)
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2sdk/_internal/scan/folder.py", line 364, in __init__
    self.bucket = api.get_bucket_by_name(bucket_name)
                  ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2sdk/_internal/api.py", line 362, in get_bucket_by_name
    self.check_bucket_name_restrictions(bucket_name)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/logfury/_logfury/trace_call.py", line 86, in wrapper
    return function(*wrapee_args, **wrapee_kwargs)
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2sdk/_internal/api.py", line 639, in check_bucket_name_restrictions
    self._check_bucket_restrictions('name', bucket_name)
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/b2-tools/4.4.1/libexec/lib/python3.13/site-packages/b2sdk/_internal/api.py", line 653, in _check_bucket_restrictions
    buckets = self.account_info.get_allowed()['buckets']
              ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
KeyError: 'buckets'

- **Type**: B2SyncFailure

## Next Steps
1. Fix the identified issues with failed files
2. Re-run the sync script to update changes
