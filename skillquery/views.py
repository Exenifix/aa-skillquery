"""Views."""

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from memberaudit.models import EveSkillType

from skillquery.forms import SkillForm, SkillsetForm
from skillquery.utils import get_skill_data, get_skillset_amount, parse_skill_data


@login_required
@permission_required("skillquery.basic_access")
def index(_):
    """Render index view."""
    return redirect("skillquery:skill")


@login_required
@permission_required("skillquery.basic_access")
def skill_analyzer(request: HttpRequest):
    if request.method == "POST":
        skills_data = parse_skill_data(request.POST)  # [{'skill_name': ..., 'skill_id': ...}, ...]

        valid = True
        for row in skills_data:
            if not SkillForm(row).is_valid():
                valid = False
                break

        forms = [SkillForm(initial=row) for row in (skills_data or [{}])]

        statistics = None
        if valid and skills_data:
            skill_ids = [row["skill_id"] for row in skills_data if row.get("skill_id")]
            statistics = get_skill_data(skill_ids, cumulative=request.POST.get("cumulative", "off") == "on")

        return render(request, "skillquery/skill.html", {"forms": forms, "statistics": statistics})

    forms = [SkillForm()]
    return render(request, "skillquery/skill.html", {"forms": forms})


@login_required
@permission_required("skillquery.basic_access")
def skillset_analyzer(request: HttpRequest):
    if request.method == "POST":
        skills_data = parse_skill_data(request.POST)  # [{'skill_name': ..., 'skill_id': ..., 'min_level': ...}, ...]

        valid = True
        for row in skills_data:
            if not SkillsetForm(row).is_valid():
                valid = False
                break

        forms = [SkillsetForm(initial=row) for row in (skills_data or [{}])]

        amount = None
        if valid and skills_data:
            skills_with_levels = {
                row["skill_id"]: row["min_level"] for row in skills_data if row.get("skill_id") and row.get("min_level")
            }
            amount = get_skillset_amount(skills_with_levels)

        return render(request, "skillquery/skillset.html", {"forms": forms, "amount": amount})

    forms = [SkillsetForm()]
    return render(request, "skillquery/skillset.html", {"forms": forms})


@login_required
@permission_required("skillquery.basic_access")
def skill_autocomplete(request: HttpRequest):
    query = request.GET.get("q", "")
    matching_skills = EveSkillType.objects.filter(name__icontains=query).values_list("id", "name")[:5]
    return JsonResponse([{"id": id, "name": name} for id, name in matching_skills], safe=False)
