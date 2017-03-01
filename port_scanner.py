import optparse
from socket import *
from threading import *

screenLock = Semaphore(value=1)


def connScan(tgtHost, tgtPort):
    try:
        connSkt = socket(AF_INET, SOCK_STREAM)  # set up socket
        connSkt.connect((tgtHost, tgtPort))  # connect to target

        # attempt banner grab
        try:
            # connSkt.send('ViolentPython\r\n')
            results = connSkt.recv(1024)
        except:
            results = None

        screenLock.acquire()
        print('[+] {0}/tcp open'.format(tgtPort))  # port is open

        if results is not None:  # if successful banner grab
            print('[+] {0}'.format(results))  # got banner
        else:
            print('[-] Failed to banner grab')  # failed to get banner

        connSkt.close()
    except:
        screenLock.acquire()
        print('[-] {0}/tcp closed'.format(tgtPort))  # port is closed
    finally:
        screenLock.release()
        connSkt.close()


def portScan(tgtHost, tgtPorts):
    try:
        tgtIP = gethostbyname(tgtHost)
    except:
        print('\n[-] Cannot resolve "{0}": Unknown host'.format(tgtHost))
        return

    try:
        tgtName = gethostbyaddr(tgtIP)
        print('\n[+] Scan Results for: {0}'.format(tgtName[0]))
    except:
        print('\n[+] Scan Results for: {0}'.format(tgtIP))

    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan, args=(tgtHost, int(tgtPort)))
        t.start()


def main():
    parser = optparse.OptionParser('usage %prog -H <target host> -p <target port>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-p', dest='tgtPort', type='string', help='specify target port')
    options, args = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPort).split(',')
    if tgtHost is None or tgtPorts[0] is None:
        print('Please specify target host and port(s)')
        exit(0)
    portScan(tgtHost, tgtPorts)

if __name__ == '__main__':
    main()
