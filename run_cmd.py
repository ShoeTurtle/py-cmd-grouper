#!/usr/bin/python

__author__ = 'bbudhathoki'

import argparse, os
import sys
from collections import OrderedDict

parser = argparse.ArgumentParser()
parser.add_argument('-cmdPath')
parser.add_argument('-list', action = 'store_true')

args = parser.parse_args()
cmdDictionary = dict()
addJobGrouping = dict()

cmdListToExecute = [] #Stores the list of commands to execute, pass it to method executeCmd
cmdGroupingDict = dict() #Associate the command group_number with the commands that are associated to it, the key points to a list of commands
cmdAssociateGroup = dict() #Assocaite command number to the grouping number

#Read the command from the external file
def readCmdLines(cmdPath):
    if not cmdPath: return

    try:
        inFile = open(cmdPath, 'r')
    except IOError as ex:
        print ('Could Not Open File: ', ex)
        sys.exit()

    inFileRead = inFile.readlines()
    inFile.close()

    return inFileRead


#Build the command dictionary as key value pair
def buildCmdGrpDict(inFileRead, cmdGroupingDict, cmdDictionary):
    if not inFileRead:
        return

    count = 1
    for line in inFileRead:
        if not line.strip() or line.strip().startswith('#'):
            continue

        if line.startswith("custom_cmd_grouping"):
            #Build the cmdGroupingDict over here
            tmp = line.split('=')

            if len(tmp) > 1:
                job_group = tmp[1].split(',')

                for group in job_group:
                    cmdGroupingDict[group.split(':')[1].strip()] = group.split(':')[0].strip()

        else:
            tmp = line.split(':')
            cmdDictionary[count] = tmp[0].strip()

            if len(tmp) > 1:
                tmp = line.split(':')[1]
                for group_number in tmp.split(','):
                    group_number = str(group_number.strip())
                    if group_number not in cmdAssociateGroup:
                        cmdAssociateGroup[group_number] = [count]
                    else:
                        cmdAssociateGroup.get(group_number).append(count)

            count += 1


#Print the commands in the terminal
def prettyPrint(cmdDictionary, cmdGroupingDict):

	if cmdList:		
		print '\n------------------'
		print ' List of Commands '
		print '------------------'

		for key in cmdDictionary:
			print("{}) {}".format(key, cmdDictionary.get(key)))
			
	print '\n------------------'
	print ' Command Grouping '
	print '------------------'

	for key in cmdGroupingDict:
		print("{}) {}".format(key, cmdGroupingDict.get(key)))


def fixCmdGroupingSequence():
	global cmdAssociateGroup, cmdGroupingDict, cmdDictionary, cmdList

	max_cmd_count = len(cmdDictionary)
	tmp_cmdGroupingDict = dict()
	tmp_cmdAssociateGroup = dict()

	for cmd_grp in cmdGroupingDict:
		max_cmd_count += 1
		key = max_cmd_count if cmdList else cmd_grp
		
		tmp_cmdGroupingDict[int(key)] = cmdGroupingDict.get(cmd_grp)
		if cmd_grp in cmdAssociateGroup:
			tmp_cmdAssociateGroup[int(key)] = cmdAssociateGroup.get(cmd_grp)

	cmdAssociateGroup = OrderedDict(sorted(tmp_cmdAssociateGroup.items()))
	cmdGroupingDict = OrderedDict(sorted(tmp_cmdGroupingDict.items()))
	cmdDictionary = OrderedDict(sorted(cmdDictionary.items()))

#Get the user input
def getCmdToExecute():
	try:
		cmd = int(raw_input("\nCOMMAND NUMBER: "))
		print
	except Exception as exp:
		print exp
		sys.exit()
		
	if cmdList:
		if cmd not in cmdGroupingDict and cmd not in cmdDictionary: invokeInvalid()
	else:
		if cmd not in cmdGroupingDict: invokeInvalid()

	cmd_list = []
	if cmd in cmdAssociateGroup: cmd_list = cmdAssociateGroup.get(cmd)
	else: cmd_list.append(cmd)

	return cmd_list

#Execute the command
def executeCmd(cmdList, cmdDictionary):
    for cmd_number in cmdList:
        print ('Executing | {} |'.format(cmdDictionary.get(int(cmd_number))))
        os.system(cmdDictionary.get(int(cmd_number)))

def invokeInvalid():
	print 'Invalid Entry'
	sys.exit()

if __name__ == "__main__":
	cmdPath = args.cmdPath
	cmdList = args.list
	if not cmdPath:
		parser.error('Please specify the location of the cmd file with -cmdPath switch.')
		
	inFileRead = readCmdLines(cmdPath)
	buildCmdGrpDict(inFileRead, cmdGroupingDict, cmdDictionary)
	fixCmdGroupingSequence()
		
	prettyPrint(cmdDictionary, cmdGroupingDict)
	cmdList = getCmdToExecute()

	# print '\n'
	# print 'Command Grouping Dictionary - ' + str(cmdGroupingDict)
	# print 'Command Dictionary - ' + str(cmdDictionary)
	# print 'Command Associate Group - ' + str(cmdAssociateGroup)
	# print 'Command to Execute - ' + str(cmdList)
	# print '\n'

	executeCmd(cmdList, cmdDictionary)