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
print("<img src='samurai.gif'>")

db  = SQLite3::Database.new("testg")
countrylist=Array.new
    eachmonth=Array.new
 db.transaction{
    db.execute("select * from googledatas where user like ? and country =? and  keyword =?ORDER BY country,month, kaisu DESC", "%"+name+"%",place,keyword){|data|
      eachmonth.push(data[2])
#     print(data)
     }
  }
  eachmonth.uniq!
resouces=Hash.new
print("<br><h2>アクセス元詳細</h2>")
        # print(key)
      # print("")
      # print("<td>"+key+"</td>")
print("<h3>ユーザー名：<font color='green'>#{name}</font></h3>")
print("<h2>キーワード:<font color='red'>#{keyword}</font></h2>")
print("<table>")
print("<tr>")
eachmonth.each{|emo|
   em = emo.to_s
  if em[0].to_i == 0
    em=emo.to_s[1]
  else
    em=emo.to_s
  end
  print("<td><h1>#{em}月</h1></td>")
}
print("</tr>")
eachmonth.each{|emonth|
   keys=""
   values=""
#   print("<table>")
     db.execute("select * from googledatas where user like ? and country = ? and month = ? and keyword  =? ORDER BY country,month, kaisu DESC", "%"+name+"%",place,emonth,keyword){|data|
            if resouces.key?(data[5])
                resouces[data[5]] +=1
            else
               resouces[data[5]] = 1
            end
        #  print(data)
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
          print("<td><img src='http://chart.apis.google.com/chart?chs=300x150&chd=t:"+values+"&cht=p&chl="+keys+"'/></td>")
       resouces=Hash.new
  }
print("</table>")

