Write-Ouput "Logging in to Azure with a service principal."
az login `
    --service-principal `
    --username $Env:SP_CLIENT_ID `
    --password $Env:SP_CLIENT_SECRET `
    --tenant $Env:SP_TENANT_ID 

Write-Output "Done"

az account set `
    --subscription $Env:AZURE_SUBSCRIPTION_NAME

$ResourceGroupName = "VirtualMachinesRG"
$VmName = "File-Management-Server"

Write-Output "Creating VM..."
try {
    az vm create `
        --resource-group $ResourceGroupName `
        --name $VmName `
        --image ubuntuLTS `
        --admin-user azureuser `
        --admin-password $Env:SP_CLIENT_SECRET 
}
catch {
    Write-Output "VM Already Exists"
}

Write-Output "Opening Port At 8088"
try {
    az vm open-port --port 8088 --resource-group $ResourceGroupName --name $VmName
}
catch {
    Write-Output "Already Opened"
}

