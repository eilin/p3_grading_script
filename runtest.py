#Author: Edward Lin
# python script to automate testing student submissions of a program that changes a files privileges.

# Ideal workflow:
# grader copies student's makefile and runpriv.c to /home/eilin/ecs153_grading/p3_test_dir/
# > python runtest.py
# script makes runpriv, moves to /badID/
# script waits for grader to visually inspect c source and change defined ID
# script makes runpriv, copies to /goodID_noSniff/, copies to /goodID_oldSniff/, copies to /goodID_sniff/
# script tests file in /badID/
#	test, delete runpriv
# script tests file in /goodID_noSniff/
#	test, delete runpriv
# script tests file in /goodID_sniff/
#	create sniff, chmod so user can't execute, test, delete sniff
#	create sniff, chmod so anyone can read, test, delete sniff
#	create sniff, chmod so only user can execute, no one else can rwx, test, delete sniff
# script tests file in /goodID_oldSniff
#	test, delete runpriv
# script asks to delete makefile and runpriv.c from /home/eilin/ecs153_grading/p3_test_dir/
# script exits

# Need to cover the following cases:

# 1) Testing ID
#  (1a)the UID defined in the source file differs from the real UID of the user running the program.
#	program should exit with error message
#  (1b)the UID defined in the source file matches the real UID of the user running the program.
#	program should continue

# 1.5) (optional) Ask user for password, check hash against stored password
#  (1.5a)wrong password
#	program should exit with error message
#  (1.5b)right password
#	program should continue

# 2) Check if 'sniff' file exists
#  (2a)file doesn't exist
#	program should exit with error message
#  (2b)file exists
#	program should continue

# 3) Check privileges of 'sniff'
#  (3a)'sniff' isn't owned by user (not sure how to get a file I don't own without root priv)
#	program should exit with error message
#  (3b)'sniff' isn't executable by user
#	program should exit with error message
#  (3c)'sniff' is readable, writable, or executable by others
#	program should exit with error message
#  (3d)'sniff' is owned and executable by user, others can not read/write/execute
#	program should continue

# 4) Check 'sniff' for time of creation and modification
#  (4a)'sniff' was created or modifed over a minute ago
#	program should exit with error message
#  (4b)'sniff' was created or modified less than a minute ago
#	program should continue

# 5) Program changes owner, group, and protection mode of 'sniff'
#  (5a)program will fail (no group 95 on testing system)

from subprocess import call 
import os.path #to check for file
import sys #for exit call

def sh( command, pw=False):
	if pw = True:
		call( command + "< pw", shell=True )
	else:
		call( command, shell=True )

# script makes runpriv, moves to /badID/
call("make", shell=True)
if not os.path.isfile("runpriv"):
	sys.exit("make failed")	
call("mv ./runpriv ./badID/", shell=True)

# script waits for grader to visually inspect c source and change defined ID
print "inspect c source and change ID"
call("gedit ./runpriv.c &", shell=True)
if raw_input("Continue? (y/n) ") != "y":
	call("rm /home/eilin/ecs153_grading/p3_test_dir/badID/runpriv", shell=True)
	sys.exit("user decided to abort")

pw = False
if raw_input("does it test a password? (y/n) ") == "y":
	pw = True

# script makes runpriv, copies to /goodID_noSniff/, copies to /goodID_oldSniff/, moves to /goodID_sniff/
sh("make")
sh("cp ./runpriv ./goodID_noSniff/")
sh("cp ./runpriv ./goodID_oldSniff/")
##call("mv ./runpriv ./goodID_sniff/", shell=True)

# script tests file in /badID/
#	test, delete runpriv
sh("./badID/runpriv", pw)
sh("rm ./badID/runpriv")

# script tests file in /goodID_noSniff/
#	test, delete runpriv
sh("./goodID_noSniff/runpriv", pw)
if pw:
	sh("./goodID_noSniff/runpriv < badpw", pw=False) #tests bad password 
sh("rm ./goodID_noSniff/runpriv")

# script tests file in /goodID_sniff/
#	create sniff, chmod so user can't execute, test, delete sniff
#	create sniff, chmod so anyone can read, test, delete sniff
#	create sniff, chmod so only user can execute, no one else can rwx, test, delete sniff
# script tests file in /goodID_oldSniff
#	test, delete runpriv
# script asks to delete makefile and runpriv.c from /home/eilin/ecs153_grading/p3_test_dir/
# script exits
