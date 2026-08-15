from pathlib import Path
root = Path(__file__).parent
base = root / 'manuscript.md'
insert = root / 'expanded_insert.md'
out = root / 'manuscript_expanded.md'
text = base.read_text(encoding='utf-8')
addition = insert.read_text(encoding='utf-8')
marker = '# Epilogue'
if marker not in text:
    raise SystemExit('Epilogue marker not found')
expanded = text.replace(marker, addition + '\n\n' + marker, 1)
out.write_text(expanded, encoding='utf-8')
# Keep the novel bible expanded copy as the current bible until further revisions.
(root / 'novel_bible_expanded.md').write_text((root / 'novel_bible.md').read_text(encoding='utf-8'), encoding='utf-8')
print(f'Wrote {out} with {len(expanded.split()):,} words')
