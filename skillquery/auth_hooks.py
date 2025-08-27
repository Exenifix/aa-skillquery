from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook
from django.utils.translation import gettext_lazy as _

from . import urls


class SkillqueryMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar
        MenuItemHook.__init__(
            self,
            _("SkillQuery"),
            "fas fa-solid fa-database",
            "skillquery:index",
            navactive=["skillquery:"],
        )

    def render(self, request):
        if request.user.has_perm("skillquery.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return SkillqueryMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "skillquery", r"^skillquery/")
