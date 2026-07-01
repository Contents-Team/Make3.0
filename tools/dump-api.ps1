param([string]$BuildDir, [string]$OutJson)

# Read .NET assembly public type/field surface WITHOUT executing it (metadata only).
$managed = Join-Path $BuildDir "Make_Data\Managed"
$targets = @("Assembly-CSharp.dll","VIRNECT_Extension.dll","com.virnect.train.dll","VirnectNetworkLibrary.dll")

Add-Type -AssemblyName System.Reflection.Metadata -ErrorAction SilentlyContinue

function Dump-Assembly($path) {
  $fs = [System.IO.File]::OpenRead($path)
  try {
    $pe = New-Object System.Reflection.PortableExecutable.PEReader($fs)
    $mr = [System.Reflection.Metadata.PEReaderExtensions]::GetMetadataReader($pe)
    $types = @()
    foreach ($h in $mr.TypeDefinitions) {
      $td = $mr.GetTypeDefinition($h)
      $ns = $mr.GetString($td.Namespace)
      $nm = $mr.GetString($td.Name)
      if ($nm -eq "<Module>") { continue }
      $attr = [int]$td.Attributes
      $isPublic = ($attr -band 0x7) -in @(1,2)  # Public or NestedPublic
      # fields (public, non-special)
      $fields = @()
      foreach ($fh in $td.GetFields()) {
        $fd = $mr.GetFieldDefinition($fh)
        $fattr = [int]$fd.Attributes
        $vis = $fattr -band 0x7
        if ($vis -eq 6) { $fields += $mr.GetString($fd.Name) }  # Public=6
      }
      $types += [pscustomobject]@{ ns=$ns; name=$nm; public=$isPublic; fields=$fields }
    }
    return $types
  } finally { $fs.Dispose() }
}

$all = @{}
foreach ($t in $targets) {
  $p = Join-Path $managed $t
  if (Test-Path $p) {
    $all[$t] = Dump-Assembly $p
  }
}

# Summaries
$asm = "Assembly-CSharp.dll"
$acs = $all[$asm]
Write-Output "=== Assembly-CSharp: total types = $($acs.Count) ==="
Write-Output "=== Namespaces (top, by count) ==="
$acs | Group-Object ns | Sort-Object Count -Descending | Select-Object -First 20 | ForEach-Object { "{0,4}  {1}" -f $_.Count, ($_.Name -eq '' ? '(global)' : $_.Name) }

Write-Output ""
Write-Output "=== Types whose namespace or name contains Component / VNT ==="
$comp = $acs | Where-Object { $_.ns -match 'Component|VNT' -or $_.name -match 'Component$|^VNT' } | Sort-Object ns,name
foreach ($c in $comp) {
  $fl = if ($c.fields.Count) { " | fields: " + ($c.fields -join ", ") } else { "" }
  "{0,-45} {1}{2}" -f ($c.ns), $c.name, $fl
}

# Persist raw JSON for diffing later
$flat = foreach ($k in $all.Keys) { $all[$k] | ForEach-Object { [pscustomobject]@{ asm=$k; ns=$_.ns; name=$_.name; public=$_.public; fields=($_.fields -join ',') } } }
$flat | ConvertTo-Json -Depth 4 | Set-Content -Path $OutJson -Encoding UTF8
Write-Output ""
Write-Output "=== wrote $OutJson (records: $($flat.Count)) ==="
