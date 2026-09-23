/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   4-1_simple_sort.c                                 :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:36 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	spin_bubble_sort(t_program *program)
{
	int	minimum;
	int	maximum;

	find_limits(program, &minimum, &maximum);
	while (!stack_a_is_sorted(program))
		if (!spin_bubble_pass(program, minimum, maximum))
			return ;
}

void	find_limits(t_program *program, int *minimum, int *maximum)
{
	t_node	*node;

	node = program->stack_a;
	*minimum = node->value;
	*maximum = node->value;
	while (node != NULL)
	{
		if (node->value < *minimum)
			*minimum = node->value;
		if (node->value > *maximum)
			*maximum = node->value;
		node = node->next;
	}
}

int	spin_bubble_pass(t_program *program, int minimum, int maximum)
{
	size_t	i;
	int		swapped;

	i = 0;
	swapped = 0;
	while (i < program->size_a && !stack_a_is_sorted(program))
	{
		if (!(program->stack_a->value == maximum
				&& program->stack_a->next->value == minimum)
			&& program->stack_a->value > program->stack_a->next->value)
		{
			op_sa(program);
			swapped = 1;
		}
		if (!stack_a_is_sorted(program))
			op_ra(program);
		i++;
	}
	return (swapped);
}
