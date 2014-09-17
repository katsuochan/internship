#!/usr/bin/ruby
# coding:utf-8
print("Content-type: text/html\n\n")
print("<!DOCTYPE HTML>")
print("<html>")
print(<<"HTGO")
<head><meta charset="UTF-8"/>
</head>
HTGO
require("kconv")
require("cgi")
require("sqlite3")
require("isbn")
require("date")
cgi = CGI.new
name = "%"+cgi["username"]+"%"
place = "%"+cgi["place"]+"%"
keyword="%"+cgi["keyword"]+"%"
print("<body>")
wordhash = Array.new
db  = SQLite3::Database.new("testg")
countryhash=Hash.new
print("<h1>検索結果一覧</h1>\n")
  db.transaction{
    db.execute("select * from ghyouka where user like ? and country like ? and keyword like ?ORDER BY country,month, kaisu DESC", name,place,keyword){|data|
        if wordhash[0]==data[1] and wordhash[1][0]==data[2]
              if wordhash[1][1][0]==data[3]
                  wordhash[1][1][1] += data[4]
              else
                 wordhash[1][1] = [data[3], data[4]]
              end
        else
            wordhash.push([data[1], [data[2], [data[3], data[4]]]])
        end

#       print(data,"<br>\n");
     }

  }

  wordhash.each{|dos|
     if countryhash.key?(dos[1][1][0])
          countryhash[dos[1][1][0]] += dos[1][1][1]
      else
        countryhash[dos[1][1][0]] = dos[1][1][1]
     end
#  print(dos, "<br>")
  }

place = Array.new
beforeplace=""
beforemonth = ""
montht = Array.new
monthword = Hash.new
keys=""
param=""
checkflag=false
wordhash.each{|data|
     
    print(data)
  
   # print("<img src='http://chart.apis.google.com/chart?chs=300x300&chd=t:20,60,50,70,30|14,21,12,18,35&cht=bhg&chco=ff0000,aa0000'/>")  
}


print("おわりー")
print(beforeplace, "\n")
print(beforemonth,"\n")
print("<img src='http://chart.apis.google.com/chart?chs=200x100&chd=t:"+param+"&cht=p&chl="+keys+"'/>")
ckey=""
cparam=""
i=0
print("whole")
countryhash.each{|key,value|
   ckey+=key
   cparam+=value.to_s
   if i<countryhash.size- 1
     ckey+="|" 
     cparam+=","
   end
   i+=1
}
print(ckey, "!!", cparam)
print("<img src='http://chart.apis.google.com/chart?chs=200x100&chd=t:"+cparam+"&cht=p&chl="+ckey+"'/>")
print("</body>")
print("</html>")
