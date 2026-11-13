from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR/'static'/'files'

ALLOWED_EXTS = {
    'png', 'jpg', 'gif', 'webp',
    'pdf', 'txt', 'md', 'csv', 'docx', 'xlsx', 'pptx', 'hwp',
    'py', 'js', 'css', 'json',
    'zip'
}
EXT_ALIAS = {'jpeg': 'jpg'}