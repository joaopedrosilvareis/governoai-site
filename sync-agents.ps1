# sync-agents.ps1 — Windows (PowerShell)
# Copia prompts de agents/ para src/content/agentes/
#
# Uso (na raiz do repositório Governo AI):
#   .\sync-agents.ps1
#   .\sync-agents.ps1 "C:\outro\caminho\para\pasta-com-agents"

param(
    [string]$StarterRoot = $PSScriptRoot
)

$origem = Join-Path $StarterRoot "agents"
$dest = Join-Path $PSScriptRoot "src\content\agentes"

if (-not (Test-Path $origem)) {
    Write-Error "Nao encontrei: $origem`nUso: .\sync-agents.ps1 (corre na raiz do repo, com pasta agents\)"
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
