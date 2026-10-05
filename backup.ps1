# Бэкап БД и медиа проекта ОАИП
# Task Scheduler: каждые 30 минут

$ProjectDir = "D:\ОАИП"
$BackupDir  = "D:\ОАИП_backups"
$LogFile    = "$ProjectDir\backup.log"
$Timestamp  = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$DirStamp   = Get-Date -Format "yyyy-MM-dd_HH-mm"
$Dest       = "$BackupDir\$DirStamp"

function Log($msg, $level="INFO") {
    $line = "[$Timestamp] [$level] $msg"
    Write-Output $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
}

try {
    New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
    New-Item -ItemType Directory -Force -Path $Dest     | Out-Null

    # SQLite база
    $dbSrc = "$ProjectDir\db.sqlite3"
    if (-not (Test-Path $dbSrc)) { throw "db.sqlite3 не найден: $dbSrc" }
    $dbSize = (Get-Item $dbSrc).Length
    Copy-Item $dbSrc "$Dest\db.sqlite3" -ErrorAction Stop
    Log "db.sqlite3 скопирован ($([math]::Round($dbSize/1KB, 1)) КБ) -> $Dest"

    # Медиафайлы
    if (Test-Path "$ProjectDir\media") {
        $mediaCount = (Get-ChildItem "$ProjectDir\media" -Recurse -File).Count
        Copy-Item "$ProjectDir\media" "$Dest\media" -Recurse -Force -ErrorAction Stop
        Log "media/ скопирован ($mediaCount файлов)"
    } else {
        Log "media/ не найден — пропущено" "WARN"
    }

    # Удаляем бэкапы старше 7 дней
    $old = Get-ChildItem $BackupDir -Directory |
        Where-Object { $_.CreationTime -lt (Get-Date).AddDays(-7) }
    $old | Remove-Item -Recurse -Force
    if ($old.Count -gt 0) { Log "Удалено старых бэкапов: $($old.Count)" }

    # Размер папки бэкапа
    $totalKB = [math]::Round((Get-ChildItem $BackupDir -Recurse -File |
        Measure-Object -Property Length -Sum).Sum / 1KB)
    Log "Бэкап УСПЕШЕН. Всего в хранилище: $totalKB КБ ($BackupDir)"

} catch {
    $errMsg = $_.Exception.Message
    $line = "[$Timestamp] [ERROR] Бэкап FAILED: $errMsg"
    Write-Output $line
    Add-Content -Path $LogFile -Value $line -Encoding UTF8
    exit 1
}
