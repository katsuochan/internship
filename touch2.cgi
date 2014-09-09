#!/usr/bin/ruby
# coding:utf-8
print("Content-type: text/html\n\n")
print("<html>")
require("kconv")
print("<head><meta http-equiv='Content-Type' charset=utf-8/></head>")
require("cgi")
require("sqlite3")
require("isbn")
cgi = CGI.new
name = cgi["username"]
#place = cgi["place"]
print("<body>")
wordhash = Array.new
db  = SQLite3::Database.new("testg")
print("<h1>検索結果一覧</h1>\n")
  db.transaction{
    db.execute("select * from ghyouka where user=? ORDER BY country,month, kaisu DESC", name){|data|
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
=begin
wordhash.each{|dos|
  print(dos, "<br>")
}
=end
place = Array.new
beforemonth = ""
montht = Array.new
monthword = Hash.new
wordhash.each{|data|
    #新しい国の表示になった場合、場所リストを増やし、つきをリセット、
    if !(place.include?(data[0]))
         place.push(data[0])
         montht=Array.new
    end
   #もし新しい月になった場合、その前の月のデータを出す
    if !(montht.include?(data[1][0])) and place.include?(data[0])
        keys=""
        param=""
         c =0
#       print("aaaa")
         monthword.each{|word,value|
        #   print(word, ":", monthword[word],"<br>")
          keys+=word
          param+=monthword[word].to_s
#        print(key,"!!")
#          print(param)
            if c <monthword.size-1
               keys+="|"
               param+=","
            end
            c += 1
         }  
       # print(keys,":", param)
          print(beforemonth,"<br>")
          print("<img src='http://chart.apis.google.com/chart?chs=460x230&chd=t:"+param+"&cht=p&chl="+keys+"'/>")
#print("<img src='http://chart.apis.google.com/chart?cht=p3&chd=t:12,13&chs=250x100&chl=Hello|World'/>")

        # monthword=Hash.new
         montht.push(data[1][0])
        # keys=""
        # param=""
    end
       beforemonth=data[1][0]
       monthword[data[1][1][0]]=data[1][1][1]
     # print(data[1][1][0])
 #    print(data[1][0])
   # print("<img src='http://chart.apis.google.com/chart?chs=300x300&chd=t:20,60,50,70,30|14,21,12,18,35&cht=bhg&chco=ff0000,aa0000'/>")  
}
print("</body>")
print("</html>")
