import streamlit as st
from huggingface_hub import InferenceClient

# --- 1. CẤU HÌNH GIAO DIỆN ---
st.set_page_config(page_title="AI Tutor", layout="wide", page_icon="🎓")

with st.sidebar:
    st.title("🚀 Easy To Access & Know AI")
    st.markdown("Founder: **Minh Quân & Hoàng Anh**")
    with st.expander("📝 Cách tạo ra tôi"):
        st.write("1. Cài streamlit, huggingface_hub")
        st.write("2. Tạo file .py bằng Notepad hoặc VS Code")
        st.write("3. Dán Token và Model ID")
        st.write("4. Chạy lệnh: streamlit run my_ai.py")
    st.divider()
    
    # Chế độ Giáo viên
    teacher_mode = st.toggle("Chế độ Giáo viên (Chỉ gợi ý)", value=False)
    
    st.divider()
    temp = st.slider("Độ sáng tạo", 0.1, 1.0, 0.7)
    if st.button("🗑️ Xóa lịch sử bài học"):
        st.session_state.messages = []
        st.rerun()

# --- 2. KẾT NỐI BỘ NÃO AI (CHỈ CHUYÊN CODE) ---
# Gọi mã bí mật từ hầm trú ẩn .streamlit/secrets.toml
HF_TOKEN = st.secrets["HF_TOKEN"]
CODE_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"

client = InferenceClient(api_key=HF_TOKEN)

# --- 3. KHỞI TẠO BỘ NHỚ ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🌐 AI Tutor & Coding Assistant")
st.caption("Chuyên gia sửa lỗi code và hỗ trợ học tập - By Quân & Anh")

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- 5. XỬ LÝ LOGIC (CHỈ XỬ LÝ VĂN BẢN & CODE) ---
if prompt := st.chat_input("Hỏi tôi về lập trình hoặc bài tập..."):
    # Lưu và hiển thị câu hỏi người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI đang suy nghĩ..."):
            try:
                # Bước A: Chọn lời nhắc hệ thống (System Prompt)
                if teacher_mode:
                    sys_text = "Bạn là giáo viên tận tâm. Không đưa đáp án ngay, hãy hướng dẫn từng bước để học sinh tự tư duy."
                else:
                    sys_content = "Bạn là chuyên gia lập trình. Hãy sửa lỗi và đưa code hoàn chỉnh."
                    sys_text = sys_content

                # Bước B: Xây dựng danh sách tin nhắn để gửi đi
                payload = [{"role": "system", "content": sys_text}]
                for m in st.session_state.messages:
                    payload.append(m)

                # Bước C: Gọi AI trả lời
                response = client.chat_completion(
                    model=CODE_MODEL,
                    messages=payload,
                    temperature=temp,
                    max_tokens=1500
                )

                # Bước D: Lấy kết quả và hiển thị
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

            except Exception as e:
                st.error(f"⚠️ Lỗi: {e}")
                st.info("Mẹo: Hãy kiểm tra kết nối mạng hoặc thử lại sau ít phút.")


