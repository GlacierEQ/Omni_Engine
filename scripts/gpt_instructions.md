# 🤖 GPT Integration Instructions for Omni_Engine

This document explains how GPT-based agents can use this repository as a boot source for personalized operations.

---

## 🔐 Secure Connection Protocol

Use Git's credential helper to authenticate locally:

```bash
git config --global credential.helper store
```

---

## 🚀 Boot Sequence

1. Clone this repository into the agent's working directory.
2. Install dependencies with `pip install -r requirements.txt`.
3. Read `AGENTS.md` for coding conventions and testing rules.
4. Run `pytest -q` before committing to ensure all checks pass.
5. Commit changes with descriptive messages.

---

## 🧠 Memory Bridge Integration

- Import components directly from the package root:

```python
from modules import FusionLoop, MemoryEntry, MemoryLayer, WitnessNetwork
```

- Register nodes with a `WitnessNetwork` to receive updates.
- Create `MemoryLayer` instances and initialize a `FusionLoop`.
- Call `FusionLoop.cycle(nodes)` to synchronize entries between nodes.

---

## 🛠 Development Workflow

- Format code with PEP8 and include type hints and docstrings.
- Use focused commits that reference related issues when applicable.
- Push your branch and open a pull request for review.

---

## 🔗 Using this Repository as a GPT Boot

Connect the repository to a custom GPT so it loads these instructions on
startup:

1. In the ChatGPT "Build" tab, add this GitHub repository under **Code
   Interpreter → Repositories**.
2. Select the branch you want the GPT to track (usually `main`).
3. The GPT will clone the repo at boot and read `AGENTS.md` and
   `scripts/gpt_instructions.md` for guidance.
4. Update the repository and push commits to change the GPT's behavior
   without rebuilding the model.

This setup provides a lightweight personalization layer that can evolve as
the project grows.

---

## 📚 Resources

- `modules/memory_bridge` contains the memory bridge implementation.
- `tests/` provides unit tests verifying synchronization behavior.

