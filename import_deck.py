import os
import genanki

INPUT_DIR = "static/lessons"  # Thư mục chứa các file bài học
OUTPUT_DIR = "static/decks"  # Thư mục xuất file deck .apkg
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Chỉnh lại đúng tên các trường header cho phù hợp với bộ của bạn
fields = [
    "Vocabulary",
    "Part of Speech",
    "Pronunciation",
    "Meaning",
    "Synonym",
    "Antonym",
    "Word Family",
    "Example",
    "Collocation",
]

# Tạo model (kiểu thẻ) cho Anki (nếu muốn đổi style, sửa lại phần html)
model = genanki.Model(
    1607392319,
    "Custom English Vocab Model",
    fields=[{"name": f} for f in fields],
    templates=[
        {
            "name": "English4EveryOne",
            "qfmt": "{{Vocabulary}}",  # mặt trước
            "afmt": """
<div style='font-size:32px;color:#e53c20; font-weight:bold'>{{Vocabulary}}</div>
<div style='margin-top:10px;'><b>{{Part of Speech}}</b> | /{{Pronunciation}}/</div>
<div><b>Meaning:</b> {{Meaning}}</div>
<div><b>Synonym:</b> {{Synonym}} <b style='margin-left:18px'>Antonym:</b> {{Antonym}}</div>
<div><b>Word Family:</b> {{Word Family}}</div>
<div><b>Example:</b> {{Example}}</div>
<div><b>Collocation:</b> {{Collocation}}</div>
""",
        },
    ],
)

for fname in sorted(os.listdir(INPUT_DIR)):
    if not fname.endswith(".tsv"):
        continue

    lesson_path = os.path.join(INPUT_DIR, fname)
    deck_name = os.path.splitext(fname)[0]
    deck = genanki.Deck(
        20000000 + hash(deck_name) % 90000000, deck_name  # unique deck id
    )
    notes = []

    with open(lesson_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    headers = lines[0].strip().split("\t")
    field_idx = [headers.index(f) for f in fields]  # vị trí trường

    for row in lines[1:]:
        cols = row.strip().split("\t")
        # Bổ sung số trường cho khớp, nếu thiếu thì điền chuỗi rỗng
        data = [cols[i] if i < len(cols) else "" for i in field_idx]
        note = genanki.Note(model=model, fields=data)
        deck.add_note(note)

    out_apkg = os.path.join(OUTPUT_DIR, f"{deck_name}.apkg")
    genanki.Package(deck).write_to_file(out_apkg)
    print(f"Đã tạo deck: {out_apkg}")

print("Xong!")
