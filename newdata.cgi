#!/usr/bin/ruby
require("cgi")
require("sqlite3")
require("isbn")
require("./isnnm.rb")
require("library_stdnums")
cgi = CGI.new
print("Content-type: text/html\n\n")
print("<head><meta http-equiv='Content-Type' charset=utf-8/></head>")
title = cgi["title"].gsub(/(\%|\&|\"|\;)/, "")
author = cgi["author"].gsub(/(\%|\&|\"|\;)/, "")
publisher = cgi["publisher"].gsub(/(\%|\&|\"|\;)/, "")
isbn=cgi["isbn"].gsub(/(\%|\&|\"|\;)/, "")
issn = cgi["issn"]
if ISBN.valid? isbn or isbn==""
  isbn = ISBN.thirteen isbn 
  if issn=="" or  StdNum::ISSN.valid?(issn)
   issn =  StdNum::ISSN.normalize(issn)
  else
   print("issnが変だよ")
   exit;
  end
  sql  ="insert into opad values(\""+title+"\",\""+author+"\",\""+publisher+"\", \""+isbn+"\", \""+issn+"\");"
  print(title);
  db  = SQLite3::Database.new("test")
  db.transaction{
   db.execute(sql)
 }
else
  print("isbnがおかしいよ")
end


