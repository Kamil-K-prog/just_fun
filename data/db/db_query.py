import sqlalchemy.orm


class QueryWithSmartDeletion(sqlalchemy.orm.Query):
    def _get_models(self) -> list:
        """Возвращает модели, задействованные при создании запроса"""
        if hasattr(self, 'attr'):
            # если это подзапрос (subquery)
            return [self.attr.target_mapper]

        return [
            desc['type']
            for desc in self.column_descriptions
            if isinstance(
                desc['type'], sqlalchemy.orm.decl_api.DeclarativeMeta)]

    _models = property(_get_models)

    def delete(self):
        ("""Если удаление строк производится из таблицы, ORM-модель которой """
         """помечена, как возможная для пагинации, то этот метод """
         """позаботится о том, чтобы после удаления первичные ключи строк """
         """таблицы были непрерывной возрастающей последовательностью чисел""")
        models = self._get_models()

        objs_to_delete_ids = []
        if models and getattr(models[0], 'CAN_BE_PAGINATED', default=False):
            # навешиваем кастомную логику только если есть пагинируемая модель
            objs_to_delete_ids = self.with_entities(models[0].id).all()

        # Даём запросу выполниться / поднять исключение
        super().delete()

        if not objs_to_delete_ids:  # если ничего не нужно удалять
            return None

        model = models[0]  # класс ORM-модели, объекты которой удаляются

        # новый запрос для получения n объектов с самыми большими id
        objs_with_max_ids = (
            self.session.query(model)  # новый объект запроса
            .order_by(model.id.desc())  # сортировка по id в обратном порядке
            .limit(len(objs_to_delete_ids))  # максимум столько же объектов,
            .all())  # сколько было удалено

        n_objs_with_max_ids = len(objs_with_max_ids)

        if not n_objs_with_max_ids:
            return None  # если в таблице больше не осталось строк

        max_obj_index = 0

        for deleted_obj_id_tuple in objs_to_delete_ids:
            deleted_obj_id = deleted_obj_id_tuple[0]

            # объект с максимальным id на данный момент
            max_obj = objs_with_max_ids[max_obj_index]

            # если у данного удалённого объекта id больше максимального
            if deleted_obj_id > max_obj.id:
                continue  # то после его удаления изменения в таблице не нужны

            # ставим объекту с макс. id идентификатор удалённого объекта
            max_obj.id = deleted_obj_id

            # Проверяем максимальный ли id у нашего объекта, может быть меняем
            if max_obj_index != n_objs_with_max_ids - 1 and \
                objs_with_max_ids[max_obj_index + 1].id > \
                    deleted_obj_id:  # если объект с макс. ID уже другой,
                max_obj_index += 1  # то переключаемся на него


# для экспорта
ActualQuery = QueryWithSmartDeletion
