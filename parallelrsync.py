import os
import subprocess
import time
from datetime import datetime
start = datetime.now()
root = "/Source2/"
target = "/Target2/"
results = []
for item in os.listdir(root):
    if os.path.isdir(os.path.join(root,item)):
        spawn = "rsync -r -c "+os.path.join(root,item)+"/ "+target+item
        results.append(subprocess.Popen(spawn,shell=True))
results.append(subprocess.Popen("rsync -c "+root+"* "+target,shell=True))
print("Spawned "+str(len(results))+ " rsync commands")
while True:
  for item in results:
      if item.poll() == None:
          print ("Process "+str(item.pid)+" still running")
      else: 
          print("Removed process "+str(item.pid))
          results.remove(item)
          print(str(len(results))+" processes remain.")
  time.sleep(10)        
  if len(results) == 0: 
      elapsed = datetime.now()-start
      print("Elapsed Copy Time: "+str(elapsed))
      exit()
