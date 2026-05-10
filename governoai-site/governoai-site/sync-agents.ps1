# sync-agents.ps1 — Windows (PowerShell)
# Copia prompts de governoai-starter/agents para src/content/agentes
#
# Uso (na raiz do site):
#   .\sync-agents.ps1
#   .\sync-agents.ps1 "C:\caminho\para\governoai-starter\governoai-starter"

param(
    [string]$StarterRoot = (Join-Path $PSScriptRoot "..\..\governoai-starter\governoai-starter")
)

$origem = Join-Path $StarterRoot "agents"
$dest = Join-Path $PSScriptRoot "src\content\agentes"

if (-not (Test-Path $origem)) {
    Write-Error "Nao encontrei: $origem`nUso: .\sync-agents.ps1 `"C:\...\governoai-starter\governoai-starter`""
    exit 1
}

New-Item -ItemType Directory -Force -Path $dest | Out-Null
Write-Host "A sincronizar de $origem"
Get-ChildItem -Path $origem -Filter "*.md" | ForEach-Object {
    Copy-Item $_.FullName (Join-Path $dest $_.Name) -Force
    Write-Host "  OK $($_.Name)"
}
$n = (Get-ChildItem (Join-Path $dest "*.md")).Count
Write-Host "`nSincronizados $n prompts. Proximo: npm run dev"
