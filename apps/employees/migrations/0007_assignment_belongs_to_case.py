import django.db.models.deletion
from django.db import migrations, models


def populate_assignment_case(apps, schema_editor):
    """Preserve existing Assignment ownership while moving it from WorkOrder to Case."""

    Assignment = apps.get_model("employees", "Assignment")
    WorkOrder = apps.get_model("requests", "WorkOrder")

    status_mapping = {
        "Assigned": "ASSIGNED",
        "Accepted": "ACCEPTED",
        "Released": "RELEASED",
    }

    for assignment in Assignment.objects.all().iterator():
        assignment.case_id = WorkOrder.objects.only("case_id").get(
            pk=assignment.work_order_id,
        ).case_id
        assignment.status = status_mapping.get(assignment.status, assignment.status)
        assignment.save(update_fields=["case", "status"])


class Migration(migrations.Migration):

    dependencies = [
        ("employees", "0006_assignment"),
        ("requests", "0006_alter_case_priority_alter_case_service"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="case",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="assignments",
                to="requests.case",
            ),
        ),
        migrations.RunPython(populate_assignment_case, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="assignment",
            name="case",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="assignments",
                to="requests.case",
            ),
        ),
        migrations.RemoveField(
            model_name="assignment",
            name="work_order",
        ),
        migrations.AddConstraint(
            model_name="assignment",
            constraint=models.CheckConstraint(
                condition=models.Q(
                    ("status__in", ["ASSIGNED", "ACCEPTED", "RELEASED"]),
                ),
                name="valid_assignment_status",
            ),
        ),
        migrations.AddConstraint(
            model_name="assignment",
            constraint=models.UniqueConstraint(
                condition=models.Q(
                    ("status__in", ["ASSIGNED", "ACCEPTED"]),
                ),
                fields=("case",),
                name="unique_active_assignment_per_case",
            ),
        ),
    ]
