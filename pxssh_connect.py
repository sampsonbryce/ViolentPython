from pexpect import pxssh


def send_command(s, command):
    s.sendline(command)
    s.prompt()
    print(s.before)

def connect(user, host, password):
    try:
        s = pxssh.pxssh()
        s.login(host, user, password)    
        return s
    except:
        print('[-] Error Connecting')     
        exit(0)


def main():
    host = "192.168.1.144"
    user = 'sampsonbryce'
    password = 'Santacruz1'
    s = connect(user, host, password)
    send_command(s, 'cat ~/.ssh/*')

if __name__ == "__main__":
    main()
