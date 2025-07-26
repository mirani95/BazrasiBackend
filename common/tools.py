import typing


class CustomOperations:
    """
    @for Custom Operations in view sets
    """

    def custom_create(  # noqa
            self,
            user: object = None,
            request: object = None,
            view: object = None,
            data_key: str = None,
            data: dict = None,
            additional_data: dict = None
    ) -> typing.Any:
        """
        to create custom view objects that
        defined in VIEW_SET dictionary to
        just calling this method in other
        view sets
        """
        view_data = request.data  # included needed data for view set # noqa
        if user:
            view_data[data_key].update({'user': user.id})  # noqa
        if additional_data:
            view_data[data_key].update(additional_data)

        # if we have data_key for dictionary data get value
        # if not, just put additional data in serializer
        if data_key:
            serializer = view.serializer_class(data=view_data[data_key])  # noqa
        if data:
            serializer = view.serializer_class(data=data)  # noqa
        serializer.is_valid(raise_exception=True)  # noqa
        view.perform_create(serializer)  # noqa
        headers = view.get_success_headers(serializer.data)  # noqa
        return serializer.data

    def custom_update(  # noqa
            self,
            user: object = None,
            request: object = None,
            obj_id: object = None,
            view: object = None,
            data_key: str = None,
            data: dict = None,
            additional_data: dict = None
    ) -> typing.Any:
        view_data = request.data  # included needed data for view set # noqa
        queryset = view.queryset.get(id=obj_id)
        if user:
            view_data[data_key].update({'user': user.id})  # noqa
        if additional_data:
            view_data[data_key].update(additional_data)
        if data_key:
            serializer = view.serializer_class(data=view_data[data_key], instance=queryset, partial=True)  # noqa
        if data:
            serializer = view.serializer_class(data=data, instance=queryset, partial=True)  # noqa
        serializer.is_valid(raise_exception=True)  # noqa
        object_data = data if data else view_data[data_key]
        serializer.save()  # noqa
        headers = view.get_success_headers(serializer.data)  # noqa
        return serializer.data
