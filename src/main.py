from bs4 import BeautifulSoup
import requests
import csv


def parse_anime_page(offset):
    url = f"https://myanimelist.net/topanime.php?type=bypopularity&limit={offset}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find_all("tr", class_="ranking-list")


def parse_anime_info(anime):
    rank_tag = anime.find("span", class_="top-anime-rank-text")
    title_tag = anime.find("h3", class_="anime_ranking_h3")
    score_tag = anime.find("span", class_="score-label")

    url = "#"
    if title_tag:
        a_tag = title_tag.find("a")
        if a_tag and a_tag.has_attr("href"):
            url = a_tag["href"]

    info_tag = anime.find("div", class_="information")
    type_and_episodes = "N/A"
    data = "N/A"
    members = "N/A"

    if info_tag:
        info_items = list(info_tag.stripped_strings)

        if info_items:
           type_and_episodes = info_items[0]
           data = info_items[1]
           members = info_items[2].replace("members", "").replace(",", "").strip()

    return {
        "Rank": rank_tag.text if rank_tag else "N/A",
        "Title": title_tag.text if title_tag else "N/A",
        "URL": url,
        "Score": score_tag.text if score_tag else "N/A",
        "Type and episodes": type_and_episodes,
        "Date": data,
        "Members": members
    }


def main():
    all_anime = []
    offset = 0

    while True:
        if offset == 150:
            break

        print(f"Парсинг страницы с offset {offset}...")
        anime_list = parse_anime_page(offset)

        if not anime_list:
            print("Достигнут конец списка")
            break

        for anime in anime_list:
            all_anime.append(parse_anime_info(anime))

        offset += 50


    if all_anime:
        with open("anime_list.csv", "w", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=["Rank", "Title", "URL", "Score", "Type and episodes", "Date", "Members"])
            writer.writeheader()
            writer.writerows(all_anime)
        print(f"Сохранено {len(all_anime)} записей")
    else:
        print("Нет данных для сохранения")


if __name__ == "__main__":
    main()

