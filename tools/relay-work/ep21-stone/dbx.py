# Range reads from Dropbox via the REST API (reusable, unlike single-use temp links).
# usage: dbx.py range <remote> <start> <end_inclusive> <outfile> [seek]   (seek: write at that offset into existing file)
import sys, json, urllib.request, importlib.util
spec = importlib.util.spec_from_file_location("dp", "/home/user/firstrehabnpb/tools/dropbox-put.py")
dp = importlib.util.module_from_spec(spec); spec.loader.exec_module(dp)
tok = dp.access_token(dp.load_credentials())
def open_range(remote, a, b):
    req = urllib.request.Request("https://content.dropboxapi.com/2/files/download", method="POST",
        headers={"Authorization": "Bearer " + tok, "Dropbox-API-Arg": json.dumps({"path": remote}),
                 "Range": f"bytes={a}-{b}"})
    return urllib.request.urlopen(req, timeout=120)
if __name__ == "__main__":
    cmd, remote, a, b, out = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    seek = int(sys.argv[6]) if len(sys.argv) > 6 else None
    r = open_range(remote, a, b)
    mode = "r+b" if seek is not None else "wb"
    n = 0
    with open(out, mode) as f:
        if seek is not None: f.seek(seek)
        while True:
            chunk = r.read(1 << 22)
            if not chunk: break
            f.write(chunk); n += len(chunk)
    print("wrote", n, "expected", b - a + 1, "OK" if n == b - a + 1 else "SHORT", r.status)
