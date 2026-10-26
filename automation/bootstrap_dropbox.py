#!/usr/bin/env python3
"""One-time Dropbox offline refresh token bootstrap. Never commit credentials."""
import getpass
from dropbox import DropboxOAuth2FlowNoRedirect

print("Create a Scoped Dropbox app (Full Dropbox) with files.metadata.read, files.content.read, files.content.write.")
key = input("App key: ").strip()
secret = getpass.getpass("App secret (hidden): ").strip()
flow = DropboxOAuth2FlowNoRedirect(key, secret, token_access_type="offline")
print("\nAuthorize this URL in your browser:\n" + flow.start())
code = getpass.getpass("Paste returned authorization code (hidden): ").strip()
result = flow.finish(code)
if not result.refresh_token:
    raise SystemExit("No offline refresh token. Check permissions/app settings.")
print("\nSave this directly as GitHub repository secret DROPBOX_REFRESH_TOKEN; never paste it into ChatGPT:")
print(result.refresh_token)
