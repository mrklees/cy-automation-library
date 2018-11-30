#from .cyschoolhousesuite import *
from .config import CHICAGO_USER, SF_URL, SF_USER, SF_PASS, SF_TOKN
from .simple_cysh import *

from . import section_creation
from . import student
from . import student_section

if CHICAGO_USER == True:
    from . import section_creation_chi
    from . import servicetrackers
    from . import tot_audit
    from . import tracker_mgmt
