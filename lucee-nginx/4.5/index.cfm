<cfset system = createobject("java", "java.lang.System")>
<cfset env = system.getEnv()>
<cfset headers = GetHttpRequestData().headers>

<cfoutput>
<h1>Hello Cruel World!</h1>

<p>
	Lucee #server.lucee.version# released #dateformat(server.lucee["release-date"], "dd mmm yyyy")#<br>
	#server.servlet.name# (java #server.java.version#) running on #server.os.name# (#server.os.version#)<br>
	Hosted at #headers.host#
</p>


<h2>Server Internals</h2>

<cfoutput><p>As at #now()#</p></cfoutput>

<h3>Environment Variables</h3>
<cfdump var="#env#" label="system.getEnv()">

<h3>Cookie Variables</h3>
<cfdump var="#cookie#" label="Cookie">

<h3>Server Variables</h3>
<cfdump var="#server#" label="Server">

<h3>HTTP Request Variables</h3>
<cfdump var="#headers#" label="GetHttpRequestData().headers">

<!--- Writes some data to the log files --->
<cflog file="application" text="Testing application.log at #now()#" log="application">
<cflog file="exception" text="Testing exception.log at #now()#" log="application">
<cflog file="orm" text="Testing orm.log at #now()#" log="application">
<cflog file="mail" text="Testing mail.log at #now()#" log="application">


</cfoutput>