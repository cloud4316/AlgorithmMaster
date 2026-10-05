# Восстановление из бэкапа ОАИП
# Запуск: powershell -ExecutionPolicy Bypass -File D:\ОАИП\restore.ps1

$ProjectDir = "D:\ОАИП"
$BackupDir  = "D:\ОАИП_backups"

if (-not (Test-Path $BackupDir)) {
    Write-Host "ОШИБКА: Папка бэкапов не найдена: $BackupDir" -ForegroundColor Red
    exit 1
}

# Список доступных бэкапов
$backups = Get-ChildItem $BackupDir -Directory | Sort-Object CreationTime -Descending

if ($backups.Count -eq 0) {
    Write-Host "Нет доступных бэкапов в $BackupDir" -ForegroundColor Yellow
    exit 1
}

Write-Host "`n=== Доступные бэкапы ===" -ForegroundColor Cyan
for ($i = 0; $i -lt $backups.Count; $i++) {
    $b = $backups[$i]
    $dbPath = "$($b.FullName)\db.sqlite3"
    $dbSize = if (Test-Path $dbPath) { "$([math]::Round((Get-Item $dbPath).Length/1KB))КБ" } else { "нет БД" }
    $age = [math]::Round(((Get-Date) - $b.CreationTime).TotalHours, 1)
    Write-Host "  [$i] $($b.Name)  БД:$dbSize  ($age ч. назад)" -ForegroundColor White
}

Write-Host ""
$choice = Read-Host "Введите номер бэкапа для восстановления (или Enter для отмены)"

if ($choice -eq "" -or $choice -eq $null) {
    Write-Host "Отмена." -ForegroundColor Yellow
    exit 0
}

$idx = [int]$choice
if ($idx -lt 0 -or $idx -ge $backups.Count) {
    Write-Host "Неверный номер." -ForegroundColor Red
    exit 1
}

$selected = $backups[$idx]
Write-Host "`nВыбран бэкап: $($selected.Name)" -ForegroundColor Cyan

# Подтверждение
$confirm = Read-Host "ВНИМАНИЕ: текущая БД будет перезаписана. Продолжить? (да/нет)"
if ($confirm -ne "да") {
    Write-Host "Отмена." -ForegroundColor Yellow
    exit 0
}

$logLine = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [RESTORE] Восстановление из: $($selected.Name)"
Add-Content -Path "$ProjectDir\backup.log" -Value $logLine -Encoding UTF8

# Создать свежий бэкап текущего состояния перед откатом
$safetyStamp = "before-restore_$(Get-Date -Format 'yyyy-MM-dd_HH-mm')"
$safetyDest  = "$BackupDir\$safetyStamp"
Write-Host "Создаю страховочный бэкап текущего состояния -> $safetyDest" -ForegroundColor DarkCyan
New-Item -ItemType Directory -Force -Path $safetyDest | Out-Null
if (Test-Path "$ProjectDir\db.sqlite3") {
    Copy-Item "$ProjectDir\db.sqlite3" "$safetyDest\db.sqlite3"
}
if (Test-Path "$ProjectDir\media") {
    Copy-Item "$ProjectDir\media" "$safetyDest\media" -Recurse -Force
}

# Восстановить БД
$srcDb = "$($selected.FullName)\db.sqlite3"
if (Test-Path $srcDb) {
    Copy-Item $srcDb "$ProjectDir\db.sqlite3" -Force
    Write-Host "БД восстановлена." -ForegroundColor Green
} else {
    Write-Host "WARN: db.sqlite3 не найден в этом бэкапе — БД не восстановлена." -ForegroundColor Yellow
}

# Восстановить media
$srcMedia = "$($selected.FullName)\media"
if (Test-Path $srcMedia) {
    if (Test-Path "$ProjectDir\media") {
        Remove-Item "$ProjectDir\media" -Recurse -Force
    }
    Copy-Item $srcMedia "$ProjectDir\media" -Recurse -Force
    Write-Host "media/ восстановлен." -ForegroundColor Green
} else {
    Write-Host "WARN: media/ не найден в этом бэкапе — пропущено." -ForegroundColor Yellow
}

$doneLog = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] [RESTORE] Восстановление УСПЕШНО из $($selected.Name)"
Add-Content -Path "$ProjectDir\backup.log" -Value $doneLog -Encoding UTF8

Write-Host "`nВосстановление завершено." -ForegroundColor Green
Write-Host "Перезапусти Django-сервер: python manage.py runserver" -ForegroundColor Cyan
