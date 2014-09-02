#!/usr/bin/ruby
#! ruby -Ku
# coding:utf-8
print("Content-type: text/html\n\n")
print("<html>")
require("kconv")
print("<head><meta http-equiv='Content-Type' charset=utf-8/></head>")
require("cgi")
require("sqlite3")
require("isbn")
cgi = CGI.new

title = "%"+cgi["title"].gsub("/(\%|\&)/", "")+"%"
author = "%"+cgi["author"].gsub(/(\%|\&)/, "")+"%"
publisher = "%"+cgi["publisher"].gsub(/(\%|\&)/, "")+"%"
isbn=cgi["isbn"]


db  = SQLite3::Database.new("test")
print("<h1>検索結果一覧</h1>\n")
print("<table border=2>")
print("<th>タイトル</th><th>著者</th><th>出版社</th><th>ISBN</th>")
  if ISBN.valid? isbn or isbn==""
      if isbn.length=="10"
        isbn = ISBN.thirteen isbn
      end
     isbn = "%"+isbn+"%"
  db.transaction{
     db.execute("select * from opad where title like  ? and author like ? and
   publisher like ? and isbn like ?;", title, author, publisher,isbn){|row|
          print("<tr><td>"+row[0]+"</td><td>"+row[1]+"</td><td>"+row[2]+"</td><td>"+row[3]+"</td></tr>")
       # print("<a href='http://komorido.nims.go.jp/~a013149/delete.cgi?title=#{row[0]}'>delete</a></br>")
     
    }
  print("</table>")
  }
  else
   print("aaaaaaaaaaaaaa")
  end
