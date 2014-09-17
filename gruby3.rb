#!/usr/bin/ruby
# coding: utf-8
require 'pp'
require 'json'
require 'nkf' 
require  'sqlite3'
require 'google/api_client'
require 'google/api_client/client_secrets'
require 'google/api_client/auth/installed_app'
#print ("Content-type:text/html\n\n")
# Initialize the client.
ENV["http_proxy"] = "http://wwwout.nims.go.jp:8888"
ENV["https_proxy"] = "http://wwwout.nims.go.jp:8888"
client = Google::APIClient.new(
  :application_name => 'deveropment test',
  :application_version => '0.0.1'
)
y=2014
sm=1
sd=1
em=1
ed=2
analytics = client.discovered_api('analytics', 'v3')

# ここでDLしたJSONを読み込んでいるので同じディレクトリにclient_secrets.jsonを置いておくこと
client_secrets = Google::APIClient::ClientSecrets.load


flow = Google::APIClient::InstalledAppFlow.new(
  :client_id => client_secrets.client_id,
  :client_secret => client_secrets.client_secret,
  :scope => ['https://www.googleapis.com/auth/analytics.readonly'],
    :redirect_uri => 'http://localhost:9292'
)
client.authorization = flow.authorize
wordhash = Hash.new
# 各ページのPV数
while em<13
  vsd=sd.to_s
  vsm=sm.to_s
  vem=em.to_s
  ved=ed.to_s
  if sm<10
      vsm="0"+sm.to_s
  end
  if sd<10
      vsd="0"+sd.to_s
  end
  if ed<10
     ved="0"+ed.to_s
  end
  if em<10
      vem="0"+em.to_s
  end
result = client.execute(
  :api_method => analytics.data.ga.get,
  :parameters => {
   # 'ids' => 'ga:90686374', # 自分のプロパティID
    'ids' => 'ga:38208115',
    'start-date' => '2014-'+vsm+'-'+vsd+'',
    'end-date' => '2014-'+vem+'-'+ved+'',
   'metrics' =>'ga:visitors,ga:visits,ga:pageviews',
     'dimensions' => 'ga:country, ga:date,ga:keyword,ga:source,ga:pagePath',
    'sort' => '-ga:pageviews'
    } 
   )



    res = result.response.body.force_encoding("UTF-8")
    body = JSON.parse(res)
i=0  
 db = SQLite3::Database.new("testg")
body['rows'].each do |vl|
    print(vl,"\n")
    
    vlf = vl[4].sub(/\//, '') 
    vlf = vlf.sub(/\-(\w|\.|\_)*/, '')
    ymds = vl[1].to_s
    wct = 0
    md = ""
    ymds.each_char{|b|
      if wct==4 || wct==5
        md.concat(b)
        wct+=1
      else
        wct +=1
      end
    }
     sql = "insert into googledatas values(\""+vlf+"\",\""+vl[0]+"\", \""+md+"\", \""+vl[2]+"\", \""+vl[5]+"\",\""+vl[3]+"\", \""+vl[1]+"\");"
     begin
      db.transaction{
      db.execute(sql)
     } 
     rescue =>e
      db.transaction{
        begin
        db.execute("delete from googledatas where user=\""+vlf+"\" and country=\""+vl[0]+"\" and month=\""+md+"\" and keyword=\""+vl[2]+"\" and source=\""+vl[3]+"\" and cdate=\""+vl[1]+"\";")
        db.execute(sql)
        rescue=>e
           sd+=1
            ed+=1
          if ed>30
             em+=1
             sm+=1
             sd=1
             ed=1
          end
          sleep(3)
            print(i,"回目の回収終了：",sm,"月",sd,"日") 
          next
        end
      }
     end
   
     i+=1
    #print("\""+vl[0]+"\", \""+vl[1]+"\", \""+vl[2]+"\", \""+vl[5]+"\");"); 
  end
   sd+=1
   ed+=1
   if ed>30
     em+=1
     sm+=1
     sd=1
     ed=1
   end
   sleep(2)
    print(i,"回目の回収終了：",sm,"月",sd,"日") 

end