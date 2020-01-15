import re

values=dict()
def parse_prog(program, controller):
    # program = controller
    # program = controller.text_input
    lines = program.split(b'\n')
    print('length of lines::::::::::', len(lines))
    principal = ""
    status = ""
    # Check if the first line of the program defines the current principal
    match = re.match(b"^ *as +principal +([A-Za-z][A-Za-z0-9_]*) +password +\"([A-Za-z0-9_ ,;\.?!-]*)\" +do *$",
                     lines[0])
    if match:
        principal = match.groups()[0]
        password = match.groups()[1]
        print(principal, password)
        print('source::',controller.principals)
        if controller.principals[principal] != password:
        	status = "{\"status\":\"FAILED\"}\n"
        	return status
    else:
        status = "{\"status\":\"FAILED\"}\n"
        return status

    match_end = re.match(b"^[*]*",lines[-2])
    if not match_end:
    	status = "{\"status\":\"FAILED\"}\n"
    	return status
    
    for line in lines[1:]:
        print(current_principal)
        print(line)
        '''
        # Regex match for if <cond> then <prim_cmd>
        match_if = re.match(b"^ *if +([A-Za-z][A-Za-z0-9_]* +[=|>|<]+ +[A-Za-z0-9][A-Za-z0-9_]*) +then +", line)
        if match_if:
            conditional = match_if.groups()[0]
            command = line.split("then ")[-1]

            # Add code to handle rule here
            status += "{\"status\":\"COND_NOT_TAKEN\"}\n"  # Update to match appropriate status
            continue

        match_if = re.match(b"^ *set +rule +([A-Za-z0-9][A-Za-z0-9_]*) = +if +([A-Za-z][A-Za-z0-9_]* +[=|>|<]+ +[A-Za-z0-9][A-Za-z0-9_]*) +then +", line)
        if match_if:
            conditional = match_if.groups()[0]
            command = line.split("then ")[-1]

            # Add code to handle rule here
            status += "{\"status\":\"COND_NOT_TAKEN\"}\n"  # Update to match appropriate status
            continue
        '''
        match_set_del = re.match(
            b"^ *set +delegation +([A-Za-z][A-Za-z0-9_]*) +([A-Za-z][A-Za-z0-9_]*) +(read|write|delegate|toggle) +-> +([A-Za-z][A-Za-z0-9_]*)$",
            line)
        if match_set_del:
            target = match_set_del.groups()[0]
            delegator = match_set_del.groups()[1]
            right = match_set_del.groups()[2]
            delegatee = match_set_del.groups()[3]

            controller.access.setdefault(target,{b'read':[b'admin', b'hub'], b'write':[b'admin', b'hub']})
            if delegator in controller.access[target][right]:
            	controller.access[target][right].append(delegatee)
            	print(controller.access)
            else:
                status += "{\"status\":\"DENIED_DELEGATION\"}\n"  # Update to match appropriate status
                continue
               
            status += "{\"status\":\"SET_DELEGATION\"}\n"  # Update to match appropriate status
            continue
        
        match_set = re.match(b"^ *set +([A-Za-z][A-Za-z0-9_]*) = +", line)
        if match_set:
            var = match_set.groups()[0]
            expr = line.split(b"= ")[-1]   
            if current_principal in controller.access[target]['write']:
            	values.setdefault(var, []).append(expr) 
            else:
            	status = "{\"status\":\"DENIED_WRITE\"}\n"
                return status

            status += "{\"status\":\"SET\"}\n"
            continue
        
        match_return = re.match(b"^ *return +", line)
        if match_return:
            var =  line.split(b" ")[-1]
            val = values[var][-1].decode("utf-8") 
           
            status += "{\"status\":\"RETURNING\",\"output\":" +str(val)+"}\n"
            continue
        '''
        #### Add additional checks for the rest of the grammar ###
        match_return = re.match(b"^ *print +", line)
        if match_return:
            var =  line.split(b" ")[-1]
            # Add code to handle rule here
            # res= values[var][0]
            
            res = 1
            status += "{\"status\":\"PRINT\",\"output\":" +str(res)+"}\n"
            continue
        
        '''
        match_create_principal = re.match(b"^ *create +principal +([A-Za-z][A-Za-z0-9_]*) +\"([A-Za-z0-9_ ,;\.?!-]*)\" *$", line)
        if match_create_principal:
            principal = match_create_principal.groups()[0]
            password = match_create_principal.groups()[1]
            controller.principals[principal] = password

            status += "{\"status\":\"CREATE_PRINCIPAL\"}\n"
            continue
        #### Add additional checks for the rest of the grammar ####
        '''
        match_activate = re.match(b"^ *activate +rule +([A-Za-z][A-Za-z0-9_]*)", line)
        if match_activate:
	        rule = match_activate.groups()[0]
	        
	        # Add code to handle rule here
	        
	        status += "{\"status\":\"ACTIVATE_RULE\"}\n"
	        continue
        
        match_deactivate = re.match(b"^ *deactivate +rule +([A-Za-z][A-Za-z0-9_]*)", line)
        if match_deactivate:
	        rule = match_deactivate.groups()[0]
	        
	        # Add code to handle rule here
	        
	        status += "{\"status\":\"DEACTIVATE_RULE\"}\n"
	        continue
 
        match_change_password = re.match(b"^ *change +password +([A-Za-z][A-Za-z0-9_]*) +([A-Za-z0-9_ ,;\.?!-]*)", line)
        if match_change_password:
            principal = match_change_password.groups()[0]
            password = match_change_password.groups()[1]

            # Add code to handle rule here
            
            print(principal, password)
            status += "{\"status\":\"CHANGE_PASSWORD\"}\n"
            continue
        #### Add additional checks for the rest of the grammar ####
        
        match_delete_del = re.match(
            b"^ *delete +delegation +([A-Za-z][A-Za-z0-9_]*) +([A-Za-z][A-Za-z0-9_]*) +(read|write|delegate|toggle) +-> +([A-Za-z][A-Za-z0-9_]*)$",
            line)
        if match_delete_del:
            target = match_delete_del.groups()[0]
            delegator = match_delete_del.groups()[1]
            right = match_delete_del.groups()[2]
            delegatee = match_delete_del.groups()[3]

            # Add code to handle rule here

            status += "{\"status\":\"DELETE_DELEGATION\"}\n"  # Update to match appropriate status
            continue
        
        match_default_delegator = re.match(b"^ *default +delegator = +([A-Za-z][A-Za-z0-9_]*)", line)
        if match_default_delegator:
            default = match_default_delegator.groups()[0]
            print('val:', default)    
            # Add code to handle rule here

            status += "{\"status\":\"DEFAULT_DELEGATOR\"}\n"
            continue
        
        match_local = re.match(b"^ *local +([A-Za-z][A-Za-z0-9_]* +[=|>|<]+ +[A-Za-z0-9][A-Za-z0-9_]*)", line)
        if match_if:
            conditional = match_if.groups()[0]
            command = line.split("then ")[-1]

            # Add code to handle rule here
            status += "{\"status\":\"COND_NOT_TAKEN\"}\n"  # Update to match appropriate status
            continue

        '''
    return status

# status = parse_prog(
#     "as principal admin password \"admin\" do\nif temperature = 80 then set ac = 1\nset x = 1\nset delegation x admin read -> bob\n***\n")
# print(status)
