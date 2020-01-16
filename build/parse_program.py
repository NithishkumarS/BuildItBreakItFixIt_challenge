import re


def parse_prog(program, controller):
    # program = controller
    # program = controller.text_input
    lines = program.split(b'\n')

    # print('length of lines::::::::::', len(lines))
    principal = ""
    status = ""
    # Check if the first line of the program defines the current principal
    match = re.match(b"^ *as +principal +([A-Za-z][A-Za-z0-9_]*) +password +\"([A-Za-z0-9_ ,;\.?!-]*)\" +do *$",
                     lines[0])
    if match:
        principal = match.groups()[0]
        password = match.groups()[1]
        # print(principal, password)
        # print('source::',controller.principals)
        if controller.principals[principal] != password:
        	status = "{\"status\":\"FAILED\"}\n"
        	return status
        else:
        	current_principal = principal
    else:
        status = "{\"status\":\"FAILED\"}\n"
        return status

    match_end = re.match(b"^[*]*",lines[-2])
    if not match_end:
    	status = "{\"status\":\"FAILED\"}\n"
    	return status
    
    for line in lines[1:]:
        line=line.split(b"//")[0]

        '''
        # Regex match for if <cond> then <prim_cmd>
        match_if = re.match(b"^ *if +([A-Za-z][A-Za-z0-9_]* +[=|>|<]+ +[A-Za-z0-9][A-Za-z0-9_]*) +then +", line)
        if match_if:
            conditional = match_if.groups()[0]
            command = line.split("then ")[-1]

            # Add code to handle rule here
            status += "{\"status\":\"COND_NOT_TAKEN\"}\n"  # Update to match appropriate status
            continue
        '''
        match_if = re.match(b"^ *set +rule +([A-Za-z0-9][A-Za-z0-9_]*) = +if +([A-Za-z][A-Za-z0-9_]* +[=|>|<]+ +[A-Za-z0-9][A-Za-z0-9_]*) +then +set +", line)
        if match_if:
            rule = match_if.groups()[0]
            command = line.split(b"then ")[-1]
            # print('command',command)
            condition = match_if.groups()[1]
            # set_command = command.split(b"set ")[-1]
            controller.rules[rule] = (condition, command)
            # print('rules:', controller.rules)
    
            status += "{\"status\":\"SET_RULE\",\"rule\": \""+rule.decode("utf-8")+"\"}\n"  # Update to match appropriate status
            continue
        
        match_set_del = re.match(
            b"^ *set +delegation +([A-Za-z][A-Za-z0-9_]*) +([A-Za-z][A-Za-z0-9_]*) +(read|write|delegate|toggle) +-> +([A-Za-z][A-Za-z0-9_]*)$",
            line)
        if match_set_del:
            target = match_set_del.groups()[0]
            delegator = match_set_del.groups()[1]
            right = match_set_del.groups()[2]
            delegatee = match_set_del.groups()[3]

            controller.access.setdefault(target,{b'read':[b'admin', b'hub'], b'write':[b'admin', b'hub'],b'delegate':[b'admin', b'hub']})
            if delegator in controller.access[target][right]:
            	controller.access[target][right].append(delegatee)
            else:
                status += "{\"status\":\"DENIED_DELEGATION\"}\n"  # Update to match appropriate status
                continue
               
            status += "{\"status\":\"SET_DELEGATION\"}\n"  # Update to match appropriate status
            continue
        
        def set(line,status):
            match_set = re.match(b"^ *set +([A-Za-z][A-Za-z0-9_]*) = +", line)
            
            if match_set:
                var = match_set.groups()[0]
                expr = line.split(b"= ")[-1]
                if current_principal == b'admin' or current_principal == b'hub':
                	controller.values.setdefault(var, []).append(controller.solve_expressions(current_principal,expr))

                	controller.access.setdefault(var,{b'read':[b'admin', b'hub'], b'write':[b'admin', b'hub'],b'delegate':[b'admin', b'hub']})
                elif current_principal in controller.access[var][b'write']: 
                	controller.values.setdefault(var, []).append(controller.solve_expressions(current_principal,expr))
                else:
                	status = "{\"status\":\"DENIED_WRITE\"}\n"
                	return status, 1
            
                status += "{\"status\":\"SET\"}\n"
                return status, 0
            return status, 2
        status, val_set = set(line,status)
        
        if val_set !=2:

            if val_set == 1:
                return status
            elif val_set ==0:
                continue
        
        match_return = re.match(b"^ *return +", line)#([A-Za-z][A-Za-z0-9_]*) +. +", line)#([A-Za-z][A-Za-z0-9_]*) ", line)
        if match_return:
            # expr = line.split(b"return")
            # print(expr)
            # val = compute_expression(expr[-1])
            var =  line.split(b" ")[-1]
            if var.isdigit():
                val = int(var)
            else:
                try:
                    if var in controller.values and var in controller.local_value:
                        status = "{\"status\":\"FAILED\"}\n"
                        return status
                    print(controller.values)
                    val = controller.values[var][-1].decode("utf-8") 
                    
                except KeyError:
                        status = "{\"status\":\"FAILED\"}\n"
                        return status
            print('access::::::',controller.access)
            import pdb
            pdb.set_trace()
            # val = 1
            status += "{\"status\":\"RETURNING\",\"output\":" +str(val)+"}\n"
            continue
        '''
        #### Add additional checks for the rest of the grammar ###
        match_print = re.match(b"^ *print +", line)
        if match_print:
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
            if current_principal == b'admin':
                if not principal in controller.principals:
                    controller.principals[principal] = password
                else:
                    status = "{\"status\":\"FAILED\"}\n"
                    return status
            else:
                status = "{\"status\":\"DENIED_WRITE\"}\n"
                return status
    
            if controller.default_delegator:
                for key in controller.access.keys():
                    for right in controller.access[key]:
                        for ele in controller.access[key][right]:
                            if ele == controller.default_delegator:
                                controller.access[key][right].append(principal)
                                break

            status += "{\"status\":\"CREATE_PRINCIPAL\"}\n"
            continue
       
        
        match_activate = re.match(b"^ *activate +rule +([A-Za-z][A-Za-z0-9_]*)", line)
        if match_activate:
            rule = match_activate.groups()[0]
            (condition, command) = controller.rules[rule]
            condition_eval = controller.evaluate_expressions(current_principal, condition)
                
            
            if condition_eval ==1 :
                status, command_exec = set(command, status)
                status, val_set = set(line,status)
                
                if val_set !=2:

                    if val_set == 1:
                        return status
                    elif val_set ==0:
                        status -= "{\"status\":\"SET\"}\n"

                status += "{\"status\":\"ACTIVATE_RULE\"}\n"
            elif condition_eval ==0 :
                status = "{\"status\":\"FAILED\"}\n"


            if condition_eval ==2:
                status += "{\"status\":\""+rule.decode("utf-8")+"\" ,\"status\":\"DENIED_READ\"}\n"
            
            continue
        '''
        match_deactivate = re.match(b"^ *deactivate +rule +([A-Za-z][A-Za-z0-9_]*)", line)
        if match_deactivate:
	        rule = match_deactivate.groups()[0]
	        
	        # Add code to handle rule here
	        
	        status += "{\"status\":\"DEACTIVATE_RULE\"}\n"
	        continue
        '''
        match_change_password = re.match(b"^ *change +password +([A-Za-z][A-Za-z0-9_]*) +\"([A-Za-z0-9_ ,;\.?!-]*)\"", line)
        if match_change_password:
            principal = match_change_password.groups()[0]
            password = match_change_password.groups()[1]
            if principal in controller.principals:
                if current_principal == principal or current_principal ==b'admin':
                    controller.principals[principal] = password
                else:
                    status = "{\"status\":\"DENIED_WRITE\"}\n"
                    return status
            else:
                status = "{\"status\":\"FAILED\"}\n"
                return status

            status += "{\"status\":\"CHANGE_PASSWORD\"}\n"
            continue
        
        
        match_delete_del = re.match(
            b"^ *delete +delegation +([A-Za-z][A-Za-z0-9_]*) +([A-Za-z][A-Za-z0-9_]*) +(read|write|delegate|toggle) +-> +([A-Za-z][A-Za-z0-9_]*)",
            line)
        if match_delete_del:
            target = match_delete_del.groups()[0]
            delegator = match_delete_del.groups()[1]
            right = match_delete_del.groups()[2]
            delegatee = match_delete_del.groups()[3]

            if delegator in controller.access[target][right]:
                controller.access[target][right].remove(delegatee)
            else:
                status += "{\"status\":\"DENIED_DELEGATION\"}\n"  # Update to match appropriate status
                continue
            

            status += "{\"status\":\"DELETE_DELEGATION\"}\n"  # Update to match appropriate status
            continue
        
        match_default_delegator = re.match(b"^ *default +delegator = +([A-Za-z][A-Za-z0-9_]*)", line)
        if match_default_delegator:
            default = match_default_delegator.groups()[0]
            print('val:', default)    
            if current_principal == b'admin':
                if default in controller.principals:
                    controller.default_delegator = default
                else:
                    status = "{\"status\":\"FAILED\"}\n"
                    return status
            else:
                status = "{\"status\":\"DENIED_WRITE\"}\n"
                return status
    
            status += "{\"status\":\"DEFAULT_DELEGATOR\"}\n"
            continue
        
        match_local = re.match(b"^ *local +([A-Za-z][A-Za-z0-9_]* +[=]+ +[A-Za-z0-9][A-Za-z0-9_]*)", line)
        if match_local:
            conditional = match_local.groups()[0]
            expr = line.split(b"= ")[-1]
            controller.local_value[conditional.split(b" ")[0]] = expr
            # Add code to handle rule here
            status += "{\"status\":\"LOCAL\"}\n"  # Update to match appropriate status
            continue
    if controller.local_value:
       controller.local_value={}
        
    return status


