# usage: mike_slice.py t0 t1 url  -> range-fetch the bytes covering cam time [t0,t1] into sparse Mike.mov
import sys,subprocess,csv
t0,t1,url=float(sys.argv[1]),float(sys.argv[2]),sys.argv[3]
rows=[(float(a),int(c),int(b)) for a,b,c,_ in csv.reader(open('mike_vpk.csv'))]
ks=[r for r in rows if r[0]>=t0-3 and r[0]<=t1+3]
lo=max(min(r[1] for r in ks)-8_000_000,0); hi=max(r[1]+r[2] for r in ks)+8_000_000
print("bytes",lo,hi,(hi-lo)/1e9,"GB",flush=True)
p=subprocess.Popen(["curl","-sS","-r",f"{lo}-{hi-1}",url],stdout=subprocess.PIPE)
with open('Mike.mov','r+b') as f:
    f.seek(lo); n=0
    while True:
        b=p.stdout.read(1<<22)
        if not b: break
        f.write(b); n+=len(b)
print("wrote",n,"expected",hi-lo, "OK" if n==hi-lo else "SHORT")
open('mike_ranges.txt','a').write(f"{lo} {hi} {t0} {t1}\n")
