from concurrent.futures import ThreadPoolExecutor
import random, time, datetime
import requests
tpe = ThreadPoolExecutor(max_workers=25)
count = 0

def generate(diff, today=None):
    global count
    count += 1
    print(f"\r[!] 生成中: {count}", end="")
    while True:
        try:
            headers = {
                "CF-Client-Version": "a-6.11-2223",
                "Host": "api.cloudflareclient.com",
                "connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "x-cache-set": "false",
                "x-envoy-upstream-service-time": "0",
            }
            key = random.choice(keys)

            with requests.Session() as client:
                client.headers.update(headers)
                r = client.post("https://api.cloudflareclient.com/v0a2223/reg", timeout=35)
                response_data = r.json()
                r_id = response_data["id"]
                token = response_data["token"]

                headers_post = {
                    "Content-Type": "application/json; charset=UTF-8",
                    "Authorization": f"Bearer {token}"
                }

                json_data = {"license": f"{key}"}
                client.put(f"https://api.cloudflareclient.com/v0a2223/reg/{r_id}/account", headers=headers_post, json=json_data, timeout=35)

                r = client.get(f"https://api.cloudflareclient.com/v0a2223/reg/{r_id}/account", headers=headers_post, timeout=35)
                account_data = r.json()
                req_data = account_data["referral_count"]
                gened_key = account_data["license"]

                client.delete(f"https://api.cloudflareclient.com/v0a2223/reg/{r_id}", headers=headers_post, timeout=35)

                if int(req_data) >= 12_000_000:
                    print(f"\n[!] {gened_key} : {req_data}", end="")
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
            break
        except Exception as e:
            if str(e) == "Expecting value: line 1 column 1 (char 0)":
                print("429 Too Many Requests（retry）")
                time.sleep(65)
            else:
                print(f"エラー：{e}")
                break

if __name__ == "__main__":
    with open("積み立てwarp.txt", "r") as f:
        keys = [key for key in f.read().split()]

    gen_keys = input("生成する数：")
    which = input("別ファイルに保存しますか？(yes/no)：")

    if which == "yes":
        today = datetime.date.today()
        for i in range(int(gen_keys)):
            tpe.submit(generate, "yes", today)
    elif which == "no":
        for i in range(int(gen_keys)):
            tpe.submit(generate, "no")

    tpe.shutdown()
