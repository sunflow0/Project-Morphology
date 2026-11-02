import streamlit as st
import nltk
from nltk.corpus import wordnet

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Word Classifier", page_icon="📝", layout="centered")

# ดาวน์โหลดข้อมูลพจนานุกรม (จะทำเพียงครั้งเดียวและถูกแคชไว้เพื่อความเร็ว)
@st.cache_resource
def download_nltk_data():
    nltk.download('wordnet')

download_nltk_data()

PREFIXES = ('un', 'dis', 're', 'pre', 'in', 'im', 'ir', 'il', 'mis', 'anti')
SUFFIXES = ('ful', 'ness', 'ment', 'less', 'able', 'ible', 'ion', 'ation', 'ity', 'ly', 'er', 'or', 'ish')

def is_in_dictionary(word):
    return len(wordnet.synsets(word)) > 0

def is_check_spelling_variants(base):
    if base.endswith('i') and is_in_dictionary(base[:-1] + 'y'):
        return True
    if is_in_dictionary(base + 'e'):
        return True
    return False

def classify_word(word):
    word = word.lower().strip()
    if not word:
        return "Please enter a word"
    
    # 1. Check Compound Word with hyphen
    if '-' in word:
        return "Compound Word"
    
    # 2. Check Derived Word (Prefix / Suffix)
    for pref in PREFIXES:
        if word.startswith(pref) and len(word) > len(pref):
            base = word[len(pref):]
            if is_in_dictionary(base):
                return "Derived Word"
                
    for suff in SUFFIXES:
        if word.endswith(suff) and len(word) > len(suff):
            base = word[:-len(suff)]
            if is_in_dictionary(base) or is_check_spelling_variants(base):
                return "Derived Word"

    # 3. Check Compound Word (Closed form like sunflower)
    for i in range(2, len(word) - 1):
        part1 = word[:i]
        part2 = word[i:]
        if is_in_dictionary(part1) and is_in_dictionary(part2):
            return "Compound Word"
            
    # 4. Check Simple Word
    if is_in_dictionary(word):
        return "Simple Word"
        
    return "Unknown (Not found in dictionary)"

# ส่วนการแสดงผลบนหน้าเว็บ (UI)
st.title("📝 Word Type Classifier")
st.write("ค้นหาประเภทของคำภาษาอังกฤษว่าเป็น **Simple, Compound, หรือ Derived**")

# ช่องใส่ข้อมูล
user_input = st.text_input("พิมพ์คำศัพท์ภาษาอังกฤษที่นี่ (เช่น unhappy, sunflower, cat):", "")

if user_input:
    # คำนวณผลลัพธ์
    result = classify_word(user_input)
    
    # แสดงผลลัพธ์แยกตามสีเพื่อความสวยงาม
    if result == "Simple Word":
        st.success(f"📌 คำว่า **'{user_input}'** คือ: **{result}**")
    elif result == "Compound Word":
        st.info(f"🧩 คำว่า **'{user_input}'** คือ: **{result}**")
    elif result == "Derived Word":
        st.warning(f"🌱 คำว่า **'{user_input}'** คือ: **{result}**")
    else:
        st.error(f"🔍 คำว่า **'{user_input}'** คือ: **{result}**")

st.markdown("---")
st.caption("พัฒนาโดยใช้ Python, Streamlit และ NLTK (WordNet)")
