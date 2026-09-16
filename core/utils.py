from pathlib import Path

import yaml

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'


def read_script(yaml_path):
    return yaml.safe_load(yaml_path.read_text(encoding='utf-8'))


def build_script_entry(yaml_path):
    data = read_script(yaml_path)
    return {
        'name': yaml_path.stem + '.sh',
        'title': data.get('title') or yaml_path.stem,
        'description': data.get('description', ''),
        'args': data.get('args', '')
    }