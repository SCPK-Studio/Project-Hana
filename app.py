import streamlit as st
import google.generativeai as genai

# 1. Cấu hình trang Web
st.set_page_config(page_title="Hana Assistant", page_icon="🌸")
st.title("🌸 Hana - Trợ lý AI Cá nhân")

# 2. Kết nối API (Lấy chìa khóa từ Secrets của Streamlit)
try:
    # Ở Colab ta dùng userdata, ở đây ta dùng st.secrets
    my_api_key = st.secrets["MY_API_KEY"]
    genai.configure(api_key=my_api_key)
except:
    # Phòng trường hợp chưa cài Key
    st.warning("⚠️ Hana chưa tìm thấy Chìa khóa! Vui lòng thiết lập Secrets trên Streamlit Cloud.")
    st.stop()

# 3. Khởi tạo Model (Hana 2.5 Flash)
model = genai.GenerativeModel('gemini-2.5-flash')

# 4. Quản lý lịch sử chat (Để Hana nhớ được chuyện cũ)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Hiển thị lại các tin nhắn cũ trên màn hình
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Khung nhập liệu & Xử lý
# Khi bạn gõ câu hỏi và Enter:
if prompt := st.chat_input("Bạn cần Hana giúp gì hôm nay?"):
    # Hiện câu hỏi của bạn lên màn hình
    with st.chat_message("user"):
        st.markdown(prompt)
    # Lưu vào bộ nhớ
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Gọi Hana trả lời
    with st.chat_message("assistant"):
        with st.spinner("Hana đang suy nghĩ..."):
            try:
                # Xây dựng ngữ cảnh từ lịch sử chat
                history_gemini = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    history_gemini.append({"role": role, "parts": [msg["content"]]})
                
                chat = model.start_chat(history=history_gemini)
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                
                # Lưu câu trả lời vào bộ nhớ
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Có lỗi xảy ra: {e}")
