import typing

from django.db import models

if typing.TYPE_CHECKING:
    from articles.models import FaultReportLog  # noqa: F401


class FaultReportLogManager(models.Manager["FaultReportLog"]):
    def log_actions(self, request, form, queryset, created=False) -> None:
        result = []
        others_recorded = False
        for obj in queryset:
            for change in form.changed_data:
                if change == 'assigned_to_user':
                    _type = self.model.TYPE_ASSIGNED
                elif change == 'closed':
                    if form.cleaned_data['closed']:
                        _type = self.model.TYPE_CLOSED
                    else:
                        _type = self.model.TYPE_REOPENED
                else:
                    if others_recorded:
                        continue
                    _type = self.model.TYPE_MODIFIED if not created else self.model.TYPE_CREATED
                    others_recorded = True
                print(change)
                result.append(
                    self.model(
                        fault_report=obj,
                        user=request.user,
                        resolver=obj.assigned_to_user,
                        type=_type,
                    )
                )
        self.bulk_create(result)
