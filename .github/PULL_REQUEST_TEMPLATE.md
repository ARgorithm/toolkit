**Pull requests that do not have issues linked will not be accepted unless changes are made in documentation or examples**

### All Submissions:

- [ ] Have you followed the guidelines in our Contributing document?
- [ ] Have you checked to ensure there aren't other open [Pull Requests](https://github.com/stevemao/github-issue-templates/pulls) for the same update/change?

### New Feature Submissions:

- [ ] Does your submission pass tests?
- [ ] Have you lint your code locally prior to submission?
- [ ] Did you check how your new feature works on server?

### Changes to Core Features:

- [ ] Have you added an explanation of what your changes do and why you'd like us to include them?
- [ ] Have you written new tests for your core changes, as applicable?
- [ ] Have you successfully ran tests with your changes locally? 
- [ ] if new structure, did you create a valid `[structure]-design.yml`?

**Pull request tags**

These extra tags help us identify what your changes revolve around

| Tag             | Description                                                  |
| --------------- | ------------------------------------------------------------ |
| `documentation` | if changes in documentation are made                         |
| `structure`     | if support for more template class has been added or previous template classes have been fixed |
| `cli`           | if command line interface has been improved                  |
| `base`          | if changes are made in the way intermediate data is generated or structures and states are handled |

**Note**

Link all related issues in the format

```markdown
closes #[issue number]
```