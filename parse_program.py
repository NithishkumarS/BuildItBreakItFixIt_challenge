import re

def parse_prog(program):
    # program = controller
    # program = controller.text_input
    lines = program.split(b'\n')
    principal = ""
    status = ""
    # Check if the first line of the program defines the current principal
    match = re.match(b"^ *as +principal +([A-Za-z][A-Za-z0-9_]*) +password +\"([A-Za-z0-9_ ,;\.?!-]*)\" +do *$", lines[0])
    if match:
    	principal = match.groups()[0]
    	password = match.groups()[1]
    else:
	    status = "{\"status\":\"FAILED\"}\n"
	    return status

    for line in lines[1:]:
	    print(line)
	    # Regex match for if <cond> then <prim_cmd>
	    match_if = re.match(b"^ *if +([A-Za-z][A-Za-z0-9_]* +[=|>|<]+ +[A-Za-z0-9][A-Za-z0-9_]*) +then +", line)
	    if match_if:
	        conditional = match_if.groups()[0]
	        command = line.split("then ")[-1]

	        # Add code to handle rule here
	        status += "{\"status\":\"COND_NOT_TAKEN\"}\n"  # Update to match appropriate status
	        continue

	    match_set_del = re.match(
	        b"^ *set +delegation +([A-Za-z][A-Za-z0-9_]*) +([A-Za-z][A-Za-z0-9_]*) +(read|write|delegate|toggle) +-> +([A-Za-z][A-Za-z0-9_]*)$",
	        line)
	    if match_set_del:
	        target = match_set_del.groups()[0]
	        delegator = match_set_del.groups()[1]
	        right = match_set_del.groups()[2]
	        delegatee = match_set_del.groups()[3]

	        # Add code to handle rule here

	        status += "{\"status\":\"SET_DELEGATION\"}\n"  # Update to match appropriate status
	        continue

	    match_set = re.match(b"^ *set +([A-Za-z][A-Za-z0-9_]*) = +", line)
	    if match_set:
	        var = match_set.groups()[0]
	        expr = line.split(b"= ")[-1]

	        # Add code to handle rule here

	        status += "{\"status\":\"SET\"}\n"
	        continue

	    #### Add additional checks for the rest of the grammar ####

    return status

	# status = parse_prog(
	#     "as principal admin password \"admin\" do\nif temperature = 80 then set ac = 1\nset x = 1\nset delegation x admin read -> bob\n***\n")
	# print(status)

