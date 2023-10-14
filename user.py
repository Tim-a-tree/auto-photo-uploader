def read_users():
    '''
    this function reads the user from the user txt file
    the file has to be in this format to recognize

    ex)
    {username} {user_num} {user_num} {user_num}
    {username} {user_num}
    {username} {user_num} {user_num} {user_num} ....
    '''
    

    filename = "user.txt"

    f = open(filename, "r")
    
    lines = f.readlines()

    users = {}
    for line in lines:
        # initialize for the arr
        arr = []

        arr = line.split()

        serial_num = []

        for i in range(1, len(arr)):
            serial_num.append(arr[i])

        users[arr[0]] = serial_num


    return users
