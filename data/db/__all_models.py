# Модели, представляющие сущность паспорта организации
from .models.passport_entity.collective_agreement import CollectiveAgreement
from .models.passport_entity.general_data import GeneralData
from .models.passport_entity.golden_mark_application import \
    GoldenMarkApplication
from .models.passport_entity.injuries import Injuries
from .models.passport_entity.passport import Passport
from .models.passport_entity.profrisk import Profrisk
from .models.passport_entity.safety_training import SafetyTraining
from .models.passport_entity.sout import Sout
from .models.passport_entity.work_condition import WorkCondition
# Модели, тоже относящиеся к системе паспортов, но
# не имеющие ONE-TO-ONE связь с моделью Passport
from .models.passport_models.passport_status import PassportStatus
from .models.passport_models.photo import Photo
from .models.passport_models.video import Video
# Модели, отвечающие за опросы
from .models.survey_models.answer import Answer
from .models.survey_models.field import Field
from .models.survey_models.field_type import FieldType
from .models.survey_models.process import Process
from .models.survey_models.quiz import Quiz
# Модели для работы системы аккаунтов
from .models.user_models.user import User
from .models.user_models.role import Role
# Модели, отвечающие за системные операции,
# использующие данные и "поведение" остальных сущностей
from .models.system_models.user_log import UserLog
from .models.system_models.passport_log import PassportLog
