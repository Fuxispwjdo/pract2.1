#!/usr/bin/env python3
import tomllib
import sys

class ConfigError(Exception):
    pass

def load_config(config_path="config.toml"):
    """Загрузка и валидация конфигурации из TOML файла"""
    try:
        with open(config_path, 'rb') as f:
            config = tomllib.load(f)
    except FileNotFoundError:
        raise ConfigError(f"Конфигурационный файл не найден: {config_path}")
    except tomllib.TOMLDecodeError as e:
        raise ConfigError(f"Ошибка парсинга TOML: {e}")
    
    # Проверка обязательных секций
    required_sections = ['package', 'repository', 'analysis']
    for section in required_sections:
        if section not in config:
            raise ConfigError(f"Отсутствует обязательная секция: {section}")
    
    # Валидация секции package
    pkg = config['package']
    if 'name' not in pkg or not pkg['name']:
        raise ConfigError("Не указано имя пакета")
    if 'version' not in pkg or not pkg['version']:
        raise ConfigError("Не указана версия пакета")
    
    # Валидация секции repository
    repo = config['repository']
    if 'url' not in repo or not repo['url']:
        raise ConfigError("Не указан URL репозитория")
    if 'use_test_repository' not in repo:
        raise ConfigError("Не указан режим тестового репозитория")
    
    # Валидация секции analysis
    analysis = config['analysis']
    if 'max_depth' not in analysis:
        raise ConfigError("Не указана максимальная глубина анализа")
    
    try:
        max_depth = int(analysis['max_depth'])
        if max_depth <= 0:
            raise ConfigError("Максимальная глубина должна быть положительным числом")
    except (ValueError, TypeError):
        raise ConfigError("Максимальная глубина должна быть целым числом")
    
    return {
        'package_name': pkg['name'],
        'package_version': pkg['version'],
        'repository_url': repo['url'],
        'use_test_repository': repo['use_test_repository'],
        'test_repository_path': repo.get('test_repository_path', ''),
        'max_depth': analysis['max_depth']
    }

def main():
    """Основная функция - вывод всех параметров конфигурации"""
    try:
        config = load_config()
        
        print("Конфигурация приложения:")
        print(f"  Имя анализируемого пакета: {config['package_name']}")
        print(f"  Версия пакета: {config['package_version']}")
        print(f"  URL-адрес репозитория: {config['repository_url']}")
        print(f"  Режим работы с тестовым репозиторием: {config['use_test_repository']}")
        print(f"  Путь к файлу тестового репозитория: {config['test_repository_path']}")
        print(f"  Максимальная глубина анализа зависимостей: {config['max_depth']}")
        
    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
