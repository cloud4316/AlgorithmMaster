"""
Нормализация названий групп к каноническому списку.
"""
import re

CANONICAL_GROUPS = [
    "2ИСП1-09/25",
    "2ИСП2-09/25",
    "2ИСП3-09/25",
    "2ИСП4-09/25",
    "2РЭУ1-11/25",
    "2ССА1-09/25",
    "2ССА2-09/25",
    "2ССА3-09/25",
    "2ССА4-09/25",
    "3ИСП1-11/24",
    "3ССА1-09/24",
    "3ССА2-09/24",
    "3ССА3-09/24",
]

# Ключ = только буквы+цифры (верхний регистр)
_KEY_TO_CANONICAL = {re.sub(r'[^А-ЯA-Z0-9]', '', g): g for g in CANONICAL_GROUPS}

# Префикс без суффикса (ключ вида "2ИСП1") → каноническая строка, только если уникальный
_PREFIX_TO_CANONICAL: dict[str, str] = {}
for _g in CANONICAL_GROUPS:
    _prefix_key = re.sub(r'[^А-ЯA-Z0-9]', '', _g.split('-')[0])  # напр. "2ИСП1"
    if _prefix_key not in _PREFIX_TO_CANONICAL:
        _PREFIX_TO_CANONICAL[_prefix_key] = _g
    else:
        # Если два канонических имеют одинаковый префикс — убрать запись
        _PREFIX_TO_CANONICAL.pop(_prefix_key, None)


def _clean(s: str) -> str:
    """Нормализовать строку перед сопоставлением."""
    s = s.upper().strip()
    # Убрать пробелы
    s = s.replace(' ', '')
    # _ → -
    s = s.replace('_', '-')
    # Точка перед двузначным числом в конце → /  (2ИСП1-09.25 → 2ИСП1-09/25)
    s = re.sub(r'\.(\d{2})$', r'/\1', s)
    # Убрать задвоенные тире
    s = re.sub(r'-{2,}', '-', s)
    # Полный год: /2025 → /25
    s = re.sub(r'(/)(20)(\d{2})$', r'/\3', s)
    # РЭУ-специфичные правила (существует только РЭУ1)
    # "2РЭУ-11/25" → "2РЭУ1-11/25"  (нет номера группы)
    s = re.sub(r'^(\d)РЭУ-', r'\1РЭУ1-', s)
    # "2РЭУ2-11/25" → "2РЭУ1-11/25"  (неверный номер)
    s = re.sub(r'^(\d)РЭУ[02-9]-', r'\1РЭУ1-', s)
    # "2РЭУ111" → "2РЭУ1-11"  (3 цифры: номер группы + 2 цифры месяца)
    s = re.sub(r'^(\d)РЭУ(\d)(\d{2})$', r'\1РЭУ\2-\3', s)
    # "2РЭУ11" → "2РЭУ1-11"  (2 цифры = месяц, группа 1 подставляется)
    s = re.sub(r'^(\d)РЭУ(\d{2})$', r'\1РЭУ1-\2', s)
    # Два тире вместо тире+слэш: 2ИСП1-09-25 → 2ИСП1-09/25
    s = re.sub(r'^(\d[А-ЯA-Z]+\d+)-(\d{2})-(\d{2})$', r'\1-\2/\3', s)
    # Тире перед буквенным блоком: 2-ИСП4 → 2ИСП4
    s = re.sub(r'^(\d)-([А-ЯA-Z]+\d)', r'\1\2', s)
    # Тире между буквами и одиночной цифрой номера группы: 2ИСП-4 или 2ИСП-4-09/25
    # Не трогать если после цифры идёт ещё цифра (то месяц, а не номер группы)
    s = re.sub(r'^(\d[А-ЯA-Z]+)-(\d)(-|$)', lambda m: m.group(1) + m.group(2) + m.group(3), s)
    return s


def normalize_group(raw: str) -> str:
    """
    Вернуть канонический вариант группы или исходную строку, если совпадения нет.
    """
    if not raw:
        return raw

    cleaned = _clean(raw)

    # 1. Точное совпадение после очистки
    if cleaned in CANONICAL_GROUPS:
        return cleaned

    # 2. Совпадение по полному ключу (все буквы+цифры)
    key = re.sub(r'[^А-ЯA-Z0-9]', '', cleaned)
    if key in _KEY_TO_CANONICAL:
        return _KEY_TO_CANONICAL[key]

    # 3. Совпадение по префиксу (без суффикса -MM/YY), если он уникален
    #    Напр. "2ИСП1" → единственная "2ИСП1-09/25"
    if key in _PREFIX_TO_CANONICAL:
        return _PREFIX_TO_CANONICAL[key]

    # 4. Отрезаем хвост цифр — вдруг студент дописал месяц без разделителя
    #    "2РЭУ111" → пробуем "2РЭУ11", "2РЭУ1" → находим "2РЭУ1" → "2РЭУ1-11/25"
    for cut in range(len(key) - 1, 0, -1):
        prefix = key[:cut]
        if prefix in _PREFIX_TO_CANONICAL:
            return _PREFIX_TO_CANONICAL[prefix]

    # 5. Год "1" как опечатка "2" (все текущие каноничные группы начинаются с 2 или 3)
    if key.startswith('1'):
        alt = '2' + key[1:]
        if alt in _KEY_TO_CANONICAL:
            return _KEY_TO_CANONICAL[alt]
        if alt in _PREFIX_TO_CANONICAL:
            return _PREFIX_TO_CANONICAL[alt]
        for cut in range(len(alt) - 1, 0, -1):
            prefix = alt[:cut]
            if prefix in _PREFIX_TO_CANONICAL:
                return _PREFIX_TO_CANONICAL[prefix]

    # Не распознано — вернуть оригинал без изменений
    return raw
