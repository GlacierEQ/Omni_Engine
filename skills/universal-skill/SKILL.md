# Universal Skill Factory
A pluggable framework that allows the system to dynamically generate, validate, and integrate new skills into the workspace on the fly.

## Capabilities
- **Template-Based Generation**: Create new skill structures (SKILL.md, logic scripts, tests) from high-level descriptions.
- **Dynamic Manifest Injection**: Automatically update `SKILLS_MANIFEST.json` and other registries.
- **Validation Suite**: Ensure new skills adhere to the "Operator-Grade" standards.
- **Feedback Loop**: Self-correct skill logic based on execution failures.

## Usage
Provide a skill name and intent, and the factory will provision the directory structure and base logic.
