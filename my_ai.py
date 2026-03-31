import streamlit as st
from huggingface_hub import InferenceClient
import random # Thư viện để xoay vòng Token
import requests
# --- CẤU HÌNH MÁY CHỦ GOOGLE SHEETS ---
URL_GSHEET = "https://script.google.com/macros/s/AKfycbw2THtNIWws5_inxQfYaMuquUQLJNCYN2jXSudCMvvcZtfbhlTYyNJjbBgSYI8GT6momw/exec"
# Khởi tạo bộ đếm tiến độ
if "stats" not in st.session_state:
    st.session_state.stats = {"correct": 0, "wrong": 0, "ai_violation": 0}
# Sửa lại hàm này ở phần đầu code của bạn
def gui_ve_google_sheets(ten_hoc_sinh, ket_qua): # Thêm tham số ket_qua ở đây
    payload = {
        "student_id": ten_hoc_sinh,
        "status": ket_qua, # Gửi trạng thái Đúng/Sai lên Sheets
        "stats": st.session_state.stats
    }
    try:
        requests.post(URL_GSHEET, json=payload, timeout=5)
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
    st.image(
        "https://quickchart.io/qr?text=https%3A%2F%2Fai-tutor-quan-anh-gtbmxeoelebxemxvgzwyis.streamlit.app%2F&size=200", 
        caption="📱 Quét mã để vào học cùng Framework Chatbots ngay!", 
        width=200
    )

    st.divider()
    # 1. Mục Tiến độ học tập
    st.subheader("📊 Thống kê học tập")
    # Học sinh nhập tên ở đây (chỉ khai báo 1 lần duy nhất)
    ten_hs = st.text_input("Họ tên học sinh:", placeholder="Nhập tên để ghi nhận điểm...")
    
    # Hiển thị số liệu
    col1, col2, col3 = st.columns(3)
    col1.metric("✅Đúng", st.session_state.stats["correct"])
    col2.metric("❌Sai", st.session_state.stats["wrong"])
    col3.metric("⚠️AI", st.session_state.stats["ai_violation"])
    
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

    st.divider()  
    with st.expander("Hướng dẫn sử dụng các chức năng📝"):
        st.write("1. 📊 Chức năng thống kê học tập : Hiển thị số câu trả lời đúng, sai hoặc bị nghi ngờ sử dụng AI và thông báo về máy chủ của giáo viên theo thời gian thực.")
        st.write("2A. 👨‍🏫Chức năng lớp học: Giáo viên sẽ đưa học sinh mật khẩu và file .txt để học sinh nạp vào bộ nhớ AI để học tập.")
        st.write("2B. 📝Chức năng giao bài tập tự giáo án: AI sẽ dựa vào dữ liệu bài tập nạp vào và đề ra câu hỏi cho học sinh.")
        st.write("3. 👨‍🏫Chế độ giáo viên: AI sẽ chỉ đưa ra chỉ dẫn cho học sinh thay vì giải trực tiếp.")
        st.write("4. 🚫Chế độ tập trung: AI sẽ chỉ trả lời câu hỏi liên quan tới bài học thay vì nói chuyện linh tinh.")
        st.write("5. 🛡️Chế độ giám sát: AI sẽ phân tích câu trả lời của học sinh sau khi làm bài tập và ngăn chặn các câu trả lời copy từ AI khác.")
        st.write("6. 🔥Độ sáng tạo: Biến số càng lớn thì AI trả lời càng bay bổng và ngược lại.")
        st.write("7. 🗑️Xóa lịch sử chat: Nhằm reset lịch sử trò truyện với AI")
    with st.expander("Ghi chú cập nhật📍"):
        st.write("Version 1.0 : Bản cập nhật sơ khai của Frameworks Chatbots nhằm thử nghiệm các tính năng cơ bản và cốt lõi nhất.")
        st.write("Version 2.0 : Cập nhật thêm tính năng 👨‍🏫Lớp học và thay thế mục Cách tạo ra tôi thành Hướng dẫn sử dụng.")
        st.write("Version 2.1 : Cập nhật lại tính nắng 👨‍🏫Lớp học và cải thiện giao diện tổng thể.")
        st.write("Version 2.7 : Cập nhật thêm về hướng dẫn sử dụng các tính năng và thêm các tính năng như 🚫Chế độ tập trung và 🛡️Chế độ giám sát.")
        st.write("Version 2.8 : Cải thiện tính năng 🚫Chế độ tập trung và thêm mục Ghi chú cập nhật cũng như cải thiện chất lượng phản hồi của Frameworks Chatbots.")
        st.write("Version 2.10 : Cập nhật mục 📊 Thống kê học tập và ghi nhận điểm trên sever chủ cũng như cải thiện lại các chức năng sẵn có.") 
        st.write("Version 2.11 : Cải thiện tính năng 📊 Thống kê học tập và ghi nhận điểm cũng như vá lại một số lỗi nhỏ xung đột.")
        st.write("Version 2.12 ( Hiện tại ) : Trang trí thêm về giao diện và thêm icon cho các tiện ích trong thanh sidebar.")
    st.divider()
    # Các chế độ hoạt động
    teacher_mode = st.toggle("👨‍🏫 Chế độ Giáo viên (Chỉ gợi ý)", value=True)
    study_only = st.toggle("🚫 Chế độ tập trung (Chặn chuyện nhảm)", value=True)
    anti_ai_copy = st.toggle("🛡️ Chế độ giám sát (Chống Copy AI)", value=False)
    
    st.divider()
    temp = st.slider("🔥Độ sáng tạo✨", 0.1, 1.0, 0.7)
    
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
st.caption("⭐️Chuyên gia hỗ trợ học tập và giám sát học tập - 💻Được lập trình bởi M.Quân(Main Dev) & H.Anh(Support Dev)-(Version:Demo2.12 - Final)")

# --- 5. HIỂN THỊ LỊCH SỬ CHAT ---
# Vòng lặp này cực kỳ quan trọng để giữ lại tin nhắn cũ trên màn hình
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👨‍🎓" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# --- 6. XỬ LÝ NHẬP LIỆU TỪ NGƯỜI DÙNG ---
if prompt := st.chat_input("Hỏi mình về bài học nhé..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- 7. AI XỬ LÝ PHẢN HỒI (Chỉ chạy khi tin nhắn cuối là của User) ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Frameworks Chatbots đang suy nghĩ ..."):
            try:
                # --- THIẾT LẬP TÍNH CÁCH MENTOR (MẶN MÀ & THÂN THIỆN) ---
                sys_text = (
                    "BẢN SẮC: Bạn là 'Frameworks Chatbots' - một người anh khóa trên (mentor) cực kỳ nhiệt huyết và thân thiện. "
                    "ỨNG DỤNG ĐƯỢC PHÁT TRIỂN CHÍNH BỞI MINH QUÂN VÀ HOÀNG ANH dựa trên API của Qwen và chạy trên nền tảng Streamlit. "
                    "PHONG CÁCH: Hãy trả lời năng động, sử dụng các emoji (🎓, ✨, 🚀, 💡) để bài giảng sinh động. "
                    "Hãy luôn khen ngợi học sinh khi họ đặt câu hỏi hay hoặc làm bài đúng để khích lệ tinh thần. "
                    "Trình bày nội dung đẹp mắt bằng Markdown, in đậm các từ khóa quan trọng."
                )

                if study_only:
                    sys_text += (
                        "\n[LỆNH NGHIÊM NGẶT]: Bạn ĐANG Ở CHẾ ĐỘ TẬP TRUNG CAO ĐỘ, không trả lời câu hỏi không liên quan tới học tập hay những câu hỏi nhảm như Gay. "
                        "1. TUYỆT ĐỐI KHÔNG trả lời các câu hỏi về đời sống, ăn uống, ngủ nghỉ, giới tính và chuyện không phải học tập hoặc tán gẫu (Ví dụ: 'Đi ngủ không?', 'Ăn gì?', 'Bạn khỏe không?'). "
                        "2. Nếu gặp câu hỏi nhảm hoặc không phải học tập, bạn chỉ được phép trả lời duy nhất một kiểu: 'Hì, mình là AI hỗ trợ học tập, mình chỉ có thể giúp bạn giải quyết các vấn đề học tập thôi."
                        "3. Không được đưa ra lời khuyên ngoài giáo dục."
                    )
                
                if anti_ai_copy:
                    sys_text += (
                        " GIÁM SÁT COPY: Nếu phát hiện học sinh dùng prompt máy móc của AI khác như của Gemini hay ChatGPT hay trả lời dài một cách bất thường,lập tức dùng thẻ [AI_CHECK]."
                        "hãy nhắc nhở vui vẻ: 'Ui, câu hỏi này nghe hơi giống copy mẫu AI đó nha! Thử tự trả lời theo ý mình đi nè! 🚀'"
                    )                
                # Nạp giáo án và Lệnh chấm điểm
                lesson_info = st.session_state.get("lesson_data", None)
                if lesson_info:
                    sys_text += f"\n[GIÁO ÁN]: {lesson_info}"
                    sys_text += (
                        "\n[QUY TẮC CHẤM ĐIỂM NGHIÊM NGẶT]:"
                        "\n- Bước 1: Tự giải bài toán học sinh đưa ra để có đáp án chuẩn sau đó đối chiếu với kết quả của học sinh."
                        "\n- Bước 2: BẮT BUỘC PHẢI BẮT ĐẦU CÂU TRẢ LỜI BẰNG THẺ: [DUNG], [SAI], hoặc [AI_CHECK]."
                        "\n- Nếu học sinh làm SAI: Dùng thẻ [SAI], tuyệt đối không khen ngợi, phải chỉ rõ lỗi sai ngay lập tức."
                        "\n- Nếu học sinh làm ĐÚNG: Dùng thẻ [DUNG] và khen ngợi khích lệ."
                        "\n- Nếu câu trả lời của học sinh có phần của AI giải hoặc prompt trả lời dài một cách bất thường hoặc dùng nhiều ngôn từ quá chuyên nghiệp thì dùng thẻ [AI_CHECK]."
                        "\n- Tuyệt đối không được 'ba phải' hoặc tự ý sửa đáp án sai của học sinh thành đúng."
                    )
               # Chế độ giáo viên gợi mở
                if teacher_mode:
                    sys_text += "\nCHẾ ĐỘ GIÁO VIÊN: Đừng bao giờ đưa đáp án ngay. Hãy đặt câu hỏi gợi mở để học sinh tự khám phá kiến thức."
                else:
                    sys_text += "\nBạn là người hướng dẫn tận tâm. Hãy giải thích kỹ càng kèm ví dụ thực tế sinh động."


                # 2. GỬI DỮ LIỆU ĐẾN API
                payload = [{"role": "system", "content": sys_text}] + st.session_state.messages
                response = client.chat_completion(
                    model=CODE_MODEL,
                    messages=payload,
                    temperature=temp,
                    max_tokens=750
                )

                # 3. XỬ LÝ PHẢN HỒI
                full_answer = response.choices[0].message.content
                res_upper = full_answer.upper()
                st.sidebar.info(f"Mã AI gửi: {res_upper[:20]}")
                # Làm sạch nội dung để hiển thị cho học sinh
                clean_answer = full_answer.replace("[DUNG]", "").replace("[SAI]", "").replace("[AI_CHECK]", "").strip()

                # --- BƯỚC QUAN TRỌNG NHẤT: LƯU VÀO LỊCH SỬ TRƯỚC KHI RERUN ---
                st.session_state.messages.append({"role": "assistant", "content": clean_answer})

                # 4. CHẤM ĐIỂM VÀ GỬI GOOGLE SHEETS
                if ten_hs and ten_hs != "Học sinh A" and ten_hs != "":
                    if "last_processed_res" not in st.session_state:
                        st.session_state.last_processed_res = ""

                    # Chỉ cộng điểm nếu câu này chưa được xử lý
                    if res_upper != st.session_state.last_processed_res:
                        # KIỂM TRA THẺ TAG (Thêm các từ khóa dự phòng)
                        if "[DUNG]" in res_upper or "ĐÚNG RỒI" in res_upper:
                            st.session_state.stats["correct"] += 1
                            gui_ve_google_sheets(ten_hs, "Đúng")
                        
                        elif "[SAI]" in res_upper or "SAI RỒI" in res_upper or "CHƯA CHÍNH XÁC" in res_upper:
                            st.session_state.stats["wrong"] += 1
                            gui_ve_google_sheets(ten_hs, "Sai")
                            
                        elif "[AI_CHECK]" in res_upper:
                            st.session_state.stats["ai_violation"] += 1
                            gui_ve_google_sheets(ten_hs, "AI Check")
                        
                        # QUAN TRỌNG: Cập nhật khóa kể cả khi không khớp thẻ nào 
                        # để tránh việc AI cứ lặp lại một câu không có thẻ.
                        st.session_state.last_processed_res = res_upper

                # 5. RERUN ĐỂ CẬP NHẬT GIAO DIỆN
                # Lệnh này sẽ load lại trang, chạy lại vòng lặp "Hiển thị lịch sử chat" 
                # ở Bước 4 và cập nhật các con số ở Sidebar.
                st.rerun()

            except Exception as e:
                st.error(f"⚠️ Lỗi hệ thống: {e}")


