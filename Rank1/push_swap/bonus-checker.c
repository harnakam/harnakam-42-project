/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   bonus-checker.c                                   :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:31 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	read_instruction(char *line)
{
	char	character;
	int		position;
	ssize_t	read_size;

	position = 0;
	while (position < 5)
	{
		read_size = read(0, &character, 1);
		if (read_size < 0)
			return (-1);
		if (read_size == 0)
		{
			if (position == 0)
				return (0);
			break ;
		}
		line[position++] = character;
		if (character == '\n')
			break ;
	}
	line[position] = '\0';
	return (1);
}

static int	execute_double_instruction(char *line, t_program *program)
{
	if (strings_are_equal(line, "ss\n"))
	{
		swap_stack(program->stack_a);
		swap_stack(program->stack_b);
	}
	else if (strings_are_equal(line, "rr\n"))
	{
		rotate_stack(&program->stack_a);
		rotate_stack(&program->stack_b);
	}
	else if (strings_are_equal(line, "rrr\n"))
	{
		reverse_rotate_stack(&program->stack_a);
		reverse_rotate_stack(&program->stack_b);
	}
	else
		return (ERROR);
	return (SUCCESS);
}

static int	execute_instruction(char *line, t_program *program)
{
	if (strings_are_equal(line, "sa\n"))
		swap_stack(program->stack_a);
	else if (strings_are_equal(line, "sb\n"))
		swap_stack(program->stack_b);
	else if (strings_are_equal(line, "pa\n"))
		push_stack(&program->stack_b, &program->stack_a,
			&program->size_b, &program->size_a);
	else if (strings_are_equal(line, "pb\n"))
		push_stack(&program->stack_a, &program->stack_b,
			&program->size_a, &program->size_b);
	else if (strings_are_equal(line, "ra\n"))
		rotate_stack(&program->stack_a);
	else if (strings_are_equal(line, "rb\n"))
		rotate_stack(&program->stack_b);
	else if (strings_are_equal(line, "rra\n"))
		reverse_rotate_stack(&program->stack_a);
	else if (strings_are_equal(line, "rrb\n"))
		reverse_rotate_stack(&program->stack_b);
	else
		return (execute_double_instruction(line, program));
	return (SUCCESS);
}

int	main(int argc, char **argv)
{
	t_program	program;
	char		line[6];
	int			read_status;

	if (argc == 1)
		return (0);
	initialize_program(&program, argc, argv);
	if (process_input(&program) == ERROR)
		return (print_error_and_free(&program));
	read_status = read_instruction(line);
	while (read_status > 0)
	{
		if (execute_instruction(line, &program) == ERROR)
			return (print_error_and_free(&program));
		read_status = read_instruction(line);
	}
	if (read_status < 0)
		return (print_error_and_free(&program));
	if (stack_a_is_sorted(&program) && program.stack_b == NULL)
		write(1, "OK\n", 3);
	else
		write(1, "KO\n", 3);
	free_all(&program);
	return (0);
}
