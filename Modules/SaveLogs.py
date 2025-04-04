def get_context(filename):
    # Reading file
    file = open(filename, 'r', encoding = 'utf-8') 
    lines = file.readlines()
    
    i = 0
    for line in lines:
        if 'assistant:' in line:
            i += 1
    
    file.seek(0)
    content = file.read()
    file.close()

    if i > 10:
        flag = False
        file = open(filename, 'w', encoding = 'utf-8')
        for line in lines:
            if flag:
                file.write(line)
            else: 
                if 'assistant: ' in line:
                    flag = True
    file.close()
    return(content)
 
def write_to_file(filename, sender, message):
    file = open(filename, 'a', encoding = 'utf-8')
    file.write(sender + ': ' + message + '\n')
    file.close()
    
def clear_context(file):
    open(file, 'w').close()


