from openpyxl import Workbook
from openpyxl.chart import PieChart, Reference
from openpyxl.chart.label import DataLabelList

from core.apps.surveys.models import Answer, Survey
from core.apps.surveys.services import SurveyService
from core.project import settings


def create_report(survey: Survey) -> None:
    service = SurveyService()
    questions = service.get_choices_questions(survey)

    wb = Workbook()
    ws = wb.active

    ws.column_dimensions["A"].width = 35

    for question in questions:
        question_title = question.title
        count = service.get_participants_number(survey)
        data = [
            [question_title],
            [f"Всего ответов: {count}"],
            ["Ответ", "Количество"],
        ]

        for row in data:
            ws.append(row)

        choices = question.choices.all()
        for choice in choices:
            count = Answer.objects.filter(question=question, value=choice.title).count()
            ws.append([choice.title, count])

        ws.append(["."])

        labels = Reference(ws, min_col=1, min_row=ws.max_row-len(choices), max_row=ws.max_row-1)
        data = Reference(ws, min_col=2, min_row=ws.max_row-len(choices), max_row=ws.max_row-1)

        chart = PieChart()

        chart.add_data(data)
        chart.set_categories(labels)
        chart.title = question_title
        chart.dataLabels = DataLabelList()
        chart.dataLabels.showVal = True

        chart_location = f"A{ws.max_row+1}"
        ws.add_chart(chart, chart_location)

        chart.width = 12
        chart.height = 6

        ws.insert_rows(ws.max_row, amount=13)

    path = settings.MEDIA_URL + f"{survey.pk}.xlsx"
    wb.save(path)
