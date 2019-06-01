add_library('net')

PORT = 5206

server = Server(this, PORT)

DIMENSION = 265, 128
DEFAULT_SIZE = 3

def drawbot(x, y):
    circle(x, y, DEFAULT_SIZE)

def setup():
    size(*DIMENSION)
    #fullScreen()
        
def draw():
    if not server.available():
        return
    #background(0,0,0)
    
    #print("Bytes available")
    bs = server.available().readBytes()

    for i in range(len(bs)):
        b = bs[i]
        if b == ord('p'):            
            x = bs[i+1]
            y = bs[i+2]
            #print("bot@", x,y)
            drawbot(x, y)
        if b == ord('c'):
            background(0)
    
