# Verify and grab the information related to the version of .Net core installed
dotnet --info

# Result of the info
.NET SDK (reflecting any global.json):
 Version:   6.0.401
 Commit:    0906eae6f8

Runtime Environment:
 OS Name:     ubuntu
 OS Version:  22.04
 OS Platform: Linux
 RID:         ubuntu.22.04-arm64
 Base Path:   /usr/share/dotnet/sdk/6.0.401/

global.json file:
  Not found

Host:
  Version:      6.0.9
  Architecture: arm64
  Commit:       163a63591c

.NET SDKs installed:
  6.0.401 [/usr/share/dotnet/sdk]

.NET runtimes installed:
  Microsoft.AspNetCore.App 6.0.9 [/usr/share/dotnet/shared/Microsoft.AspNetCore.App]
  Microsoft.NETCore.App 6.0.9 [/usr/share/dotnet/shared/Microsoft.NETCore.App]

Download .NET:
  https://aka.ms/dotnet-download

Learn about .NET Runtimes and SDKs:
  https://aka.ms/dotnet/runtimes-sdk-info

# Create a new project
mkdir -p arm_comp_proj/ && cd arm_comp_proj/
dotnet new console

# Add the package
dotnet add package Newtonsoft.Json --version 6.0.0

# Output of adding a package
Determining projects to restore...
Writing /tmp/tmpSlvIbk.tmp
info : X.509 certificate chain validation will use the fallback certificate bundle at '/usr/share/dotnet/sdk/6.0.401/trustedroots/codesignctl.pem'.
info : Adding PackageReference for package 'Newtonsoft.Json' into project '/home/ubuntu/test/test.csproj'.
info :   GET https://api.nuget.org/v3/registration5-gz-semver2/newtonsoft.json/index.json
info :   OK https://api.nuget.org/v3/registration5-gz-semver2/newtonsoft.json/index.json 30ms
info : Restoring packages for /home/ubuntu/test/test.csproj...
info :   GET https://api.nuget.org/v3-flatcontainer/newtonsoft.json/index.json
info :   OK https://api.nuget.org/v3-flatcontainer/newtonsoft.json/index.json 23ms
info :   GET https://api.nuget.org/v3-flatcontainer/newtonsoft.json/13.0.1/newtonsoft.json.13.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/newtonsoft.json/13.0.1/newtonsoft.json.13.0.1.nupkg 8ms
info : Installed Newtonsoft.Json 13.0.1 from https://api.nuget.org/v3/index.json with content hash ppPFpBcvxdsfUonNcvITKqLl3bqxWbDCZIzDWHzjpdAHRFfZe0Dw9HmA0+za13IdyrgJwpkDTDA9fHaxOrt20A==.
info : Package 'Newtonsoft.Json' is compatible with all the specified frameworks in project '/home/ubuntu/test/test.csproj'.
info : PackageReference for package 'Newtonsoft.Json' version '13.0.1' added to file '/home/ubuntu/test/test.csproj'.
info : Writing assets file to disk. Path: /home/ubuntu/test/obj/project.assets.json
log  : Restored /home/ubuntu/test/test.csproj (in 336 ms).

# Output of re-adding a package
Determining projects to restore...
Writing /tmp/tmp8GtT62.tmp
info : X.509 certificate chain validation will use the fallback certificate bundle at '/usr/share/dotnet/sdk/6.0.401/trustedroots/codesignctl.pem'.
info : Adding PackageReference for package 'Newtonsoft.Json' into project '/home/ubuntu/test/test.csproj'.
info :   CACHE https://api.nuget.org/v3/registration5-gz-semver2/newtonsoft.json/index.json
info : Restoring packages for /home/ubuntu/test/test.csproj...
info : Package 'Newtonsoft.Json' is compatible with all the specified frameworks in project '/home/ubuntu/test/test.csproj'.
info : PackageReference for package 'Newtonsoft.Json' version '13.0.1' updated in file '/home/ubuntu/test/test.csproj'.
info : Assets file has not changed. Skipping assets file writing. Path: /home/ubuntu/test/obj/project.assets.json
log  : Restored /home/ubuntu/test/test.csproj (in 115 ms).

# Reinstall other version
  Determining projects to restore...
  Writing /tmp/tmpa3lGM6.tmp
info : X.509 certificate chain validation will use the fallback certificate bundle at '/usr/share/dotnet/sdk/6.0.401/trustedroots/codesignctl.pem'.
info : Adding PackageReference for package 'Newtonsoft.Json' into project '/home/ubuntu/test/test.csproj'.
info : Restoring packages for /home/ubuntu/test/test.csproj...
info :   CACHE https://api.nuget.org/v3-flatcontainer/newtonsoft.json/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/newtonsoft.json/12.0.1/newtonsoft.json.12.0.1.nupkg
info :   OK https://api.nuget.org/v3-flatcontainer/newtonsoft.json/12.0.1/newtonsoft.json.12.0.1.nupkg 402ms
info : Installed Newtonsoft.Json 12.0.1 from https://api.nuget.org/v3/index.json with content hash pBR3wCgYWZGiaZDYP+HHYnalVnPJlpP1q55qvVb+adrDHmFMDc1NAKio61xTwftK3Pw5h7TZJPJEEVMd6ty8rg==.
warn : NU1603: test depends on Newtonsoft.Json (>= 12.0.0) but Newtonsoft.Json 12.0.0 was not found. An approximate best match of Newtonsoft.Json 12.0.1 was resolved.
info : Package 'Newtonsoft.Json' is compatible with all the specified frameworks in project '/home/ubuntu/test/test.csproj'.
info : PackageReference for package 'Newtonsoft.Json' version '12.0.0' updated in file '/home/ubuntu/test/test.csproj'.
info : Writing assets file to disk. Path: /home/ubuntu/test/obj/project.assets.json
log  : Restored /home/ubuntu/test/test.csproj (in 821 ms).


# Package not found
ubuntu@ip-172-31-10-226:~/test$ dotnet add package Newtoeffefefnsoft.Json --version 12.0.0
  Determining projects to restore...
  Writing /tmp/tmpeyornY.tmp
info : X.509 certificate chain validation will use the fallback certificate bundle at '/usr/share/dotnet/sdk/6.0.401/trustedroots/codesignctl.pem'.
info : Adding PackageReference for package 'Newtoeffefefnsoft.Json' into project '/home/ubuntu/test/test.csproj'.
info : Restoring packages for /home/ubuntu/test/test.csproj...
info :   CACHE https://api.nuget.org/v3-flatcontainer/newtonsoft.json/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/newtoeffefefnsoft.json/index.json
info :   NotFound https://api.nuget.org/v3-flatcontainer/newtoeffefefnsoft.json/index.json 426ms
warn : NU1603: test depends on Newtonsoft.Json (>= 12.0.0) but Newtonsoft.Json 12.0.0 was not found. An approximate best match of Newtonsoft.Json 12.0.1 was resolved.
error: NU1101: Unable to find package Newtoeffefefnsoft.Json. No packages exist with this id in source(s): nuget.org
error: Package 'Newtoeffefefnsoft.Json' is incompatible with 'all' frameworks in project '/home/ubuntu/test/test.csproj'.

# Version not found
ubuntu@ip-172-31-10-226:~/test$ dotnet add package Newtoeffefefnsoft.Json --version 12.0.0
  Determining projects to restore...
  Writing /tmp/tmpeyornY.tmp
info : X.509 certificate chain validation will use the fallback certificate bundle at '/usr/share/dotnet/sdk/6.0.401/trustedroots/codesignctl.pem'.
info : Adding PackageReference for package 'Newtoeffefefnsoft.Json' into project '/home/ubuntu/test/test.csproj'.
info : Restoring packages for /home/ubuntu/test/test.csproj...
info :   CACHE https://api.nuget.org/v3-flatcontainer/newtonsoft.json/index.json
info :   GET https://api.nuget.org/v3-flatcontainer/newtoeffefefnsoft.json/index.json
info :   NotFound https://api.nuget.org/v3-flatcontainer/newtoeffefefnsoft.json/index.json 426ms
warn : NU1603: test depends on Newtonsoft.Json (>= 12.0.0) but Newtonsoft.Json 12.0.0 was not found. An approximate best match of Newtonsoft.Json 12.0.1 was resolved.
error: NU1101: Unable to find package Newtoeffefefnsoft.Json. No packages exist with this id in source(s): nuget.org
error: Package 'Newtoeffefefnsoft.Json' is incompatible with 'all' frameworks in project '/home/ubuntu/test/test.csproj'.


# Invalid command line
ubuntu@ip-172-31-10-226:~/test$ dotnet add package Newtonsoft.Json --version efefef
  Determining projects to restore...
  Writing /tmp/tmp4fZNtF.tmp
info : X.509 certificate chain validation will use the fallback certificate bundle at '/usr/share/dotnet/sdk/6.0.401/trustedroots/codesignctl.pem'.
info : Adding PackageReference for package 'Newtonsoft.Json' into project '/home/ubuntu/test/test.csproj'.
error: 'efefef' is not a valid version string.


Usage: NuGet.CommandLine.XPlat.dll package add [options]

Options:
  -h|--help               Show help information
  --force-english-output  Forces the application to run using an invariant, English-based culture.
  --package               Id of the package to be added.
  --version               Version of the package to be added.
  -d|--dg-file            Path to the dependency graph file to be used to restore preview and compatibility check.
  -p|--project            Path to the project file.
  -f|--framework          Frameworks for which the package reference should be added.
  -n|--no-restore         Do not perform restore preview and compatibility check. The added package reference will be unconditional.
  -s|--source             Specifies NuGet package sources to use during the restore.
  --package-directory     Directory to restore packages in.
  --interactive           Allow the command to block and require manual action for operations like authentication.
  --prerelease            Allows prerelease packages to be installed.