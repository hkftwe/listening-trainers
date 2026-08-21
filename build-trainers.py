#!/usr/bin/env python3
"""
build-trainers.py — Generate listening trainer HTML files from shared template + CSV data.

Usage:  python3 build-trainers.py
Output: All trainer HTML files in the current directory, overwriting existing ones.
        The index.html navigation page is also regenerated.
"""

import csv
import os
import json

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
TEMPLATE_PATH = os.path.join(SCRIPT_DIR, "template.html")

# ── Trainer configurations ──────────────────────────────────────────

TRAINERS = {
    "tr-ch": {
        "filename": "tr-ch-listening-trainer.html",
        "title_tag": "/tr/ vs /tʃ/ Listening Trainer",
        "h1": "/tr/ vs /tʃ/ 聽力辨識",
        "subtitle": "Listening Discrimination Trainer",
        "storage_key": "tr-ch-listening-trainer-v2",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "tr", "label": "/tr/", "example": "train, trip, true",
                     "color": "#059669", "bg": "#ecfdf5", "border": "#a7f3d0"},
        "sound_b": {"id": "ch", "label": "/tʃ/", "example": "chain, chip, chew",
                     "color": "#7c3aed", "bg": "#f5f3ff", "border": "#c4b5fd"},
        "stages": [
            {"icon": "🎯", "title": "train vs chain", "desc": "3 組核心詞對<br>train·true·trip"},
            {"icon": "🔀", "title": "8 組混合詞對", "desc": "trees·treat·trace<br>trill·trap …"},
            {"icon": "📻", "title": "完整句子辨識", "desc": "句中找出<br>/tr/ 或 /tʃ/ 音"},
        ],
        "bonus_preview": [
            {"word": "chase", "sound": "ch", "ipa": "/tʃeɪs/"},
            {"word": "trace", "sound": "tr", "ipa": "/treɪs/"},
            {"word": "trees", "sound": "tr", "ipa": "/triːz/"},
            {"word": "cheese", "sound": "ch", "ipa": "/tʃiːz/"},
            {"word": "chill", "sound": "ch", "ipa": "/tʃɪl/"},
            {"word": "trill", "sound": "tr", "ipa": "/trɪl/"},
            {"word": "cheat", "sound": "ch", "ipa": "/tʃiːt/"},
            {"word": "treat", "sound": "tr", "ipa": "/triːt/"},
        ],
        "has_sentences": True,
        "report_title": "/tr/ vs /tʃ/ 聽力練習報告",
        "report_stage_names": {
            1: "train vs chain（核心詞對）",
            2: "8 組混合詞對",
            3: "句子中辨識",
        },
        "error_direction_a_label": "/tr/ → /tʃ/",
        "error_direction_b_label": "/tʃ/ → /tr/",
        "error_direction_note_a": "⚠️ 主方向為 /tr/ → /tʃ/，與產出錯誤方向一致",
        "error_direction_note_b": "⚠️ 主方向為 /tʃ/ → /tr/，與產出方向相反——值得注意",
    },

    "fr-fire": {
        "filename": "fr-fire-listening-trainer.html",
        "title_tag": "/fr/ vs /f/ Listening Trainer",
        "h1": "/fr/ vs /f/ 聽力辨識",
        "subtitle": "Listening Discrimination Trainer — Consonant Cluster",
        "storage_key": "fr-fire-listening-trainer-v2",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "fr", "label": "/fr/", "example": "fry, free, fresh",
                     "color": "#7c3aed", "bg": "#f5f3ff", "border": "#c4b5fd"},
        "sound_b": {"id": "f", "label": "/f/", "example": "fire, fee, flesh",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "stages": [
            {"icon": "🎯", "title": "fry vs fire", "desc": "4 組核心詞對<br>fry·free·fresh·frame"},
            {"icon": "🔀", "title": "7 組混合詞對", "desc": "fright·from·fruit<br>flesh·fame·fight …"},
            {"icon": "📻", "title": "完整句子辨識", "desc": "句中找出<br>/fr/ 或 /f/ 音"},
        ],
        "has_sentences": True,
        "report_title": "/fr/ vs /f/ 聽力練習報告",
        "report_stage_names": {
            1: "fry vs fire（核心詞對）",
            2: "7 組混合詞對",
            3: "句子中辨識",
        },
        "error_direction_a_label": "/fr/ → /f/",
        "error_direction_b_label": "/f/ → /fr/",
        "error_direction_note_a": "⚠️ 主方向為 /fr/ → /f/，輔音叢集被簡化",
        "error_direction_note_b": "⚠️ 主方向為 /f/ → /fr/，與產出方向相反——值得注意",
    },

    "n-l": {
        "filename": "nl-listening-trainer.html",
        "title_tag": "/n/ vs /l/ Listening Trainer",
        "h1": "/n/ vs /l/ 聽力辨識",
        "subtitle": "Listening Discrimination Trainer — Nasal vs Lateral",
        "storage_key": "nl-listening-trainer-v3",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "n", "label": "/n/", "example": "need, knife, no",
                     "color": "#0891b2", "bg": "#ecfeff", "border": "#a5f3fc"},
        "sound_b": {"id": "l", "label": "/l/", "example": "lead, life, low",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "stages": [
            {"icon": "🎯", "title": "need vs lead", "desc": "4 組核心詞對<br>need·knife·no·night"},
            {"icon": "🔀", "title": "8 組混合詞對", "desc": "nap·name·net<br>nine·nose·knot …"},
            {"icon": "📻", "title": "完整句子辨識", "desc": "句中找出<br>/n/ 或 /l/ 音"},
        ],
        "bonus_preview": [
            {"word": "knot", "sound": "n", "ipa": "/nɒt/"},
            {"word": "lot",  "sound": "l", "ipa": "/lɒt/"},
            {"word": "snow", "sound": "n", "ipa": "/snoʊ/"},
            {"word": "slow", "sound": "l", "ipa": "/sloʊ/"},
        ],
        "has_sentences": True,
        "report_title": "/n/ vs /l/ 聽力練習報告",
        "report_stage_names": {
            1: "need vs lead（核心詞對）",
            2: "8 組混合詞對",
            3: "句子中辨識",
        },
        "error_direction_a_label": "/n/ → /l/",
        "error_direction_b_label": "/l/ → /n/",
        "error_direction_note_a": "⚠️ 主方向為 /n/ → /l/，鼻音被誤聽為舌側音",
        "error_direction_note_b": "⚠️ 主方向為 /l/ → /n/，舌側音被誤聽為鼻音",
    },

    "n-l-complex": {
        "filename": "nl-listening-trainer-complex.html",
        "title_tag": "/n/ vs /l/ 複雜環境聽力訓練",
        "h1": "/n/ vs /l/ 複雜環境聽力辨識",
        "subtitle": "Listening Discrimination Trainer — Complex Environment (Multi-syllable)",
        "storage_key": "nl-complex-listening-trainer-v1",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "n", "label": "/n/", "example": "needing, nightly, nearly",
                     "color": "#0891b2", "bg": "#ecfeff", "border": "#a5f3fc"},
        "sound_b": {"id": "l", "label": "/l/", "example": "leading, lightly, really",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "stages": [
            {"icon": "🎯", "title": "needing vs leading", "desc": "2 組核心詞對<br>needing·nightly<br>（多音節複雜環境）"},
            {"icon": "🔀", "title": "6 組混合詞對", "desc": "nearly·nothing·nervous<br>really·learning·lighter …"},
            {"icon": "📻", "title": "完整句子辨識", "desc": "句中找出<br>/n/ 或 /l/ 音<br>含 medial /l/ 詞"},
        ],
        "bonus_preview": [
            {"word": "narrow", "sound": "n", "ipa": "/ˈnær.oʊ/"},
            {"word": "living", "sound": "l", "ipa": "/ˈlɪ.vɪŋ/"},
            {"word": "lonely", "sound": "l", "ipa": "/ˈloʊn.li/"},
            {"word": "lovely", "sound": "l", "ipa": "/ˈlʌv.li/"},
        ],
        "has_sentences": True,
        "report_title": "/n/ vs /l/ 複雜環境聽力練習報告",
        "report_stage_names": {
            1: "needing vs leading（核心詞對）",
            2: "6 組混合詞對",
            3: "句子中辨識（含 medial /l/）",
        },
        "error_direction_a_label": "/n/ → /l/",
        "error_direction_b_label": "/l/ → /n/",
        "error_direction_note_a": "⚠️ 主方向為 /n/ → /l/，鼻音被誤聽為舌側音",
        "error_direction_note_b": "⚠️ 主方向為 /l/ → /n/，舌側音被誤聽為鼻音",
    },

    "n-l-core": {
        "filename": "nl-listening-trainer-core.html",
        "title_tag": "/n/ vs /l/ 核心聽力訓練",
        "h1": "/n/ vs /l/ 核心聽力辨識",
        "subtitle": "Listening Discrimination Trainer — Core Pairs Only",
        "storage_key": "nl-core-listening-trainer-v2",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "n", "label": "/n/", "example": "need, night, no",
                     "color": "#0891b2", "bg": "#ecfeff", "border": "#a5f3fc"},
        "sound_b": {"id": "l", "label": "/l/", "example": "lead, light, low",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "stages": [
            {"icon": "🎯", "title": "need vs lead", "desc": "4 組核心詞對<br>need·night·no·nap"},
        ],
        "bonus_preview": [
            {"word": "knot", "sound": "n", "ipa": "/nɒt/"},
            {"word": "lot",  "sound": "l", "ipa": "/lɒt/"},
            {"word": "snow", "sound": "n", "ipa": "/snoʊ/"},
            {"word": "slow", "sound": "l", "ipa": "/sloʊ/"},
        ],
        "has_sentences": False,
        "report_title": "/n/ vs /l/ 核心聽力練習報告",
        "report_stage_names": {
            1: "need vs lead（核心詞對）",
        },
        "error_direction_a_label": "/n/ → /l/",
        "error_direction_b_label": "/l/ → /n/",
        "error_direction_note_a": "⚠️ 主方向為 /n/ → /l/",
        "error_direction_note_b": "⚠️ 主方向為 /l/ → /n/",
    },

    "f-th": {
        "filename": "f-th-listening-trainer.html",
        "title_tag": "/f/ vs /θ/ Listening Trainer",
        "h1": "/f/ vs /θ/ 聽力辨識",
        "subtitle": "Listening Discrimination Trainer",
        "storage_key": "f-th-listening-trainer-v3",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "f", "label": "/f/", "example": "first, free, fin",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "sound_b": {"id": "th", "label": "/θ/", "example": "third, three, thin",
                     "color": "#0891b2", "bg": "#ecfeff", "border": "#a5f3fc"},
        "stages": [
            {"icon": "🎯", "title": "first vs third", "desc": "3 組核心詞對<br>first·free·fin"},
            {"icon": "🔀", "title": "6 組混合詞對", "desc": "fought·four<br>thought·thaw …"},
            {"icon": "📻", "title": "完整句子辨識", "desc": "句中找出<br>/f/ 或 /θ/ 音"},
        ],
        "has_sentences": True,
        "report_title": "/f/ vs /θ/ 聽力練習報告",
        "report_stage_names": {
            1: "first vs third（核心詞對）",
            2: "6 組混合詞對",
            3: "句子中辨識",
        },
        "error_direction_a_label": "/f/ → /θ/",
        "error_direction_b_label": "/θ/ → /f/",
        "error_direction_note_a": "⚠️ 主方向為 /f/ → /θ/",
        "error_direction_note_b": "⚠️ 主方向為 /θ/ → /f/",
    },

    "f-th-focused": {
        "filename": "f-th-listening-trainer-focused.html",
        "title_tag": "/f/ vs /θ/ 聚焦聽力訓練（fin/thin、free/three、first/thirst）",
        "h1": "/f/ vs /θ/ 純聽音辨識",
        "subtitle": "Focused Listening — Audio-Only, No Word Display",
        "storage_key": "f-th-focused-trainer-v1",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "single",
        "sound_a": {"id": "f", "label": "/f/", "example": "fin, free, first",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "sound_b": {"id": "th", "label": "/θ/", "example": "thin, three, thirst",
                     "color": "#0891b2", "bg": "#ecfeff", "border": "#a5f3fc"},
        "stages": [
            {"icon": "🎯", "title": "純音辨識", "desc": "3 組核心詞對<br>fin·free·first"},
            {"icon": "🔀", "title": "純音辨識", "desc": "3 組核心詞對<br>重複練習"},
        ],
        "has_sentences": False,
        "report_title": "/f/ vs /θ/ 聚焦聽力練習報告",
        "report_stage_names": {
            1: "純音辨識（第一輪）",
            2: "純音辨識（第二輪）",
        },
        "error_direction_a_label": "/f/ → /θ/",
        "error_direction_b_label": "/θ/ → /f/",
        "error_direction_note_a": "⚠️ 主方向為 /f/ → /θ/",
        "error_direction_note_b": "⚠️ 主方向為 /θ/ → /f/",
    },

    "f-th-simple": {
        "filename": "f-th-listening-trainer-simple.html",
        "title_tag": "/f/ vs /θ/ 聽力訓練",
        "h1": "/f/ vs /θ/ 聽力辨識",
        "subtitle": "Listening Discrimination Trainer",
        "storage_key": "f-th-simple-trainer-v4",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "single",
        "sound_a": {"id": "f", "label": "/f/", "example": "first, free, fin",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "sound_b": {"id": "th", "label": "/θ/", "example": "third, three, thin",
                     "color": "#0891b2", "bg": "#ecfeff", "border": "#a5f3fc"},
        "stages": [
            {"icon": "🎯", "title": "first vs third", "desc": "4 組核心詞對<br>first·free·fin·fought"},
            {"icon": "🔀", "title": "6 組混合詞對", "desc": "four·Fred<br>thaw·thread …"},
        ],
        "has_sentences": False,
        "report_title": "/f/ vs /θ/ 聽力練習報告",
        "report_stage_names": {
            1: "first vs third（核心詞對）",
            2: "6 組混合詞對",
        },
        "error_direction_a_label": "/f/ → /θ/",
        "error_direction_b_label": "/θ/ → /f/",
        "error_direction_note_a": "⚠️ 主方向為 /f/ → /θ/",
        "error_direction_note_b": "⚠️ 主方向為 /θ/ → /f/",
    },

    "thr-tr": {
        "filename": "thr-tr-listening-trainer.html",
        "title_tag": "/θr/ vs /tr/ Listening Trainer",
        "h1": "/θr/ vs /tr/ 聽力辨識",
        "subtitle": "Listening Discrimination Trainer — /θ/ in Cluster",
        "storage_key": "thr-tr-listening-trainer-v1",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "thr", "label": "/θr/", "example": "three, through, thrill",
                     "color": "#0891b2", "bg": "#ecfeff", "border": "#a5f3fc"},
        "sound_b": {"id": "tr", "label": "/tr/", "example": "tree, true, trill",
                     "color": "#7c3aed", "bg": "#f5f3ff", "border": "#c4b5fd"},
        "stages": [
            {"icon": "🎯", "title": "three vs tree", "desc": "3 組核心詞對<br>three·through·thrill"},
            {"icon": "🔀", "title": "4 組混合詞對", "desc": "thread·tread<br>加入擴充詞"},
            {"icon": "📻", "title": "完整句子辨識", "desc": "句中找出<br>/θr/ 或 /tr/ 音"},
        ],
        "has_sentences": True,
        "report_title": "/θr/ vs /tr/ 聽力練習報告",
        "report_stage_names": {
            1: "three vs tree（核心詞對）",
            2: "4 組混合詞對",
            3: "句子中辨識",
        },
        "error_direction_a_label": "/θr/ → /tr/",
        "error_direction_b_label": "/tr/ → /θr/",
        "error_direction_note_a": "⚠️ 主方向為 /θr/ → /tr/，/θ/ 在叢集中被聽成 /t/",
        "error_direction_note_b": "⚠️ 主方向為 /tr/ → /θr/，與產出方向相反——值得注意",
    },

    "u-oo": {
        "filename": "u-oo-listening-trainer.html",
        "title_tag": "/ʊ/ vs /uː/ Listening Trainer",
        "h1": "/ʊ/ vs /uː/ 聽力辨識",
        "subtitle": "Listening Discrimination Trainer (full vs fool)",
        "storage_key": "u-oo-listening-trainer-v1",
        "accent_color": "#2563eb",
        "accent_hover": "#1d4ed8",
        "voice_mode": "pool",
        "sound_a": {"id": "u", "label": "/ʊ/", "example": "full, pull, could",
                     "hint": "嘴唇放鬆、短促（彈出來）",
                     "color": "#d97706", "bg": "#fffbeb", "border": "#fcd34d"},
        "sound_b": {"id": "oo", "label": "/uː/", "example": "fool, pool, cooed",
                     "hint": "嘴唇收攏、用力（說出來）",
                     "color": "#7c3aed", "bg": "#f5f3ff", "border": "#c4b5fd"},
        "stages": [
            {"icon": "🎯", "title": "full vs fool", "desc": "3 組核心詞對<br>full·pull·could"},
            {"icon": "🔀", "title": "4 組混合詞對", "desc": "look·wood·stood<br>nook …"},
            {"icon": "📻", "title": "完整句子辨識", "desc": "句中找出<br>/ʊ/ 或 /uː/ 音"},
        ],
        "has_sentences": True,
        "report_title": "/ʊ/ vs /uː/ 聽力練習報告",
        "report_stage_names": {
            1: "full vs fool（核心詞對）",
            2: "4 組混合詞對",
            3: "句子中辨識",
        },
        "error_direction_a_label": "/ʊ/ → /uː/",
        "error_direction_b_label": "/uː/ → /ʊ/",
        "error_direction_note_a": "⚠️ 主方向為 /ʊ/ → /uː/",
        "error_direction_note_b": "⚠️ 主方向為 /uː/ → /ʊ/",
    },
}


# ── CSV loading ─────────────────────────────────────────────────────

def load_csv(trainer_id):
    """Load word bank CSV, return {stage: [items]} and bonus_preview list."""
    path = os.path.join(DATA_DIR, f"{trainer_id}.csv")
    banks = {}
    for row in _read_csv(path):
        stage = int(row["stage"])
        if stage not in banks:
            banks[stage] = []
        ttype = _detect_type(row)
        if ttype == "sentence":
            banks[stage].append({
                "sentence": row["text"],
                "sound": row["sound"],
                "word": row.get("target", ""),
            })
        else:
            banks[stage].append({
                "word": row["text"],
                "sound": row["sound"],
                "ipa": row["ipa"],
            })
    return banks


def _read_csv(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append(r)
    return rows


def _detect_type(row):
    """Return 'sentence' if row has a non-empty target field, else 'word'."""
    return "sentence" if row.get("target", "").strip() else "word"


# ── JS code generation ──────────────────────────────────────────────

def js_word_banks(config, banks):
    """Generate WORD_BANKS JS object from CSV data."""
    lines = ["const WORD_BANKS = {"]
    for stage_num in sorted(banks.keys()):
        items = banks[stage_num]
        lines.append(f"  {stage_num}: [")
        for item in items:
            if "sentence" in item:
                lines.append(
                    f"    {{ sentence: {json.dumps(item['sentence'])}, "
                    f"sound: '{item['sound']}', word: {json.dumps(item['word'])} }},"
                )
            else:
                lines.append(
                    f"    {{ word: {json.dumps(item['word'])}, "
                    f"sound: '{item['sound']}', ipa: {json.dumps(item['ipa'])} }},"
                )
        lines.append("  ],")
    lines.append("};")
    return "\n".join(lines)


def js_contrast_map(config, banks):
    """Generate CONTRAST_MAP or CONTRAST_PAIRS JS."""
    # For standard trainers with adjacent-pair structure
    lines = []
    lines.append("const CONTRAST_MAP = {};")
    lines.append("(function buildContrastMap() {")
    lines.append("  for (const stageData of Object.values(WORD_BANKS)) {")
    lines.append("    for (let i = 0; i < stageData.length - 1; i += 2) {")
    lines.append("      const a = stageData[i], b = stageData[i + 1];")
    lines.append("      if (a.sound === b.sound) continue;")
    lines.append(
        "      CONTRAST_MAP[a.word || a.sentence] = "
        "{ word: b.word || b.sentence, ipa: b.ipa || '', sentence: b.sentence || '' };"
    )
    lines.append(
        "      CONTRAST_MAP[b.word || b.sentence] = "
        "{ word: a.word || a.sentence, ipa: a.ipa || '', sentence: a.sentence || '' };"
    )
    lines.append("    }")
    lines.append("  }")
    lines.append("})();")
    return "\n".join(lines)


def js_bonus_preview(config):
    """Generate BONUS_PREVIEW JS array."""
    bonus = config.get("bonus_preview", [])
    if not bonus:
        return "const BONUS_PREVIEW = [];"
    lines = ["const BONUS_PREVIEW = ["]
    for item in bonus:
        lines.append(
            f"    {{ word: {json.dumps(item['word'])}, "
            f"sound: '{item['sound']}', ipa: {json.dumps(item['ipa'])} }},"
        )
    lines.append("  ];")
    return "\n".join(lines)


# ── HTML generation ─────────────────────────────────────────────────

def css_sound_vars(config):
    """Generate CSS custom properties for the two sounds."""
    sa = config["sound_a"]
    sb = config["sound_b"]
    return (
        f"--sa-color: {sa['color']}; --sa-bg: {sa['bg']}; --sa-border: {sa['border']};\n"
        f"      --sb-color: {sb['color']}; --sb-bg: {sb['bg']}; --sb-border: {sb['border']};"
    )


def css_answer_buttons(config):
    """Generate answer button CSS classes."""
    sa_id = config["sound_a"]["id"]
    sb_id = config["sound_b"]["id"]
    sa_color = config["sound_a"]["color"]
    sb_color = config["sound_b"]["color"]
    return f"""  .answer-btn.{sa_id}-btn {{ border-color: var(--sa-border); background: var(--sa-bg); }}
  .answer-btn.{sa_id}-btn:hover:not(:disabled) {{ border-color: {sa_color}; }}
  .answer-btn.{sb_id}-btn {{ border-color: var(--sb-border); background: var(--sb-bg); }}
  .answer-btn.{sb_id}-btn:hover:not(:disabled) {{ border-color: {sb_color}; }}"""


def html_stage_cards(config):
    """Generate stage selector cards HTML."""
    stages = config["stages"]
    cards = []
    for i, st in enumerate(stages):
        num = i + 1
        active = " active" if num == 1 else " locked"
        lock_html = ""
        if num > 1:
            prev = num - 1
            lock_html = (
                f'\n      <div class="stage-lock">'
                f'🔒 第{prev}關 80% 解鎖<br>'
                f'<span style="font-size:0.6rem;opacity:0.7">Shift+點擊／長按 強制解鎖</span></div>'
            )
        cards.append(
            f'    <button class="stage-card{active}" data-stage="{num}">\n'
            f'      <div class="stage-icon">{st["icon"]}</div>\n'
            f'      <div class="stage-title">{st["title"]}</div>\n'
            f'      <div class="stage-desc">{st["desc"]}</div>{lock_html}\n'
            f"    </button>"
        )
    return "\n".join(cards)


def html_answer_buttons(config):
    """Generate answer buttons HTML."""
    sa = config["sound_a"]
    sb = config["sound_b"]
    hint_a = f'\n        <span class="sound-hint">{sa["hint"]}</span>' if sa.get("hint") else ""
    hint_b = f'\n        <span class="sound-hint">{sb["hint"]}</span>' if sb.get("hint") else ""
    return (
        f'      <button class="answer-btn {sa["id"]}-btn" id="aBtn" disabled>\n'
        f'        <span class="sound-label">{sa["label"]} 音</span>\n'
        f'        <span class="sound-example">像 {sa["example"]}</span>'
        f'{hint_a}\n'
        f"      </button>\n"
        f'      <button class="answer-btn {sb["id"]}-btn" id="bBtn" disabled>\n'
        f'        <span class="sound-label">{sb["label"]} 音</span>\n'
        f'        <span class="sound-example">像 {sb["example"]}</span>'
        f'{hint_b}\n'
        f"      </button>"
    )


def html_voice_ui(config):
    """Generate voice UI HTML block — bar for single mode, footer for pool mode."""
    mode = config["voice_mode"]
    if mode == "single":
        return (
            '  <div class="voice-bar">\n'
            '    🎤 語音：<span class="voice-name" id="currentVoiceName">載入中...</span>\n'
            '    <button class="voice-reroll-btn" id="voiceRerollBtn">🔄 換聲</button>\n'
            '  </div>'
        )
    else:
        return '  <div class="voice-info" id="voiceInfo">載入語音引擎中...</div>'


def html_voice_info(config):
    """Deprecated — use html_voice_ui instead."""
    return ""


def html_voice_bar(config):
    """Deprecated — use html_voice_ui instead."""
    return ""


# ── JS section generators ───────────────────────────────────────────

def js_dom_refs(config):
    """Generate DOM refs section."""
    sa_id = config["sound_a"]["id"]
    sb_id = config["sound_b"]["id"]
    voice_mode = config["voice_mode"]

    refs = []
    refs.append(f"const aBtn = $('aBtn');")
    refs.append(f"const bBtn = $('bBtn');")

    if voice_mode == "pool":
        refs.append("const voiceInfo = $('voiceInfo');")
    else:
        refs.append("const currentVoiceName = $('currentVoiceName');")
        refs.append("const voiceRerollBtn = $('voiceRerollBtn');")

    return "\n".join(refs)


def js_voice_management(config):
    """Generate voice management JS."""
    mode = config["voice_mode"]
    if mode == "pool":
        return _voice_js_pool()
    else:
        return _voice_js_single()


def js_voice_event_listeners(config):
    """Generate voice-specific event listeners."""
    if config["voice_mode"] == "single":
        return (
            "voiceRerollBtn.addEventListener('click', () => { pickRandomVoice(); });"
        )
    else:
        return ""


def _voice_js_pool():
    return """function buildVoicePool() {
  const all = speechSynthesis.getVoices();
  if (all.length === 0) return;
  const english = all.filter(v => v.lang.startsWith('en'));
  const preferred = [];
  const names = new Set();
  for (const v of english) {
    if (v.name === 'Samantha' && !names.has('Samantha')) { preferred.push(v); names.add('Samantha'); }
    if (v.name === 'Daniel' && !names.has('Daniel')) { preferred.push(v); names.add('Daniel'); }
    if (v.name === 'Karen' && !names.has('Karen')) { preferred.push(v); names.add('Karen'); }
    if (v.name === 'Alex' && !names.has('Alex')) { preferred.push(v); names.add('Alex'); }
    if (v.name === 'Moira' && !names.has('Moira')) { preferred.push(v); names.add('Moira'); }
    if (v.name === 'Fiona' && !names.has('Fiona')) { preferred.push(v); names.add('Fiona'); }
    if (v.name === 'Veena' && !names.has('Veena')) { preferred.push(v); names.add('Veena'); }
    if (v.name === 'Tom' && !names.has('Tom')) { preferred.push(v); names.add('Tom'); }
  }
  for (const v of english) {
    if (preferred.length >= 5) break;
    if (!names.has(v.name)) { preferred.push(v); names.add(v.name); }
  }
  if (preferred.length < 3) {
    for (const v of all) {
      if (preferred.length >= 3) break;
      if (!names.has(v.name)) { preferred.push(v); names.add(v.name); }
    }
  }
  state.voicePool = preferred;
  updateVoiceLabel();
}

function pickVoice() {
  if (state.voicePool.length === 0) return null;
  const idx = Math.floor(Math.random() * state.voicePool.length);
  return state.voicePool[idx];
}

function pickVoiceDifferentFromLast() {
  if (state.voicePool.length === 0) return null;
  if (state.voicePool.length === 1) return state.voicePool[0];
  const candidates = state.voicePool.filter(v => v !== state.lastReviewVoice);
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  state.lastReviewVoice = chosen;
  return chosen;
}

function updateVoiceLabel() {
  if (state.voicePool.length === 0) {
    voiceInfo.innerHTML = '語音引擎載入中...';
    return;
  }
  const names = state.voicePool.map(v => `<span class="voice-name">${v.name}</span>`).join(' · ');
  voiceInfo.innerHTML = `語音：${names}<br><span style="font-size:0.65rem;opacity:0.7">每題隨機輪換</span>`;
}

speechSynthesis.onvoiceschanged = () => { buildVoicePool(); };
buildVoicePool();

function speak(text, voice) {
  return new Promise((resolve) => {
    speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);
    const v = voice || pickVoice();
    if (v) utt.voice = v;
    utt.rate = 0.85;
    utt.pitch = 1;
    utt.onend = resolve;
    utt.onerror = resolve;
    speechSynthesis.speak(utt);
  });
}"""


def _voice_js_single():
    return """function buildVoicePool() {
  const all = speechSynthesis.getVoices();
  if (all.length === 0) return;
  const english = all.filter(v => v.lang.startsWith('en'));
  const pool = [];
  const names = new Set();
  const allowed = ['Karen', 'Daniel', 'Moira', 'Samantha', 'Rocko'];
  for (const name of allowed) {
    const match = english.find(v => v.name === name);
    if (match && !names.has(match.name)) { pool.push(match); names.add(match.name); }
  }
  state.voicePool = pool;
  if (!state.currentVoice && pool.length > 0) {
    state.currentVoice = pool[Math.floor(Math.random() * pool.length)];
    updateVoiceLabel();
  }
}

function pickRandomVoice() {
  if (state.voicePool.length === 0) return;
  const candidates = state.voicePool.filter(v => v !== state.currentVoice);
  if (candidates.length > 0) {
    state.currentVoice = candidates[Math.floor(Math.random() * candidates.length)];
  } else {
    state.currentVoice = state.voicePool[Math.floor(Math.random() * state.voicePool.length)];
  }
  updateVoiceLabel();
}

function pickVoiceDifferentFromLast() {
  if (state.voicePool.length === 0) return null;
  if (state.voicePool.length === 1) return state.voicePool[0];
  const candidates = state.voicePool.filter(v => v !== state.lastReviewVoice);
  const chosen = candidates[Math.floor(Math.random() * candidates.length)];
  state.lastReviewVoice = chosen;
  return chosen;
}

function updateVoiceLabel() {
  currentVoiceName.textContent = state.currentVoice ? state.currentVoice.name : '系統預設';
}

speechSynthesis.onvoiceschanged = () => { buildVoicePool(); };
buildVoicePool();

function speak(text, voice) {
  return new Promise((resolve) => {
    speechSynthesis.cancel();
    const utt = new SpeechSynthesisUtterance(text);
    const v = voice || state.currentVoice;
    if (v) utt.voice = v;
    utt.rate = 0.85;
    utt.pitch = 1;
    utt.onend = resolve;
    utt.onerror = resolve;
    speechSynthesis.speak(utt);
  });
}"""


def js_state(config):
    """Generate state object."""
    mode = config["voice_mode"]
    if mode == "pool":
        return """let state = {
  stage: 1,
  unlockedStages: [1],
  roundWords: [],
  currentIndex: 0,
  currentItem: null,
  hasPlayed: false,
  currentSelection: null,
  roundAnswers: [],
  roundRevealed: false,
  voicePool: [],
  previewMode: false,
  previewWords: [],
  previewIndex: 0,
  lastReviewVoice: null,
};"""
    else:
        return """let state = {
  stage: 1,
  unlockedStages: [1],
  voicePool: [],
  currentVoice: null,
  roundWords: [],
  currentIndex: 0,
  currentItem: null,
  hasPlayed: false,
  currentSelection: null,
  roundAnswers: [],
  roundRevealed: false,
  previewMode: false,
  previewWords: [],
  previewIndex: 0,
  lastReviewVoice: null,
};"""


# ── Full HTML assembly ──────────────────────────────────────────────

def build_html(config, banks):
    """Generate complete HTML from config + word banks."""
    # Read template
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        template = f.read()

    sa = config["sound_a"]
    sb = config["sound_b"]
    num_stages = len(config["stages"])
    has_sentences = config.get("has_sentences", False)

    # Build the JS that replaces inline in the template
    word_banks_js = js_word_banks(config, banks)
    contrast_map_js = js_contrast_map(config, banks)
    bonus_preview_js = js_bonus_preview(config)

    replacements = {
        "{{TITLE_TAG}}": config["title_tag"],
        "{{H1}}": config["h1"],
        "{{SUBTITLE}}": config["subtitle"],
        "{{STORAGE_KEY}}": config["storage_key"],
        "{{ACCENT_COLOR}}": config["accent_color"],
        "{{ACCENT_HOVER}}": config["accent_hover"],
        "{{CSS_SOUND_VARS}}": css_sound_vars(config),
        "{{CSS_ANSWER_BUTTONS}}": css_answer_buttons(config),
        "{{STAGE_CARDS}}": html_stage_cards(config),
        "{{ANSWER_BUTTONS}}": html_answer_buttons(config),
        "{{VOICE_UI}}": html_voice_ui(config),
        "{{SOUND_A_ID}}": sa["id"],
        "{{SOUND_B_ID}}": sb["id"],
        "{{SOUND_A_LABEL}}": sa["label"],
        "{{SOUND_B_LABEL}}": sb["label"],
        "{{SOUND_A_EXAMPLE}}": sa["example"],
        "{{SOUND_B_EXAMPLE}}": sb["example"],
        "{{WORD_BANKS}}": word_banks_js,
        "{{CONTRAST_MAP}}": contrast_map_js,
        "{{BONUS_PREVIEW}}": bonus_preview_js,
        "{{VOICE_MODE}}": config["voice_mode"],
        "{{NUM_STAGES}}": str(num_stages),
        "{{HAS_SENTENCES}}": "true" if has_sentences else "false",
        "{{HAS_STAGE3}}": "true" if num_stages >= 3 else "false",
        "{{VOICE_DOM_REFS}}": js_dom_refs(config),
        "{{VOICE_JS}}": js_voice_management(config),
        "{{STATE_OBJ}}": js_state(config),
        "{{VOICE_EVENT_LISTENERS}}": js_voice_event_listeners(config),
        "{{REPORT_TITLE}}": config["report_title"],
        "{{REPORT_STAGE_NAMES}}": json.dumps(config["report_stage_names"]),
        "{{ERROR_A_LABEL}}": config.get("error_direction_a_label", ""),
        "{{ERROR_B_LABEL}}": config.get("error_direction_b_label", ""),
        "{{ERROR_NOTE_A}}": config.get("error_direction_note_a", ""),
        "{{ERROR_NOTE_B}}": config.get("error_direction_note_b", ""),
    }

    html = template
    for key, value in replacements.items():
        html = html.replace(key, value)

    return html


# ── Index page ──────────────────────────────────────────────────────

def build_index(trainers):
    """Generate index.html navigation page."""
    links = []
    for tid, cfg in trainers.items():
        links.append(
            f'<a href="dist/{cfg["filename"]}">{cfg["h1"]}</a>'
        )
    links_html = "\n".join(links)
    return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Listening Trainers</title><style>:root{{color-scheme:light}}body{{font-family:-apple-system,system-ui,sans-serif;max-width:540px;margin:40px auto;padding:0 20px;line-height:1.8}}h1{{font-size:1.3rem}}a{{display:block;padding:10px 14px;margin:6px 0;border:1px solid #e5e7eb;border-radius:8px;text-decoration:none;color:#1a1a2e;font-weight:500}}a:hover{{background:#f3f4f6}}</style></head><body><h1>Listening Trainers</h1>{links_html}</body></html>"""


# ── Main ────────────────────────────────────────────────────────────

def main():
    os.chdir(SCRIPT_DIR)
    dist_dir = os.path.join(SCRIPT_DIR, "dist")
    os.makedirs(dist_dir, exist_ok=True)

    for trainer_id, config in TRAINERS.items():
        print(f"Building {trainer_id}...")
        banks = load_csv(trainer_id)
        html = build_html(config, banks)
        outpath = os.path.join(dist_dir, config["filename"])
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  → {config['filename']} ({len(html)} bytes)")

    # Copy hand-maintained trainers into dist/
    import shutil
    manual_trainers = {
        "v-f": "v-f-listening-trainer.html",
        "vowel-assessment": "vowel-minimal-pairs-assessment.html",
        "nl-training": "nl-listening-trainer-training.html",
    }
    for key, fname in manual_trainers.items():
        src = os.path.join(SCRIPT_DIR, "manual", fname)
        dst = os.path.join(dist_dir, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)
            print(f"Copied {fname} → dist/")

    # Build index (includes all generated trainers + manual trainers)
    all_trainers = dict(TRAINERS)
    all_trainers["n-l-regression"] = {
        "filename": "nl-listening-trainer-regression.html",
        "h1": "/n/ vs /l/ 漸進式聽力訓練（退階設計）",
    }
    all_trainers["nl-training"] = {
        "filename": "nl-listening-trainer-training.html",
        "h1": "/n/ vs /l/ 聽力訓練（訓練模式）",
    }
    all_trainers["v-f"] = {
        "filename": "v-f-listening-trainer.html",
        "h1": "/v/ vs /f/ 聽力辨識 + every 聽覺重建",
    }
    all_trainers["vowel-assessment"] = {
        "filename": "vowel-minimal-pairs-assessment.html",
        "h1": "母音 Minimal Pair 聽辨評估（第 0 天評估）",
    }
    index_html = build_index(all_trainers)
    with open(os.path.join(SCRIPT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Built index.html")


if __name__ == "__main__":
    main()
