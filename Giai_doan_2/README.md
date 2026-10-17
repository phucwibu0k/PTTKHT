# Giai đoạn 2 — Quản lý phòng khám tư nhân

## Hai tài liệu dùng để nộp

- [Báo cáo giai đoạn 2 (PDF)](Bao_cao_Giai_doan_2.pdf), 22 trang. [Bản Word](Bao_cao_Giai_doan_2.docx).
- [Giai đoạn 1 cập nhật (PDF)](../Giai_doan_1/Bao_cao_Giai_doan_1_cap_nhat.pdf), 22 trang. [Bản Word](../Giai_doan_1/Bao_cao_Giai_doan_1_cap_nhat.docx). Bổ sung 3 sơ đồ phân rã và 7 Use Case con theo góp ý; bản giai đoạn 1 ban đầu được giữ nguyên.

Bìa giữ thông tin đã điền trong Word giai đoạn 1 hiện có; các thành viên còn trống cần bổ sung. Tài liệu dùng A4 dọc/ngang, số trang giữa đầu trang, không có chữ ở footer. Nhóm cần đọc và bổ sung phần phản biện AI trước khi nộp.

## Nguồn chỉnh sửa

- `nguon/noi_dung.md`: nội dung giai đoạn 2.
- `nguon/mo_hinh_lop.iuml`: định nghĩa chung của 18 lớp; bốn file `lop_*.puml` là bốn góc nhìn, không phải bốn mô hình khác nhau.
- `nguon/tuan_tu_*.puml`: ba tương tác; khám/kê đơn chia hai hình a/b.
- `nguon/trang_thai_luot_kham.puml`: vòng đời lượt khám.
- `nguon/phan_ra_*.puml` và `nguon/bo_sung_giai_doan_1.md`: nội dung bổ sung giai đoạn 1.
- PNG dùng trong Word/PDF; SVG dùng để xem/phóng to độc lập.
- `nguon/ket_qua_kiem_tra.txt`: kết quả đối chiếu tĩnh và kiểm tra tài liệu.

## Xuất lại bằng công cụ trong arch-box

Chạy từ thư mục dự án. Các lệnh dưới ghi đè **bản giai đoạn 2 và bản giai đoạn 1 cập nhật**; nếu đã sửa Word trực tiếp, lưu bản riêng trước khi xuất lại từ Markdown.

```bash
distrobox enter arch-box -- bash -lc 'cd /home/phuc/PTTKHT/Giai_doan_2/nguon && plantuml -charset UTF-8 -tpng *.puml && plantuml -charset UTF-8 -tsvg *.puml'
distrobox enter arch-box -- python Giai_doan_2/nguon/kiem_tra.py
distrobox enter arch-box -- python Giai_doan_2/nguon/tao_bao_cao.py
```

Công cụ sử dụng: PlantUML, Pandoc, python-docx và LibreOffice đã có trong box. Sau khi sửa nội dung, kiểm tra lại phân trang và mục lục: mục lục được dựng theo các dấu ngắt trang trong nguồn, không tự biết nếu nội dung mới dài hơn một trang.

Đây là hồ sơ phân tích–thiết kế theo đề bài, chưa phải ứng dụng triển khai. Kiểm tra tên phương thức/cú pháp không chứng minh các giao dịch đã được chạy trên cơ sở dữ liệu thực tế.
