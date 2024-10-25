# Read me

This script is designed to automatically transfer your various json appsettings files for different environments over to Azure devops variable groups. This will not create an appsettings file for you, it only transfers the config details from an existing appsettings file. This is meant for transfering config variables from the different environment appsettings. Like appsettings.Prod.json etc. You will still need the default appsettings.json to exist.

## Login to Azure

You will first need to login to the Azure DevOps originization where your project is located in your terminal using Azure CLI. You can find the organization name in the project url:

    https://dev.azure.com/<organization-name>/<project-name>

You use this command in your terminal to login to your organization in the terminal:

    az devops login --org https://dev.azure.com/<organization-name>

You will then be prompted to enter your personal access token (PAT). Information on how to create a PAT can be found here: [Use personal access tokens](https://learn.microsoft.com/en-us/azure/devops/organizations/accounts/use-personal-access-tokens-to-authenticate?view=azure-devops&tabs=Windows#create-a-pat). Further information on signing in with a PAT can be found here: [Sign in with a personal access token (PAT)](https://learn.microsoft.com/en-us/azure/devops/cli/log-in-via-pat?view=azure-devops&tabs=windows)

## Using the script

### Set default organization and project

Now that you are logged in to your azure organization in your terminal, you can begin to use the script. You need to then setup your organization and the project you are working with as your defaults. That can be done using this command.

    az devops configure --defaults organization=https://dev.azure.com/<organization-name> project=<Project Name or ID> 

If you need to find the project id (for example your project name has whitespace) then you can find it by using the list API.

    https://dev.azure.com/<organization-name>/_apis/projects?api-version=5.0

And look for your project there.

### Create variable group

How to create a variable group in your azure devops project can be found here: [Manage variable groups|Create a variable group](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups?view=azure-devops&tabs=azure-devops-cli%2Cyaml#create-a-variable-group)

You will need to make note of the id for your variable group. To find the ids for your variable groups you can run this command:

    az pipelines variable-group list --query-order Asc --output table

### Actually time to use the script

Now you can use the script. First you download the script, then you use the script with this command (Windows):

    py .\addVariablesToVariableGroup.py -g <group-id> -a <path-to-appsettings-file>

It will then begin to add the your config variables to your devops variable group. If any errors happen they are printet to the console.

How to use variable groups for your project is out of scope for this readme. For resources pertaining to their use case, you can read Microsoft's official documentation [Variable groups](https://learn.microsoft.com/en-us/azure/devops/pipelines/library/variable-groups?view=azure-devops&tabs=azure-pipelines-ui%2Cyaml)

## Things to be aware of

If you want a variable to be secret, you will have to manually set it to secret after running the script.

For the variable groups to work as a replacement for appsettings.Environment.json, you will still need the base appsettings.json file to exist in the code base.

The name for each variable in the variable groups is case sensetive to the exisiting name in the appsettings.json file.
