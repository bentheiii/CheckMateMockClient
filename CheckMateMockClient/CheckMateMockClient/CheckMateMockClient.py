import socket

def splitBy(inputstream,chunksize):
    while len(inputstream) >= chunksize:
        yield inputstream[:chunksize]
        inputstream = inputstream[chunksize:]
def toBoard(input):
    ret = [[':' for _ in xrange(8)] for _ in xrange(8)]
    for ind in xrange(32):
        if ind%16 < 8:
            c = 'P'
        elif ind%16 < 10:
            c = 'R'
        elif ind%16 < 12:
            c = 'H'
        elif ind%16 < 14:
            c = 'B'
        elif ind%16 == 14:
            c = 'Q'
        else:
            c = 'K'
        if ind>=16:
            c = c.lower()
        loc = ord(input[ind])
        if loc == 64:
            continue
        #loc = chr(loc)
        ret[loc%8][loc/8] = c
    for loc in input[32:-1]:
        if ord(loc)==128:
            break
        loc = ord(loc) % 64
        if ret[loc%8][loc/8] == ':':
            ret[loc%8][loc/8] = '+'
    return ret
def strBoard(board):
    ret = []
    for row in board:
        for cell in row:
            ret.append(cell)
        ret.append("\n")
    return "".join(ret)

TCP_IP = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print "enter server port"
sock.connect((TCP_IP, input()))
print "connected!"
try:
    while 1:
        print "enter message:"
        message = raw_input()
        sock.send(message)
        print
        reply = sock.recv(4096)
        if reply=='':
            raise socket.error("connection terminated")
        print reply
        if message[0] != '0':
            for c in splitBy(reply,37):
                print strBoard(toBoard(c))
                print
except socket.error as e:
    print e
    pass
finally:
    sock.close()