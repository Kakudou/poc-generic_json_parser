Feature: We should be able to normalize an input json into a desired output json.

    Scenario Outline: We have an input json, and we wrote a mapping file describing the output we want, then we should obtain the output json filled with the good data.
        Given I have an <input_json> as a str, and an <mapping_description> as a str.
        When I apply the mapping description over the json data.
        Then I obtain the desire <normalized_json>

        Examples:
            | input_json | mapping_description | normalized_json |
            | {"name": "John","age":30} | {"jq_root":".\|","person":{"person_name":".name","person_age":".age"}} | [{'person': {'person_name': 'John', 'person_age': 30}}] |
            | [{"fetchTime":"2025-01-29T10:36:35.834Z","numberOfChanges":1,"new":[{"cveId":"CVE-2025-0762","cveOrgLink":"https://www.cve.org/CVERecord?id=CVE-2025-0762","githubLink":"https://raw.githubusercontent.com/CVEProject/cvelistV5/main/cves/2025/0xxx/CVE-2025-0762.json","dateUpdated":"2025-01-29T10:33:45.673Z"}],"updated":[],"error":[]}] | {"jq_root":".[]\|(.new[]?,.updated[]?)\|","vulnerability":{"name":".cveId","external_references":{"source_name":(".cveId",lambda x:"url"),"url":".cveOrgLink"}}} | [{'vulnerability': {'name': 'CVE-2025-0762', 'external_references': {'source_name': 'url', 'url': 'https://www.cve.org/CVERecord?id=CVE-2025-0762'}}}] |
