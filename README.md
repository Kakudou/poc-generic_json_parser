This is a Proof of Concept (PoC) project created during a late-night coding session, with bad code and probably not optimized in any way. 

Please keep your sanity intact, and have tissues on hand if you plan to read this code—it might make your eyes bleed.

### What was the purpose of this project?

I often need to parse JSON/API responses, and I wanted to create a simple way to handle this task.

I also need to write an OpenCTI connector to enrich CVE entries when an existing PoC is available. Specifically, I need to parse a JSON file and convert it into a STIX 2.1 format.

In this case, I don’t need to build the entire STIX object from scratch because that will be handled by the STIX library and the connector later on. For this project, I simply wanted to focus on parsing the JSON.

I found it unnecessary to parse the JSON and manually recreate my STIX object piece by piece. Instead, I decided to transform the JSON directly into my desired STIX description.

I'm not sure if this is the best way to approach it, but it’s one way to do it.

### Example

Let’s consider the following JSON (the full version is available in the repo, but here's the first part):

```json
{
  "new": [
    {
      "id": 923420005,
      "node_id": "R_kgDONwpFZQ",
      "name": "CVE-2025-0282",
      "full_name": "AdaniKamal/CVE-2025-0282",
      "private": false,
      "owner": {
        "login": "AdaniKamal",
        "id": 44063862,
        "node_id": "MDQ6VXNlcjQ0MDYzODYy",
        "avatar_url": "https://avatars.githubusercontent.com/u/44063862?v=4",
        "url": "https://api.github.com/users/AdaniKamal",
        "html_url": "https://github.com/AdaniKamal",
        "type": "User",
        "projects": [
          {
            "name": "b70ba621-38c0-4879-ad62-93d7a546fc6f",
            "url": "https://a72c3954-2588-4aa1-8b85-3d72e3e5c699"
          },
          {
            "name": "ade1b04a-4e9f-4c06-aa18-951972a6b9ca",
            "url": "https://fd8bb810-fa5f-40b9-9b06-803a17dd6c0e"
          }
        ]
      },
      "html_url": "https://github.com/AdaniKamal/CVE-2025-0282",
      "description": "Ivanti Connect Secure, Policy Secure & ZTA Gateways - CVE-2025-0282",
      "fork": false,
      "url": "https://api.github.com/repos/AdaniKamal/CVE-2025-0282",
      "created_at": "2025-01-28T07:56:05Z",
      "updated_at": "2025-01-28T07:56:09Z",
      "pushed_at": "2025-01-28T07:56:06Z",
      "stargazers_count": 0,
      "watchers_count": 0,
      "forks_count": 0,
      "archived": false,
      "disabled": false,
      "allow_forking": true,
      "is_template": false,
      "topics": [],
      "visibility": "public",
      "forks": 0,
      "watchers": 0,
      "default_branch": "main",
      "score": 1
    },
    {
      "id": 923546795,
      ...
    }
  ]
}
```

From this JSON, I want to extract the necessary information.

First, I need to create a STIX Identity object with the following properties:

- **name**: AdaniKamal
- **type**: User
- **external_references**:
  - **source_name**: github
  - **description**: AdaniKamal GitHub
  - **url**: https://github.com/AdaniKamal

Next, I need to create a STIX Vulnerability object:

- **name**: CVE-2025-0282
- **external_references**:
  - **source_name**: github
  - **description**: Ivanti Connect Secure, Policy Secure & ZTA Gateways - CVE-2025-0282
  - **url**: https://github.com/AdaniKamal/CVE-2025-0282
- **note**:
  - **abstract**: PoC for CVE-2025-0282
  - **content**: PoC CVE-2025-0282 found at https://github.com/AdaniKamal/CVE-2025-0282, by AdaniKamal

With this information, I can now define my mapping file.

### Mapping File

```json
{
  "jq_root": ".[][] |",
  "identity": {
    "name": ".owner?.login",
    "role": ".owner?.type",
    "external_references": {
      "source_name": (".owner?.login", lambda x: "GitHub"),
      "description": ".owner?.login",
      "url": ".owner?.html_url"
    }
  },
  "vulnerability": {
    "name": (".name",
        lambda cve: (
            __import__('re').search(r'CVE-\d{4}-\d+', cve).group()
            if __import__('re').search(r'CVE-\d{4}-\d+', cve)
            else None
        )
    ),
    "external_references": {
        "source_name": (".url", lambda x: "GitHub"),
        "description": ".description",
        "url": ".html_url"
    },
    "note": {
      "content": ("[.name, .html_url, .owner?.login]", lambda x: f"PoC {x[0]} found at {x[1]}, by {x[2]}"),
    }
  }
}
```

### Parsing the JSON

Now we can parse and normalize the data:

```bash
>python parser.py --mapping mapping.json --json data.json
```

And the resulting output will be:

```json
[
  {
    "identity": {
      "name": "AdaniKamal",
      "role": "User",
      "external_references": {
        "source_name": "GitHub",
        "description": "AdaniKamal",
        "url": "https://github.com/AdaniKamal"
      }
    },
    "vulnerability": {
      "name": "CVE-2025-0282",
      "external_references": {
        "source_name": "GitHub",
        "description": "Ivanti Connect Secure, Policy Secure & ZTA Gateways - CVE-2025-0282",
        "url": "https://github.com/AdaniKamal/CVE-2025-0282"
      },
      "note": {
        "content": "PoC CVE-2025-0282 found at https://github.com/AdaniKamal/CVE-2025-0282, by AdaniKamal"
      }
    }
  },
  ...
]
```

### Conclusion

And that’s it! We now have our STIX objects ready to be used by the connector. They are easily transformable into a STIX object with SRO (Structured Data Representation), as everything is already “bundled” for easy use.

