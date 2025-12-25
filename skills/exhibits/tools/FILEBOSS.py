#!/usr/bin/env python3
import os, sys, hashlib, shutil, json
input_dir = sys.argv[1] if len(sys.argv)>1 else 'evidence'
output_dir = sys.argv[2] if len(sys.argv)>2 else 'exhibits/processed'
os.makedirs(output_dir, exist_ok=True)
exhibits = []
for i, f in enumerate(os.listdir(input_dir)):
    if os.path.isfile(f'{input_dir}/{f}'):
        h = hashlib.sha256(open(f'{input_dir}/{f}','rb').read()).hexdigest()
        new_name = f'EXH-{i+1:04d}-{f}'
        shutil.copy2(f'{input_dir}/{f}', f'{output_dir}/{new_name}')
        exhibits.append({'bates': new_name, 'hash': h})
print(f'✅ FILEBOSS: {len(exhibits)} exhibits')
with open(f'{output_dir}/EXHIBIT_INVENTORY.json', 'w') as f:
    json.dump({'exhibits': exhibits}, f, indent=2)
