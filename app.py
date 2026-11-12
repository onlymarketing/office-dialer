import time
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Office Auto Dialer", page_icon="📞")

st.title("📞 Office Auto Dialer Web App")
st.write(
    "உங்கள் Excel ஷீட்டை அப்லோட் செய்யுங்கள். ஒன்றன் பின் ஒன்றாக உங்கள்"
    " மொபைலுக்கு கால் செல்லும்."
)

# 1. Excel / CSV Upload
uploaded_file = st.file_uploader(
    "இங்கே Excel அல்லது CSV ஃபைலை அப்லோட் செய்யவும்", type=["xlsx", "csv"]
)

if uploaded_file is not None:
  if uploaded_file.name.endswith(".csv"):
    df = pd.read_csv(uploaded_file)
  else:
    df = pd.read_excel(uploaded_file)

  # போன் நம்பர் உள்ள Column தேர்வு செய்தல்
  phone_col = st.selectbox(
      "போன் நம்பர் உள்ள Column எது?", df.columns
  )

  # அடுத்த காலுக்கு எவ்வளவு நேரம் இடைவெளி வேண்டும்?
  delay_seconds = st.number_input(
      "ஒரு காலுக்கும் அடுத்த காலுக்கும் எத்தனை வினாடிகள் (Seconds) இடைவெளி"
      " வேண்டும்?",
      min_value=10,
      max_value=300,
      value=30,
  )

  # Session state-ல் நம்பர்களை சேமித்தல்
  if "current_index" not in st.session_state:
    st.session_state.current_index = 0
  if "calling" not in st.session_state:
    st.session_state.calling = False

  numbers = df[phone_col].dropna().astype(str).tolist()
  # தேவையற்ற .0 மற்றும் space நீக்குதல்
  clean_numbers = [
      num.strip().replace(" ", "").split(".")[0] for num in numbers
  ]

  st.info(f"மொத்தம் {len(clean_numbers)} நம்பர்கள் உள்ளன.")

  col1, col2, col3 = st.columns(3)
  with col1:
    if st.button("▶️ Start Auto Dial"):
      st.session_state.calling = True
  with col2:
    if st.button("⏸️ Pause"):
      st.session_state.calling = False
  with col3:
    if st.button("🔄 Reset"):
      st.session_state.calling = False
      st.session_state.current_index = 0

  # Auto Dialing நடக்கும் பகுதி
  if st.session_state.calling:
    idx = st.session_state.current_index
    if idx < len(clean_numbers):
      target_num = clean_numbers[idx]
      st.success(
          f"இப்போது கால் செல்லும் நம்பர் ({idx + 1}/{len(clean_numbers)}):"
          f" **{target_num}**"
      )

      # பிரவுசர் மூலம் போனுக்கு கால் சிக்னல் அனுப்பும் HTML/JS கோட்
      call_html = f"""
                <script>
                    window.top.location.href = "tel:{target_num}";
                </script>
            """
      components.html(call_html, height=0)

      # அடுத்த நம்பருக்கு நகர்தல்
      st.session_state.current_index += 1
      time.sleep(delay_seconds)
      st.rerun()
    else:
      st.balloons()
      st.success("🎉 அனைத்து நம்பர்களுக்கும் கால் செய்து முடிக்கப்பட்டது!")
      st.session_state.calling = False
