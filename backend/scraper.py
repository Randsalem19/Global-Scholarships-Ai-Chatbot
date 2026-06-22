import json
import os
import requests
from bs4 import BeautifulSoup

# مسار ملف البيانات الخاص بنا
DATA_FILE = "data.json"

def load_existing_data():
    """قراءة المنح الحالية من ملف JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    """حفظ البيانات المحدثة في ملف JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)
    print(f"✅ تم حفظ البيانات بنجاح! الإجمالي الآن: {len(data)} منحة.")

def scrape_scholarships():
    """
    دالة سحب البيانات من مواقع المنح.
    (هذا الهيكل مصمم ليتناسب مع موقع افتراضي، يجب تعديل الـ Tags 
    بناءً على الموقع الحقيقي الذي تريد السحب منه).
    """
    # رابط الموقع الذي تريد سحب المنح منه (مثال توضيحي)
    url = "https://www.scholars4dev.com/category/level-of-study/masters-scholarships/"
    
    # استخدام User-Agent ليبدو الطلب وكأنه من متصفح حقيقي لتجنب الحظر
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("⏳ جاري الاتصال بالموقع وسحب البيانات...")
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() # التأكد من نجاح الاتصال
        
        soup = BeautifulSoup(response.text, 'html.parser')
        new_scholarships = []

        # البحث عن العناصر التي تحتوي على المنح (يجب تغييرها حسب الموقع)
        # في موقع scholars4dev، المنح تكون داخل ديف باسم 'post'
        posts = soup.find_all('div', class_='post')

        for post in posts:
            try:
                # استخراج اسم المنحة
                title_elem = post.find('h2')
                name = title_elem.text.strip() if title_elem else "Unknown Scholarship"

                # استخراج الوصف
                desc_elem = post.find('div', class_='entry')
                description = desc_elem.text.strip()[:200] + "..." if desc_elem else "No description available."

                # تجهيز هيكل المنحة ليتطابق مع data.json
                scholarship = {
                    "name": name,
                    "country": "Various/Check Site", # قد تحتاج لتحليل النص برمجياً (NLP) لاستخراج البلد
                    "degree_level": "Master",
                    "majors": ["Any field"],
                    "description": description
                }
                
                new_scholarships.append(scholarship)
            except Exception as e:
                print(f"⚠️ خطأ أثناء معالجة منحة معينة: {e}")
                continue

        return new_scholarships

    except requests.exceptions.RequestException as e:
        print(f"❌ فشل الاتصال بالموقع: {e}")
        return []

def main():
    existing_data = load_existing_data()
    existing_names = {item['name'].lower() for item in existing_data}
    
    scraped_data = scrape_scholarships()
    
    if not scraped_data:
        print("لم يتم العثور على منح جديدة أو فشل السحب.")
        return

    added_count = 0
    for item in scraped_data:
        # التأكد من عدم تكرار المنحة في قاعدة البيانات
        if item['name'].lower() not in existing_names:
            existing_data.append(item)
            existing_names.add(item['name'].lower())
            added_count += 1

    if added_count > 0:
        print(f"🎉 تم العثور على {added_count} منحة جديدة! جاري التحديث...")
        save_data(existing_data)
    else:
        print("⚡ قاعدة البيانات محدثة بالفعل، لم يتم العثور على منح جديدة غير مسجلة.")

if __name__ == "__main__":
    main()