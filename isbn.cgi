#!/usr/bin/ruby
print("Content-type: text/html\n\n")
print("<head><meta http-equiv='Content-Type' charset=utf-8/></head>")
require("cgi")
require("sqlite3")
require("isbn")
cgi = CGI.new
isbn = "9784797357400";
if  ISBN.valid? isbn
   if isbn.length==13 
     print("10表記 : ")
     print(ISBN.ten isbn)
     print("<br>旧表記 : ")
     print(ISBN.as_used isbn);
   elsif isbn.length==10
     print("13表記 : ")
     print(ISBN.thirteen isbn);
     print("<br>旧表記 ; ")
     print(ISBN.as_used isbn);
   else
     print("変更できない")
   end
else
   print("ただしいisbnを記述してください")
end
