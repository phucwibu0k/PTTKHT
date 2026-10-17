"""Check this project's PlantUML conventions; no UML execution is implied."""
from pathlib import Path
from collections import Counter
import re
import subprocess

ROOT = Path(__file__).resolve().parent

def definitions(text):
    classes = {}
    current = None
    for line in text.splitlines():
        match = re.match(r'(?:abstract )?class (\w+)', line)
        if match:
            current = match[1]
            assert current not in classes, current
            classes[current] = {}
        method = re.match(r'\s*([+-])\s*(\w+)\(([^)]*)\)', line)
        if method:
            assert current is not None
            params = [x for x in method[3].split(',') if x.strip()]
            classes[current][method[2]] = (len(params), method[1])
    return classes

def validate_sequence(text, classes):
    participants = dict(re.findall(r'participant "[^":]+:(\w+)" as (\w+)', text))
    participants = {alias: cls for cls, alias in participants.items()}
    # shortcut: this project has one instance per class per diagram; use a UML parser if that changes.
    calls, returns, active = Counter(), Counter(), Counter()
    for cls in participants.values():
        assert cls in classes, f'Undeclared lifeline class: {cls}'
    for line in text.splitlines():
        line = line.strip()
        match = re.match(r'(activate|deactivate) (\w+)$', line)
        if match:
            active[match[2]] += 1 if match[1]=='activate' else -1
            assert active[match[2]] >= 0, line
        match = re.match(r'(\w+) (->|-->) (\w+) : (\w+)\(([^)]*)\)', line)
        if not match:
            continue
        src, arrow, dst, method, params = match.groups()
        if arrow == '->':
            cls = participants[dst]
            assert method in classes[cls], f'{cls}.{method} not declared'
            arity, visibility = classes[cls][method]
            assert len([x for x in params.split(',') if x.strip()]) == arity, line
            assert visibility == '+' or src == dst, f'Private operation called externally: {line}'
            calls[src, dst, method] += 1
        else:
            returns[dst, src, method] += 1
    assert calls == returns, f'Unpaired messages: {calls - returns}; {returns - calls}'
    assert all(n == 0 for n in active.values()), active
    return sum(calls.values())

def self_check():
    classes = definitions('class A {\n + run(x: String): void\n}')
    good = 'actor "User" as U\nparticipant "a:A" as A\nU -> A : run(x)\nactivate A\nA --> U : run(): ok\ndeactivate A'
    assert validate_sequence(good, classes) == 1
    try:
        validate_sequence(good.replace('run(x)', 'missing(x)'), classes)
    except AssertionError:
        pass
    else:
        raise AssertionError('The check must reject an undeclared method')

if __name__ == '__main__':
    self_check()
    classes = definitions((ROOT/'mo_hinh_lop.iuml').read_text())
    assert len(classes) == 18, len(classes)
    report = ['PASS: 18 lớp được khai báo một lần.', 'PASS: kiểm tra tự thử phát hiện method không được khai báo.']
    total = 0
    for path in sorted(ROOT.glob('tuan_tu_*.puml')):
        count = validate_sequence(path.read_text(), classes)
        total += count
        report.append(f'PASS: {path.name}: {count} lời gọi, đúng tên/số tham số/quyền truy cập; return tương ứng; activation cân bằng.')
    sources = sorted(ROOT.glob('*.puml'))
    subprocess.run(['plantuml', '-charset', 'UTF-8', '-checkonly', *map(str, sources)], check=True)
    report += [f'PASS: {len(sources)} sơ đồ PlantUML hợp lệ cú pháp.', f'Tổng: {total} lời gọi; 3 tương tác nghiệp vụ, SD02 chia 2 hình.', 'Giới hạn: kiểm tra tĩnh nguồn sơ đồ, chưa chạy phần mềm hoặc kiểm thử giao dịch trên CSDL.']
    (ROOT/'ket_qua_kiem_tra.txt').write_text('\n'.join(report)+'\n')
    print('\n'.join(report))
