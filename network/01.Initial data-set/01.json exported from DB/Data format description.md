These json files are exported directly from the MongoDB database. And the data format list as follows:

## papers

```json
[
	{
		"_id": "",//paper_id,
        "abstract": "",
        "author_keywords": [  //keywords listed by author
        ],
        "authors": [ //author_list
            {
                "_id": "",//author_id,
                "dblp_name": "",//author's name in dblp,
                "index": "",//the author contributing order,
                "affiliation": "",//author's affiliation when this paper came out
                "name": "",//author's true name
            }
        ],
        "doi": "",//paper's doi number,
        "end_page": "",
        "key": "",//Key words of the paper in dblp,
        "links":[ //paper's access link
            //e.g.,"https://ieeexplore.ieee.org/document/8512175"
        ],
        "number": "",//the number of journal,
        "start_page":"",
        "title": "",//paper's title,
        "type": "",//paper's type, including Conference and Workshop Papers and Journal Articles
        "venue":  "",//Abbreviation of the conference/journal to which it belongs, such as NOCS.
        "volume": "",//volume of journal,
        "year": "",//publication year,
        "citations": [  //This article cite the following articles：
        	{
        		'text': "",//the title of the cited paper
        		'_id': "",//the id of the cited paper
        	}
        ],
        "references": [ //This article is cited by the following articles:
        	{
        		'text': "",
        		'_id': "",
        	}
        ]
	}
]
```



## authors

```json
[
    {
        "_id": "",//author's id,
        "affiliations": [ 
        	//All affiliations where the author has stayed
        ],
        "aliases":[
            //Author alias list
        ],
        "current_affiliation":"", //Author's current affiliation,
        "dblp_name": "",//author's name in dblp,
        "email": "",//the email of the author,
        "links": [
            "https://ieeexplore.ieee.org/author/38188695900"
        ],
        "name": "",//author's true name,
        "orcid": "",//the orcid of the author,
        "photo_url": "",//Author's avatar image address
    },
]
```



## co-authors

```json
{
    "author_id": [ //co-author's list
        {
            "_id": "",//co-author's id，
            "num": //Number of collaborative papers
        },
        ...
    ],
    ...
}
```



## citations

```json
{ //This article cite the following articles：
	"paper_id": [ //citation list
		{
			"text": "",//the title of the cited paper
			'_id': //the id of the cited paper
		},
		...
	],
	...
}
```



## references

```json
{ //This article is cited by the following articles：
	"paper_id": [ //references list
		{
			"text": "",//the title of the citing paper
			'_id': //the id of the citing paper
		},
		...
	],
	...
}
```

