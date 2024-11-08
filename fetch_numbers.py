import json
import time

import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,nl;q=0.6",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": "yandex_gid=193; is_gdpr=0; is_gdpr_b=CNCkdRDdnAIoAg==; yuidss=5449457651730801169; i=s6iPZVCkMfc7TXdehEQV9nr3oeHs2wpsg2tAqu6pPOHwURVEv88CCOHhwcxl1QeImWC/I5b2cg2G6S7/hKwuW19w1n0=; yandexuid=5449457651730801169; yashr=2657911911730801169; ymex=2046161172.yrts.1730801172; gdpr=0; _ym_uid=1730801171311506601; _ym_d=1730801174; amcuid=5612982401730803799; receive-cookie-deprecation=1; skid=1615206921730815809; Session_id=3:1730891050.5.0.1730891050336:tCpqwQ:25f4.1.2:1|1954887915.0.2.3:1730891050|3:10297825.299624.QK3crjJOwh8senNgjhaj6NWawE0; sessar=1.1195.CiABLkdJZRyztqcZvt7XuWJ6p1Ewil2P6Fj5XLFDSCyrHw.beb9tYoINDDXXEIWEGEeOp_3BapuvgmDfRAX5K5rKpE; sessionid2=3:1730891050.5.0.1730891050336:tCpqwQ:25f4.1.2:1|1954887915.0.2.3:1730891050|3:10297825.299624.fakesign0000000000000000000; yp=1733393169.ygu.1#2046251050.udn.cDpiaWJh; L=CQIFXVpVdnkJaQNcQWJ+VAx9U3tgRUZ5QwUrJAA2J2MAUg==.1730891050.15942.328220.d998b84ec4567f8f05958a45c7166c51; yandex_login=whythat456; ys=udn.cDpiaWJh#c_chck.761484170; font_loaded=YSv1; _ym_isad=2; yclid_src=edin.center:880289532592783359:5449457651730801169; spravka=dD0xNzMwOTc5NDU0O2k9MTkzLjEwNi40Mi4xODA7RD02RTY5REM2NUI3RTIyRTg0M0U0NkY0ODdCN0Q0MjMxMUQ1OUY0NTczRDYzMEFFRDQ2NTlENDIwMzRFMzBEMkVCNkMwMEJCNjFDNDY0OTY5RDFCNjhDOUExOTBGNEU2REIyMDgzREY5MkE2NjVGMkM4MDM2RTEyNzVFQzJBQTI2QzA0NUMxNEZGMDhCRjY3MTg1NzQ0QjlGRjIzNTc2MTc0MzI7dT0xNzMwOTc5NDU0NjA4NjM2MzQ3O2g9Mzg3ODg5N2NhMTdjOGY2N2FmOThkMTJkZjcyZTgzNmY=; yandex_expboxes=912284%2C0%2C58%3B1068828%2C0%2C72%3B1131450%2C0%2C11%3B998603%2C0%2C28%3B663874%2C0%2C32%3B663860%2C0%2C58%3B1142999%2C0%2C13%3B1133021%2C0%2C29%3B1145913%2C0%2C48%3B1150691%2C0%2C49%3B1139493%2C0%2C16; _yasc=Q7Y03zzMfh6fdhtNw6tWqGMX456tWBGR/R5iOpSAC6RHbfaU3JlhmKgAyTXMGIXFJClTT9S5qO8ZmtvDJosyBwEsQQ==; yabs-vdrf=B3IrdR02z_Z410; maps_session_id=1731005872075443-11441046109885716553-balancer-l7leveler-kubr-yp-klg-205-BAL; bh=EkEiQ2hyb21pdW0iO3Y9IjEzMCIsICJHb29nbGUgQ2hyb21lIjt2PSIxMzAiLCAiTm90P0FfQnJhbmQiO3Y9Ijk5IhoFIng4NiIiECIxMzAuMC42NzIzLjExNiIqAj8wMgIiIjoHIkxpbnV4IkIJIjYuMS4xMTIiSgQiNjQiUl0iQ2hyb21pdW0iO3Y9IjEzMC4wLjY3MjMuMTE2IiwgIkdvb2dsZSBDaHJvbWUiO3Y9IjEzMC4wLjY3MjMuMTE2IiwgIk5vdD9BX0JyYW5kIjt2PSI5OS4wLjAuMCJaAj8wYL6btLkGahncyumIDvKst6UL+/rw5w3r//32D6fIzIcI",
    "Host": "cloud-api.yandex.ru",
    "Origin": "https://yandex.ru",
    "Pragma": "no-cache",
    "Sec-Ch-Ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Linux"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "X-Requested-With": "XMLHttpRequest",
}

# Чтение данных из JSON файла
with open("company_links.json", "r", encoding="utf-8") as file:
    data = json.load(file)

# Словарь для хранения собранных данных
collected_data = {}

# Проход по каждой ссылке в JSON
for city, links in data.items():
    collected_data[city] = []  # Создаем список для каждого города

    for link in links:
        try:
            response = requests.get(link, headers=headers)
            response.raise_for_status()  # Проверка на ошибки HTTP

            # Парсинг HTML страницы
            tree = etree.fromstring(response.content, etree.HTMLParser())

            # Здесь вы можете определить, какие данные вам нужны. Например:
            company_name = tree.xpath(
                "//h1[@class='orgpage-header-view__header']/text()"
            )
            company_number = tree.xpath(
                '//div[@class="orgpage-phones-view__phone-number"]/text()'
            )
            print(company_number)

            if company_number:
                # print(f"{company_name[0]} || {company_number[0]}")

                # Сохраняем данные в словарь
                collected_data[city].append(
                    {
                        "company_name": company_name[0],
                        "company_number": company_number[0],
                    }
                )

        except requests.exceptions.RequestException as e:
            print(f"Ошибка при запросе к {link}: {e}")

# Сохранение собранных данных в новый JSON файл
with open("company_numbers.json", "w", encoding="utf-8") as outfile:
    json.dump(collected_data, outfile, indent=4, ensure_ascii=False)

print("Сбор данных завершен!")
