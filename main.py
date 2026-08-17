import json
import sys
import requests


def get_headers():
    projecta = {"device_info": {"os_ver": "33"}}
    return {
        "Ual-Access-Businessid": "projecta",
        "Ual-Access-ProjectA": json.dumps(projecta, separators=(",", ":")),
    }


def download_apk(package_name):
    api_url = "https://tapi.pureapk.com/v3/get_app_detail"
    payload = {"action": "Download", "package_name": package_name}

    res = requests.post(api_url, headers=get_headers(), json=payload)
    res.raise_for_status()

    app_detail = res.json().get("app_detail", {})
    download_url = app_detail.get("asset", {}).get("url")

    if not download_url:
        print("ダウンロードURLの取得に失敗しました")
        sys.exit(1)

    print(f"Downloading from: {download_url}")

    # app.xapk として保存
    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open("app.xapk", "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    print("保存完了: app.xapk")


if __name__ == "__main__":
    pkg = sys.argv[1] if len(sys.argv) > 1 else "jp.co.ponos.battlecats"
    download_apk(pkg)
