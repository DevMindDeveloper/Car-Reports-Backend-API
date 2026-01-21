# High-Level Explanation of Flow-Conservation Encoding (add_flow_penalty)

## 1. Purpose of the Encoding

The goal of the encoding is to transform a **shortest-path problem** into a **Binary Quadratic Model (BQM) / QUBO** that can be solved using different optimization approaches such as:
- Simulated Annealing (SA)
- Digital Annealing (DA)
- Simulated Quantum Annealing (SQA)
- Quantum Approximate Optimization Algorithm (QAOA)

The encoding ensures that:
- A **valid path** exists from a single source node to a single target node
- The selected edges form **one continuous path**
- Invalid solutions (disconnected edges, branching, multiple paths) are penalized

This is achieved using **flow conservation constraints**.

---

## 2. Decision Variables (Edge-Based Encoding)

The formulation uses an **edge-based encoding**:

- Each directed edge \( (u \rightarrow v) \) is associated with a binary variable:

  \[
  x_{uv} \in \{0, 1\}
  \]

- \( x_{uv} = 1 \) means the edge is selected as part of the path
- \( x_{uv} = 0 \) means the edge is not used

There are **no node variables** and **no auxiliary (slack) variables**.

---

## 3. Flow Conservation Constraint (Conceptual View)

For every node \( v \), the path must satisfy:

\[
\sum_{e \in \text{out}(v)} x_e - \sum_{e \in \text{in}(v)} x_e = \delta_v
\]

Where:
- \( \delta_v = +1 \) for the **start (source) node**
- \( \delta_v = -1 \) for the **target (sink) node**
- \( \delta_v = 0 \) for all **intermediate nodes**

This enforces:
- One unit of flow leaves the source
- One unit of flow enters the target
- All intermediate nodes have equal incoming and outgoing flow

---

## 4. From Constraint to Penalty (Why Squaring is Used)

Instead of enforcing the constraint directly, it is added as a **penalty term** to the objective:

\[
\lambda \left( \sum_{\text{out}} x_e - \sum_{\text{in}} x_e - \delta \right)^2
\]

Key idea:
- If the constraint is satisfied → penalty = 0
- If violated → penalty > 0

This allows the constraint to be handled naturally within a QUBO framework.

---

## 5. What add_flow_penalty Does (High-Level Breakdown)

The function `add_flow_penalty` adds the expanded squared penalty term into the BQM. It does this in **five conceptual steps**:

### 5.1 Constant Offset

```python
bqm.offset += lambda_ * delta ** 2
```

- This comes from squaring the constant term \( \delta \)
- It does not affect optimization decisions
- Ensures the energy expression is mathematically correct

---

### 5.2 Base Penalty on All Incident Edges

```python
for var in pos_vars + neg_vars:
    bqm.add_linear(var, lambda_)
```

- Adds a baseline penalty to all edges touching the node
- Prevents trivial activation of many edges
- Sets up the squared expansion

---

### 5.3 Penalizing Multiple Outgoing Edges

```python
bqm.add_quadratic(pos_vars[i], pos_vars[j], 2 * lambda_)
```

- Applies when **more than one outgoing edge** is selected
- Discourages path branching
- Enforces "at most one outgoing edge" behavior

---

### 5.4 Penalizing Multiple Incoming Edges

```python
bqm.add_quadratic(neg_vars[i], neg_vars[j], 2 * lambda_)
```

- Applies when **more than one incoming edge** is selected
- Prevents path merging or cycles

---

### 5.5 Balancing Incoming vs Outgoing Flow

```python
bqm.add_quadratic(p, n, -2 * lambda_)
```

- Couples incoming and outgoing edges
- Encourages equality between in-flow and out-flow
- Enforces continuity of the path

---

### 5.6 Source and Target Bias (Flow Direction)

```python
bqm.add_linear(p, -2 * delta * lambda_)
bqm.add_linear(n,  2 * delta * lambda_)
```

- Adds **directional bias** based on node role

For the **source** (\( \delta = +1 \)):
- Encourages one outgoing edge
- Discourages incoming edges

For the **target** (\( \delta = -1 \)):
- Encourages one incoming edge
- Discourages outgoing edges

For intermediate nodes (\( \delta = 0 \)):
- No directional bias

---

## 6. Resulting Behavior (What This Guarantees)

Together, these terms ensure that:

- Exactly one path starts at the source
- Exactly one path ends at the target
- All intermediate nodes have balanced flow
- No disconnected edges are selected
- No branching or merging occurs

Thus, **any low-energy solution corresponds to a valid path**.

---

## 7. Why No Slack Variables Are Needed

Because the squared constraint is **fully expanded algebraically**, the encoding uses:

- Only original edge variables
- No auxiliary or slack variables

This makes the formulation:
- Qubit-efficient (important for QAOA)
- Consistent across SA, DA, SQA, and QAOA

---

## 8. Summary

- The encoding uses **edge-based binary variables**
- Flow conservation is enforced via **quadratic penalties**
- The `add_flow_penalty` function implements the exact expansion of a squared flow constraint
- Valid paths correspond to **minimum-energy solutions**
- The same encoding is reused across all four optimization approaches

This ensures both **correctness** (valid paths only) and **comparability** across solvers.

