#!/usr/bin/ruby
# coding:utf-8

require("kconv")
require("sqlite3")
name = "WADAKEISHI"
 place ="Ibaraki Prefecture"
wordhash = Hash.new
db  = SQLite3::Database.new("testg")
print("<h1>検索結果一覧</h1>\n")
  db.transaction{
     db.execute("select * from ghyouka where country=? and user=? ORDER BY month, kaisu",place, name){|data|
        if wordhash[0]==(data[1]) and wordhash[1]==(data[2])
              #国名と月が同じ場合
              if wordhash[2][0]==data[3]
                   #かつキーワードがすでに存在する場合
                  wordhash[2][1] += data[4]
              else
                  #初めてのキーワードの場合
                 wordhash[2] = [data[3], data[4]]
              end
        else
            #初めての国名と月のペアの場合
            wordhash = [data[1], data[2], [data[3], data[4]]]
        end


        print(data,"\n");
     }

  }

