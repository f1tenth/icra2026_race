---
title: Registration
short_title: Registration
layout: page
section: reg
---
<!-- REG_INFO_PARAGRAPH -->
<p>
    This competition is open for everyone of all levels, everyone is welcome to participate in this competition.
    A team can consist of multiple teammates. Teams with only one person are also allowed.
    Teams that take part in the in-person competition need to provide and build an Roboracer car by themselves.
    To register in the 5th Roboracer Sim Racing League, please refer to the
    <a href="https://autodrive-ecosystem.github.io/competitions/roboracer-sim-racing-icra-2026/#registration">
        Sim Racing Registration page
    </a>.
    <br>
    <!--The following pre-registration form is only for preliminary registration and for orientation and information sessions. Registration to ICRA 2026 is expected for all competitors.-->
</p>
<!-- /REG_INFO_PARAGRAPH -->

<center class="actions">
    <!-- REG_BUTTON -->
    <!--<a href="https://selapp.lanthan.at/?selection=icra2026" class="button disabled">Pre-registration Closed</a>-->
    <a href="https://selapp.lanthan.at/?selection=icra2026" class="button primary">Register Your Team</a>
    <!-- /REG_BUTTON -->
</center>

<br>
<br>

If you have any question regarding your participation, please contact us at
<a href="mailto:{{ site.NAV_EMAIL_LINK }}"><span class="label">{{ site.NAV_EMAIL_LINK }}</span></a>.

<hr>

<header class="post">
<h3 id="accomodation">Accomodation</h3>
</header>

<p>
Registration of accommodation needs to be organized and paid for individually by the participants. However, we are listing here a selection of options that you might consider interesting. Disclosure: The organizers are not affiliated with any of these accommodations and do not get any benefits from them.
</p>

<ul>
    <li>
        <strong>Vienna Brigittenau - Youth Hostel</strong><br />
        Webpage: <a target="_blank" href="https://www.oejhv.at/en/youth-hostels/vienna/1200-vienna/">https://www.oejhv.at/en/youth-hostels/vienna/1200-vienna/</a><br />
        Address: Adalbert Stifter Straße 73, A-1200 Wien, AUSTRIA<br />
        Public transport connections: Direct bus connection (line 11A) between the hostel and the conference location, which takes approximately 25 minutes.<br />
        Breakfast included<br />
        Booking happens per team directly with the hostel. For room rates, please check the webpage.
    </li>
    <li>
        Potentially further suggestions to come.
    </li>
    <li>
        <strong>Official ICRA Conference Hotels</strong><br />
        Webpage: <a target="_blank" href="https://2026.ieee-icra.org/attend/housing-information/">https://2026.ieee-icra.org/attend/housing-information/</a><br />
        Depending on your available budget, you might also consider the official ICRA conference hotels.
    </li>
</ul>

{% if site.data.registered_participants %}
<!-- PARTICIPANTS_SECTION -->
<hr>

<header>
<h3 id="participants">Participants</h3>
<p markdown="1">
    Note: Only teams that submitted all the required materials are listed below. This table is updated manually, for an automatically updated table see [this page](https://selapp.lanthan.at/export_icra_list.php).
</p>
</header>

<p style="display:none;">
If you have registered for participation but the list below is not updated, please contact us at <a href="mailto:{{ site.NAV_EMAIL_LINK }}"><span class="label">{{ site.NAV_EMAIL_LINK }}</span></a>.
<br>
Register the modified information under the same team name, and we will update it accordingly.
</p>

<table>
<thead>
    <tr>
        <th style="text-align: left">TEAM NAME</th>
        <th style="text-align: left">AFFILIATION</th>
        {%- assign names_available = site.data.registered_participants | where_exp: "item", "item['First name (Given name)']" | where_exp: "item", "item['Last name (Surname)']" -%}
        {%- if names_available.size > 0 -%}
        <th style="text-align: left">TEAM MEMBERS</th>
        {%- endif -%}
    </tr>
</thead>
<tbody>
{%- comment -%}
https://stackoverflow.com/questions/32015337/intelligent-way-to-generate-tables-with-liquid-from-a-csv-file
The '-' are done so that it renders nicely even in the HTML code.
{%- endcomment -%}
{%- assign participants = site.data.registered_participants | sort_natural: "Team name" -%}
{%- for item in participants -%}
    {% if item["State"] == "submitted" %}
    <tr>
        <td>{{- item["Team name"] -}}</td>
        <td>{{- item["Affiliation"] -}}</td>
        {% if names_available.size > 0 %}<td>
            {%- assign first_names = item["First name (Given name)"] | split: '
' -%}
            {%- assign last_names = item["Last name (Surname)"] | split: '
' -%}
            {%- for last_name in last_names -%}
                {{- last_name | strip | append: ", " | append: first_names[forloop.index0] | strip -}}
                {%- unless forloop.last -%}
                    <br />
                {%- endunless -%}
            {%- endfor -%}
        </td>{% endif %}
    </tr>
    {%- endif -%}
{% endfor %}
</tbody>
</table>
<!-- /PARTICIPANTS_SECTION -->
{% endif %}
