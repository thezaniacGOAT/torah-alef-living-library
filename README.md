# Torah Aleph — Living Library

A private, speaker-organized archive for the worldwide Kollel Toras Chaim Torah Aleph chaburah.

## Daily workflow
Discover public YouTube shiurim → assign permanent speaker/shiur IDs → archive *unaltered* timestamped captions → produce an unverified Word reading edition → draft timestamped per-shiur summaries → rebuild the master Word/CSV index and each speaker's cumulative summary in Dropbox.

## Dropbox root
`/05. TORAH/Torah Aleph/Shiur Library`

Your existing primary Torah texts and source sheets outside the Shiur Library are not modified.

## Setup
1. Create a **scoped Full Dropbox app** at https://www.dropbox.com/developers/apps; grant `files.metadata.read`, `files.content.read`, `files.content.write`. The existing archive path requires Full Dropbox access. Use `automation/bootstrap_dropbox.py` locally to obtain an *offline refresh token*.
2. Enable YouTube Data API v3 in Google Cloud and create a restricted API key.
3. Create an OpenAI API key for summary generation (separately billed).
4. In GitHub → Settings → Secrets and variables → Actions, add `DROPBOX_APP_KEY`, `DROPBOX_APP_SECRET`, `DROPBOX_REFRESH_TOKEN`, `YOUTUBE_API_KEY`, and optionally `OPENAI_API_KEY`.
5. Actions → **Torah Aleph Daily Archive** → Run workflow. Inspect that it writes only to the new library.
6. The workflow is scheduled daily at 7:13 p.m. Toronto time, to avoid the top-of-hour scheduling congestion.

### Data policy
The **Dropbox catalog is authoritative**; metadata IDs are immutable. Never overwrite raw caption files. Automatic captions may badly garble Hebrew and Yiddish; a reading edition does not represent audio-verified speech. Anything uncertain is marked for review. No captions means no invented summary. Duplicate/uncertain sources are held as unassigned leads.

This automation has been installed but requires credentials and a successful live smoke test. See `automation/README.md`.
