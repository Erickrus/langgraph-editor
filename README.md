# langgraph editor

This tool is designed to visually edit langgraph workflow. You can open the notebook in google's colab. 
Below is the interface of the tool. It is based on [litegraph.js](https://github.com/jagenjo/litegraph.js) as its workflow engine. 

## Installation
### Local machine
```shell
pip3 install -q tornado
git clone https://github.com/Erickrus/langgraph-editor
```

### Google colab
`ngrok` or other NAT Traversal tool is required (e.g. `cpolar`) is used to display the iframe. 

When using `ngrok`, you need input `NGROK_AUTH_KEY` and `NGROK_BEARER_API_KEY`.

## Run
### Local machine
open the url `http://localhost:8082/static/index.html` in your browser.

### Google colab
In google colab, run through the cells, and you will see the interface.

<img src="https://raw.githubusercontent.com/Erickrus/langgraph-editor/main/snapshot.png" width=720px />

## Nodes
3 types of nodes are added, including:
- `LangGraphNode`: normal workflow node
- `LangGraphConditionalNode`: work as the conditional edge
- `LangGraphEndNode`: `END`

## Compile the graph to python code
When finish editing the workflow, click `Compile` menuitem to compile the workflow as a python script. The file will be saved as `/content/output.py` by default. Following is the output python script

```python
from langgraph.graph import END, StateGraph
workflow = StateGraph(GraphState)

# Define the nodes
workflow.add_node("query", query) # query
workflow.add_node("web_search", web_search) # web_search

# Build graph
workflow.add_conditional_edge(
    "query",
    decide,
    {
        "end": END,
        "web_search": "web_search",

    })
workflow.set_entry_point("query")
workflow.add_edge("web_search", END)

# Compile
app = workflow.compile()
```

## Load and Save workflow
The workflow can be loaded or saved locally from or to `/content/workflow.json` .
