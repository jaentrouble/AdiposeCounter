from console.console import Console
from viewer.viewer import Viewer
from multiprocessing import Queue
import time
import numpy as np

if __name__ == '__main__':
    console_test = Console()
    imgQ = Queue()
    evntQ = Queue()
    etcQ = Queue()
    viewer_test = Viewer(720, 300, evntQ, imgQ, etcQ)
    viewer_test.start()
    console_test.start()
    time.sleep(5)
    newimg = np.ones((600,600,3), dtype=np.uint8)*100
    imgQ.put(newimg)
    time.sleep(3)
    newimg = np.random.randint(0,255,(400,300,3),dtype=np.uint8)
    imgQ.put(newimg)
    time.sleep(3)