class GatherlyError(Exception):
    """Базовое исключение для Gatherly OS"""
    pass

class DatabaseError(GatherlyError):
    """Ошибка работы с базой данных"""
    pass

class ServiceError(GatherlyError):
    """Ошибка в бизнес-логике"""
    pass

class ValidationError(GatherlyError):
    """Ошибка валидации данных"""
    pass

class NotFoundError(GatherlyError):
    """Объект не найден"""
    pass

class PermissionError(GatherlyError):
    """Недостаточно прав"""
    pass
