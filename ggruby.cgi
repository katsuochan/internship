#!/usr/bin/ruby
#coding:utf-8
print("Content-type: text/html\n\n")
print("<html>")
require("cgi")
cgi = CGI.new
print(<<"HTGO")
<head>
<meta charset="utf-8"/>
</head>
<body>
<img src="http://chart.apis.google.com/chart?cht=p3&chd=s:hW
&chs=250x100&chl=Hello|World"/>
<div id="visualization"></div>
HTGO
print("<img src='http://chart.apis.google.com/chart?cht=p3&chd=s:hW
&chs=250x100&chl=Hello|World'/>")
print("</body>")
print("</html>")
