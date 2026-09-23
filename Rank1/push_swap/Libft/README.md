*This project has been created as part of the 42 curriculum by harnakam.*

# Libft

## Description

This project implements `libft.a`, a small C utility library containing libc-like
functions, additional string/output helpers, and linked-list helpers required by
Libft PDF v19.2.

## Instructions

Build:

```sh
make
```

Clean:

```sh
make clean
make fclean
make re
```

The archive `libft.a` is created at the repository root with `ar`.

## Library Details

The library includes:

- Part 1 libc reimplementations, with `ft_` prefix.
- Part 2 additional allocation/string/output helpers.
- Part 3 linked-list helpers using `t_list`.

The implementation avoids global variables. Helper functions are `static`.

## Algorithm and Data Structure Notes

Most functions use direct linear scans over byte arrays or NUL-terminated
strings. Allocation helpers compute the exact output length first, then copy and
NUL-terminate once. The mandatory Part 3 linked-list section uses the `t_list` singly linked data
structure from the subject; ownership is explicit, and `del` is called whenever
mapped or cleared content must be released.

## Resources

- Libft subject PDF v19.2.
- `man 3` pages for libc behavior.
- AI was used to draft and review this reference implementation structure and
  edge-case checklist; the code remains intentionally simple for peer review.
