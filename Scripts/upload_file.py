# upload_ropc_inline_safe.py
# -*- coding: utf-8 -*-

import os, sys, json, argparse, mimetypes, requests

try:
    # --------- Parámetros por CLI ----------
    p = argparse.ArgumentParser(description="Sube un archivo a OneDrive vía Graph con ROPC (simple upload).")
    p.add_argument("--tenant-id",required=True)
    p.add_argument("--client-id",required=True)
    p.add_argument("--username",required=True)
    p.add_argument("--password",required=True)
    p.add_argument("--local-path",required=True)
    p.add_argument("--graph-url",required=True)
    p.add_argument("--client-secret",required=True)
    args = p.parse_args()

    # --------- 1) Token ROPC ----------------------------------------------------------
    token_url = f"https://login.microsoftonline.com/{args.tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "password",
        "client_id":  args.client_id,
        "scope":      "https://graph.microsoft.com/Files.ReadWrite.All offline_access openid profile",
        "username":   args.username,
        "password":   args.password,
    }
    if args.client_secret:
        data["client_secret"] = args.client_secret

    tok = requests.post(token_url, data=data)
    if tok.status_code != 200:
        raise RuntimeError(f"Error token: {tok.status_code} {tok.text}")

    access_token = tok.json().get("access_token")
    if not access_token:
        raise RuntimeError(f"La respuesta de token no contiene access_token: {tok.text}")

    # --------- 2) Subida simple (PUT /.../content) -----------------------------------
    if not os.path.exists(args.local_path):
        raise FileNotFoundError(f"Archivo no encontrado: {args.local_path}")

    ext = os.path.splitext(args.local_path)[1].lower()
    content_type = {
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls":  "application/vnd.ms-excel",
        ".csv":  "text/csv",
        ".txt":  "text/plain; charset=utf-8",
        ".json": "application/json",
        ".pdf":  "application/pdf",
    }.get(ext, mimetypes.guess_type(args.local_path)[0] or "application/octet-stream")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type":  content_type
    }

    with open(args.local_path, "rb") as f:
        resp = requests.put(args.graph_url, headers=headers, data=f)

    if resp.status_code not in (200, 201):
        preview = resp.text[:800].replace("\n", " ")
        raise RuntimeError(f"Error upload: {resp.status_code} {preview}")

    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
    sys.exit(0)

except Exception as e:
    # salida de error clara para PowerShell
    sys.stderr.write(f"{str(e)}\n")
    sys.exit(1)