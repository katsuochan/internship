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

analytics = client.discovered_api('analytics', 'v3')

# ここでDLしたJSONを読み込んでいるので同じディレクトリにclient_secrets.jsonを置いておくこと
client_secrets = Google::APIClient::ClientSecrets.load

# Run installed application flow. Check the samples for a more
# complete example that saves the credentials between runs.
flow = Google::APIClient::InstalledAppFlow.new(
  :client_id => client_secrets.client_id,
  :client_secret => client_secrets.client_secret,
  :scope => ['https://www.googleapis.com/auth/analytics.readonly'],
    :redirect_uri => 'http://localhost:9292'
)
client.authorization = flow.authorize
wordhash = Hash.new
# 各ページのPV数
result = client.execute(
  :api_method => analytics.data.ga.get,
  :parameters => {
    'ids' => 'ga:90686374', # 自分のプロパティID
    'start-date' => '2013-07-01',
    'end-date' => '2014-09-10',
   'metrics' =>'ga:visitors,ga:visits,ga:pageviews',
    #'dimensions' => 'ga:pagePath,ga:pageTitle, ga:browser',
     'dimensions' => 'ga:region,ga:month,ga:keyword',
    'sort' => '-ga:pageviews'
  }
)


res = result.response.body.force_encoding("UTF-8")
body = JSON.parse(res)

db = SQLite3::Database.new("testg")

body['rows'].each do |vl|
  #print(vl,"\n")
  sql = "insert into ghyouka values(\"WADAKEISHI\",\""+vl[0]+"\", \""+vl[1]+"\", \""+vl[2]+"\", \""+vl[5]+"\");"
   begin
   db.transaction{
    db.execute(sql)
   } 
   rescue =>e
     puts e
   end
 
  #print("\""+vl[0]+"\", \""+vl[1]+"\", \""+vl[2]+"\", \""+vl[5]+"\");");
end
=begin
db = SQLite3::Database.new("testg")
 db.transaction{
    db.execute(sql) 
 }
=end
