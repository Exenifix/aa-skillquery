from eveuniverse.models import EveType
from memberaudit.constants import EveCategoryId
from memberaudit.models import CharacterSkill


# vibecoded
def parse_skill_data(post_data):
    """Parse the flat skill data into a structured format"""
    skill_names = post_data.getlist("skill_name")
    skill_ids = post_data.getlist("skill_ids")
    min_levels = post_data.getlist("min_levels", [])

    skills = []
    for i, skill_name in enumerate(skill_names):
        if skill_name:  # Only process if skill name is provided
            skill_data = {"skill_name": skill_name, "skill_id": skill_ids[i] if i < len(skill_ids) else None}

            # Add min_level if available (for skillset)
            if i < len(min_levels) and min_levels[i]:
                skill_data["min_level"] = min_levels[i]

            skills.append(skill_data)

    return skills


def get_skill_data(skill_ids: list[int], cumulative: bool = False) -> dict[str, list[int]]:
    base_queryset = CharacterSkill.objects.filter(
        eve_type__id__in=skill_ids, eve_type__eve_group__eve_category_id=EveCategoryId.SKILL, eve_type__published=True
    )
    data: dict[str, list[int]] = {}  # {skill name: [amount of ppl on each level]}
    for skill_id in skill_ids:
        ls = []
        data[EveType.objects.get(id=skill_id).name] = ls
        for level in range(1, 6):
            q = base_queryset.filter(eve_type__id=skill_id)
            q = q.filter(active_skill_level__gte=level) if cumulative else q.filter(active_skill_level=level)
            ls.append(q.count())

    return data


def get_skillset_amount(skillset: dict[int, int]) -> int:
    base_queryset = CharacterSkill.objects.filter(
        eve_type__id__in=skillset.keys(),
        eve_type__eve_group__eve_category_id=EveCategoryId.SKILL,
        eve_type__published=True,
    )
    member_set = set(base_queryset.values_list("character__id", flat=True))
    for skill_id, min_level in skillset.items():
        member_set &= set(
            base_queryset.filter(eve_type__id=skill_id, active_skill_level__gte=min_level).values_list(
                "character__id", flat=True
            )
        )

    return len(member_set)
