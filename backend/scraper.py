import json
import os
import requests
from bs4 import BeautifulSoup

DATA_FILE = "data.json"

def load_existing_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"✅ تم حفظ البيانات بنجاح! الإجمالي الآن: {len(data)} منحة.")

def scrape_scholarships():
    url = "https://www.scholars4dev.com/category/level-of-study/masters-scholarships/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    print("⏳ جاري الاتصال بالموقع وسحب البيانات...")
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        new_scholarships = []
        posts = soup.find_all('div', class_='post')

        for post in posts:
            try:
                title_elem = post.find('h2')
                name = title_elem.text.strip() if title_elem else "Unknown Scholarship"
                desc_elem = post.find('div', class_='entry')
                description = desc_elem.text.strip()[:200] + "..." if desc_elem else "No description available."
                scholarship = {
                    "name": name,
                    "country": "Various",
                    "degree_level": "Master",
                    "majors": ["Any field"],
                    "description": description
                }
                new_scholarships.append(scholarship)
            except Exception as e:
                continue
        return new_scholarships
    except requests.exceptions.RequestException as e:
        print(f"❌ فشل الاتصال: {e}")
        return []

def main():
    existing_data = load_existing_data()
    existing_names = {item['name'].lower() for item in existing_data}
    scraped_data = scrape_scholarships()
    
    if not scraped_data:
        return

    added_count = 0
    for item in scraped_data:
        if item['name'].lower() not in existing_names:
            existing_data.append(item)
            existing_names.add(item['name'].lower())
            added_count += 1

    if added_count > 0:
        print(f"🎉 تم العثور على {added_count} منحة جديدة!")
        save_data(existing_data)
    else:
        print("⚡ قاعدة البيانات محدثة بالفعل.")

if __name__ == "__main__":
    main()