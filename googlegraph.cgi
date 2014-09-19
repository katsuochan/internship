#!/usr/bin/ruby
#coding:utf-8
require "benchmark"
require("cgi")
require("sqlite3")
require("isbn")
require("date")
require("kconv")

benchmark = Benchmark.realtime do
print("Content-type: text/html\n\n")
print("<!DOCTYPE HTML>")
print("<html>")


cgi = CGI.new
name = "%"+cgi["username"]+"%"
place = cgi["place"]
keyword = "%"+cgi["keyword"]+"%"
today = Date.today
db=SQLite3::Database.new("testg")
countrylist=Array.new
print(<<"HTGO")
<head><meta charset="UTF-8"/>
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/common.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/ja.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/common/css/samurai.css" />
<link rel="stylesheet" type="text/css" media="all" href="http://www.nims.go.jp/samurai.css" />
<link rel="stylesheet" type="text/css" href="samu.css"/>
<title>表示結果</title>
</head>
HTGO
print("<body>")
print("<div id='whole' align='center'>")
print("<div id='whole2' align='center'>")
print("<img src='samurai.gif'>")
print("<h1>検索結果一覧</h1>\n")
if place == "" and keyword == "%%"
     db.transaction{
    db.execute("select DISTINCT * from googledatas where user like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,keyword){|data|
                  countrylist.push(data[1])
     }

 }
    #各国中での処
   countrylist.each{|country|
    print("<table border='2'>")
      eachmonth=Array.new
print("<h1>----------------------",country,"----------------------------<br></h1>")
       db.transaction{
           db.execute("select DISTINCT * from googledatas where user like ? and country like ? ORDER BY country,month, kaisu DESC", name,country){|data|
              if !(eachmonth.include?([data[2]]))
                    eachmonth.push(data[2])
              end         
           }
       }
       
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
    print("<h1><font color='red'>#{place}</font></h1>")
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
  #各月についての動作
  eachmonth.each{|month|
  mc+=1
  if mc % 3==1
     print("<tr>")
  end
  print("<td>")
  print("<h2>",month.to_s[1],"月</h2>")
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
   print("<br><h3>アクセスキーワード一覧（クリックで詳細）</h3>")
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
    db.execute("select DISTINCT * from googledatas where user like ? and keyword like ? ORDER BY country,month, kaisu DESC", name,keyword){|data|
                  countrylist.push(data[1])
     }

  }
   #各国処理

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

tm = today.month
monthary = ["01","02","03","04","05","06","07","08","09","10","11","12"]
monthary.each_with_index{|monthe,i|
  if i>=tm
   break
  end
    
  if not(eachmonth.has_key?(monthe)) 
      eachmonth[monthe]=0
  end
}

eachmonth=eachmonth.sort_by{|a,b| a}
counter = eachmonth.size-1
eachmonth.each{|key,value|
     arymoji+="[#{key},#{value}]"
      if i < counter
         arymoji+=","
         i+=1
      end
}
#print(arymoji)
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

end
#puts benchmark
print(<<"FOOT")
<div id="footer">

<div id="cent">独立行政法人物質・材料研究機構　〒305-0047 茨城県つくば市千現1-2-1<br />
TEL.029-859-2000 (代表)　E-mail:info=nims.go.jp<small>([ = ] を [ @ ] にしてくだ
さい)</small><br />
Copyright &copy; 2001-2013 National Institute for Materials Science (NIMS).
</div>
FOOT
print("</div>")
print("</div>")
print("</body>")
print("</html>")
