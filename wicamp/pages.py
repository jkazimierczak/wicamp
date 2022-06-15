from enum import Enum


class WikampPages:
    cas = "https://cas.p.lodz.pl"
    cas_login = "https://cas.p.lodz.pl/cas/login"
    virtul = "https://virtul.p.lodz.pl/virtul"
    virtul_login = virtul + "/login"
    ftims_login = "https://ftims.edu.p.lodz.pl/login/index.php"
    sysop2022 = "https://ftims.edu.p.lodz.pl/course/view.php?id=2388"


class SysopLectures(Enum):
    lekcja4 = "https://ftims.edu.p.lodz.pl/mod/lesson/view.php?id=102021&pageid=10594"
    lekcja5_1 = "https://ftims.edu.p.lodz.pl/mod/lesson/view.php?id=102033"
    lecture15 = "https://ftims.edu.p.lodz.pl/pluginfile.php/181592/mod_resource/content/58/v26/img0.html"
