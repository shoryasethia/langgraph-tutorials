## ✅ 1. What are `tool_calls`? How does the check work?

### 🔍 Where do `tool_calls` come from?

When you call:

```python
response = model.invoke([...])
```

If you've used `model.bind_tools(...)`, the model is allowed to **call tools**.

If the LLM decides a tool should be called, it returns an `AIMessage` like this:

```python
AIMessage(
  content=None,
  tool_calls=[
    ToolCall(
      name="add",
      args={"a": 3, "b": 4},
      id="some-uuid"
    )
  ]
)
```

So, in your code:

```python
last_message = state["messages"][-1]
if not last_message.tool_calls:
    return "end"
else:
    return "continue"
```

LangGraph checks if the last message **includes tool calls**, and based on that, either:

* runs the tool node, or
* ends the graph.

---

### 🧠 What is `.tool_calls`?

* It’s a **property of `AIMessage`**
* It contains one or more `ToolCall` objects (which hold the tool name + args)

You can even `print(last_message.tool_calls)` to see the raw calls.

---

## ✅ 2. How is the model response structured?

Let’s walk through an example response **in actual structure**:

### Prompt: `"Add 3+4."`

### Output from Gemini after `.invoke()` (when using `bind_tools`):

```python
AIMessage(
    content=None,
    tool_calls=[
        ToolCall(
            name="add",
            args={"a": 3, "b": 4},
            id="tool_call_1"
        )
    ]
)
```

This means:

* The model **didn’t reply with text**
* Instead, it **decided a tool should be used**
* And it returned a structured call to `add(a=3, b=4)`

LangGraph sees this, runs the tool function (the `ToolNode`), and then continues.

---

## ✅ 3. Can I write `model.invoke([...])` differently?

Yes. Here’s how you can break it down or rewrite it depending on what you want.

---

### ✅ Option 1: More readable version

```python
messages = [system_prompt] + state["messages"]
response = model.invoke(messages)
```

---

### ✅ Option 2: Without system prompt (optional)

You can remove the `SystemMessage` if you want to avoid biasing the LLM:

```python
response = model.invoke(state["messages"])
```

But the system prompt is usually important for setting tone + guardrails.

---

### ✅ Option 3: Explicit `HumanMessage`

If you want full manual control:

```python
from langchain_core.messages import HumanMessage

state = {
    "messages": [HumanMessage(content="Add 3+4.")]
}
```

---

### ✅ Option 4: Direct ReAct prompting

If you don’t use `bind_tools`, you could prompt the model to **respond with `Action:` and `Action Input:`**, i.e., classic ReAct style.

```python
HumanMessage(content="""
Thought: I need to add two numbers
Action: add
Action Input: {"a": 3, "b": 4}
""")
```

But this only works **without** tool binding, and you'd have to **parse outputs manually** — so not ideal with LangGraph.

---

## ✅ 4. Is prompt engineering involved?

Yes — in **two places**:

### 🔸 (A) `SystemMessage`

Sets how the agent behaves:

```python
SystemMessage(content="You are my assistant. Please answer to the best of your ability.")
```

You can tweak this:

* Add constraints like: “You can only use tools.”
* Or: “Always explain why you’re calling a tool.”

### 🔸 (B) `Tool docstrings`

Remember:

```python
@tool
def add(a: int, b: int) -> int:
  """Function to add two numbers"""
```

That docstring is shown to the model in the prompt — so if it’s vague, the model may misuse the tool.

---

### 🔥 Tool Prompting Tip:

```python
@tool
def search_in_pdf(query: str) -> str:
    """Searches for an exact phrase or sentence in the uploaded PDF and returns surrounding context"""
```

This gives the LLM very **strong affordance** on when to use this tool — compared to just `"Search tool"`.

---

## ✅ Recap:

| Topic                   | Summary                                                                    |
| ----------------------- | -------------------------------------------------------------------------- |
| `tool_calls`            | Present in `AIMessage` if a tool is invoked                                |
| `model.invoke(...)`     | Sends the message list to LLM and returns a structured response            |
| `should_continue()`     | Checks if tool calls exist in the last message                             |
| Prompt engineering      | Comes in via `SystemMessage` and `@tool` docstrings                        |
| Rewrite `model.invoke`? | Yes — you can cleanly split into steps, or tweak which messages are passed |