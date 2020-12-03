Write-Host Clear generated
Remove-Item .\* -Filter *pb2.py 

$protoFiles = ""
Get-ChildItem -Path .\proto\ -Filter *.proto -Recurse -File -Name| ForEach-Object {
    $protoFiles += ".\proto\" + [System.IO.Path]::GetFileName($_) + " "
}
Write-Host Proto: $protoFiles

if ($protoFiles -Eq "") {
    throw "Proto files not found"
}

Write-Host Start generating
# & "protoc" --python_out=generated $protoFiles
Start-Process protoc -ArgumentList "--proto_path=proto --python_out=. $protoFiles" -NoNewWindow -Wait
Write-Host Generated