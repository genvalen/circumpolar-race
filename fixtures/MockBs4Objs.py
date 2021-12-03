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

mock_html_3 = """
<td>
<a href="/RaceGroups/95983/Groups/1" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 1 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/11" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 11 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/10" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 10 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/9" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 9 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/8" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 8 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/7" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 7 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/6" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 6 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/5" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 5 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/4" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a </td>
<td>Region 4 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/3" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 3 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/2" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 2 - Running</td>

<td> <a href="/RaceGroups/95983/Groups/12" class="fs-lg d-block margin-t-10 margin-b-10 bold"></a> </td>
<td>Region 12 - Running</td>
"""

# Mock HTML for scraping participant identification endpoints
bs4_objs = [BeautifulSoup(mock_html_1, "lxml"), BeautifulSoup(mock_html_2, "lxml")]

# Mock HTML for scraping region endpoints
mock_soup = BeautifulSoup(mock_html_3, "lxml")
