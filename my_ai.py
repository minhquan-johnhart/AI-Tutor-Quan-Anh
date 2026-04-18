import streamlit as st
from huggingface_hub import InferenceClient
import random # Thư viện để xoay vòng Token
import requests
from supabase import create_client, Client
# --- CẤU HÌNH MÁY CHỦ SUPABASE ---
URL = st.secrets["SUPABASE_URL"]
KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(URL, KEY)
# --- CẤU HÌNH MÁY CHỦ GOOGLE SHEETS ---
URL_GSHEET = "https://script.google.com/macros/s/AKfycbw2THtNIWws5_inxQfYaMuquUQLJNCYN2jXSudCMvvcZtfbhlTYyNJjbBgSYI8GT6momw/exec"
# Khởi tạo bộ đếm tiến độ
if "stats" not in st.session_state:
    st.session_state.stats = {"correct": 0, "wrong": 0, "ai_violation": 0}
# Sửa lại hàm này ở phần đầu code của bạn
def gui_ve_google_sheets(ten_hoc_sinh, ket_qua): # Thêm tham số ket_qua
    payload = {
        "student_id": ten_hoc_sinh,
        "status": ket_qua, # Gửi trạng thái Đúng/Sai lên Sheets
        "stats": st.session_state.stats
    }
    try:
        requests.post(URL_GSHEET, json=payload, timeout=5)
    except:
        pass
# --- 1. CẤU HÌNH GIAO DIỆN & STYLE ---
st.set_page_config(page_title="Frameworks Chatbots", layout="wide", page_icon="🎓")
@st.dialog("⚙️ Cài đặt hệ thống")
def show_settings():
    st.write("Tùy chỉnh chế độ hoạt động của Chatbot")
    st.divider()
    
    # PHẢI CÓ CÁC DÒNG NÀY NÓ MỚI HIỆN NÚT NHA:
    st.session_state.teacher_mode = st.toggle(
        "👨‍🏫 Chế độ Giáo viên (Chỉ gợi ý)", 
        value=st.session_state.get('teacher_mode', True)
    )
    
    st.session_state.study_only = st.toggle(
        "🚫 Chế độ tập trung (Chặn chuyện nhảm)", 
        value=st.session_state.get('study_only', True)
    )
    
    st.session_state.anti_ai_copy = st.toggle(
        "🛡️ Chế độ giám sát (Chống Copy AI)", 
        value=st.session_state.get('anti_ai_copy', True)
    )
    if st.button("Lưu & Đóng"):
        st.rerun()
menu = st.sidebar.selectbox("Chọn trang", ["Trang chủ🎓", "Thư viện📚"])
if menu == "Thư viện📚":
    st.image("https://wallpapers.com/images/hd/colorful-bookshelf-vector-illustration-9pk8lci6j9gxzjer.jpg", width=200)
    # --- CSS PHẢI THỤT LỀ ---
    st.markdown("""
        <style>
        .stApp { background-color: #F0FFF4 !important; } /* Nền xanh bạc hà */
        
        /* Card trắng quý tộc */
        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: white !important;
            border-radius: 20px !important;
            border: 1px solid #C6F6D5 !important;
            box-shadow: 0 10px 20px rgba(0,0,0,0.05) !important;
            transition: 0.3s;
        }
        
        div[data-testid="stVerticalBlockBorderWrapper"]:hover {
            transform: translateY(-5px);
            border: 1px solid #003366 !important;
        }

        h1, h2, h3 { color: #003366 !important; font-family: 'Playfair Display', serif; }
        </style>
    """, unsafe_allow_html=True)
    st.header("📚 Thư viện tài liệu")
    st.caption("📑Thư viện file , nơi tổng hợp và chứa các đề án, giáo án, bài tập,... - 💻Được lập trình và quản lí bởi M.Quân(Engine Dev) & H.Anh(Idea & Q/A Dev)-")
    with st.sidebar:
        st.title("Thư viện📚-Frameworks Chatbots-")
        st.markdown("Dự án bởi: **Minh Quân & Hoàng Anh**")
        st.divider()
        st.write("Mẹo nhỏ 💡: Bạn có thể tìm thấy những bài tập cũng như bài giảng cũ nếu giáo viên nạp vào ở đây để học lại!")
        st.write("Mẹo nhỏ 💡: Giáo viên có thể upload file .txt và soạn thảo file đó theo ý muốn hoặc theo cấu trúc như : Nội dung chính -> Bài tập -> Củng cố bài học.")

    # --- CHIA CỘT ---
    col_upload, col_find = st.columns([1, 1.2])

    # --- PHẦN GIÁO VIÊN ---
    with col_upload: # Phải lùi vào để nằm trong cột
        with st.expander("👨‍🏫 -Khu vực đăng tải file .txt của Giáo viên-"):
            mk = st.text_input("Mật mã", type="password", key="lib_pwd")
            if mk == "giaovien":
                f = st.file_uploader("Chọn file .txt", type="txt", key="f_up")
                if st.button("🚀 Đăng lên thư viện"):
                    if f:
                        text_content = f.read().decode("utf-8")
                        supabase.table("library").insert({"filename": f.name, "content": text_content}).execute()
                        st.success("Đã đăng tải thành công!")
                        st.rerun()

    # --- THANH TÌM KIẾM ---
    with col_find: # Phải lùi vào để nằm trong cột
        search_query = st.text_input("🔍 Tìm kiếm tài liệu...", placeholder="Nhập tên bài học/bài tập cần tìm...")

    st.divider()

    # --- PHẦN HỌC SINH ---
    st.subheader("📖 Danh sách tài liệu📑")
    try:
        res = supabase.table("library").select("*").order("created_at", desc=True).execute()
        full_data = res.data 

        if search_query:
            filtered_data = [item for item in full_data if search_query.lower() in item['filename'].lower()]
        else:
            filtered_data = full_data

        if not filtered_data:
            if search_query:
                st.warning("Không tìm thấy kết quả nào phù hợp📑.")
            else:
                st.info("Thư viện hiện đang trống.")
        else: 
            for item in filtered_data:
                with st.container(border=True):
                    c1, c2 = st.columns([4, 1])
                    c1.markdown(f"📄 **{item['filename']}**")
                    c2.download_button("📥 Tải file về", data=item['content'], file_name=item['filename'], key=f"dl_{item['id']}")
                    with st.expander("🔍📄Đọc nhanh trước nội dung file .txt"):
                        st.text(item['content'])
                    
                    # Nút xóa (Để thụt lề thẳng hàng với container)
                    if mk == "ADMINGarez":
                        if st.button(f"🗑️ Xóa file vi phạm {item['id']}", key=f"del_{item['id']}"):
                            supabase.table("library").delete().eq("id", item['id']).execute()
                            st.rerun()
    except Exception as e:
        st.error(f"Lỗi hệ thống: {e}")

    st.stop()

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
    with st.expander("Điểm số⭐️"):
        col1, col2, col3 = st.columns(3)
        col1.metric("✅Đúng", st.session_state.stats["correct"])
        col2.metric("❌Sai", st.session_state.stats["wrong"])
        col3.metric("⚠️AI", st.session_state.stats["ai_violation"])
    

    # 2. Mục Lớp học (Dành cho học sinh nạp file)
    st.subheader("🏫 Lớp học-Mật khẩu hiện tại là: 2026")
    password = st.text_input("Nhập mật mã để bắt đầu nạp file và học.", type="password")

    if password == "2026":
        uploaded_file = st.file_uploader("Nạp giáo án hoặc bài tập (.txt)", type=["txt"])
        if uploaded_file is not None:
            lesson_context = uploaded_file.read().decode("utf-8")
            st.session_state["lesson_data"] = lesson_context
            st.success("✅ Đã nạp bài tập/giáo án thành công!")

    # 3. Nút Giao bài tập (Nếu đã nạp file)
    if "lesson_data" in st.session_state:
        if st.button(" 📝Giao bài tập từ giáo án"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Dựa vào giáo án đã nạp, hãy giao cho mình một bài tập cụ thể để thực hành nhé!"
            })
            st.rerun()
        if st.button(" 📝Học bài từ giáo án"):
            st.session_state.messages.append({
                "role": "user", 
                "content": "Dựa vào giáo án đã nạp, hãy giảng cho mình nội dung bài học nhé!"
            })
            st.rerun()


    st.divider()  
    with st.expander("Hướng dẫn sử dụng các chức năng📝"):
        st.write("Mục thư viện📚 , giáo viên nhập mật khẩu để mở khóa tính năng đăng tỉa file .txt bài tập , lí thuyết, ôn tập lên thư viện-được cập nhật theo thời gian thực- để học sinh có thể thấy và tải về file .txt để nạp vào AI học theo hướng dẫn-học sinh có khả năng xem trước nội dung file .txt")
        st.write("1. 📊 Chức năng thống kê học tập : Hiển thị số câu trả lời đúng, sai hoặc bị nghi ngờ sử dụng AI và thông báo về máy chủ của giáo viên theo thời gian thực -có yêu cầu nhập tên-.")
        st.write("2A. 👨‍🏫Chức năng lớp học: Học sinh nhập mật khẩu vào và nạp file .txt vào bộ nhớ AI để học tập, ôn tập,...")
        st.write("2B. 📝Chức năng giao bài tập tự giáo án: AI sẽ dựa vào dữ liệu bài tập nạp vào và đề ra câu hỏi cho học sinh.")
        st.write("2C. 📝Chức năng học bài từ giáo án : AI sẽ dựa vào dữ liệu nội dung lí thuyết được nạp vào để giảng nội dung học.")
        st.write("3Settings. 👨‍🏫Chế độ giáo viên: AI sẽ chỉ đưa ra chỉ dẫn cho học sinh thay vì giải trực tiếp.")
        st.write("4Settings. 🚫Chế độ tập trung: AI sẽ chỉ trả lời câu hỏi liên quan tới bài học thay vì nói chuyện linh tinh.")
        st.write("5Settings. 🛡️Chế độ giám sát: AI sẽ phân tích câu trả lời của học sinh sau khi làm bài tập và ngăn chặn các câu trả lời copy từ AI khác.")
        st.write("6. 🔥Độ sáng tạo: Biến số càng lớn thì AI trả lời càng bay bổng và ngược lại -thích hợp với văn học về sự bay bổng và toán học về sự logic-.")
        st.write("7. 🗑️Xóa lịch sử chat: Nhằm reset lịch sử trò truyện với AI")
    with st.expander("Ghi chú cập nhật📍"):
        st.write("Version Demo1.0 : Bản cập nhật sơ khai của Frameworks Chatbots nhằm thử nghiệm các tính năng cơ bản và cốt lõi nhất.")
        st.write("Version Demo2.0 : Cập nhật thêm tính năng 👨‍🏫Lớp học và thay thế mục Cách tạo ra tôi thành Hướng dẫn sử dụng.")
        st.write("Version Demo2.1 : Cập nhật lại tính nắng 👨‍🏫Lớp học và cải thiện giao diện tổng thể.")
        st.write("Version Demo2.7 : Cập nhật thêm về hướng dẫn sử dụng các tính năng và thêm các tính năng như 🚫Chế độ tập trung và 🛡️Chế độ giám sát.")
        st.write("Version Demo2.8 : Cải thiện tính năng 🚫Chế độ tập trung và thêm mục Ghi chú cập nhật cũng như cải thiện chất lượng phản hồi của Frameworks Chatbots.")
        st.write("Version Demo2.10 : Cập nhật mục 📊 Thống kê học tập và ghi nhận điểm trên sever chủ cũng như cải thiện lại các chức năng sẵn có.") 
        st.write("Version Demo2.11 : Cải thiện tính năng 📊 Thống kê học tập và ghi nhận điểm cũng như vá lại một số lỗi nhỏ xung đột.")
        st.write("Version Demo2.12-Final : Trang trí thêm về giao diện và thêm icon cho các tiện ích trong thanh sidebar.")
        st.write("Version Neo3.0 : Thêm page Thư viện 📚, đưa các chế độ của chatbots vào thanh ⚙️ Cài đặt hệ thống, thay API Qwen2.5-7B Instruct thành bản Qwen2.5-32B Instruct, cải thiện prompt engine.")
        st.write("Version Neo3.1 ( Hiện tại ) : Tối ưu prompt engineering cho tính năng giám sát chống copy AI và chế độ giáo viên, câu trả lời của chatbot giờ sẽ là dạng streaming.")
    st.divider()
    temp = st.slider("🔥Độ sáng tạo✨", 0.1, 1.0, 0.7)
    if st.button("🗑️ Xóa lịch sử bài học"):
        st.session_state.messages = []
        st.rerun()
    st.divider()
    if st.button("⚙️ Cài đặt hệ thống"):
        show_settings() # Gọi cái hàm dialog

# --- 3. KẾT NỐI BỘ NÃO AI (XOAY VÒNG 2 TOKEN) ---
try:
    # Hệ thống tự động chọn ngẫu nhiên 1 trong 2 Token để bảo vệ hạn mức
    token_list = [st.secrets["HF_TOKEN_1"], st.secrets["HF_TOKEN_2"]]
    selected_token = random.choice(token_list)
    
    CODE_MODEL = "Qwen/Qwen2.5-Coder-32B-Instruct"
    client = InferenceClient(api_key=selected_token)
except Exception as e:
    st.error("⚠️ Lỗi: Chưa cấu hình đủ HF_TOKEN_1 và HF_TOKEN_2 trong Secrets!")
    st.stop()
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- 4. GIAO DIỆN CHÍNH ---
st.title("🌐 Frameworks Chatbots")
st.caption("⭐️Chuyên gia hỗ trợ học tập và giám sát học tập - 💻Được lập trình bởi M.Quân(Main Dev) & H.Anh(Support Dev)-(Version:Neo3.1✨)")
st.caption("👨‍🎓Vì một môi trường học tập minh bạch, chính xác và tiến bộ!📈")

# --- 5. HIỂN THỊ LỊCH SỬ CHAT ---
# Vòng lặp này cực kỳ quan trọng để giữ lại tin nhắn cũ trên màn hình
for msg in st.session_state.messages:
    if msg["role"] != "system":
        avatar = "👨‍🎓" if msg["role"] == "user" else "🎓"
        with st.chat_message(msg["role"], avatar=avatar):
            st.markdown(msg["content"])

# --- 6. XỬ LÝ NHẬP LIỆU TỪ NGƯỜI DÙNG ---
if prompt := st.chat_input("Hỏi mình về bài học nhé..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.rerun()

# --- 7. AI XỬ LÝ PHẢN HỒI ---
if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
    with st.chat_message("assistant", avatar="🎓"):
        with st.spinner("Frameworks Chatbots đang suy nghĩ vui lòng đợi chút nhé!..."):
            try:
                # --- THIẾT LẬP TÍNH CÁCH ---
                sys_text = (
                    "BẢN SẮC: Bạn là 'Frameworks Chatbots' - một người thầy giáo cực kỳ nhiệt huyết và thân thiện. "
                    "ỨNG DỤNG ĐƯỢC PHÁT TRIỂN CHÍNH BỞI MINH QUÂN VÀ HOÀNG ANH dựa trên API của Qwen và chạy trên nền tảng Streamlit. "
                    "PHONG CÁCH: Hãy trả lời năng động, sử dụng các emoji (🎓, ✨, 🚀, 💡) để bài giảng sinh động. "
                    "Hãy luôn khen ngợi học sinh khi họ đặt câu hỏi hay hoặc làm bài đúng để khích lệ tinh thần. "
                    "Trình bày nội dung đẹp mắt bằng Markdown, in đậm các từ khóa quan trọng."
                )

                if st.session_state.get('study_only', True):
                    sys_text += (
                        "\n[LỆNH NGHIÊM NGẶT]: Bạn ĐANG Ở CHẾ ĐỘ TẬP TRUNG CAO ĐỘ, không trả lời câu hỏi không liên quan tới học tập hay những câu hỏi nhảm không liên quan tới lĩnh vực học tập. "
                        "1. TUYỆT ĐỐI KHÔNG trả lời các câu hỏi về đời sống, ăn uống, ngủ nghỉ, giới tính và chuyện không phải học tập hoặc tán gẫu (Ví dụ: 'Đi ngủ không?', 'Ăn gì?', 'Bạn khỏe không?'). "
                        "2. Nếu gặp câu hỏi nhảm hoặc không phải học tập, bạn chỉ được phép trả lời duy nhất một kiểu: 'Hì, mình là AI hỗ trợ học tập, mình chỉ có thể giúp bạn giải quyết các vấn đề học tập thôi."
                        "3. Không được đưa ra lời khuyên ngoài giáo dục."
                    )
                
                if st.session_state.get('anti_ai_copy', True):
                    sys_text += (
                        "\n- GIÁM SÁT COPY: Nếu phát hiện học sinh dùng prompt máy móc của AI khác như của Gemini hay ChatGPT để trả lời câu hỏi. Chẳng hạn dài một cách bất thường hoặc quá chuyên nghiệp, lập tức dùng thẻ [AI_CHECK]."
                        "\n- hãy nhắc nhở học sinh để học sinh tự làm bài chứ không phải dùng AI để giải bài hộ."
                        "\n- nếu học sinh trả lời đúng thì hãy hỏi vì sao học sinh làm được như vậy và áp dụng những kiến thức gì để xem học sinh có thực sự làm hay không."
                        "\n- Nếu nghi ngờ học sinh dùng AI (thẻ [AI_CHECK]), sau khi nhắc nhở, hãy TRÍCH DẪN một câu ngắn từ câu trả lời của học sinh và hỏi: 'Ý này em tự viết hay tham khảo ở đâu? Em giải thích rõ hơn cho mình cụm từ [từ_khóa] này được không?'"
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
                        "\n- Ưu tiên giảng dạy theo dữ liệu được nạp vào và bám sát nội dung học."
                    )
               # Chế độ giáo viên gợi mở
                if st.session_state.get('teacher_mode', True):
                    sys_text += "\nCHẾ ĐỘ GIÁO VIÊN: Đừng bao giờ đưa đáp án ngay. Hãy đặt câu hỏi gợi mở để học sinh tự khám phá kiến thức, hãy luôn bảo học sinh đưa ra đáp án trước."
                else:
                    sys_text += "\nBạn là người hướng dẫn tận tâm. Hãy giải thích kỹ càng nhưng hãy hạn chế đưa ra đáp án và đưa ra dạng bài tập tương tự để học sinh áp dụng lại."

                # 2. GỬI DỮ LIỆU ĐẾN API
                payload = [{"role": "system", "content": sys_text}] + st.session_state.messages
                response = client.chat_completion(
                    model=CODE_MODEL,
                    messages=payload,
                    temperature=temp,
                    max_tokens=750,
                    stream=True
                )

                # 3. XỬ LÝ PHẢN HỒI
                def text_generator():
                    for chunk in response:
                        try:
                            # Kiểm tra xem gói tin có chứa dữ liệu hợp lệ không
                            if hasattr(chunk, 'choices') and len(chunk.choices) > 0:
                                content = chunk.choices[0].delta.content
                                if content:
                                    yield content
                        except (AttributeError, IndexError):
                            continue # Bỏ qua nếu gói tin đó bị lỗi định dạng

                # Hiển thị chữ chạy trên màn hình
                full_answer = st.write_stream(text_generator())

                # Xử lý hậu kỳ
                res_upper = full_answer.upper()
                st.sidebar.info(f"Mã AI gửi: {res_upper[:20]}")
                
                clean_answer = full_answer.replace("[DUNG]", "").replace("[SAI]", "").replace("[AI_CHECK]", "").strip()

                # --- LƯU VÀO LỊCH SỬ ---
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

                # 5. RERUN CẬP NHẬT GIAO DIỆN
                # Lệnh này sẽ load lại trang, chạy lại vòng lặp "Hiển thị lịch sử chat" 
                # ở Bước 4 và cập nhật các con số ở Sidebar.
                st.rerun()
            except Exception as e:
                st.error(f"⚠️ Lỗi hệ thống: {e}")

