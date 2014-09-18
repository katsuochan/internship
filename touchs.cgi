#!/usr/bin/ruby
#coding:utf-8
print("Content-type: text/html\n\n")
print("<!DOCTYPE HTML>")
print("<html>")
require("kconv")
print(<<"HTGO")
<head><meta charset="UTF-8"/>
<link rel="stylesheet" type="text/css" href="samu.css"/>
<title>表示結果</title>
</head>
HTGO
require("cgi")
require("sqlite3")
require("isbn")
require("date")
cgi = CGI.new
name = "%"+cgi["username"]+"%"
place = cgi["place"]
keyword = "%"+cgi["keyword"]+"%"
today = Date.today
db=SQLite3::Database.new("testg")
countrylist=Array.new
print("<body>")
print("<div id='whole'>")
print("<img src='samurai.gif'>")
print("<h1>検索結果一覧</h1>\n")
if place == "" and keyword == "%%"
     db.transaction{
    db.execute("select * from googledatas where user like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,keyword){|data|
                  countrylist.push(data[1])
     }

 }
   countrylist.uniq!
    #各国中での処
   countrylist.each{|country|
    print("<table border='2'>")
      eachmonth=Array.new
print("<h1>----------------------",country,"----------------------------<br></h1>")
       db.transaction{
           db.execute("select * from googledatas where user like ? and country like ? ORDER BY country,month, kaisu DESC", name,country){|data|
              if !(eachmonth.include?([data[2]]))
                    eachmonth.push(data[2])
              end         
           }
       }
          eachmonth.uniq!
          eachmonth.each{|month|
           stocker = Hash.new
            keys="" 
            values=""
           db.transaction{
               db.execute("select * from googledatas where user like ? and country like ? and month like? ORDER BY country,month, kaisu DESC", name,country,month){|data|
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
          print("<th>"+month+"</th>")
          print("<td><img src='http://chart.apis.google.com/chart?chs=200x100&chd=t:"+values+"&cht=p&chco=0000ff&chl="+keys+"'/></td>")
        #  print("-----------------------</br>")
      gname = name.gsub(/\%/, '')
      gkeyword= keyword.gsub(/\%/, '')
      print("<td><a href='proper.cgi?name=#{gname}&country=#{country}&month=#{month}&keyword=#{gkeyword}'>property</a></td>")
       
        }
      print("</table>")
     #ここまで一国分
  }
elsif place != "" and keyword =="%%"
    print("<table border='1'>")
    mc=0
    eachmonth=Array.new
tm = today.month
maryc=1
while maryc <= tm
    if maryc < 10
    str = "0".concat(maryc.to_s)
    eachmonth.push(str)
    else
      eachmonth.push(maryc.to_s)
    end
    maryc+=1
end
#eachmonth=["01","02","03","04","05","06","07","08","09","10","11","12"]
  eachmonth.uniq!
  #各月についての動作
  eachmonth.each{|month|
  mc+=1
  if mc % 3==1
     print("<tr>")
  end
  print("<td>")
  print("<h1>",month.to_s[1],"月</h1>")
   wordlist = Hash.new
   db.transaction{
      db.execute("select * from googledatas where user like? and country =? and month =? ORDER BY country,month,kaisu DESC", name,place,month){|data|
         if wordlist.key?(data[3])
             wordlist[data[3]] += data[4] 
         else
             if data[3]!="(not set)" && data[3]!="(not provided)"
             wordlist[data[3]] = data[4] 
             end
         end  
      }
    }
      keys=""
      values=""
     i=0
    cv=0
   wordlist= wordlist.sort_by{|key,val| -val}
    wordlist.each{|key,value|
       if cv==10
        break;
       end
       keys+=key
       values+=value.to_s
       if i<wordlist.size-1 && cv!=9
          keys+="|"
          values+=","
          i+=1
       end
       cv+=1
      # print(key,":", value)
     }
    
  if wordlist.size>0
 print("<img src='http://chart.apis.google.com/chart?chs=300x200&chd=t:"+values+"&cht=p&chl="+keys+"'/>")
  else
     print("<div style='width:100px;height:100px'></div><font color='red' size=15px >sorry,no&nbsp;data</font><br>
      <font color='green' size=6px>reasons</font><br>・visitors come to your page through  <font color='red'>direct access</font> <br>・
      visitors <font color='red'>invalidate their cookie</font><div style='width:300px;height:190px'><font color='red'>・google has stopped providing keyword</div>")
  end
   keys=""
   values=""
   if wordlist.size>0
   print("<br><h2>アクセスキーワード一覧（クリックで詳細）</h2>")
   print("<div id='prop'>")
 i=0
  cv=0
 wordlist= wordlist.sort_by{|key,val| -val}
   wordlist.each{|key,value|
        if cv==9
           break;
        end
           cv+=1
          i+=1
       if i<4
       print("・<a style='color:#ff0000;'red href='proper.cgi?month=#{month}&name=#{name.gsub(/\%/,'')}&country=#{place}&keyword=#{key.gsub(/\%/,'')}'/>#{key}</a>")
        else
        print("・<a  href='proper.cgi?month=#{month}&name=#{name.gsub(/\%/,'')}&country=#{place}&keyword=#{key.gsub(/\%/,'')}'/>#{key}</a>")
      end
     }
     end
    print("</div>")
    print("</td>")
    if mc % 3==0
       print("</tr>")
    end
  }
print("</table>")
elsif place=="" and  keyword !="%%"
   print("<h1><font color='red'>#{keyword.gsub(/\%/,'')}</font></h1>")
   db.transaction{
    db.execute("select * from googledatas where user like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,keyword){|data|
                  countrylist.push(data[1])
     }

  }
   #各国処理
   countrylist.uniq!
   countrylist.each{|country|
     # print("<h1>",keyword.gsub(/\%/, ''),"</h1><br>")
      eachmonth=Hash.new
       db.transaction{
           db.execute("select distinct * from googledatas where user like ? and country like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,country,keyword){|data|
              if eachmonth.key?(data[2])    
                 eachmonth[data[2]] +=data[4]
              else
                 eachmonth[data[2]] =data[4]     
              end          
       }
   }
              keys="" 
              values=""
            i=0
arymoji=""
i=0
counter = eachmonth.size-1
eachmonth.each{|key,value|
     arymoji+="[#{key},#{value}]"
      if i < counter
         arymoji+=","
         i+=1
      end
}

print(<<"HTGOs")
   <script type="text/javascript" src="https://www.google.com/jsapi"></script>
    <script type="text/javascript">
      google.load("visualization", "1", {packages:["corechart"]});
      google.setOnLoadCallback(drawChart);
      function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ["month", "kaisu"],
            #{arymoji}
        ]);

        var options = {
          title: '#{country}',
          hAxis: {title: 'アクセス月', minValue: 1, maxValue: #{today.month}},
          vAxis: {title: 'アクセス回数', minValue: 0, maxValue: 20},
        };

        var chart = new google.visualization.LineChart(document.getElementById('#{country}'));

        chart.draw(data, options);
      }
    </script>
HTGOs
print("<div id='#{country}'></div>")
=begin
        print("<img src='http://chart.apis.google.com/chart?cht=lc&amp;chs=300x125&amp;chxt=x,y&amp;chxl=0:|"+keys+"&amp;chd=t:"+values+"&amp;chm=s,FF9904,0,-1,6&chxt=x,y' />")
         print("<br>-------------------------------------------</br>")
=end  
  }
end
print("</div>")
print("</body>")
print("</html>")
