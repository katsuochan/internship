#!/usr/bin/ruby
print("Content-type: text/html\n\n")
print("<html>")
require("kconv")
<<"HTGO"
"<head><meta http-equiv='Content-Type' charset=utf-8/>
</head>"
HTGO
require("cgi")
require("sqlite3")
require("isbn")
require("date")
cgi = CGI.new
name = "%"+cgi["username"]+"%"
place = cgi["place"]
keyword = "%"+cgi["keyword"]+"%"
db=SQLite3::Database.new("testg")
countrylist=Array.new
print("<h1>検索結果一覧</h1>\n")
if place == "" and keyword == "%%"
     db.transaction{
    db.execute("select * from ghyouka where user like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,keyword){|data|
                  countrylist.push(data[1])
     }

  }
   countrylist.uniq!
    #各国中での処理
   countrylist.each{|country|
      eachmonth=Array.new
      print("--------------------------------------------------<br>")
       db.transaction{
           db.execute("select * from ghyouka where user like ? and country like ? ORDER BY country,month, kaisu DESC", name,country){|data|
              if !(eachmonth.include?([data[2]]))
                    eachmonth.push(data[2])
              end         
           }
       }
          eachmonth.uniq!
          eachmonth.each{|month|
           print(month,"<br>")
           stocker = Hash.new
            keys="" 
            values=""
           db.transaction{
               db.execute("select * from ghyouka where user like ? and country like ? and month like? ORDER BY country,month, kaisu DESC", name,country,month){|data|
            #  print(data)
              stocker[data[3]]=data[4]
              } 
          } 
          i = 0
           stocker.each{|key,value|
               keys+=key
               values+=value.to_s
              if i < stocker.size-1
                   keys+="|"
                  values += ","
                  i+=1
               end
            }
           
          print("<img src='http://chart.apis.google.com/chart?chs=200x100&chd=t:"+values+"&cht=p&chl="+keys+"'/>")
        #  print("-----------------------</br>")
       
        }
      print("--------------------<br>")
     #ここまで一国分
  }
elsif place != "" and keyword =="%%"
 db.transaction{
    db.execute("select * from ghyouka where user like ? and country =? ORDER BY country,month, kaisu DESC", name,place){|data|

      print(data,"<br>\n");
     }

  }
elsif place=="" and  keyword !="%%"
   
   db.transaction{
    db.execute("select * from ghyouka where user like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,keyword){|data|
                  countrylist.push(data[1])
     }

  }
   #各国処理
   countrylist.uniq!
   countrylist.each{|country|
      print("<h1>",country,"</h1><br>")
      eachmonth=Hash.new
       db.transaction{
           db.execute("select * from ghyouka where user like ? and country like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,country,keyword){|data|
                  eachmonth[data[2]]=data[4]                    
       }
   }
              keys="" 
              values=""
            i=0
        eachmonth.each{|key,value|
       #       print(key,":",value,"\n")
               keys+=key
               values+=value.to_s
              if i < eachmonth.size-1
                   keys+="|"
                  values += ","
                  i+=1
               end
            }
        print("<img src='http://chart.apis.google.com/chart?cht=lc&amp;chs=300x125&amp;chxt=x,y&amp;chxl=0:|"+keys+"&amp;chd=t:"+values+"&amp;chm=s,FF9904,0,-1,6&chxt=x,y' />")
         print("<br>-------------------------------------------</br>")
        
  }
end
