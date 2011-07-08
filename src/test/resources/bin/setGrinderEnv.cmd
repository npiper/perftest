@ECHO OFF
set GRINDERPATH=%CD%

set GRINDERPROPERTIES=%CD%\grinder.properties

if NOT exist %WL_HOME%\server\lib\weblogic.jar (
	echo The Weblogic JDK was not found in directory %WL_HOME%. ^(WL_HOME^)
	echo Please edit your environment and set the WL_HOME
	echo variable to point to the root directory of your Weblogic Server installation.
	popd
	pause
	GOTO :EOF
)

if NOT exist %JAVA_HOME%\lib (
	echo The JRE was not found in directory %JAVA_HOME%. ^(JAVA_HOME^)
	echo Please edit your environment and set the JAVA_HOME
	echo variable to point to the root directory of your Java installation.
	popd
	pause
	GOTO :EOF
)

set WL_CLASSPATH=%WL_HOME%\server\lib\weblogic.jar;%WL_HOME%\server\lib\wls-api.jar

set CLASSPATH=%GRINDERPATH%\..\..\..\lib\grinder.jar;%WL_CLASSPATH%;%CLASSPATH%

set JAVA_HOME=%JAVA_HOME%

PATH=%JAVA_HOME%\bin;%PATH%


:CMD_LINE_DONE