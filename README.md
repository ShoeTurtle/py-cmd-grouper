py-cmd-grouper
==============

Group various shell commands and run it on a go!!

Usage : python run_cmd.py -cmdPath cmd_runner_sample.txt

------------------
 Command Grouping 
------------------
1) CmdGroupA
2) CmdGroupB

COMMAND NUMBER: 1

Executing | echo 'How do u do' |
How do u do
Executing | ls |
cmd_runner_sample.txt run_cmd.py            sample.txt
Executing | touch sample.txt |
Executing | echo 'Inserting the sample text' > sample.txt |
Executing | cat ./sample.txt |
Inserting the sample text
Executing | pwd |
/Users/Binay/Development/ST_Dev/py-cmd-grouper
