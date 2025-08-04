import httpx

osu_id = 15166598
playmode = "osu"

url_user = f"https://osuworld.octo.moe/api/users/{osu_id}?mode={playmode}"
url_regions = "https://osuworld.octo.moe/locales/en/regions.json"

with httpx.Client(http2=True) as client:
    response_user = client.get(url_user)
    data_user = response_user.json()

    response_regions = client.get(url_regions)
    data_regions = response_regions.json()

region_id = str(data_user.get("region_id", "—"))

# Выделяем код страны (первую часть region_id)
country_code = region_id.split("-")[0]

region_name = "—"

if country_code in data_regions:
    # Ищем вложенный словарь регионов у страны
    country_regions = data_regions[country_code]

    # Пытаемся найти полное название региона в подсловаре
    region_name = country_regions.get(region_id, "—")
else:
    # Если страна не найдена, пытаемся найти по самому region_id
    region_name = data_regions.get(region_id, "—")

print("Region ID:", region_id)
print("Region name:", region_name)
print("Region placement:", data_user.get("placement"))

