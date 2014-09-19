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
<title>samura　データサーチャー</title>
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/common.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/ja.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/css/samurai.css" />
<link rel="stylesheet" type="text/css" media="all" href=""http://www.nims.go.jp/samurai.css" />
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
<link rel="stylesheet" type="text/css" href="samu.css"/>
</head>
HTGO
countries = Array.new
name = cgi["username"]
keyword =cgi["keyword"]
db.transaction{
  countries = db.execute("select distinct country from googledatas where user like? ORDER BY kaisu","%"+name+"%")
}
countrylist=["China", "Germany", "India", "Austria", "Japan", "Italy", "Netherlands", "South Korea", "UNited States", "Taiwan", "Australia", "Belgium", "Bolivia", "Brazil", "Canada", "Egypt", "France", "Hong Kong", "Hungary", "Iran", "Mexico", "Pakistan", "Philippines", "Russia", "Singapore", "Spain", "Sweden", "Taiwan", "United Kingdom", "Vietnam"]
print("<body>")
print("<div id='whole' align='center'>")
print("<div id='wide' align='center'>")
print("<img src='samurai.gif'>")
print(<<"HTG")
<font color="green">説明</font>
<div id="top">
  このページでは、SAMURAIにおける研究者個人のページが、どのような国からどのような検索語で検索されたかをグラフで表示します。国別に研究者個人ページへの検索履歴を知りたい場合は「表示対象国一覧」の国名をクリックしてください。また、研究者個人へのページへアクセスされた際の検索キーワードとその回数の推移を国別表示したい場合は「キーワード検索」に検索語を入力するか、「キーワード一覧」の検索語をクリックしてください。
</div>
HTG
print("<h1>表示対象国一覧</h1>")

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
#print("</div>")
#print("<div id='wide'>")
print("<h1>キーワード検索</h1>")
print(<<"HTG2")
<form action="touchs.cgi" method="get">
<input type="text" name="keyword" value=""/>
<input type="hidden" name="username" value="#{name}"/>
<input type="submit" value="検索">
</form>
HTG2
print("<h3>キーワード一覧</h3>")
result.each do |word|
  puts"<a href='touchs.cgi?name=#{name}&keyword=#{word[0]}'><font color='red'>",word,"</font></a>&nbsp; ,&nbsp; "
end
#print("</div>")
print(<<"HTGO3")
<div id='spacer'>
</div>
<div id="footer">
   
<div id="cent">独立行政法人物質・材料研究機構　〒305-0047 茨城県つくば市千現1-2-1<br />
TEL.029-859-2000 (代表)　E-mail:info=nims.go.jp<small>([ = ] を [ @ ] にしてくだ
さい)</small><br />
Copyright &copy; 2001-2013 National Institute for Materials Science (NIMS).
</div>
HTGO3
print("</div>")
print("</div>")


print("</body>")
print("</html>")

