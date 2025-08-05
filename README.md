# Folder Scanner

This script provides a graphical user interface (GUI) to scan a selected folder, generate a CSV report of its contents, and create a log file. It also offers an option to generate a markdown file with a visual tree of the folder structure.

---

## English Instructions

### How to Use

1.  **Run the script:**
    Execute the `scanfolder.py` file using Python.
    ```bash
    python "scanfolder.py"
    ```

2.  **Select a Folder:**
    Click the "Select Folder" button to choose the directory you want to scan.

3.  **Scan and Generate Report:**
    Click the "Scan and Generate Report" button to start the scanning process.

### Configuration (`config.json`)

You can customize the script's behavior by editing the `config.json` file:

-   `log_file`: The name of the log file (e.g., `"folder_scan.log"`).
-   `max_files_to_scan`: The maximum number of files to include in the CSV report (e.g., `1000`).
-   `generate_tree_limit`: The maximum number of files to include in the `output.md` tree view. If the scanned folder contains fewer files than this limit, `output.md` will be generated (e.g., `100`).
-   `scan_hidden_files`: Set to `true` to include hidden files and folders in the scan, or `false` to exclude them.

### Output Files

-   **CSV Report:** A file named `folder_scan_YYYYMMDD_HHMMSS.csv` containing a list of all scanned files, their sizes, and their full paths.
-   **Log File:** A log file (e.g., `folder_scan.log`) that records all operations and errors.
-   **Map Tree:** An `output.md` file that shows a visual tree of the scanned folder's structure, generated only if the number of files is below the `generate_tree_limit`.

---

## Hướng dẫn tiếng Việt

### Cách sử dụng

1.  **Chạy script:**
    Thực thi tệp `scanfolder.py` bằng Python.
    ```bash
    python "scanfolder.py"
    ```

2.  **Chọn Thư mục:**
    Nhấp vào nút "Select Folder" để chọn thư mục bạn muốn quét.

3.  **Quét và Tạo Báo cáo:**
    Nhấp vào nút "Scan and Generate Report" để bắt đầu quá trình quét.

### Cấu hình (`config.json`)

Bạn có thể tùy chỉnh hoạt động của script bằng cách chỉnh sửa tệp `config.json`:

-   `log_file`: Tên của tệp log (ví dụ: `"folder_scan.log"`).
-   `max_files_to_scan`: Số lượng tệp tối đa để đưa vào báo cáo CSV (ví dụ: `1000`).
-   `generate_tree_limit`: Số lượng tệp tối đa để đưa vào chế độ xem cây trong `output.md`. Nếu thư mục được quét chứa ít tệp hơn giới hạn này, `output.md` sẽ được tạo (ví dụ: `100`).
-   `scan_hidden_files`: Đặt thành `true` để bao gồm các tệp và thư mục ẩn trong quá trình quét, hoặc `false` để loại trừ chúng.

### Tệp đầu ra

-   **Báo cáo CSV:** Một tệp có tên `folder_scan_YYYYMMDD_HHMMSS.csv` chứa danh sách tất cả các tệp đã được quét, kích thước và đường dẫn đầy đủ của chúng.
-   **Tệp Log:** Một tệp log (ví dụ: `folder_scan.log`) ghi lại tất cả các hoạt động và lỗi.

-   **Cây thư mục:** Một tệp `output.md` hiển thị cây trực quan của cấu trúc thư mục đã quét, chỉ được tạo nếu số lượng tệp dưới `generate_tree_limit`.
