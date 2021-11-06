"This file contains mock data for unit testing."
from bs4 import BeautifulSoup

mock_html_1 = """
<!-- PARTICIPANT 1 -->
<tr>
<td>
    <a href="/Race/Results/95983/IndividualResult/?resultSetId=212380#U44542375" class="rsuBtn rsuBtn--text-whitebg rsuBtn--xs margin-r-0"><i class="icon icon-search action-icon padding-0" aria-hidden="true" ></i>
        Christopher J.
    </a>
</td>
</tr>

<!-- PARTICIPANT 2 -->
<tr>
<td>
    <a href="/Race/Results/95983/IndividualResult/?resultSetId=212380#U45884193" class="rsuBtn rsuBtn--text-whitebg rsuBtn--xs margin-r-0"><i class="icon icon-search action-icon padding-0" aria-hidden="true" ></i>
        Karen O.
    </a>
</td>
</tr>
"""

mock_html_2 = """
<!-- PARTICIPANT 1 -->
<tr>
<td>
    <a href="/Race/Results/95983/IndividualResult/?resultSetId=212380#U3349257" class="rsuBtn rsuBtn--text-whitebg rsuBtn--xs margin-r-0"><i class="icon icon-search action-icon padding-0" aria-hidden="true" ></i>
        Chris J.
    </a>
</td>
</tr>

<!-- PARTICIPANT 2 -->
<tr>
<td>
    <a href="/Race/Results/95983/IndividualResult/?resultSetId=212380#U21890947" class="rsuBtn rsuBtn--text-whitebg rsuBtn--xs margin-r-0"><i class="icon icon-search action-icon padding-0" aria-hidden="true" ></i>
        Karen O.
    </a>
</td>
</tr>

<!-- PARTICIPANT 3 -->
<tr>
<td>
    <a href="/Race/Results/95983/IndividualResult/?resultSetId=212380#U23755991" class="rsuBtn rsuBtn--text-whitebg rsuBtn--xs margin-r-0"><i class="icon icon-search action-icon padding-0" aria-hidden="true" ></i>
        Jonathon G.
    </a>
</td>
</tr>
"""

bs4_objs = [BeautifulSoup(mock_html_1, "lxml"), BeautifulSoup(mock_html_2, "lxml")]
