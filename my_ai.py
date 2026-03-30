import streamlit as st
from huggingface_hub import InferenceClient
import random # Thư viện để xoay vòng Token
import requests
# --- CẤU HÌNH MÁY CHỦ GOOGLE SHEETS ---
URL_GSHEET = "https://script.google.com/macros/s/AKfycbw2THtNIWws5_inxQfYaMuquUQLJNCYN2jXSudCMvvcZtfbhlTYyNJjbBgSYI8GT6momw/exec"
# Khởi tạo bộ đếm tiến độ
if "stats" not in st.session_state:
    st.session_state.stats = {"correct": 0, "wrong": 0, "ai_violation": 0}

def gui_ve_google_sheets(ten_hoc_sinh):
    # Dữ liệu gửi đi
    payload = {
        "student_id": ten_hoc_sinh,
        "stats": st.session_state.stats
    }
    try:
        # Nhớ dùng dấu = để truyền tham số nhé
        requests.post(URL_GSHEET, json=payload, timeout=2)
    except:
        pass

# --- 1. CẤU HÌNH GIAO DIỆN & STYLE (GIỮ NGUYÊN BẢN SẮC) ---
st.set_page_config(page_title="Frameworks Chatbots", layout="wide", page_icon="🎓")

# CSS tùy chỉnh giao diện
st.markdown("""
    <style>
    .stApp { background-color: #e3f2fd; }
    .main-title { text-align: center; color: #1E88E5; font-size: 3rem !important; font-weight: 700; margin-bottom: 0px; }
    .stChatMessage { border-radius: 20px !important; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2A9LHMxk2bl5e9OFBVnskl_KAhB1SjbTcVA&s", width=200) 

# --- 2. PHẦN SIDEBAR ---
# --- PHẦN SIDEBAR DUY NHẤT ---
with st.sidebar:
    st.title("🎓 Frameworks Chatbots")
    st.markdown("Dự án bởi: **Minh Quân & Hoàng Anh**")
    st.divider()

    # 1. Mục Tiến độ học tập
    st.subheader("📊 Tiến độ học tập")
    # Học sinh nhập tên ở đây (chỉ khai báo 1 lần duy nhất)
    ten_hs = st.text_input("Họ tên học sinh:", placeholder="Nhập tên để ghi nhận điểm...")
    
    # Hiển thị số liệu
    col1, col2, col3 = st.columns(3)
    col1.metric("Đúng", st.session_state.stats["correct"])
    col2.metric("Sai", st.session_state.stats["wrong"])
    col3.metric("AI", st.session_state.stats["ai_violation"])
    
    st.divider()

    # 2. Mục Lớp học (Dành cho giáo viên)
    st.subheader("🏫 Lớp học")
    password = st.text_input("Nhập mật mã Giáo viên", type="password")

    if password == "2026":
        uploaded_file = st.file_uploader("Nạp giáo án hoặc bài tập (.txt)", type=["txt"])
        if uploaded_file is not None:
            lesson_context = uploaded_file.read().decode("utf-8")
            st.session_state["lesson_data"] = lesson_context
            st.success("✅ Đã nạp bài tập thành công!")

    # 3. Nút Giao bài tập (Nếu đã nạp file)
    if "lesson_data" in st.session_state:
        if st.button(" 📝Giao bài tập từ giáo án"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Dựa vào giáo án đã nạp, hãy giao cho mình một bài tập cụ thể để thực hành nhé!"
            })
            st.rerun()
  
    with st.expander("Hướng dẫn sử dụng các chức năng📝"):
        st.write("1. 📊 Chức năng tiến độ học tập : Hiển thị số câu trả lời đúng, sai và bị nghi ngờ và thông báo về máy chủ của giáo viên")
        st.write("2A. 👨‍🏫Chức năng lớp học: Giáo viên sẽ đưa học sinh mật khẩu và file .txt để học sinh nạp vào bộ nhớ AI để học tập.")
        st.write("2B. 📝Chức năng giao bài tập tự giáo án: AI sẽ dựa vào dữ liệu bài tập nạp vào và đề ra câu hỏi cho học sinh.")
        st.write("3. 👨‍🏫Chế độ giáo viên: AI sẽ chỉ đưa ra chỉ dẫn cho học sinh thay vì giải trực tiếp.")
        st.write("4. 🚫Chế độ tập trung: AI sẽ chỉ trả lời câu hỏi liên quan tới bài học thay vì nói chuyện linh tinh.")
        st.write("5. 🛡️Chế độ giám sát: AI sẽ phân tích câu trả lời của học sinh sau khi làm bài tập và ngăn chặn các câu trả lời copy từ AI khác.")
        st.write("6. 🔥Độ sáng tạo: Biến số càng lớn thì AI trả lời càng bay bổng và ngược lại.")
        st.write("7. 🗑️Xóa lịch sử chat: Nhằm reset lịch sử trò truyện với AI")
    with st.expander("Ghi chú cập nhật"):
        st.write("Version 1.0 : Bản cập nhật sơ khai của Frameworks Chatbots nhằm thử nghiệm các tính năng cơ bản và cốt lõi nhất.")
        st.write("Version 2.0 : Cập nhật thêm tính năng 👨‍🏫Lớp học và thay thế mục Cách tạo ra tôi thành Hướng dẫn sử dụng.")
        st.write("Version 2.1 : Cập nhật lại tính nắng 👨‍🏫Lớp học và cải thiện giao diện tổng thể.")
        st.write("Version 2.7 : Cập nhật thêm về hướng dẫn sử dụng các tính năng và thêm các tính năng như 🚫Chế độ tập trung và 🛡️Chế độ giám sát.")
        st.write("Version 2.8 : Cải thiện tính năng 🚫Chế độ tập trung và thêm mục Ghi chú cập nhật cũng như cải thiện chất lượng phản hồi của Frameworks Chatbots")
        st.write("Version 2.10 ( Hiện tại ) : Cập nhật mục 📊 Tiến độ học tập và ghi nhận điểm trên sever chủ cũng như cải thiện lại các chức năng sẵn có.") 
    st.divider()
    # Các chế độ hoạt động
    teacher_mode = st.toggle("👨‍🏫 Chế độ Giáo viên (Chỉ gợi ý)", value=True)
    study_only = st.toggle("🚫 Chế độ tập trung (Chặn chuyện nhảm)", value=True)
    anti_ai_copy = st.toggle("🛡️ Chế độ giám sát (Chống Copy AI)", value=False)
    
    st.divider()
    temp = st.slider("🔥 Độ sáng tạo", 0.1, 1.0, 0.7)
    
    if st.button("🗑️ Xóa lịch sử bài học"):
        st.session_state.messages = []
        st.rerun()

# --- 3. KẾT NỐI BỘ NÃO AI (XOAY VÒNG 2 TOKEN) ---
try:
    # Hệ thống tự động chọn ngẫu nhiên 1 trong 2 Token để bảo vệ hạn mức
    token_list = [st.secrets["HF_TOKEN_1"], st.secrets["HF_TOKEN_2"]]
    selected_token = random.choice(token_list)
    
    CODE_MODEL = "Qwen/Qwen2.5-Coder-7B-Instruct"
    client = InferenceClient(api_key=selected_token)
except Exception as e:
    st.error("⚠️ Lỗi: Chưa cấu hình đủ HF_TOKEN_1 và HF_TOKEN_2 trong Secrets!")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🌐 Frameworks Chatbots")
st.caption("Chuyên gia hỗ trợ học tập và giám sát học tập - Developed by M.Quân(Main Dev) & H.Anh(Support Dev) (Version:Demo2.10)")

# Hiển thị lịch sử chat
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👨‍🎓" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])
# --- 5. XỬ LÝ LOGIC ---
if prompt := st.chat_input("Hỏi mình về bài học nhé..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# AI xử lý phản hồi khi có tin nhắn mới từ User
if len(st.session_state.messages) > 0 and st.session_state.messages[-1]["role"] == "user":
       with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Frameworks Chatbots đang suy nghĩ ..."):
            try:
                # 1. THIẾT LẬP TÍNH CÁCH MENTOR
                sys_text = (
                    "BẢN SẮC: Bạn là 'Frameworks Chatbots' - một người anh khóa trên (mentor) cực kỳ nhiệt huyết sẵn sàng giúp đỡ các em học sinh trong học tập. "
                    "PHONG CÁCH: Trả lời năng động, sử dụng emoji (🎓, ✨, 🚀). "
                    "Trình bày nội dung đẹp mắt bằng Markdown."
                    "QUY TẮC DANH TÍNH: Bạn là 'Frameworks Chatbots'. "
                    "ỨNG DỤNG ĐƯỢC PHÁT TRIỂN CHÍNH BỞI MINH QUÂN VÀ SỰ GIÚP ĐỠ CỦA HOÀNG ANH dựa trên API của Qwen và chạy trên nền tảng Streamlit. "
                )
                if study_only:
                    sys_text += (
                        "\n[LỆNH NGHIÊM NGẶT]: Bạn ĐANG Ở CHẾ ĐỘ TẬP TRUNG CAO ĐỘ, không trả lời câu hỏi không liên quan tới học tập hay những câu hỏi nhảm như Gay. "
                        "1. TUYỆT ĐỐI KHÔNG trả lời các câu hỏi về đời sống, ăn uống, ngủ nghỉ, giới tính và chuyện không phải học tập hoặc tán gẫu (Ví dụ: 'Đi ngủ không?', 'Ăn gì?', 'Bạn khỏe không?'). "
                        "2. Nếu gặp câu hỏi nhảm hoặc không phải học tập, bạn chỉ được phép trả lời duy nhất một kiểu: 'Hì, mình là AI hỗ trợ học tập, mình chỉ có thể giúp bạn giải quyết các vấn đề học tập thôi."
                        "3. Không được đưa ra lời khuyên ngoài giáo dục cũng như hạn chế trả lời các câu ngoài giáo dục."
                    )
                
                if anti_ai_copy:
                    sys_text += (
                        " GIÁM SÁT COPY: Nếu phát hiện học sinh dùng prompt máy móc của AI khác như của Gemini hay ChatGPT, "
                        "hãy nhắc nhở vui vẻ: 'Ui, câu hỏi này nghe hơi giống văn mẫu AI đó nha! Thử tự đặt câu hỏi theo ý mình đi nè! 🚀'"
                    )

                # Nạp giáo án và Lệnh chấm điểm
                lesson_info = st.session_state.get("lesson_data", None)
                if lesson_info:
                    sys_text += f"\n[GIÁO ÁN]: {lesson_info}"
                    sys_text += (
                        "\n[HỆ THỐNG CHẤM ĐIỂM]: Hãy tự giải bài tập trong giáo án để làm đáp án. "
                        "Bắt đầu phản hồi bằng mã: [DUNG], [SAI], hoặc [AI_CHECK] nếu học sinh trả lời bài tập. "
                        "Sau đó mới giải thích chi tiết."
                    )

                if teacher_mode:
                    sys_text += "\nCHẾ ĐỘ GIÁO VIÊN: Đừng bao giờ đưa đáp án ngay. Hãy đặt câu hỏi gợi mở để học sinh tự khám phá kiến thức."
                else:
                    sys_text += "\nBạn là người hướng dẫn tận tâm. Hãy giải thích kỹ càng kèm ví dụ thực tế sinh động."

                # 2. GỬI DỮ LIỆU ĐẾN API QWEN
                payload = [{"role": "system", "content": sys_text}] + st.session_state.messages
                response = client.chat_completion(
                    model=CODE_MODEL,
                    messages=payload,
                    temperature=temp,
                    max_tokens=750
                )

                # 3. XỬ LÝ PHẢN HỒI VÀ CHẤM ĐIỂM
                full_answer = response.choices[0].message.content
                res_upper = full_answer.upper()

                # Kiểm tra tên học sinh và cập nhật điểm số
                # (Đảm bảo biến ten_hs đã được khai báo ở Sidebar)
                if 'ten_hs' in locals() and ten_hs and ten_hs != "Học sinh A" and ten_hs != "":
                    if "[DUNG]" in res_upper:
                        st.session_state.stats["correct"] += 1
                        gui_ve_google_sheets(ten_hs)
                    elif "[SAI]" in res_upper:
                        st.session_state.stats["wrong"] += 1
                        gui_ve_google_sheets(ten_hs)
                    elif "[AI_CHECK]" in res_upper:
                        st.session_state.stats["ai_violation"] += 1
                        gui_ve_google_sheets(ten_hs)

                # 4. LÀM SẠCH VÀ HIỂN THỊ
                clean_answer = full_answer.replace("[DUNG]", "").replace("[SAI]", "").replace("[AI_CHECK]", "").strip()
                st.markdown(clean_answer)
                
                # Lưu vào lịch sử chat
                st.session_state.messages.append({"role": "assistant", "content": clean_answer})
                st.toast("Frameworks đã trả lời xong!", icon='✅')

                # Nút tải bài giảng
                st.divider()
                st.download_button(
                    label="💾 Tải bài giảng của Frameworks",
                    data=clean_answer,
                    file_name="bai_giang_frameworks.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"⚠️ Có chút trục trặc nhỏ: {e}")
                st.toast("Lỗi kết nối API!", icon='❌')




