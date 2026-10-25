# Coding Standards

<!--
Precise, verifiable style rules. Rules must be specific enough for a reviewer
to say "this line passes" or "this line fails."

Only document deliberate project choices that go beyond tool defaults (linters,
formatters, type checkers). Do not duplicate rules that are already enforced by
a configuration file — reference those files instead.

This file is read by the /code-review skill for the Standards axis of its review.
Reference it from CONTRIBUTING.md and AGENTS.md. Do not copy rules between files.
-->

## Language and formatting

> <!--
> Indentation, line length, quote style, trailing commas, and any formatting
> rule not already enforced by a tool configuration file.
>
> Example:
> - Use 2-space indentation.
> - Maximum line length is 100 characters.
> - Use single quotes for strings unless the string contains a single quote.
> -->

[Describe language and formatting rules.]

## Naming conventions

> <!--
> File names, function names, class names, variable names, and constants.
>
> Example:
> - Use camelCase for functions and variables.
> - Use PascalCase for classes and types.
> - Use SCREAMING_SNAKE_CASE for module-level constants.
> - Prefix boolean variables with is, has, or can.
> -->

[Describe naming conventions.]

## Module and import rules

> <!--
> How to organise imports. Module boundaries. Barrel file policy.
>
> Example:
> - Group imports: external packages first, then internal modules, then types.
> - No barrel re-exports (index.ts) inside src/.
> -->

[Describe module and import rules.]

## Error handling

> <!--
> The approved error-handling pattern and how to surface errors to callers.
>
> Example:
> - Use Result<T, E> types instead of throwing for expected errors.
> - Only throw for programming errors (invalid arguments, unreachable code).
> - Log errors at the boundary where they are caught, not at the throw site.
> -->

[Describe error-handling conventions.]

## Testing conventions

> <!--
> Test file naming, directory structure, what must be tested, mocking rules.
>
> Example:
> - Test files live next to the source file: foo.ts → foo.test.ts.
> - Use describe/it blocks. The describe block mirrors the module name.
> - Do not mock the database. Use a test database with real migrations.
> - Test observable behaviour, not implementation details.
> -->

[Describe testing conventions.]

## Patterns to follow

> <!--
> Code patterns the team has agreed to use. Cite the reason where it is not
> obvious.
> -->

[List approved patterns.]

## Patterns to avoid

> <!--
> Code patterns the team has agreed to ban. Cite the reason.
> -->

[List banned patterns.]
