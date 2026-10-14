import importlib.util, json, sys
spec = importlib.util.spec_from_file_location("dp", "/home/user/firstrehabnpb/tools/dropbox-put.py")
dp = importlib.util.module_from_spec(spec); spec.loader.exec_module(dp)
tok = dp.access_token(dp.load_credentials())
cmd, *a = sys.argv[1:]
if cmd == "ls":
    r = dp._call(f"{dp.API}/2/files/list_folder", tok, json_body={"path": a[0]})
    for e in r["entries"]:
        print(e[".tag"], e.get("size", ""), e.get("server_modified", ""), e.get("content_hash","")[:12], e["name"])
elif cmd == "mkdir":
    try: print(dp._call(f"{dp.API}/2/files/create_folder_v2", tok, json_body={"path": a[0]})["metadata"]["path_display"])
    except RuntimeError as e: print(e)
elif cmd == "link":
    print(dp._call(f"{dp.API}/2/files/get_temporary_link", tok, json_body={"path": a[0]})["link"])
