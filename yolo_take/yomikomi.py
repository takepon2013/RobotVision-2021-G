import detect
import threading
import time




def kansi():
    count = 0

    
    while (True):
        
      hand = open('out.txt', 'r')
      hoge = hand.read()
      hand.close
      count += 1  
      print(hoge)
      hand.close()
      time.sleep(2)
      
      if (count > 10):
          break


detecting = threading.Thread(target=detect.run, kwargs={'source' : 0, 'weights' : 'best3.pt'})
kan = threading.Thread(target=kansi)

detecting.start()
kan.start()

detecting.join()
kan.join()
