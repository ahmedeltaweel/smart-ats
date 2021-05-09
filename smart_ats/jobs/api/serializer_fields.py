class CurrrentCompanyAdmin:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["request"].user.companyadmin


class CurrrentCompanyId:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["view"].kwargs["company_id"]


class CurrrentJobId:
    requires_context = True

    def __call__(self, serializer_field):
        return serializer_field.context["view"].kwargs["job_id"]
