Threaded Log Parser - Large/Distributed Exercise
================================================

You have four servers. Each of them has several terabytes of log files of a 
HTTP server, including `cookie`, `userid`, ordered by `time`. Write a program that 
separate all data for a given userid in a file itself, ordered by 
time. The output files can be place in any of the servers or 
any combination of servers, but all entries from a particular `userid` must 
be in a single file in the cluster. 

- Make run as fast as you can, but think architecturally and pragmatically (one 
best algorithm is ok, to rewrite the assembler parser is not ok) 

- Parsing the file is not the point of the exercise, assume all simplifications 

- You do not need to implement something really distributed. Feel free to simulate the 
logs from multiple servers in multiple files and directories instead of using connections via 
network, using some way to locally simulate the four servers (example: threads, processes).


######Sample entry: 
<pre>
177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /meme.jpg HTTP / 1.1" 200 2148 "-" 
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a" 
177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-" 
"userid = f85f124a-05cd-11e3-8a11-a8206608c529" 
177.126.180.83 - - [15 / Aug / 2013: 13: 57: 48 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-" 
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a" 
</pre>

######Example of output: 
<pre>
3 On the server (for example) there is a file called / tmp / 5352b590-05ac-11e3-9923-c3e7d8408f3a lines containing: 
177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /meme.jpg HTTP / 1.1" 200 2148 "-" 
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a" 
177.126.180.83 - - [15 / Aug / 2013: 13: 57: 48 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-" 
"userid = 5352b590-05ac-11e3-9923-c3e7d8408f3a" 

2 On the server (for example) there is a file called / tmp / f85f124a-05cd-11e3-8a11-a8206608c529 that contains the line: 
177.126.180.83 - - [15 / Aug / 2013: 13: 54: 38 -0300] "GET /lolcats.jpg HTTP / 1.1" 200 5143 "-" 
"userid = f85f124a-05cd-11e3-8a11-a8206608c529"
</pre>

