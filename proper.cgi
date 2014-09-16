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
name="%"+cgi["name"]+"%"
place=cgi["country"]
month=cgi["month"]
keyword="%"+cgi["keyword"]+"%"


db  = SQLite3::Database.new("testg")
countrylist=Array.new
    eachmonth=Array.new
 db.transaction{
    db.execute("select * from googledatas where user like ? and country =? ORDER BY country,month, kaisu DESC", name,place){|data|
      eachmonth.push(data[2])
     }
  }
  eachmonth.uniq!
  #各月についての動作
  eachmonth.each{|month|
  print("<h1>",month,"</h1>")
   wordlist = Hash.new
   resouces = Hash.new
   db.transaction{
      db.execute("select * from googledatas where user like? and country =? and month =? ORDER BY country,month,kaisu DESC", name,place,month){|data|
         if wordlist.key?(data[3])
             wordlist[data[3]] += data[4]
         else
             wordlist[data[3]] = data[4]
         end
      }
    }
      keys=""
      values=""
     i=0
     wordlist.each{|key,value|
       keys+=key
       values+=value.to_s
       if i<wordlist.size-1
          keys+="|"
          values+=","
          i+=1
       end
      # print(key,":", value)
     }
     wordlist.each{|key,value|
       db.execute("select * from googledatas where user like ? and month = ? and keyword  =? ORDER BY country,month, kaisu DESC", name,month,key){|data|               }
    }
 print("<img src='http://chart.apis.google.com/chart?chs=300x200&chd=t:"+values+"&cht=p&chl="+keys+"'/>")
keys=""
values=""
print("<br><h2>各単語アクセス元詳細</h2>")
print("<table border='2'>")
wordlist.each{|key,value|
        # print(key)
      # print("")
      # print("<td>"+key+"</td>")
       db.execute("select * from googledatas where user like ? and month = ? and keyword  =? ORDER BY country,month, kaisu DESC", name,month,key){|data|
           if resouces.key?(data[5])
              resouces[data[5]] +=1
           else
             resouces[data[5]] = 1
           end
        }
         print("<td>"+key+"</td>")
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
        }
      # print(keys, ":", values)
         if key !="(not set)"
        print("<td><img src='http://chart.apis.google.com/chart?chs=200x100&chd=t:"+values+"&cht=p&chl="+keys+"'/></td>")
         else
         print("<td><h2><font color='red'>no data</font></h2></td>")
         end
     # print("<br>----------</br>")
      resouces=Hash.new
     }
    print("</table>")
  }
