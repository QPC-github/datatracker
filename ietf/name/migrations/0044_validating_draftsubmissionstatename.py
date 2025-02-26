# Generated by Django 2.2.28 on 2022-05-17 11:35

from django.db import migrations


def forward(apps, schema_editor):
    DraftSubmissionStateName = apps.get_model('name', 'DraftSubmissionStateName')
    new_state = DraftSubmissionStateName.objects.create(
        slug='validating',
        name='Validating Submitted Draft',
        desc='Running validation checks on received submission',
        used=True,
        order=1 + DraftSubmissionStateName.objects.order_by('-order').first().order,
    )
    new_state.next_states.set(
        DraftSubmissionStateName.objects.filter(
            slug__in=['cancel', 'uploaded'],
        )
    )


def reverse(apps, schema_editor):
    Submission = apps.get_model('submit', 'Submission')
    # Any submissions in the state we are about to delete would be deleted.
    # Remove these manually if you really mean to do this.
    assert Submission.objects.filter(state__slug='validating').count() == 0
    DraftSubmissionStateName = apps.get_model('name', 'DraftSubmissionStateName')
    DraftSubmissionStateName.objects.filter(slug='validating').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('name', '0043_editorial_stream_grouptype'),
        ('submit', '0001_initial'),  # ensure Submission model exists
    ]

    operations = [
        migrations.RunPython(forward, reverse)
    ]
