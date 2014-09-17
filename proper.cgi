#!/usr/bin/ruby
#! ruby -Ku
# coding:utf-8
print("Content-type: text/html\n\n")
print("<html>")
require("kconv")
require("cgi")
require("sqlite3")
print <<"HTGO"
<head>
<meta http-equiv='Content-Type' content="text/html; charset=utf-8" />
</head>
HTGO

cgi = CGI.new
name=cgi["name"]
place=cgi["country"]
month=cgi["month"]
keyword=cgi["keyword"]


db  = SQLite3::Database.new("testg")
countrylist=Array.new
    eachmonth=Array.new
 db.transaction{
    db.execute("select * from googledatas where user like ? and country =? and  keyword =?ORDER BY country,month, kaisu DESC", "%"+name+"%",place,keyword){|data|
      eachmonth.push(data[2])
     print(data)
     }
  }
  eachmonth.uniq!
resouces=Hash.new
print("<br><h2>各単語アクセス元詳細</h2>")
        # print(key)
      # print("")
      # print("<td>"+key+"</td>")
print(name)
eachmonth.each{|emonth|
 keys=""
 values=""
print(emonth)
db.execute("select * from googledatas where user like ? and country = ? and month = ? and keyword  =? ORDER BY country,month, kaisu DESC", "%"+name+"%",place,emonth,keyword){|data|
           if resouces.key?(data[5])
              resouces[data[5]] +=1
           else
             resouces[data[5]] = 1
           end
         print(data)
     }
       i=0
        resouces.each{|key, value|
         # print("<td>"+key+"</td>")
         # print(key,":",value,"<br>")
           keys+=key
           values+=value.to_s
           if i<resouces.size-1
              keys+="|"
              values+=","
           end
          i+=1
        }
        print("<td><img src='http://chart.apis.google.com/chart?chs=200x100&chd=t:"+values+"&cht=p&chl="+keys+"'/></td>")
      print("<br>----------</br>")
      resouces=Hash.new
}
=begin
eachmonth.each{|month|
print("<table>")
db.execute("select * from googledatas where user like ? and country = ? and month=? and keyword  =? ORDER BY country,month, kaisu DESC", name,place,month,keyword){|data|
          i=0
          keys=""
          values=""
        resouces.each{|key, value|
         # print("<td>"+key+"</td>")
         # print(key,":",value,"<br>")
           keys+=key
           values+=value.to_s
           if i<resouces.size-1
              keys+="|"
              values+=","
           end
        }
        print("<td><img src='http://chart.apis.google.com/chart?chs=200x100&chd=t:"+values+"&cht=p&chl="+keys+"'/></td>")
     # print("<br>----------</br>")
      resouces=Hash.new
     }
    print("</table>")
}a
=end
