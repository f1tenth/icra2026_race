---
title: RoboRacer ICRA 2026 Results
short_title: Results
layout: page
section: stream
---
<script src="{% link assets/js/sorttable.js %}"></script>
<style>
table {
    /* table-wrapper class */
    -webkit-overflow-scrolling: touch;
    overflow-x: auto;
    max-width: 760px;
}

table.time-trial {
    @media screen and (max-width: 736px) {
        display: inline-block;
        text-align: left;
    }
}

table.results td {
    height: 1em;
}
table.results td img, object {
    height: calc(1em + 0.75rem);
    max-width: calc(1em + 0.75rem);
    vertical-align: middle;
    object-fit: contain;
}

table.sortable th:not(.sorttable_sorted):not(.sorttable_sorted_reverse):not(.sorttable_nosort):after {
    content: " \25B4\25BE";
}
</style>

- ToC
{:toc}

<hr>

# Live Stream

<script src="https://player.twitch.tv/js/embed/v1.js"></script>

<center>
<div id="1" style="display: flex; justify-content: center"></div>
</center>
<script type="text/javascript">
    var options = {
        width: 854,
        height: 480,
        channel: "roboracer_ai",
        // video: "<video ID>",
        // collection: "<collection ID>",
        parent: ["icra2026-race.f1tenth.org", "localhost"]
    };
    var player = new Twitch.Player("1", options);
    player.setVolume(0.5);
</script>
<!-- STREAM_PLACEHOLDER --><!--<p style="color: #888; font-style: italic;">Live stream will appear here during the event.</p>--><!-- /STREAM_PLACEHOLDER -->

<hr>

# Time Trial
<center>
<table class="time-trial results sortable">
    <thead>
        <tr>
            <th>
                Place
            </th>
            <th>
                Team Name
            </th>
            <th>
                Best Lap Time
            </th>
            <th>
                Consecutive Laps
            </th>
            <th>
                Points
            </th>
        </tr>
    </thead>
    <tbody>
    {%- assign time_trial_results = site.data.teams | where_exp: "item", "item.points != nil" | sort: "points" | reverse -%}
    {%- for team in time_trial_results -%}
        {%- case forloop.index -%}
            {%- when 1 -%}
                <tr style="background-color: #fbbc04">
            {%- when 2 -%}
                <tr style="background-color: #cccccc">
            {%- when 3 -%}
                <tr style="background-color: #ce8946">
            {%- else -%}
                <tr>
        {%- endcase -%}
            <td sorttable_customkey="{{ forloop.index }}">
                {{ forloop.index }}
                {%- if forloop.index > 10 and forloop.index < 21 -%}
                    th
                {%- else -%}
                    {%- assign position = forloop.index | modulo: 10 -%}
                    {%- case position -%}
                        {%- when 1 -%}
                            st
                        {%- when 2 -%}
                            nd
                        {%- when 3 -%}
                            rd
                        {%- else -%}
                            th
                    {%- endcase -%}
                {%- endif -%}
            </td>
            <td>
                {%- comment -%}
                <object data="images/logos/lq/{{ team.id }}.png" type="image/png"><img src="images/logos/lq/0.png" /></object>
                {%- endcomment -%}
                <img src="images/logos/lq/{{ team.id }}.png" />
                {{ team.name }}
            </td>
            <td style="text-align: center">
                {%- comment -%}
                https://stackoverflow.com/questions/37862167/trailing-zeros-in-jekyll-liquid
                {%- endcomment -%}
                {%- assign lap_split = team.lap_time | round: 3 | split: "." -%}
                {%- if lap_split[1] -%}
                    {%- assign fraction = lap_split[1] | append: "000" | truncate: 3, "" -%}
                {%- else -%}
                    {%- assign fraction = "000" -%}
                {%- endif -%}
                {%- if team.lap_time -%}
                    {{ lap_split[0] }}.{{ fraction }} s
                {%- else -%}
                    <span style="display: none">999</span>
                {%- endif -%}
            </td>
            <td style="text-align: center">
                {{ team.consecutive_laps }}
            </td>
            <td style="text-align: center" sorttable_customkey="{{ forloop.index }}">
                {{ team.points | round }}
            </td>
        </tr>
    {%- endfor -%}
    </tbody>
</table>
</center>

<hr>

# Classic Cup
## Results
<center>
<table class="results">
    <thead>
        <tr>
            <th>
                Place
            </th>
            <th>
                Team Name
            </th>
        </tr>
    </thead>
    <tbody>
    {%- assign classic_cup_results = site.data.teams | where: "cup", "Classic" | sort: "position" -%}
    {%- for team in classic_cup_results -%}
        {%- case team.position -%}
            {%- when 1 -%}
                <tr style="background-color: #fbbc04">
            {%- when 2 -%}
                <tr style="background-color: #cccccc">
            {%- when 3 -%}
                <tr style="background-color: #ce8946">
            {%- else -%}
                <tr>
        {%- endcase -%}
            <td>
                {{ team.position }}
                {%- if team.position > 10 and team.position < 21 -%}
                    th
                {%- else -%}
                    {%- assign position = team.position | modulo: 10 -%}
                    {%- case position -%}
                        {%- when 1 -%}
                            st
                        {%- when 2 -%}
                            nd
                        {%- when 3 -%}
                            rd
                        {%- else -%}
                            th
                    {%- endcase -%}
                {%- endif -%}
            </td>
            <td>
                {%- comment -%}
                <object data="images/logos/lq/{{ team.id }}.png" type="image/png"><img src="images/logos/lq/0.png" /></object>
                {%- endcomment -%}
                <img src="images/logos/lq/{{ team.id }}.png" />
                {{ team.name }}
            </td>
        </tr>
    {%- endfor -%}
    </tbody>
</table>
</center>

## Bracket
<iframe src="https://brackethq.com/b/wchhd/embed/?name=1" width="100%" height="550" frameborder="0"></iframe>
<p style="font-size: smaller; margin-top: -0.5em"><i>Note: The order of the races does not correspond to the reality.</i></p>

<hr>

# Master Cup
## Results
<center>
<table class="results">
    <thead>
        <tr>
            <th>
                Place
            </th>
            <th>
                Team Name
            </th>
        </tr>
    </thead>
    <tbody>
    {%- assign master_cup_results = site.data.teams | where: "cup", "Master" | sort: "position" -%}
    {%- for team in master_cup_results -%}
        {%- case team.position -%}
            {%- when 1 -%}
                <tr style="background-color: #fbbc04">
            {%- when 2 -%}
                <tr style="background-color: #cccccc">
            {%- when 3 -%}
                <tr style="background-color: #ce8946">
            {%- else -%}
                <tr>
        {%- endcase -%}
            <td>
                {{ team.position }}
                {%- if team.position > 10 and team.position < 21 -%}
                    th
                {%- else -%}
                    {%- assign position = team.position | modulo: 10 -%}
                    {%- case position -%}
                        {%- when 1 -%}
                            st
                        {%- when 2 -%}
                            nd
                        {%- when 3 -%}
                            rd
                        {%- else -%}
                            th
                    {%- endcase -%}
                {%- endif -%}
            </td>
            <td>
                {%- comment -%}
                <object data="images/logos/lq/{{ team.id }}.png" type="image/png"><img src="images/logos/lq/0.png" /></object>
                {%- endcomment -%}
                <img src="images/logos/lq/{{ team.id }}.png" />
                {{ team.name }}
            </td>
        </tr>
    {%- endfor -%}
    </tbody>
</table>
</center>

## Bracket
<iframe src="https://brackethq.com/b/8chhd/embed/?name=1" width="100%" height="550" frameborder="0"></iframe>
<p style="font-size: smaller; margin-top: -0.5em"><i>Note: The order of the races does not correspond to the reality.</i></p>