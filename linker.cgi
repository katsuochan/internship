#!/usr/bin/ruby
#coding:utf-8
print("Content-type: text/html\n\n")
print("<html>")
require("cgi")
require("sqlite3")
require("nkf")
cgi = CGI.new
db = SQLite3::Database.new("testg")
print(<<"HTGO")
<head>
<link rel="stylesheet" type="text/css" href="samu.css"/>
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/common.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/ja.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/css/samurai.css" />
<link rel="stylesheet" type="text/css" media="all" href=""http://www.nims.go.jp/samurai.css" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
<div id='whole'>
HTGO
countries = Array.new
name = cgi["username"]
keyword =cgi["keyword"]
db.transaction{
  countries = db.execute("select distinct country from googledatas where user like? ORDER BY kaisu","%"+name+"%")
}
countrylist=["China", "Germany", "India", "Austria", "Japan", "Italy", "Netherlands", "South Korea", "UNited States", "Taiwan", "Australia", "Belgium", "Bolivia", "Brazil", "Canada", "Egypt", "France", "Hong Kong", "Hungary", "Iran", "Mexico", "Pakistan", "Philippines", "Russia", "Singapore", "Spain", "Sweden", "Taiwan", "United Kingdom", "Vietnam"]
print("<body>")
print("<div id='wide'>")
print("<img src='samurai.gif'>")
print("<h1>対象国一覧</h1>")

countries.each{|co|
 co=co[0]
 print("<a href='touchs.cgi?username=#{name}&place=#{co}&keyword=#{keyword}'>#{co}</a> ")
}
print("</br>")
wordlist = Array.new
result=Array.new
db.transaction{
  result = db.execute("select distinct keyword from googledatas where user like? ORDER BY kaisu  LIMIT 20 ","%"+name+"%")
#p result
}
print("</div>")
print("<h1>キーワード検索</h1>")
print(<<"HTG2")
<form action="touchs.cgi" method="get">
<input type="text" name="keyword" value=""/>
<input type="hidden" name="username" value="#{name}"/>
<input type="submit" value="検索">
</form>
HTG2
print("</div>")
print("<h3>キーワード一覧</h3>")
print("<div id='wide'>")
result.each do |word|
  puts"<font color='red'>",word,"</font>&nbsp; ,&nbsp; "
end
print("</div>")


print("</div>")
print("</body>")
print("</html>")


