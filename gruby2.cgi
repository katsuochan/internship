#!/usr/bin/ruby
require 'google/api_client'
require 'date'
require("cgi")
# Update these to match your own apps credentialsa
print("Content-type:text/html\n\n")
service_account_email = '866879777618-0sskm8h7kcp99pp2nmp7rkdjis0d2hqg@developer.gserviceaccount.com' # Email of service account
key_file = './My Project-3b616e3135d5.p12' # File containing your private key
key_secret = 'notasecret' # Password to unlock private key
profileID = '90686374' # Analytics profile ID.


client = Google::APIClient.new(:application_name => 'deveropment test',
  :application_version => '0.7.1')

# Load our credentials for the service account
key = Google::APIClient::KeyUtils.load_from_pkcs12(key_file, key_secret)
client.authorization = Signet::OAuth2::Client.new(
  :token_credential_uri => 'https://accounts.google.com/o/oauth2/token',
  :audience => 'https://accounts.google.com/o/oauth2/token',
  :scope => 'https://www.googleapis.com/auth/analytics.readonly',
  :issuer => service_account_email,
  :signing_key => key)

# Request a token for our service account
client.authorization.fetch_access_token!

analytics = client.discovered_api('analytics','v3')

startDate = DateTime.now.prev_month.strftime("%Y-%m-%d")
endDate = DateTime.now.strftime("%Y-%m-%d")

visitCount = client.execute(:api_method => analytics.data.ga.get, :parameters => { 
  'ids' => "ga:" + profileID, 
  'start-date' => startDate,
  'end-date' => endDate,
  'dimensions' => "ga:day,ga:month",
  'metrics' => "ga:visits",
  'sort' => "ga:month,ga:day" 
})

print visitCount.data.column_headers.map { |c|
  c.name  
}.join("\t")
visitCount.data.rows.each do |r|
  print r.join("\t"), "\n"
end
