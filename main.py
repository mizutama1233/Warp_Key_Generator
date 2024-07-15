from concurrent.futures import ThreadPoolExecutor
import random, time, datetime
import requests

tpe = ThreadPoolExecutor(max_workers=5)

def get_headers(token):
    return {
        "Authorization": f"Bearer {token}"
    }

def generate(diff, today=None):
    print(f"[!] 生成中")
    try:
        headers = {
            "CF-Client-Version": "a-6.11-2223",
            "Host": "api.cloudflareclient.com",
            "Connection": "Keep-Alive",
            "Accept-Encoding": "gzip",
            "User-Agent": "okhttp/3.12.1",
        }

        with requests.Session() as client:
            client.headers.update(headers)
            r = client.post("https://api.cloudflareclient.com/v0a2223/reg", timeout=35)
            response_data = r.json()
            id = response_data["id"]
            klych = response_data["account"]["license"]
            token = response_data["token"]

            r = client.post("https://api.cloudflareclient.com/v0a2223/reg", timeout=35)
            response_data2 = r.json()
            id2 = response_data2["id"]
            token2 = response_data2["token"]

            headers_post = {
                "Content-Type": "application/json; charset=UTF-8",
                "Authorization": f"Bearer {token}"
            }

            json_data = {"referrer": f"{id2}"}
            client.patch(f"https://api.cloudflareclient.com/v0a2223/reg/{id}", headers=headers_post, json=json_data, timeout=35)
            client.delete(f"https://api.cloudflareclient.com/v0a2223/reg/{id2}", headers=get_headers(token2), timeout=35)

            key = random.choice(keys)

            json_data = {"license": f"{key}"}
            client.put(f"https://api.cloudflareclient.com/v0a2223/reg/{id}/account", headers=headers_post, json=json_data, timeout=35)

            json_data = {"license": f"{klych}"}
            client.put(f"https://api.cloudflareclient.com/v0a2223/reg/{id}/account", headers=headers_post, json=json_data, timeout=35)

            r = client.get(f"https://api.cloudflareclient.com/v0a2223/reg/{id}/account", headers=get_headers(token), timeout=35)
            account_data = r.json()
            req_data = account_data["referral_count"]
            gened_key = account_data["license"]

            client.delete(f"https://api.cloudflareclient.com/v0a2223/reg/{id}", headers=get_headers(token), timeout=35)

            if int(req_data) >= 12_000_000:
                print(f"[!] キー発見！ -> {gened_key} : {req_data}")
                if diff == "yes":
                    with open(f'./gen/{today}.txt', 'a') as f:
                        f.write(f"{gened_key} - {req_data} GB\n")
                elif diff == "no":
                    with open('Keys.txt', 'a') as f:
                        f.write(f"{gened_key} - {req_data} GB\n")
                with open("積み立てwarp.txt", "a") as f:
                    f.write(f"{gened_key}\n")
            else:
                print(f"{gened_key} : {req_data}")

    except Exception as e:
        print(f"エラー：{e}")
        time.sleep(5)

if __name__ == "__main__":
    with open("積み立てwarp.txt", "r") as f:
        keys = [key for key in f.read().split()]

    gen_keys = int(input("生成する数："))
    which = input("他のtxtに保存しますか？(yes/no)：")

    if which == "yes":
        today = datetime.date.today()
        for i in range(gen_keys):
            tpe.submit(generate, "yes", today)
    elif which == "no":
        for i in range(gen_keys):
            tpe.submit(generate, "no")

    tpe.shutdown()
