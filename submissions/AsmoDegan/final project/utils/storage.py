from pathlib import Path
from models.donors import BloodBank, Donor

# Xogta waxay ku kaydsantaa folder-ka data/ donors.txt
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "donors.txt"
FILE_HEADER = "donor_id|name|blood_group|age"

def _is_column_header_line(line: str) -> bool:
    return line.strip().lower().replace(" ", "") == FILE_HEADER.lower().replace(" ", "")

def load_bank(path: Path, bank: BloodBank) -> None:
    bank.clear()
    try:
        with open(path, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line or line.startswith("#") or _is_column_header_line(line):
                    continue
                parts = line.split("|", 3)
                if len(parts) != 4:
                    continue
                did, name, bg, age_txt = parts[0].strip(), parts[1].strip(), parts[2].strip(), parts[3].strip()
                try:
                    age = int(age_txt)
                except ValueError:
                    continue
                bank.add(Donor(donor_id=did, name=name, blood_group=bg, age=age))
    except FileNotFoundError:
        pass

def save_bank(path: Path, bank: BloodBank) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# Blood Bank Records\n", f"{FILE_HEADER}\n"]
    for d in bank.all():
        lines.append(f"{d.donor_id}|{d.name}|{d.blood_group}|{d.age}\n")
    with open(path, "w", encoding="utf-8") as f:
        f.writelines(lines)
