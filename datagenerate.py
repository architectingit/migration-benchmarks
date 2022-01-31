import random
import string
import os
import pathlib
from pathlib import Path
from argparse import ArgumentParser
from multiprocessing.pool import Pool
from time import time 

maxfilecount = 1000000
directorywidth = 15 #change directory in the current directory 15/1000 times
directorydepth = 5  #change directory depth 5 in 1000 times
dirlength = 10      #max directory depth before returning to the root directory

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")

parser = ArgumentParser()
parser.add_argument("-f","--filecount",type=int,dest="filecount",help="specify the number of files to generate.")
parser.add_argument("--maxfilesize",type=int,dest="maxfilesize",default=1024)
parser.add_argument("--minfilesize",type=int,dest="minfilesize",default=512)
parser.add_argument("-t","--threads",type=int,dest="threads",default=10)
parser.add_argument("--path",type=dir_path,dest="baselocation",default="/Source")
args = parser.parse_args()
baselocation = args.baselocation
defaultlocation = args.baselocation

def check_change_dir_depth(dirdepth):
    if random.randint(1,1000) < dirdepth:
        return True
    else:
        return False    

def check_change_dir_width(dirwidth):
    if random.randint(1,1000) < dirwidth:
        return True
    else:
        return False

def get_random_string(length):
    letters = string.ascii_letters + string.digits + string.punctuation
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

def generate_file_name(length):
    global defaultlocation
    global baselocation
    if check_change_dir_depth(directorydepth):
        newdir = os.path.join(defaultlocation,generate_dir_name(dirlength),"")
        os.mkdir(newdir)
        defaultlocation = newdir
    if check_change_dir_width(directorywidth):
        if baselocation != defaultlocation:
            parent = Path(defaultlocation).parent.as_posix()
            newdir = os.path.join(parent,generate_dir_name(dirlength),"")
    filename = ''.join(random.choice(string.ascii_letters) for i in range(5,length))    
    return filename

def generate_dir_name(length):
    dirname = ''.join(random.choice(string.ascii_letters) for i in range(5,length))
    dirname = "dir_"+dirname
    return dirname

def create_file(filenum):
    global defaultlocation
    for i in range(filenum):
        filename = os.path.join(defaultlocation,generate_file_name(20)+".txt")
        if len(filename) > 255:
            defaultlocation = baselocation
            filename = os.path.join(defaultlocation,generate_file_name(20)+".txt")
        filehandle = open(filename,"w+")
        for j in range (100):
          filehandle.write(get_random_string(int(random.uniform(args.minfilesize,args.maxfilesize)/100)))
        filehandle.close

def main():

    if args.filecount <=0 or args.filecount > maxfilecount:
        print ("File count must be between 1 and ",maxfilecount)
        exit()

    ts=time()
    print("Running with ",args.threads," threads, generating ",args.filecount," files into ",baselocation)

#for i in range(args.filecount):
#    create_file()
    thread_file_count = int(args.filecount/args.threads)
    thread_array = [thread_file_count] * args.threads
    with Pool(args.threads) as p:
        p.map(create_file,thread_array)


    print ("Took ",time()-ts," seconds.")
#    print ("file number ",i, " name ",generate_file_name(20)," length ",random.uniform(args.minfilesize,args.maxfilesize))
#    print ("file number ",i, " length ",random.triangular(args.minfilesize,args.maxfilesize,99))


if __name__ == '__main__':
    main()
