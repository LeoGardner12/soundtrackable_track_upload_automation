import ast



def find_square(s):
	c = 0
	inside_square = []

	for ch in s:
		num_open_square = 0
		if ch == "[":
			for i in s[c:]:
				if i =="[":
					num_open_square += 1
				if i =="]":
					num_open_square -= 1 
					
				inside_square.append(i)
	
				if i == "]" and num_open_square == 0:
					break
				c+=1
			else:
				continue
			break
		c+=1

	out = ""
	for i in inside_square:
			out = out+i
	
	return out

# s= "[{'id': 3, 'name': 'Choose', 'position': 0, 'visible': True, 'variation': True, 'options': ['Track Only $10', 'Track+Bundle $20']}]"

def find_curly(s):
	c = 0
	inside_curly = []

	for ch in s:
		num_open_curly = 0
		if ch == "{":
			for i in s[c:]:
				if i =="{":
					num_open_curly += 1
				if i =="}":
					num_open_curly -= 1 
					
				inside_curly.append(i)
	
				if i == "}" and num_open_curly == 0:
					break
				c+=1
			else:
				continue
			break
		c+=1

	out = ""
	for i in inside_curly:
			out = out+i
	
	return out

def find_all_dict(s):
	#takes a list of dictionarys in the form of a string and returns a list of actual python dictionarys
	if "{" not in s:
		if "[" in s:
			s = ast.literal_eval(find_square(s))
		return s
	list_of_dicts=[]
	while "{" in s:
		list_of_dicts.append(ast.literal_eval(find_curly(s)))
		s = s.replace(find_curly(s), "")
	return list_of_dicts


# s= "[{'id': 3, 'name': 'Choose', 'position': 0, 'visible': True, 'variation': True, 'options': ['Track Only $10', 'Track+Bundle $20']}, {'id': 2, 'name': 'Mins', 'position': 0, 'visible': True, 'variation': False, 'options': ['01:37']}, {'id': 1, 'name': 'BPM', 'position': 0, 'visible': True, 'variation': False, 'options': ['175']}]"
# print(find_all_dict(s))

