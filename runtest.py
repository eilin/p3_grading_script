#Author: Edward Lin
# python script to automate testing student submissions of a program that changes a files privileges.
# if a program doesn't fail when it should have during a test, it will fail later on and I can see that the error message doesn't match the test.
# if the program succeeds completely, something has gone terribly wrong.


from subprocess import call 
import os #to check for file and change dir
import sys #for exit call

def sh( command, pw=False):
	if pw == True:
		call( command + "< pw", shell=True )
	else:
		call( command, shell=True )

# script makes runpriv, moves to /badID/
call("make", shell=True)
if not os.path.isfile("runpriv"):
	sys.exit("make failed")	
call("mv ./runpriv ./badID/", shell=True)

# script waits for grader to visually inspect c source and change defined ID
print "\n***Inspect c source and change ID***"
call("gedit ./runpriv.c &", shell=True)
if raw_input("Continue? (y/n) ") != "y":
	call("rm /home/eilin/ecs153_grading/p3_test_dir/badID/runpriv", shell=True)
	sys.exit("user decided to abort")

pw = False
if raw_input("does it test a password? (y/n) ") == "y":
	pw = True

# script makes runpriv, copies to /goodID_noSniff/, copies to /goodID_oldSniff/, move to /goodID_sniff/
sh("make")
sh("cp ./runpriv ./goodID_noSniff/")
sh("cp ./runpriv ./goodID_oldSniff/")
sh("mv ./runpriv ./goodID_sniff/")

# script tests file in /badID/
#	test, delete runpriv
print "\nTesting bad ID"
sh("./badID/runpriv", pw)
sh("rm ./badID/runpriv")

# script tests file in /goodID_noSniff/
#	test, delete runpriv
os.chdir("/home/eilin/ecs153_grading/p3_test_dir/goodID_noSniff/")
if pw:
	print "\nTesting bad password"
	sh("./runpriv < badpw", pw=False) #tests bad password
print "\nTesting no sniff file"
sh("./runpriv", pw)
sh("rm ./runpriv")

# script tests file in /goodID_sniff/
#	create sniff, chmod so user can't execute, test
os.chdir("/home/eilin/ecs153_grading/p3_test_dir/goodID_sniff/")
sh("touch ./sniff")
print "\nTesting no user x privilege"
sh("chmod 400 ./sniff")
sh("./runpriv", pw)
#	chmod so anyone can read and write, test
print "\nTesting others' r privilege"
sh("chmod 466 ./sniff")
sh("./runpriv", pw)
#	chmod so only user can execute, no one else can rwx, test, delete sniff and runpriv
print "\nTesting all conditions pass (should fail still)"
sh("chmod 700 ./sniff")
sh("./runpriv", pw)
sh("rm -f ./runpriv ./sniff")

# script tests file in /goodID_oldSniff
#	test, delete runpriv
print "\nTesting old sniff file"
os.chdir("/home/eilin/ecs153_grading/p3_test_dir/goodID_oldSniff/")
sh("./runpriv", pw)
sh("rm ./runpriv")
os.chdir("/home/eilin/ecs153_grading/p3_test_dir/")

# script asks to delete makefile and runpriv.c from /home/eilin/ecs153_grading/p3_test_dir/
if raw_input("\nDelete makefile and runpriv.c? (y/n) ") == "y":
	sh("rm -v ./*akefile ./runpriv.c")

# script exits
