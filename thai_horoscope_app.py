import streamlit as st
import swisseph as swe
import datetime
import pytz

st.set_page_config(page_title="เช็กดวงไทย", layout="centered")

st.title("🔮 เช็กดวงพื้นดวงแบบไทย")
st.markdown("กรอกวันเวลาเกิดของคุณ เพื่อดูพื้นดวงตามโหราศาสตร์ไทย")

# รับข้อมูลผู้ใช้
col1, col2 = st.columns(2)
with col1:
    birth_date = st.date_input("📅 วันเกิด")
with col2:
    birth_time = st.time_input("🕰️ เวลาเกิด")

province = st.text_input("📍 จังหวัดที่เกิด (กรอกชื่อจังหวัด)", value="กรุงเทพ")

# แปลงเวลา
timezone = pytz.timezone("Asia/Bangkok")
birth_datetime = datetime.datetime.combine(birth_date, birth_time)
birth_datetime_utc = timezone.localize(birth_datetime).astimezone(pytz.utc)

# คำนวณ Julian Day
jd = swe.julday(birth_datetime_utc.year, birth_datetime_utc.month,
                birth_datetime_utc.day, birth_datetime_utc.hour +
                birth_datetime_utc.minute / 60)

# ตำแหน่งกรุงเทพ (จุดอ้างอิง)
swe.set_topo(100.5018, 13.7563)

# คำนวณตำแหน่งดาวพื้นดวง
planets = {
    "อาทิตย์ (Sun)": swe.SUN,
    "จันทร์ (Moon)": swe.MOON,
    "พุธ (Mercury)": swe.MERCURY,
    "ศุกร์ (Venus)": swe.VENUS,
    "อังคาร (Mars)": swe.MARS,
    "พฤหัสบดี (Jupiter)": swe.JUPITER,
    "เสาร์ (Saturn)": swe.SATURN,
    "ราหู (Rahu)": swe.TRUE_NODE
}

st.subheader("🌟 ตำแหน่งดาวในวันเกิดของคุณ")

for name, code in planets.items():
    pos = swe.calc_ut(jd, code)[0]
    degree = pos % 30
    sign = int(pos // 30)
    rasi = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์",
            "ตุล", "พิจิก", "ธนู", "มกร", "กุมภ์", "มีน"]
    st.write(f"- {name} อยู่ที่ {degree:.2f}° ราศี {rasi[sign]}")
