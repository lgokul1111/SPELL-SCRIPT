def interpret(source):
    src=source.splitlines()
    output=[]
    for line in src:
        cmd = line.strip()
        if cmd.startswith("spell"):
            message = cmd[5:]
            output.append(message)
        
    return "\n".join(output)
