import os

INPUT_FILE = "static/400vob.tsv"  # đường dẫn đến file gốc
OUTPUT_DIR = "static/lessons"  # thư mục chứa file kết quả
WORDS_PER_LESSON = 35  # số từ mỗi bài

# Đảm bảo thư mục kết quả tồn tại
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(INPUT_FILE, "r", encoding="utf-8") as infile:
    lines = infile.readlines()

header = lines[0]
words = lines[1:]

for i in range(0, len(words), WORDS_PER_LESSON):
    lesson_number = i // WORDS_PER_LESSON + 1
    lesson_lines = words[i : i + WORDS_PER_LESSON]
    with open(
        f"{OUTPUT_DIR}/lesson_{lesson_number}.tsv", "w", encoding="utf-8"
    ) as outfile:
        outfile.write(header)
        outfile.writelines(lesson_lines)

print(f"Đã chia xong thành {((len(words)-1)//WORDS_PER_LESSON)+1} bài.")
