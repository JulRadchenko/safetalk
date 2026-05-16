# android_permissions.py
from kivy.logger import Logger

try:
    from android.permissions import request_permissions, Permission, check_permission
    from android import api_version
    
    def request_app_permissions():
        permissions = [
            Permission.INTERNET,
            Permission.RECORD_AUDIO,
            Permission.READ_EXTERNAL_STORAGE,
            Permission.WRITE_EXTERNAL_STORAGE
        ]
        
        # Для Android 13+ (API 33)
        if api_version >= 33:
            try:
                from android.permissions import Permission as NewPermission
                permissions.append(NewPermission.POST_NOTIFICATIONS)
            except:
                pass
        
        Logger.info(f"Requesting permissions: {permissions}")
        request_permissions(permissions)
        
    def check_all_permissions():
        perms = ['INTERNET', 'RECORD_AUDIO', 'READ_EXTERNAL_STORAGE', 'WRITE_EXTERNAL_STORAGE']
        for perm in perms:
            if not check_permission(f'android.permission.{perm}'):
                return False
        return True
        
except ImportError:
    Logger.warning("Android permissions module not available - running on desktop")
    def request_app_permissions():
        pass
    def check_all_permissions():
        return True
