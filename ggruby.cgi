#!/usr/bin/ruby
#coding:utf-8
print("Content-type: text/html\n\n")
print("<html>")
require("cgi")
cgi = CGI.new
print(<<"HTGO")
<head>
<meta charset="utf-8"/>
<script type="text/javascript" src="https://www.google.com/jsapi"></script>
<script type="text/javascript">
var dataset=[
["date","aa","tempmin"],
["12/11",12.8,7.3],
["12/12",13.2,7.9],
["12/13",14.9,4.1],
["12/14",11.2,4.6],
["12/15",11.4,2.8],
["12/16",11.9,5.4],
["12/17",12,7],
["12/18",8.8,3.6],
["12/19",7.6,3.7],
["12/20",9.4,3.3],
["12/21",11,2.8],
["12/22",11.4,5.5],
["12/23",8.4,4.4],
["12/24",12.5,4.5],
["12/25",10.3,3.3],
["12/26",10,3.4],
["12/27",9.4,5.1],
["12/28",9.3,2.7],
["12/29",9.5,0.5],
["12/30",10.5,0.6],
["12/31",12.7,1.3],
["1/1",15.5,3.1],
["1/2",12.1,3.1],
["1/3",8.5,3.8],
["1/4",11.7,2.4],
["1/5",7.3,3.9],
["1/6",10.5,2.1],
["1/7",9.9,1.9],
["1/8",12.8,2.8],
["1/9",11.8,3],
["1/10",6.8,1.4],
["1/11",9,0.7]
];
google.load("visualization", "1", {packages:["corechart"]});

google.setOnLoadCallback(drawChart);

function drawChart() {
    var data = google.visualization.arrayToDataTable(dataset);
    var options = {
    title: 'Temperature in Tokyo',
    hAxis: {title: 'DATE', titleTextStyle: {color: 'red'}},
    bar: {groupWidth: "100%"},
        colors: ['red', 'blue']
    };
    var chart = new google.visualization.ColumnChart(document.getElementById('chart_div'));
    chart.draw(data, options);

}
</script>
</head>
<body>
<script src = "https://www.google.com/jsapi"></script>
<div id ='chart_div' style="width:550px; height:500px;"></div>
HTGO
print("<img src='http://chart.apis.google.com/chart?cht=p3&chd=s:hW
&chs=250x100&chl=Hello|World'/>")
print("</body>")
print("</html>")
