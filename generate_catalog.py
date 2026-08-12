import os
import json
import hashlib
from datetime import datetime

# 設定資料夾與輸出路徑
FIRMWARE_DIR = "firmwares"
OUTPUT_JSON = "catalog.json"

# 【重要】請將這裡換成你的 GitHub 帳號與 Repository 名稱
GITHUB_OWNER = "Yehtech"
GITHUB_REPO = "firmwares"
BRANCH = "main"

def calculate_md5(file_path):
    """計算檔案的 MD5 (APP 拿到後可驗證檔案是否損壞)"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def main():
    # 確保資料夾存在
    if not os.path.exists(FIRMWARE_DIR):
        os.makedirs(FIRMWARE_DIR)

    # 初始化 JSON 結構
    catalog = {
        "last_updated": datetime.utcnow().isoformat() + "Z", 
        "firmwares": []
    }

    # 掃描資料夾內所有的 .bin 檔案
    for filename in os.listdir(FIRMWARE_DIR):
        if filename.endswith(".bin"):
            filepath = os.path.join(FIRMWARE_DIR, filename)
            
            # 獲取檔案資訊
            size = os.path.getsize(filepath)
            md5 = calculate_md5(filepath)
            
            # 組合直接下載連結 (使用 GitHub Raw 網址)
            download_url = f"https://raw.githubusercontent.com/{GITHUB_OWNER}/{GITHUB_REPO}/{BRANCH}/{FIRMWARE_DIR}/{filename}"

            # 加入清單
            catalog["firmwares"].append({
                "filename": filename,
                "size_bytes": size,
                "md5": md5,
                "download_url": download_url
            })

    # 將結果寫入 catalog.json
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(catalog, f, indent=4, ensure_ascii=False)

    print(f"✅ 成功產生目錄！共包含 {len(catalog['firmwares'])} 個韌體檔案。")

if __name__ == "__main__":
    main()
