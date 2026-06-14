---
title: Participating Teams
short_title: Teams
layout: page
section: teams
---
<style>
div.teams-list {
    display: flex;
    flex-flow: row wrap;
    justify-content: space-evenly;
    align-content: space-between;
    gap: 2em;
}

div.teams-list div.grid-parent {
    width: 30%;
    min-width: 260px;
    border: 1px solid black;
    padding: 0.75rem 0.75rem;

    display: grid;
    grid-template-columns: 80px 1fr;
    gap: 0.5em;

    @media screen and (max-width: 736px) {
        width: 30%;
    }
}

div.grid-child.logo {
    justify-self: center;
    align-self: center;

    img {
        height: 64px;
        max-width: 64px;
        vertical-align: middle;
        object-fit: contain;
    }
}

div.grid-child.team-name {
    justify-self: center;
    align-self: center;
    text-align: center;
}
</style>

<div class="teams-list">
{%- assign teams = site.data.teams | where_exp: "item", "item.points != nil" | sort_natural: "name" -%}
{%- for team in teams -%}
    <div class="grid-parent"><a href="{%- capture teampage -%}{% link teams/0.md %}{%- endcapture -%}{{ teampage | split: "0." | first | append: team.id | append: ".html" }}" style="display: contents">
        <div class="grid-child logo">
            <img src="images/logos/lq/{{ team.id }}.png" />
        </div>
        <div class="grid-child team-name">
            {{ team.name }}
        </div>
    </a></div>
{%- endfor -%}
</div>
<br />
<p style="font-size: smaller">
<i>Original registration page is available <a href="{% link registration.md %}">here</a>.</i>
</p>