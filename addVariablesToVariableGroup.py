import subprocess, sys, getopt, json, os

def run(cmd):
    completed = subprocess.run(["powershell", "-Command", cmd], capture_output=True)
    return completed

def readAppsettings(data, keystring, appsettingsDict):
    for k, v in data.items():
        if isinstance(v, dict):
            if keystring == "":
                appsettingsDict = readAppsettings(v, k, appsettingsDict)
            else:
                appsettingsDict = readAppsettings(v, keystring+"__"+k, appsettingsDict)
            
        else:
            if keystring == "":
                appsettingsDict[k] = v
            else:
                appsettingsDict[keystring+"__"+k] = v

    return appsettingsDict

def getArguments(argv):
    groupId = ''
    appsettingsFilePath = ''

    try:
        opts, args = getopt.getopt(argv,"hg:a:")
    except getopt.GetoptError:
        print ('-g <group-id> -a <appsettings-file-path>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print ('-g <group-id> -a <appsettings-file-path>')
            sys.exit()
        elif opt in ("-g"):
            groupId = arg
        elif opt in ("-a"):
            appsettingsFilePath = os.path.abspath(arg)

    return groupId, appsettingsFilePath

def uploadVariables(appsettingsDictionary, groupId):
    for k, v in appsettingsDictionary.items():
        name = k
        value = v

        azureCmd = f"az pipelines variable-group variable create --group-id {groupId} --secret false --name '{name}' --value '{value}'"
        completed = run(azureCmd)
        if completed.returncode != 0:
            print("%s", completed.stderr)
        else:
            print(f"Added to the variable group: {name}: {value}")

def main(argv):
    
    groupId, appsettingsFilePath = getArguments(argv)
        
    with open(appsettingsFilePath, encoding='utf-8-sig') as f:
        data = json.load(f)
    appsettingsDict = readAppsettings(data, "", {})
    
    uploadVariables(appsettingsDict, groupId)

if __name__ == '__main__':
    main(sys.argv[1:])