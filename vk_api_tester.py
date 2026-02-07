#!/usr/bin/env python3
"""
VK API Tester - Утилита для тестирования VK API и проверки настроек
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, Optional


class VKAPITester:
    """Класс для тестирования VK API"""
    
    def __init__(self, access_token: str, api_version: str = "5.131"):
        self.access_token = access_token
        self.api_version = api_version
        self.base_url = "https://api.vk.com/method/"
    
    def _make_request(self, method: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Выполняет запрос к VK API"""
        params['access_token'] = self.access_token
        params['v'] = self.api_version
        
        url = f"{self.base_url}{method}"
        
        try:
            response = requests.post(url, data=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": {"error_msg": str(e)}}
    
    def test_token(self) -> bool:
        """Проверяет валидность токена"""
        print("🔑 Проверка токена...")
        
        result = self._make_request("users.get", {})
        
        if "error" in result:
            print(f"❌ Ошибка: {result['error'].get('error_msg', 'Unknown error')}")
            return False
        
        if "response" in result:
            user = result["response"][0]
            print(f"✅ Токен валиден! Пользователь: {user.get('first_name')} {user.get('last_name')}")
            return True
        
        return False
    
    def get_groups(self) -> Optional[list]:
        """Получает список групп пользователя"""
        print("\n👥 Получение списка групп...")
        
        result = self._make_request("groups.get", {
            "extended": 1,
            "filter": "admin"
        })
        
        if "error" in result:
            print(f"❌ Ошибка: {result['error'].get('error_msg', 'Unknown error')}")
            return None
        
        if "response" in result:
            groups = result["response"]["items"]
            print(f"✅ Найдено групп (где вы администратор): {len(groups)}")
            
            for group in groups:
                print(f"  - {group['name']} (ID: -{group['id']})")
            
            return groups
        
        return None
    
    def test_wall_post(self, owner_id: str, message: str = None) -> bool:
        """Тестирует возможность публикации на стене"""
        if message is None:
            message = f"🧪 Тестовый пост от n8n workflow - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        print(f"\n📝 Тестирование публикации в группу/на стену {owner_id}...")
        
        params = {
            "owner_id": owner_id,
            "message": message,
            "from_group": 1 if owner_id.startswith("-") else 0
        }
        
        result = self._make_request("wall.post", params)
        
        if "error" in result:
            error = result["error"]
            print(f"❌ Ошибка: {error.get('error_msg', 'Unknown error')}")
            print(f"   Код ошибки: {error.get('error_code', 'N/A')}")
            return False
        
        if "response" in result:
            post_id = result["response"]["post_id"]
            print(f"✅ Пост успешно опубликован! Post ID: {post_id}")
            print(f"   Ссылка: https://vk.com/wall{owner_id}_{post_id}")
            return True
        
        return False
    
    def get_wall_post(self, owner_id: str, post_id: str) -> Optional[Dict]:
        """Получает информацию о посте"""
        print(f"\n📊 Получение информации о посте {owner_id}_{post_id}...")
        
        result = self._make_request("wall.getById", {
            "posts": f"{owner_id}_{post_id}"
        })
        
        if "error" in result:
            print(f"❌ Ошибка: {result['error'].get('error_msg', 'Unknown error')}")
            return None
        
        if "response" in result and len(result["response"]) > 0:
            post = result["response"][0]
            print(f"✅ Пост найден!")
            print(f"   Текст: {post.get('text', 'N/A')[:100]}...")
            print(f"   Просмотры: {post.get('views', {}).get('count', 0)}")
            print(f"   Лайки: {post.get('likes', {}).get('count', 0)}")
            print(f"   Репосты: {post.get('reposts', {}).get('count', 0)}")
            print(f"   Комментарии: {post.get('comments', {}).get('count', 0)}")
            return post
        
        return None
    
    def delete_wall_post(self, owner_id: str, post_id: str) -> bool:
        """Удаляет пост"""
        print(f"\n🗑️  Удаление поста {owner_id}_{post_id}...")
        
        result = self._make_request("wall.delete", {
            "owner_id": owner_id,
            "post_id": post_id
        })
        
        if "error" in result:
            print(f"❌ Ошибка: {result['error'].get('error_msg', 'Unknown error')}")
            return False
        
        if "response" in result and result["response"] == 1:
            print(f"✅ Пост успешно удален!")
            return True
        
        return False
    
    def check_permissions(self) -> Dict[str, bool]:
        """Проверяет права доступа токена"""
        print("\n🔐 Проверка прав доступа...")
        
        permissions = {
            "wall": False,
            "photos": False,
            "groups": False
        }
        
        # Проверка прав через account.getAppPermissions
        result = self._make_request("account.getAppPermissions", {})
        
        if "response" in result:
            perms = result["response"]
            
            # VK API возвращает битовую маску прав
            # wall = 8192, photos = 4, groups = 262144
            permissions["wall"] = bool(perms & 8192)
            permissions["photos"] = bool(perms & 4)
            permissions["groups"] = bool(perms & 262144)
            
            print("Права доступа:")
            for perm, has_access in permissions.items():
                status = "✅" if has_access else "❌"
                print(f"  {status} {perm}")
        else:
            print("⚠️  Не удалось проверить права доступа")
        
        return permissions


def main():
    """Основная функция"""
    print("=" * 60)
    print("VK API Tester для n8n Workflow")
    print("=" * 60)
    
    # Получение токена
    if len(sys.argv) > 1:
        access_token = sys.argv[1]
    else:
        access_token = input("\n🔑 Введите VK Access Token: ").strip()
    
    if not access_token:
        print("❌ Токен не указан!")
        sys.exit(1)
    
    # Создание тестера
    tester = VKAPITester(access_token)
    
    # Проверка токена
    if not tester.test_token():
        print("\n❌ Токен невалиден! Проверьте правильность токена.")
        sys.exit(1)
    
    # Проверка прав
    permissions = tester.check_permissions()
    
    if not permissions.get("wall"):
        print("\n⚠️  Внимание! У токена нет прав на публикацию на стене (wall).")
        print("   Получите новый токен с правами: wall, photos, groups")
        sys.exit(1)
    
    # Получение групп
    groups = tester.get_groups()
    
    if not groups:
        print("\n⚠️  У вас нет групп, где вы администратор.")
        print("   Вы можете публиковать только на своей стене.")
        owner_id = input("\n📝 Введите owner_id (или нажмите Enter для публикации на своей стене): ").strip()
    else:
        print("\n📝 Выберите группу для тестовой публикации:")
        print("   0 - Моя стена")
        for i, group in enumerate(groups, 1):
            print(f"   {i} - {group['name']} (ID: -{group['id']})")
        
        choice = input("\nВыбор (0-{}): ".format(len(groups))).strip()
        
        try:
            choice_idx = int(choice)
            if choice_idx == 0:
                owner_id = ""
            elif 1 <= choice_idx <= len(groups):
                owner_id = f"-{groups[choice_idx - 1]['id']}"
            else:
                print("❌ Неверный выбор!")
                sys.exit(1)
        except ValueError:
            print("❌ Неверный ввод!")
            sys.exit(1)
    
    if not owner_id:
        # Получаем ID текущего пользователя
        result = tester._make_request("users.get", {})
        if "response" in result:
            owner_id = str(result["response"][0]["id"])
    
    # Тестовая публикация
    print("\n" + "=" * 60)
    confirm = input("🚀 Опубликовать тестовый пост? (y/n): ").strip().lower()
    
    if confirm == 'y':
        if tester.test_wall_post(owner_id):
            print("\n✅ Все работает! Можете использовать workflow в n8n.")
            
            # Предложение удалить тестовый пост
            delete = input("\n🗑️  Удалить тестовый пост? (y/n): ").strip().lower()
            if delete == 'y':
                # Получаем последний пост
                result = tester._make_request("wall.get", {
                    "owner_id": owner_id,
                    "count": 1
                })
                if "response" in result and result["response"]["items"]:
                    post_id = str(result["response"]["items"][0]["id"])
                    tester.delete_wall_post(owner_id, post_id)
        else:
            print("\n❌ Публикация не удалась. Проверьте права и настройки группы.")
    else:
        print("\n✅ Тестирование завершено без публикации.")
    
    print("\n" + "=" * 60)
    print("📋 Используйте эти данные в n8n workflow:")
    print(f"   Access Token: {access_token[:20]}...")
    print(f"   Owner ID: {owner_id}")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Прервано пользователем")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
