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
        {%- assign countries_available = site.data.registered_participants | where_exp: "item", "item['Country']" -%}
        {%- if countries_available.size > 0 -%}
        <th style="text-align: left">COUNTRY</th>
        {%- endif -%}
    </tr>
</thead>
<tbody>
{%- comment -%}
https://stackoverflow.com/questions/32015337/intelligent-way-to-generate-tables-with-liquid-from-a-csv-file
The '-' are done so that it renders nicely even in the HTML code.
{%- endcomment -%}
{%- assign participants = site.data.registered_participants | sort_natural: "Team name" -%}
{%- assign countries = "," | split: "," -%}
{%- for item in participants -%}
    {% if item["State"] == "submitted" %}
    <tr>
        <td>{{- item["Team name"] -}}</td>
        <td>{{- item["Affiliation"] -}}</td>
        {% if countries_available.size > 0 %}<td>
            {%- assign countries = countries | push: item["Country"] -%}
            {{- item["Country"] -}}
        </td>{% endif %}
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

{%- if countries_available.size > 0 -%}
<!-- https://stephanwagner.me/coding/blog/create-world-map-charts-with-svgmap -->
<script src="https://cdn.jsdelivr.net/npm/svgmap@v2.19.3/dist/svg-map.umd.min.js"></script>
<link href="https://cdn.jsdelivr.net/npm/svgmap@v2.19.3/dist/svg-map.min.css" rel="stylesheet">

<div id="svgMap"></div>

<script markdown="0">
var countryCodes = {
    'Andorra' : 'AD',
    'United Arab Emirates' : 'AE',
    'Afghanistan' : 'AF',
    'Antigua and Barbuda' : 'AG',
    'Anguilla' : 'AI',
    'Albania' : 'AL',
    'Armenia' : 'AM',
    'Angola' : 'AO',
    'Antarctica' : 'AQ',
    'Argentina' : 'AR',
    'American Samoa' : 'AS',
    'Austria' : 'AT',
    'Australia' : 'AU',
    'Aruba' : 'AW',
    'Åland Islands' : 'AX',
    'Azerbaijan' : 'AZ',
    'Bosnia and Herzegovina' : 'BA',
    'Barbados' : 'BB',
    'Bangladesh' : 'BD',
    'Belgium' : 'BE',
    'Burkina Faso' : 'BF',
    'Bulgaria' : 'BG',
    'Bahrain' : 'BH',
    'Burundi' : 'BI',
    'Benin' : 'BJ',
    'Saint Barthélemy' : 'BL',
    'Bermuda' : 'BM',
    'Brunei Darussalam' : 'BN',
    'Bolivia, Plurinational State of' : 'BO',
    'Bonaire, Sint Eustatius and Saba' : 'BQ',
    'Brazil' : 'BR',
    'Bahamas' : 'BS',
    'Bhutan' : 'BT',
    'Bouvet Island' : 'BV',
    'Botswana' : 'BW',
    'Belarus' : 'BY',
    'Belize' : 'BZ',
    'Canada' : 'CA',
    'Cocos (Keeling) Islands' : 'CC',
    'Congo, Democratic Republic of the' : 'CD',
    'Central African Republic' : 'CF',
    'Congo' : 'CG',
    'Switzerland' : 'CH',
    'Côte d\'Ivoire' : 'CI',
    'Cook Islands' : 'CK',
    'Chile' : 'CL',
    'Cameroon' : 'CM',
    'China' : 'CN',
    'Colombia' : 'CO',
    'Costa Rica' : 'CR',
    'Cuba' : 'CU',
    'Cabo Verde' : 'CV',
    'Curaçao' : 'CW',
    'Christmas Island' : 'CX',
    'Cyprus' : 'CY',
    'Czechia' : 'CZ',
    'Germany' : 'DE',
    'Djibouti' : 'DJ',
    'Denmark' : 'DK',
    'Dominica' : 'DM',
    'Dominican Republic' : 'DO',
    'Algeria' : 'DZ',
    'Ecuador' : 'EC',
    'Estonia' : 'EE',
    'Egypt' : 'EG',
    'Western Sahara' : 'EH',
    'Eritrea' : 'ER',
    'Spain' : 'ES',
    'Ethiopia' : 'ET',
    'Finland' : 'FI',
    'Fiji' : 'FJ',
    'Falkland Islands (Malvinas)' : 'FK',
    'Micronesia, Federated States of' : 'FM',
    'Faroe Islands' : 'FO',
    'France' : 'FR',
    'Gabon' : 'GA',
    'United Kingdom of Great Britain and Northern Ireland' : 'GB',
    'Grenada' : 'GD',
    'Georgia' : 'GE',
    'French Guiana' : 'GF',
    'Guernsey' : 'GG',
    'Ghana' : 'GH',
    'Gibraltar' : 'GI',
    'Greenland' : 'GL',
    'Gambia' : 'GM',
    'Guinea' : 'GN',
    'Guadeloupe' : 'GP',
    'Equatorial Guinea' : 'GQ',
    'Greece' : 'GR',
    'South Georgia and the South Sandwich Islands' : 'GS',
    'Guatemala' : 'GT',
    'Guam' : 'GU',
    'Guinea-Bissau' : 'GW',
    'Guyana' : 'GY',
    'Hong Kong' : 'HK',
    'Heard Island and McDonald Islands' : 'HM',
    'Honduras' : 'HN',
    'Croatia' : 'HR',
    'Haiti' : 'HT',
    'Hungary' : 'HU',
    'Indonesia' : 'ID',
    'Ireland' : 'IE',
    'Israel' : 'IL',
    'Isle of Man' : 'IM',
    'India' : 'IN',
    'British Indian Ocean Territory' : 'IO',
    'Iraq' : 'IQ',
    'Iran, Islamic Republic of' : 'IR',
    'Iceland' : 'IS',
    'Italy' : 'IT',
    'Jersey' : 'JE',
    'Jamaica' : 'JM',
    'Jordan' : 'JO',
    'Japan' : 'JP',
    'Kenya' : 'KE',
    'Kyrgyzstan' : 'KG',
    'Cambodia' : 'KH',
    'Kiribati' : 'KI',
    'Comoros' : 'KM',
    'Saint Kitts and Nevis' : 'KN',
    'North Korea' : 'KP',
    'South Korea' : 'KR',
    'Kuwait' : 'KW',
    'Cayman Islands' : 'KY',
    'Kazakhstan' : 'KZ',
    'Lao People\'s Democratic Republic' : 'LA',
    'Lebanon' : 'LB',
    'Saint Lucia' : 'LC',
    'Liechtenstein' : 'LI',
    'Sri Lanka' : 'LK',
    'Liberia' : 'LR',
    'Lesotho' : 'LS',
    'Lithuania' : 'LT',
    'Luxembourg' : 'LU',
    'Latvia' : 'LV',
    'Libya' : 'LY',
    'Morocco' : 'MA',
    'Monaco' : 'MC',
    'Moldova, Republic of' : 'MD',
    'Montenegro' : 'ME',
    'Saint Martin (French part)' : 'MF',
    'Madagascar' : 'MG',
    'Marshall Islands' : 'MH',
    'North Macedonia' : 'MK',
    'Mali': 'ML',
    'Myanmar' : 'MM',
    'Mongolia' : 'MN',
    'Macao' : 'MO',
    'Northern Mariana Islands' : 'MP',
    'Martinique' : 'MQ',
    'Mauritania' : 'MR',
    'Montserrat' : 'MS',
    'Malta' : 'MT',
    'Mauritius' : 'MU',
    'Maldives' : 'MV',
    'Malawi' : 'MW',
    'Mexico' : 'MX',
    'Malaysia' : 'MY',
    'Mozambique' : 'MZ',
    'Namibia' : 'NA',
    'New Caledonia' : 'NC',
    'Niger' : 'NE',
    'Norfolk Island' : 'NF',
    'Nigeria' : 'NG',
    'Nicaragua' : 'NI',
    'Netherlands, Kingdom of the' : 'NL',
    'Norway' : 'NO',
    'Nepal' : 'NP',
    'Nauru' : 'NR',
    'Niue' : 'NU',
    'New Zealand' : 'NZ',
    'Oman' : 'OM',
    'Panama' : 'PA',
    'Peru' : 'PE',
    'French Polynesia' : 'PF',
    'Papua New Guinea' : 'PG',
    'Philippines' : 'PH',
    'Pakistan' : 'PK',
    'Poland' : 'PL',
    'Saint Pierre and Miquelon' : 'PM',
    'Pitcairn' : 'PN',
    'Puerto Rico' : 'PR',
    'Palestine, State of' : 'PS',
    'Portugal' : 'PT',
    'Palau' : 'PW',
    'Paraguay' : 'PY',
    'Qatar' : 'QA',
    'Réunion' : 'RE',
    'Romania' : 'RO',
    'Serbia' : 'RS',
    'Russian Federation' : 'RU',
    'Rwanda' : 'RW',
    'Saudi Arabia' : 'SA',
    'Solomon Islands' : 'SB',
    'Seychelles' : 'SC',
    'Sudan' : 'SD',
    'Sweden' : 'SE',
    'Singapore' : 'SG',
    'Saint Helena, Ascension and Tristan da Cunha' : 'SH',
    'Slovenia' : 'SI',
    'Svalbard and Jan Mayen' : 'SJ',
    'Slovakia' : 'SK',
    'Sierra Leone' : 'SL',
    'San Marino' : 'SM',
    'Senegal' : 'SN',
    'Somalia' : 'SO',
    'Suriname' : 'SR',
    'South Sudan' : 'SS',
    'Sao Tome and Principe' : 'ST',
    'El Salvador' : 'SV',
    'Sint Maarten (Dutch part)' : 'SX',
    'Syrian Arab Republic' : 'SY',
    'Eswatini' : 'SZ',
    'Turks and Caicos Islands' : 'TC',
    'Chad' : 'TD',
    'French Southern Territories' : 'TF',
    'Togo' : 'TG',
    'Thailand' : 'TH',
    'Tajikistan' : 'TJ',
    'Tokelau' : 'TK',
    'Timor-Leste' : 'TL',
    'Turkmenistan' : 'TM',
    'Tunisia' : 'TN',
    'Tonga' : 'TO',
    'Türkiye' : 'TR',
    'Trinidad and Tobago' : 'TT',
    'Tuvalu' : 'TV',
    'Taiwan, Province of China' : 'TW',
    'Tanzania, United Republic of' : 'TZ',
    'Ukraine' : 'UA',
    'Uganda' : 'UG',
    'United States Minor Outlying Islands' : 'UM',
    'United States' : 'US',
    'United States of America' : 'US',
    'Uruguay' : 'UY',
    'Uzbekistan' : 'UZ',
    'Holy See' : 'VA',
    'Saint Vincent and the Grenadines' : 'VC',
    'Venezuela, Bolivarian Republic of' : 'VE',
    'Virgin Islands (British)' : 'VG',
    'Virgin Islands (U.S.)' : 'VI',
    'Viet Nam' : 'VN',
    'Vanuatu' : 'VU',
    'Wallis and Futuna' : 'WF',
    'Samoa' : 'WS',
    'Yemen' : 'YE',
    'Mayotte' : 'YT',
    'South Africa' : 'ZA',
    'Zambia' : 'ZM',
    'Zimbabwe' : 'ZW'
};

function get_code(country) {
    if (countryCodes.hasOwnProperty(country)) {
        return countryCodes[country];
    } else {
        return country;
    }
}
var data_values = {};
{% assign vals = countries | group_by: tag | sort: 'size' %}
{%- for elem in vals -%}
data_values[get_code('{{ elem.name }}')] = {n: {{ elem.size }}};
{% endfor %}

new svgMap({
  targetElementID: 'svgMap',
  showZoomReset: true,
  mouseWheelZoomEnabled: false,
  mouseWheelZoomWithKey: false, /* Does not work very well. */
  zoomScaleSensitivity: 0.4,
  onGetTooltip: function (tooltipDiv, countryID, countryValues) {
    if (countryValues !== undefined) {
      return "Registered teams: "  + countryValues["n"];
    }
    throw new Error("No data available."); // Just throw this.
  },
  /*colorNoData: "#d9ecff",*/
  colorMin: "#cc0033",
  data: {
    data: {
      n: {
        name: 'Registered teams',
        format: '{0}',
        /*thresholdMin: 1,
        thresholdMax: 1*/
      },
    },
    applyData: 'n',
    values: data_values
  }
});
</script>
{%- endif -%}