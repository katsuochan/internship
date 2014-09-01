#!/usr/bin/ruby
#! ruby -Ku
print "Content-type: text/html\n\n"
print("<html")
print "<head><meta http-equiv='Content-Type' charset=utf-8/></head>"
require("cgi")
require("sqlite3")
cgi = CGI.new
title = cgi["title"]
author = cgi["author"]
publisher = cgi["publisher"]
isbn=cgi["isbn"]
sql  ="select * from opad where title=\""+title+"\" or author=\""+author+"\" or
 publisher=\""+publisher+"\" or isbn=\""+isbn+"\";"
print(title);
db  = SQLite3::Database.new("test")
 print("a")
db.transaction{
   db.execute(sql){|row|
        print(row)
     
   }
}
