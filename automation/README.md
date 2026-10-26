# Activation checklist

**Repository:** https://github.com/thezaniacGOAT/torah-alef-living-library

## Step 1: Dropbox
Go to https://www.dropbox.com/developers/apps and create a scoped **Full Dropbox** app. Scopes: `files.metadata.read`, `files.content.read`, `files.content.write`. Grant offline authorization by running `python automation/bootstrap_dropbox.py` locally with Python and the installed requirements. The refresh token must never be placed in a commit, message, or public document.

## Step 2: YouTube
Enable YouTube Data API v3 at https://console.cloud.google.com/apis/library/youtube.googleapis.com and create an API key. Keep quota and key restrictions in mind.

## Step 3: AI summaries
Create OpenAI API key at https://platform.openai.com/api-keys (optional; if omitted, full captions still archive and summaries remain pending). API usage is independently billed.

## Step 4: GitHub secrets
In repository Settings → Secrets and variables → Actions, add:
- `DROPBOX_APP_KEY`
- `DROPBOX_APP_SECRET`
- `DROPBOX_REFRESH_TOKEN`
- `YOUTUBE_API_KEY`
- `OPENAI_API_KEY` (optional)

Secrets are never committed. No Dropbox files are written until the workflow is executed with a valid Dropbox authorization.

## Step 5: Test
Actions → Torah Aleph Daily Archive → Run workflow. Verify these Dropbox paths:
`/05. TORAH/Torah Aleph/Shiur Library/Indexes`,
`Speakers/REB - David Reboh/Raw`, `Clean`, `Summaries`, `Logs`.
The first run takes the existing `master_catalog.csv` in Dropbox as its baseline. Failed extraction is logged; it does not fabricate transcript contents.

## Limitations
- Captions may be unavailable or inaccurate, especially Hebrew/Yiddish.
- Third-party transcript endpoints can change, and direct YouTube caption calls may be blocked.
- Speaker attribution based only on metadata is *provisional*. New videos without clear identification remain in the unassigned queue.
- Duplicate uploads may require human review.
- Summary output is a draft from automated captions, not an authoritative exact quote.
- GitHub scheduled runs can be delayed, although 19:13 Toronto avoids the start-of-hour load peak.

## Security
Application scopes allow access broader than the library path because the existing folder lives in a Full Dropbox account. The script separately limits writes to the dedicated library folder. Dropbox preserves file version history; raw files are always write-once. Rotate credentials if compromised.
