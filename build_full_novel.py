from pathlib import Path
root = Path(__file__).parent
text = (root / 'manuscript.md').read_text(encoding='utf-8')
insertions = [
    ('## Chapter One', '\n\n# EXPANDED SCENE CYCLE — PART I\n\n' + (root / 'scene_expansions_part_1.md').read_text(encoding='utf-8') + '\n\n'),
    ('## Chapter Five', '\n\n# EXPANDED SCENE CYCLE — PART II\n\n' + (root / 'scene_expansions_part_2.md').read_text(encoding='utf-8') + '\n\n'),
    ('## Chapter Thirteen', '\n\n# EXPANDED SCENE CYCLE — PART III\n\n' + (root / 'scene_expansions_part_3.md').read_text(encoding='utf-8') + '\n\n'),
    ('## Chapter Twenty-One', '\n\n# EXPANDED SCENE CYCLE — PART IV\n\n' + (root / 'scene_expansions_part_4.md').read_text(encoding='utf-8') + '\n\n'),
]
for marker, addition in insertions:
    if marker not in text:
        raise SystemExit(f'Missing marker: {marker}')
    text = text.replace(marker, addition + marker, 1)
old_expansion = (root / 'expanded_insert.md').read_text(encoding='utf-8')
if '# EXPANDED EDITION — THE SOCIETY' not in text:
    text = text.replace('# Epilogue', old_expansion + '\n\n# Epilogue', 1)
(root / 'manuscript_full_novel.md').write_text(text, encoding='utf-8')
print(f'Wrote manuscript_full_novel.md with {len(text.split()):,} words')
