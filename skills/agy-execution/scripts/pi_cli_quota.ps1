param([Parameter(Mandatory=$true)][string]$Manager,
      [Parameter(Mandatory=$true)][string]$Recovery,
      [switch]$RestoreOnly)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [Text.UTF8Encoding]::new($false)
if (@(Get-Process -Name agy -ErrorAction SilentlyContinue).Count) { throw 'Close AGY before quota discovery.' }
# Reuse the user's installed profile manager. Never print decrypted credentials.
. $Manager help *> $null
function Restore-QuotaSnapshot {
    $saved = Unprotect-FromFile $Recovery
    if ($saved.credential) {
        $c = $saved.credential
        [CredMan]::Write($CRED_TARGET, $c.userName, $c.comment, [uint32]$c.persist, [Convert]::FromBase64String($c.blobB64))
    } else { [void][CredMan]::Delete($CRED_TARGET) }
    foreach ($item in $saved.files) {
        # Paths come only from our own encrypted snapshot of exact account-bound files.
        if ($null -ne $item.base64) { [IO.File]::WriteAllBytes($item.path, [Convert]::FromBase64String($item.base64)) }
        elseif (Test-Path -LiteralPath $item.path) { Remove-Item -LiteralPath $item.path }
    }
    $restored = Get-CurrentCred
    if ($saved.credential) {
        if (-not $restored -or (Get-BlobHash $restored.Blob) -ne (Get-BlobHash ([Convert]::FromBase64String($saved.credential.blobB64)))) { throw 'CLI credential restoration failed' }
    } elseif ($restored) { throw 'CLI credential deletion failed' }
    foreach ($item in $saved.files) {
        if ($null -ne $item.base64) {
            if ([Convert]::ToBase64String([IO.File]::ReadAllBytes($item.path)) -ne $item.base64) { throw 'CLI file restoration failed' }
        } elseif (Test-Path -LiteralPath $item.path) { throw 'CLI absence restoration failed' }
    }
    Remove-Item -LiteralPath $Recovery
}
if ($RestoreOnly) { Restore-QuotaSnapshot; exit 0 }
if (Test-Path -LiteralPath $Recovery) { throw 'An interrupted quota snapshot must be restored before another query.' }
$originalCred = Get-CurrentCred
$originalActive = if (Test-Path -LiteralPath $ACTIVE_FILE) { [IO.File]::ReadAllBytes($ACTIVE_FILE) } else { $null }
$originalFiles = @{}
foreach ($relative in $PER_PROFILE_FILES) {
    $file = Join-Path $CLI_DIR $relative
    $originalFiles[$file] = if (Test-Path -LiteralPath $file) { [IO.File]::ReadAllBytes($file) } else { $null }
}
$rows = @()
$fileSnapshots = @()
foreach ($file in $originalFiles.Keys) {
    $fileSnapshots += @{path=$file; base64=$(if ($null -ne $originalFiles[$file]) { [Convert]::ToBase64String($originalFiles[$file]) } else { $null })}
}
$fileSnapshots += @{path=$ACTIVE_FILE; base64=$(if ($null -ne $originalActive) { [Convert]::ToBase64String($originalActive) } else { $null })}
$credentialSnapshot = if ($originalCred) { @{userName=$originalCred.UserName;comment=$originalCred.Comment;persist=$originalCred.Persist;blobB64=[Convert]::ToBase64String($originalCred.Blob)} } else { $null }
Protect-JsonToFile (@{credential=$credentialSnapshot;files=$fileSnapshots} | ConvertTo-Json -Depth 8) $Recovery
try {
    foreach ($profile in Get-SavedProfiles) {
        if (@(Get-Process -Name agy -ErrorAction SilentlyContinue).Count) { throw 'AGY started during quota discovery.' }
        $row = @{profile=$profile.Name; remaining_5h=$null; remaining_weekly=$null; reset_5h=$null; reset_weekly=$null}
        try {
            Apply-ProfileFilesAndCred $profile.Name | Out-Null
            $raw = & agy -p '/usage' --output-format json --print-timeout 30s 2>$null | Out-String
            if ($LASTEXITCODE -ne 0) { throw 'usage failed' }
            $data = $raw | ConvertFrom-Json
            $groups = @($data.command.data.groups | Where-Object { $_.name -like '*Gemini*' })
            if ($groups.Count -ne 1) { throw 'ambiguous Gemini quota group' }
            foreach ($bucket in $groups[0].buckets) {
                if ($null -eq $bucket.remaining_fraction) { continue }
                $remaining = [Math]::Floor(100 * [double]$bucket.remaining_fraction)
                if ($bucket.id -eq 'gemini-5h' -or $bucket.window -eq '5h') {
                    $row.remaining_5h=$remaining; $row.reset_5h=$bucket.reset_time
                } elseif ($bucket.id -eq 'gemini-weekly' -or $bucket.window -eq 'weekly') {
                    $row.remaining_weekly=$remaining; $row.reset_weekly=$bucket.reset_time
                }
            }
        } catch { $row.error='quota unavailable' }
        $rows += $row
    }
} finally {
    Restore-QuotaSnapshot
}
ConvertTo-Json -InputObject @($rows) -Depth 8 -Compress
