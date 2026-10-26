# Generate a long-lived Dropbox refresh token using Windows PowerShell 5.1+.
# No Python installation required. Run locally, never in ChatGPT.
# Do not put app secrets or refresh tokens in the repository.
$ErrorActionPreference = 'Stop'
Write-Host 'Dropbox offline authorization — Torah Aleph Living Library'
Write-Host 'Confirm scopes files.metadata.read, files.content.read, files.content.write in Dropbox Permissions before running.'
$key = (Read-Host 'Dropbox App key').Trim()
if (-not $key) { throw 'App key is required' }
$secretSec = Read-Host 'Dropbox App secret (hidden)' -AsSecureString
$ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secretSec)
try { $secret = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr) }
finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr) }
$url = 'https://www.dropbox.com/oauth2/authorize?client_id=' + [Uri]::EscapeDataString($key) + '&response_type=code&token_access_type=offline'
Write-Host 'Opening Dropbox authorization page. Sign in and approve your app.'
Start-Process $url
$code = (Read-Host 'Paste the authorization code shown by Dropbox').Trim()
if (-not $code) { throw 'Authorization code required' }
$payload = @{
    code = $code
    grant_type = 'authorization_code'
    client_id = $key
    client_secret = $secret
}
$response = Invoke-RestMethod -Uri 'https://api.dropboxapi.com/oauth2/token' -Method Post -ContentType 'application/x-www-form-urlencoded' -Body $payload
$secret = $null
$payload = $null
if (-not $response.refresh_token) {
    throw 'Dropbox did not return a refresh token. Check that token_access_type=offline was used.'
}
Set-Clipboard -Value $response.refresh_token
Write-Host ''
Write-Host 'Success. Refresh token is in your Windows clipboard (NOT printed here).' -ForegroundColor Green
Write-Host 'Open https://github.com/thezaniacGOAT/torah-alef-living-library/settings/secrets/actions'
Write-Host 'New repository secret: DROPBOX_REFRESH_TOKEN. Paste clipboard contents as its value.'
Write-Host 'Add DROPBOX_APP_KEY and DROPBOX_APP_SECRET separately, from your Dropbox App Console.'
Write-Host 'After saving and verifying, clear your clipboard by copying nonsecret text.'
