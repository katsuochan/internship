#!/usr/bin/ruby
print("Content-type:text/html\n\n")
print("<head><meta http-equiv='Content-Type' charset=utf-8/></head>")
require("cgi")
require("sqlite3")
#require("./isnnm.rb")
cgi = CGI.new
issn = "1234-567"

def issnrt(issn)
  issnm = issn.gsub(/-/, "")
  isnary = issnm.split("")
  i = 8
  sum = 0

  isnary.each do |is|
     sum += is.to_i*i
     i -= 1
  end
  res = sum%11
  matubi = 11-res
  return issn+matubi.to_s
end

print(issnrt(issn))
