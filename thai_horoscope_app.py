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
   birth_date = st.date_input(
    "📅 วันเกิด",
    value=datetime.date(1995, 1, 1),
    min_value=datetime.date(1900, 1, 1),
    max_value=datetime.date.today()
)
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

st.subheader("🧘‍♂️ พื้นดวงย่อของคุณ")

# วันในสัปดาห์ (ภาษาไทย)
thai_days = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
birth_day = thai_days[birth_date.weekday()]

# ธาตุประจำวันเกิด
day_elements = {
    "อาทิตย์": "ไฟ",
    "จันทร์": "น้ำ",
    "อังคาร": "ไฟ",
    "พุธ": "ดิน",
    "พฤหัสบดี": "ไฟ",
    "ศุกร์": "น้ำ",
    "เสาร์": "ดิน"
}
element = day_elements.get(birth_day, "ไม่ระบุ")

# ราศีจากตำแหน่งดวงอาทิตย์
sun_pos, _ = swe.calc_ut(jd, swe.SUN)
sun_sign = int(sun_pos[0] // 30)
thai_rasi = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์",
             "ตุล", "พิจิก", "ธนู", "มกร", "กุมภ์", "มีน"]
sun_rasi = thai_rasi[sun_sign]

# จุดแข็ง–จุดอ่อนจากวันเกิด (เวอร์ชันง่าย)
strengths = {
    "จันทร์": "อ่อนโยน ใจดี มีเสน่ห์",
    "อังคาร": "กล้าหาญ ชัดเจน ไม่ยอมแพ้",
    "พุธ": "ฉลาด ช่างพูด วางแผนเก่ง",
    "พฤหัสบดี": "มีเมตตา รอบคอบ รักครอบครัว",
    "ศุกร์": "รักสวยงาม เข้ากับคนง่าย",
    "เสาร์": "อดทน หนักแน่น ทำงานได้ยาว",
    "อาทิตย์": "เป็นผู้นำ มีพลังในตัว"
}

weaknesses = {
    "จันทร์": "ลังเล อ่อนไหวง่าย",
    "อังคาร": "หัวร้อน ใจร้อน",
    "พุธ": "ขี้กังวล พูดมากเกินไป",
    "พฤหัสบดี": "หัวโบราณ ปรับตัวช้า",
    "ศุกร์": "หลงใหลวัตถุ โลเลในความรัก",
    "เสาร์": "เก็บกด เคร่งเครียด",
    "อาทิตย์": "หยิ่ง ดื้อรั้น"
}

# แสดงผล
st.markdown(f"""
- 🗓️ คุณเกิดวัน **{birth_day}**
- 🔥 ธาตุประจำตัว: **{element}**
- 🌞 ราศีที่ดวงอาทิตย์สถิตอยู่: **ราศี {sun_rasi}**
- 💪 จุดแข็งของคุณ: _{strengths[birth_day]}_
- ⚠️ จุดอ่อนที่ควรระวัง: _{weaknesses[birth_day]}_
""")

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
# คำนวณวันปัจจุบัน (ในเขตเวลาไทย)
thai_weekdays = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
today = datetime.datetime.now(pytz.timezone("Asia/Bangkok"))
today_weekday = thai_weekdays[today.weekday()]

# สีมงคลและสีที่ควรหลีกเลี่ยง
lucky_colors = {
    "จันทร์": "ขาว, เหลือง",
    "อังคาร": "ชมพู",
    "พุธ": "เขียว",
    "พฤหัสบดี": "ส้ม, เหลือง",
    "ศุกร์": "ฟ้า, น้ำเงิน",
    "เสาร์": "ม่วง, น้ำเงินเข้ม",
    "อาทิตย์": "แดง"
}

unlucky_colors = {
    "จันทร์": "แดง",
    "อังคาร": "ขาว",
    "พุธ": "ชมพู",
    "พฤหัสบดี": "ม่วง",
    "ศุกร์": "เขียว",
    "เสาร์": "ส้ม",
    "อาทิตย์": "น้ำเงิน"
}

st.write(f"วันนี้คือวัน **{today_weekday}**")
st.success(f"🎨 สีเสื้อมงคลวันนี้: {lucky_colors[today_weekday]}")
st.error(f"⛔ สีที่ควรหลีกเลี่ยง: {unlucky_colors[today_weekday]}")

st.subheader("📅 ทำนายสีเสื้อจากวันที่คุณเลือก")

selected_date = st.date_input("เลือกวันที่คุณต้องการดูสีเสื้อ", value=datetime.date.today())
selected_weekday = selected_date.weekday()  # 0 = Monday, 6 = Sunday

thai_weekdays = ["จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์", "เสาร์", "อาทิตย์"]
day_name = thai_weekdays[selected_weekday]

lucky_colors = {
    "จันทร์": "ขาว, เหลือง",
    "อังคาร": "ชมพู",
    "พุธ": "เขียว",
    "พฤหัสบดี": "ส้ม, เหลือง",
    "ศุกร์": "ฟ้า, น้ำเงิน",
    "เสาร์": "ม่วง, น้ำเงินเข้ม",
    "อาทิตย์": "แดง"
}

unlucky_colors = {
    "จันทร์": "แดง",
    "อังคาร": "ขาว",
    "พุธ": "ชมพู",
    "พฤหัสบดี": "ม่วง",
    "ศุกร์": "เขียว",
    "เสาร์": "ส้ม",
    "อาทิตย์": "น้ำเงิน"
}

st.write(f"วันที่คุณเลือกคือวัน **{day_name}**")
st.success(f"🎨 สีเสื้อมงคล: {lucky_colors[day_name]}")
st.error(f"⛔ สีที่ควรหลีกเลี่ยง: {unlucky_colors[day_name]}")

for name, code in planets.items():
    pos, _ = swe.calc_ut(jd, code)
    degree = pos[0] % 30
    sign = int(pos[0] // 30)
    rasi = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์",
            "ตุล", "พิจิก", "ธนู", "มกร", "กุมภ์", "มีน"]
    st.write(f"- {name} อยู่ที่ {degree:.2f}° ราศี {rasi[sign]}")

from collections import defaultdict

st.subheader("🧭 แผนภูมิดาวพื้นดวง (Birth Chart)")

# ตั้งชื่อราศีไทย 12 ราศี
rasi_names = ["เมษ", "พฤษภ", "มิถุน", "กรกฎ", "สิงห์", "กันย์",
              "ตุล", "พิจิก", "ธนู", "มกร", "กุมภ์", "มีน"]

# เตรียม dict เพื่อเก็บดาวในแต่ละราศี
birth_chart = defaultdict(list)

# วนลูปดาวทั้งหมด แล้วใส่ไว้ในตำแหน่งราศี
for name, code in planets.items():
    pos, _ = swe.calc_ut(jd, code)
    sign = int(pos[0] // 30)
    degree = pos[0] % 30
    birth_chart[sign].append(f"{name} ({degree:.2f}°)")

# แสดงผลแบบตารางข้อความ
for i in range(12):
    rasi = rasi_names[i]
    planets_in_rasi = ", ".join(birth_chart[i]) if birth_chart[i] else "–"
    st.markdown(f"**ราศี {rasi}**: {planets_in_rasi}")
