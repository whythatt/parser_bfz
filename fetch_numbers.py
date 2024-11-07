import json

import requests
from lxml import etree

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Cookie": "maps_los=0; yandex_gid=193; is_gdpr=0; is_gdpr_b=CNCkdRDdnAIoAg==; yuidss=5449457651730801169; i=s6iPZVCkMfc7TXdehEQV9nr3oeHs2wpsg2tAqu6pPOHwURVEv88CCOHhwcxl1QeImWC/I5b2cg2G6S7/hKwuW19w1n0=; yandexuid=5449457651730801169; yashr=2657911911730801169; ymex=2046161172.yrts.1730801172; gdpr=0; _ym_uid=1730801171311506601; _ym_d=1730801174; amcuid=5612982401730803799; receive-cookie-deprecation=1; yandex_expboxes=912281%2C0%2C77%3B1142094%2C0%2C45%3B1068828%2C0%2C72%3B1131450%2C0%2C11%3B998603%2C0%2C28%3B663874%2C0%2C32%3B663860%2C0%2C58%3B1134720%2C0%2C82%3B1142999%2C0%2C13%3B1133021%2C0%2C29%3B1145913%2C0%2C48%3B1139493%2C0%2C16; yabs-vdrf=A0; skid=1615206921730815809; _ym_isad=2; Session_id=3:1730891050.5.0.1730891050336:tCpqwQ:25f4.1.2:1|1954887915.0.2.3:1730891050|3:10297825.299624.QK3crjJOwh8senNgjhaj6NWawE0; sessar=1.1195.CiABLkdJZRyztqcZvt7XuWJ6p1Ewil2P6Fj5XLFDSCyrHw.beb9tYoINDDXXEIWEGEeOp_3BapuvgmDfRAX5K5rKpE; sessionid2=3:1730891050.5.0.1730891050336:tCpqwQ:25f4.1.2:1|1954887915.0.2.3:1730891050|3:10297825.299624.fakesign0000000000000000000; yp=1733393169.ygu.1#2046251050.udn.cDpiaWJh; L=CQIFXVpVdnkJaQNcQWJ+VAx9U3tgRUZ5QwUrJAA2J2MAUg==.1730891050.15942.328220.d998b84ec4567f8f05958a45c7166c51; yandex_login=whythat456; ys=udn.cDpiaWJh#c_chck.761484170; font_loaded=YSv1; spravka=dD0xNzMwODk1ODE0O2k9MTkzLjEwNi40Mi4xODA7RD0xNkEzNkIwRjVFRTc1MkEzNEE3QzQ5ODBFRDYxNkQ5NTExOEU4OEZDQjc5OUVFOUNFMTEyRDRCMEU3RTBEQzEzQjNBNzRFNTdBNDdCNENERjA2ODI1QkRFRERGM0IyRDM3MzU2RjY3QzBGMDVCOUE0RjZGREIxM0IzNTU0NERCNDBBQzcxMDAzMzEzNDZFNUI4REZFRERCM0I2NDlENDQxNzk7dT0xNzMwODk1ODE0MDc0NDE3NDgzO2g9YTE3NGJkY2U1MTMzMTlkN2I5NjQ3YWNhYWQxNTdjNmQ=; maps_session_id=1730896841990732-12717987022251982460-balancer-l7leveler-kubr-yp-sas-106-BAL; yclid_src=yandex.ru/maps/org/154909962475:658042231790501887:5449457651730801169; _yasc=tFpzi5BQptOgqYLgbj9y4lWjKXVWbCXUvz5xAgT8nk2a4trlzNAuiD+9qUrys2bJxXIx9Uo9Vz+x+XAGNEZn54Y=; bh=EkEiQ2hyb21pdW0iO3Y9IjEzMCIsICJHb29nbGUgQ2hyb21lIjt2PSIxMzAiLCAiTm90P0FfQnJhbmQiO3Y9Ijk5IhoFIng4NiIiDyIxMzAuMC42NzIzLjkxIioCPzAyAiIiOgciTGludXgiQgkiNi4xLjExMiJKBCI2NCJSWyJDaHJvbWl1bSI7dj0iMTMwLjAuNjcyMy45MSIsICJHb29nbGUgQ2hyb21lIjt2PSIxMzAuMC42NzIzLjkxIiwgIk5vdD9BX0JyYW5kIjt2PSI5OS4wLjAuMCJaAj8wYLbZrbkGahncyumIDvKst6UL+/rw5w3r//32D6fIzIcI",
    "Referer": "https://yandex.ru/maps/?display-text=%D0%B1%D0%B0%D0%BD%D0%BA%D1%80%D0%BE%D1%82%D1%81%D1%82%D0%B2%D0%BE%20%D1%8E%D1%80%D0%B8%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D0%BB%D0%B8%D1%86&ll=40.441998%2C53.067964&mode=search&sctx=ZAAAAAgBEAAaKAoSCQ0AVdy4m0NAEa6f%2FrPm00lAEhIJcLa5MT1hwz8R6Ih8l1KXrD8iBgABAgMEBSgKOABAkE5IAWoCcnWdAc3MzD2gAQCoAQC9AWPDi57CAZIBq6fAleoE7fLp2QbkxbvriweT74eR6ALu14fYmAG17%2FzOtAbyzojMRLSgsdXMBq600OS4A9uQopLJBdfbzuDrAfyB3uGGBo7854O3A4GGtMHXA9%2FjjJsR1JfOov4CsPXRuuIGjfensdYC3deFu%2FgG6abf0wX4tvqfugPasN3slAbHuL6fmQacif%2By5Abgzorb%2FgSCAjTQsdCw0L3QutGA0L7RgtGB0YLQstC%2BINGO0YDQuNC00LjRh9C10YHQutC40YUg0LvQuNGGigITMTg0MTA1NjMwJDE4NDEwNTYyNpICAJoCDGRlc2t0b3AtbWFwc6oChwIxNDI1OTkzODQ3OTcsMTI3NjI1NjE1Njk1LDE4NzI3OTY0ODE2OCwyNDAzMDk0NzUzNzQsNzU1MTk0MDg3NTYsNDM0NTg2Mzk3MzksNTQxNjQyODk5NzAsMTExNTI5MjUyODg2LDEyMDgxNTQ5ODkzMiwyMzM4MTg3MTIxMzUsODY2OTYzODg3MTIsMTYxNjQwMTI4NDIxLDIzNzYzOTAxMzQzOCwxOTc5MTk1NTEyNDQsNjM0NDkxMzgzNDksMzEzOTgyODgyNTgsMjE4NTUwOTMzNCwyOTEzODY5MzUyMSwxMDQyMDg1MTQ4NTUsMTI5MDkxNzkxOTg2LDIyOTU1NzQxNjczNA%3D%3D&sll=40.441998%2C53.067964&sspn=36.668973%2C13.455914&text=%D0%B1%D0%B0%D0%BD%D0%BA%D1%80%D0%BE%D1%82%D1%81%D1%82%D0%B2%D0%BE%20%D1%8E%D1%80%D0%B8%D0%B4%D0%B8%D1%87%D0%B5%D1%81%D0%BA%D0%B8%D1%85%20%D0%BB%D0%B8%D1%86&z=5",
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
            tree = etree.fromstring(response.text, etree.HTMLParser())

            # Здесь вы можете определить, какие данные вам нужны. Например:
            company_name = tree.xpath(
                "//h1[@class='orgpage-header-view__header']/text()"
            )

            company_number = tree.xpath(
                '//div[@class="orgpage-phones-view__phone-number"]/text()'
            )
            if company_number:
                print(f"{company_name[0]} || {company_number[0]}")

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
