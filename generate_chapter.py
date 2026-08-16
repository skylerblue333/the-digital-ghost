from pathlib import Path
import os
from openai import OpenAI

chapter = os.environ.get('CHAPTER', 'Chapter Nine — The Church of Four Doors')
context = os.environ.get('CONTEXT', '')
out = Path(os.environ.get('OUT', 'generated_chapter.md'))
client = OpenAI()
prompt = f'''Write one original literary thriller chapter for the fictional novel *Loathing in the Woes of Ruthlessness: The Chosen One* by Skyler Blue Spillers.\n\nChapter: {chapter}\n\nContinuity context:\n{context}\n\nUse close third person centered on Skyler, with occasional first-person Truth Protocol entries. Use cinematic but precise sensory detail, meaningful dialogue, moral ambiguity, and original lyrical language. Develop a concrete scene with an objective, interpersonal conflict, a revelation, and a closing decision. The Society, Aegis, the Choir, the Ledger, and the Mirror Room are fictional. Do not provide real hacking instructions, criminal logistics, or claims about real people or governments. Do not imitate any named author. Write approximately 1,800 to 2,200 words and return only the chapter prose with a chapter heading.'''
resp = client.chat.completions.create(model='gpt-5-mini', messages=[{'role':'user','content':prompt}], max_completion_tokens=3200, extra_body={'reasoning': {'effort': 'low'}})
out.write_text(resp.choices[0].message.content, encoding='utf-8')
print(f'Wrote {out} with {len(resp.choices[0].message.content.split()):,} words')
