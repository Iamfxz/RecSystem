#!/usr/bin/env python
import os
import sys

if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MusicRec.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
# 下列命令自动生成UML图
# python manage.py graph_models -a -o myapp_models.png
# python manage.py graph_models -a -g -o my_project_visualized.png

# 生成依赖版本
# pipreqs ./ --encoding=utf-8

