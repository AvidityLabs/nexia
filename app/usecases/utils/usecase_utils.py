from .models import UseCase, UseCaseCategory


def bulk_insert_use_cases(use_cases):
    # Perform the bulk insert of use cases
    use_case_objs = []
    for use_case in use_cases:
        category_name = use_case.pop('category')
        category, _ = UseCaseCategory.objects.get_or_create(name=category_name)
        use_case['category'] = category
        use_case_objs.append(UseCase(**use_case))
    UseCase.objects.bulk_create(use_case_objs)