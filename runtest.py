# python script to automate testing student submissions of a program that changes a files privileges.
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
 
