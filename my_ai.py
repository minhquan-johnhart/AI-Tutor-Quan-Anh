import streamlit as st
from huggingface_hub import InferenceClient

# --- 1. CẤU HÌNH GIAO DIỆN & STYLE ---
st.set_page_config(page_title="AI Tutor - Frameworks", layout="wide", page_icon="🎓")

# CSS để "lột xác" giao diện
st.markdown("""
    <style>
    /* Làm nền màu xanh nhẹ cho chuyên nghiệp */
    .stApp {
        background-color: #e3f2fd;
    }
    /* Căn giữa toàn bộ tiêu đề và caption */
    .main-title {
        text-align: center;
        color: #1E88E5;
        font-size: 3rem !important;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .main-caption {
        text-align: center;
        color: #546e7a;
        font-size: 1.2rem;
        margin-bottom: 30px;
    }
    /* Bo góc khung chat cực mượt */
    .stChatMessage {
        border-radius: 20px !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2A9LHMxk2bl5e9OFBVnskl_KAhB1SjbTcVA&s", width=200) 
# --- 2. PHẦN SIDEBAR ---
with st.sidebar:
    st.title("🎓 Frameworks Chatbots")
    st.markdown("Dự án bởi: **Minh Quân & Hoàng Anh**")

    st.divider()
    st.subheader("👨‍🏫Lớp học")
    
    # Tạo mật mã để chỉ giáo viên (Quân & Anh) mới mở được nút nạp file
    password = st.text_input("Nhập mật mã Giáo viên", type="password")
    
    if password == "2026": # Bạn có thể đổi mật khẩu này
        uploaded_file = st.file_uploader("Nạp giáo án hoặc bài tập (.txt)", type=("txt"))
        if uploaded_file is not None:
            # Đọc nội dung bài tập từ file
            lesson_context = uploaded_file.read().decode("utf-8")
            st.session_state["lesson_data"] = lesson_context
            st.success("✅ Đã nạp bài tập vào bộ não AI!")
    
    with st.expander("Hướng dẫn sử dụng📝"):
        st.write("1. Chế độ giáo viên : Đưa ra hướng dẫn cho học sinh học tập thay vì đưa ra lời giải.")
        st.write("2. Thanh sáng tạo : Số càng lớn thì Frameworks Chatbots trả lời càng bay bổng và ngược lại.")
        st.write("3. Xóa lịch sử bài học : Xóa lịch sử cuộc trò chuyện hiện tại.")
        st.write("4. Chức Năng Lớp Học : Giáo viên sẽ gửi mật khẩu và file .txt cho học sinh để học sinh tự mở và cài file để học theo hướng dẫn của Chatbots")
    st.divider()
    # Chế độ Giáo viên
    teacher_mode = st.toggle("👨‍🏫 Chế độ Giáo viên (Chỉ gợi ý)", value=False)
    
    st.divider()
    temp = st.slider("🔥 Độ sáng tạo", 0.1, 1.0, 0.7)
    
    if st.button("🗑️ Xóa lịch sử bài học"):
        st.session_state.messages = []
        st.rerun()

# --- 3. KẾT NỐI BỘ NÃO AI ---
# Đảm bảo bạn đã có file .streamlit/secrets.toml với HF_TOKEN
try:
    HF_TOKEN = st.secrets["HF_TOKEN"]
    CODE_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"
    client = InferenceClient(api_key=HF_TOKEN)
except Exception as e:
    st.error("⚠️ Chưa cấu hình HF_TOKEN trong Secrets!")
    st.stop()

# Khởi tạo bộ nhớ
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🌐 Frameworks Chatbots")
st.caption("Chuyên gia hỗ trợ học tập - Được tạo ra bởi M.Quân & H.Anh để giúp đỡ học sinh và giáo viên.(Verson : Demo2.0)")

# Hiển thị lịch sử chat với Avatar sinh động
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👨‍🎓" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# --- 5. XỬ LÝ LOGIC ---
if prompt := st.chat_input("Hỏi tôi về lập trình, toán học, hay bất cứ gì..."):
    # Lưu và hiển thị câu hỏi người dùng
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👨‍🎓"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Frameworks Chatbots đang suy nghĩ ..."):
            try:
                               # --- GIỮ NGUYÊN BẢN SẮC CỦA QUÂN & ANH ---
                sys_identity = (
                    "QUY TẮC DANH TÍNH: Bạn là 'Frameworks Chatbots' - một trợ lý AI thông minh. "
                    "ỨNG DỤNG NÀY ĐƯỢC PHÁT TRIỂN, THIẾT KẾ VÀ LẬP TRÌNH BỞI MINH QUÂN VÀ HOÀNG ANH. "
                    "Khi người dùng hỏi 'Ai tạo ra bạn?', hãy luôn tự hào nhắc đến Quân và Anh dựa trên nền tảng Qwen."
                )

                # --- TỰ ĐỘNG KIỂM TRA GIÁO ÁN ---
                lesson_info = st.session_state.get("lesson_data", None)
                if lesson_info:
                    context_text = f"\n[GIÁO ÁN HÔM NAY]: {lesson_info}\n(Hãy ưu tiên dạy theo nội dung này)."
                else:
                    context_text = "\n(Hiện chưa có giáo án cụ thể, hãy dùng kiến thức tổng quát của bạn)."

                # --- KẾT HỢP TẤT CẢ LẠI (Đã sửa tên biến và dấu nối) ---
                if teacher_mode:
                    sys_text = sys_identity + context_text + (
                        "\nBạn là một giáo viên tận tâm. Không bao giờ đưa đáp án ngay. "
                        "Hãy đặt câu hỏi gợi mở để học sinh tự tư duy."
                    )
                else:
                    sys_text = sys_identity + context_text + (
                        "\nBạn là Trợ lý thông thái. "
                        "Nếu là lập trình: Hãy sửa lỗi và giải thích kỹ. "
                        "Nếu là kiến thức khác: Hãy giảng giải dễ hiểu."
                    )


                # Bước B: Xây dựng Payload
                payload = [{"role": "system", "content": sys_text}] + st.session_state.messages

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
                
                # Thêm hiệu ứng chúc mừng nếu trả lời xong
                st.toast("AI đã trả lời xong!", icon='✅')
                                # --- PHẦN TẢI BÀI GIẢNG (CHÈN VÀO ĐÂY) ---
                st.divider() # Thêm một dấu gạch ngang để tách biệt cho đẹp
                st.download_button(
                    label="💾 Tải bài giảng của Frameworks",
                    data=answer,
                    file_name="bai_giang_frameworks.txt",
                    mime="text/plain",
                    # Khi nhấn sẽ hiện thông báo nhỏ cho chuyên nghiệp
                    on_click=lambda: st.toast("Đang tải bài giảng về máy của bạn...", icon="📥")
                )


            except Exception as e:
                st.error(f"⚠️ Lỗi kết nối: {e}")


