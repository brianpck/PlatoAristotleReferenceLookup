# PlatoAristotleCorpusSearch

This is a Python tool run on the command line that allows you to lookup specific pages or lines from the Aristotle or Plato TLG corpus, using Bekker or Stephanus numbers. To run:

``` 
py corpus_search.py
```

I have done very little to isolate logic or make the code pretty, but (so far) it works for the limited scholarly purpose in ancient philosophy that I've used it for, so I've shared it here.

The following **Bekker** formats for Aristotle citations are supported:
- 423a1 (one line)
- 1117a3-5 (multiple lines)
- 1234b (one column)
- 414b9-415a1 (multiple lines across pages/columns)

The following **Stephanus** formats for Plato are supported:
- 13 (whole page)
- 83b (one section of page)
- 98a1 (individual line)
- 436e1-5 (multiple lines)
- 437b-d (multiple sections)
- 899d5-900a2 (exact span)

Note: For Plato citations, the same page often can refer to different works on different volumes. In this case, you will be prompted to enter the work that you are looking up from a list of possible locations; the tool will then automatically select this work until you enter a Stephanus number that is not contained in the selected work.
