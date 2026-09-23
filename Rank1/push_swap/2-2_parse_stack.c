/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   2-2_parse_stack.c                                 :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:38 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	parse_numbers_into_stack_a(t_program *program)
{
	int	i;

	i = 1;
	while (i < program->argc)
	{
		if (!is_option(program->argv[i]))
		{
			if (parse_argument(program, program->argv[i]) == ERROR)
				return (ERROR);
		}
		i++;
	}
	return (SUCCESS);
}

int	append_value_to_stack_a(t_program *program, int value)
{
	t_node	*new_node;
	t_node	*last;

	new_node = malloc(sizeof(t_node));
	if (new_node == NULL)
		return (ERROR);
	new_node->value = value;
	new_node->index = -1;
	new_node->prev = NULL;
	new_node->next = NULL;
	if (program->stack_a == NULL)
		program->stack_a = new_node;
	else
	{
		last = program->stack_a;
		while (last->next != NULL)
			last = last->next;
		last->next = new_node;
		new_node->prev = last;
	}
	program->size_a++;
	return (SUCCESS);
}

int	parse_one_word(t_program *program, const char *start, size_t length)
{
	int	value;

	if (parse_integer(start, length, &value) == ERROR)
		return (ERROR);
	if (value_already_exists(program, value))
		return (ERROR);
	if (append_value_to_stack_a(program, value) == ERROR)
		return (ERROR);
	return (SUCCESS);
}

int	parse_argument(t_program *program, const char *argument)
{
	size_t	i;
	size_t	start;
	int		found_number;

	i = 0;
	found_number = 0;
	while (argument[i] != '\0')
	{
		while (is_space(argument[i]))
			i++;
		if (argument[i] == '\0')
			break ;
		start = i;
		while (argument[i] != '\0' && !is_space(argument[i]))
			i++;
		if (parse_one_word(program, argument + start, i - start) == ERROR)
			return (ERROR);
		found_number = 1;
	}
	if (!found_number)
		return (ERROR);
	return (SUCCESS);
}
