$ErrorActionPreference="Continue"
$root="C:\Projects\opencode\video_image"
$ctl="C:\Users\arulp\AppData\Local\Temp\opencode\runpodctl.exe"
# $envl was read below but never assigned, so $key/$eid came out empty and every
# runpodctl call failed with {"code":"no_credentials"} (see ./nil).
$envl = Get-Content "$root\.env"
$key=(($envl|Where-Object{$_ -match '^RUNPOD_API_KEY='}|Select-Object -First 1) -split '=',2)[1]
$eid=(($envl|Where-Object{$_ -match '^WAN_ENDPOINT_ID='}|Select-Object -First 1) -split '=',2)[1]
$env:RUNPOD_API_KEY=$key
"eid=[$eid] keylen=$($key.Length) now=$(Get-Date -Format HH:mm:ss)"
"== 1) ALL templates incl USER-created (name carries our endpoint; find the SDPA one CI upserted @20:34) =="
$tj=(& $ctl template list --type user -o json 2>&1|Out-String)
$arr=$null; try{ $arr=$tj|ConvertFrom-Json }catch{}
if($null -eq $arr){ "  (json parse failed; raw{0}={1})" -f ' len',$tj.Length; $tj.Substring(0,[Math]::Min(2000,$tj.Length)) }else{
 "  count={0}" -f @($arr).Count
 $arr|Sort-Object { $_.updatedAt } -Descending|ForEach-Object{
  "  {0,-14} {1,-55} upd={2}  img={3}" -f $_.id,$_.name,$_.updatedAt,$_.imageName
 }
}
"== 2) endpoint owner + template binding + lastDeploy (authority, incl flag) =="
$g=(& $ctl serverless get $eid --include-template -o json 2>&1|Out-String)
try{
 $ge=$g|ConvertFrom-Json
 "  name={0} state={1} workers={2}md wait={3} emps={4}" -f $ge.name,$ge.state,$ge.workers_max,$ge.idleTimeoutSec,$ge.scaleBy
 "  template: id={0} name={1} img={2}" -f $ge.template.id,$ge.template.name,$ge.template.image
 "  templateId={0}" -f $ge.templateId
 }catch{ $g.Substring(0,[Math]::Min(2000,$g.Length)) }
