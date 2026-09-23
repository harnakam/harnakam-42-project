/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-7-1_rank_assign.c                           :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:21 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	find_rank(const int *values, size_t size, int value)
{
	size_t	i;
	int		rank;

	i = 0;
	rank = 0;
	while (i < size)
	{
		if (values[i] < value)
			rank++;
		i++;
	}
	return (rank);
}

void	copy_stack_values(t_node *stack, int *values)
{
	size_t	position;

	position = 0;
	while (stack != NULL)
	{
		values[position++] = stack->value;
		stack = stack->next;
	}
}

void	assign_node_ranks(t_node *stack, const int *values, size_t size)
{
	while (stack != NULL)
	{
		stack->index = find_rank(values, size, stack->value);
		stack = stack->next;
	}
}
