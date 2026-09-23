/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   5-2_sort_opticsri_exec.c                          :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:33 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_move	choose_move(t_program *program)
{
	t_move	best;
	t_node	*node;
	size_t	a_position;

	best.cost = (size_t) - 1;
	node = program->stack_a;
	a_position = 0;
	while (node != NULL)
	{
		best = choose_node_move(program, node, a_position, best);
		node = node->next;
		a_position++;
	}
	return (best);
}

t_move	choose_node_move(t_program *program, t_node *node,
	size_t	a_position, t_move best)
{
	t_move	candidate;
	size_t	b_position;
	int		mode;

	b_position = insertion_position(program, node->index);
	mode = 0;
	while (mode < 4)
	{
		candidate = make_move(program, a_position, b_position, mode++);
		if (candidate.cost < best.cost)
			best = candidate;
	}
	return (best);
}

size_t	insertion_position(t_program *program, int index)
{
	t_node	*node;
	t_node	*previous;
	size_t	position;
	size_t	maximum;

	if (program->size_b < 2)
		return (0);
	maximum = find_maximum_position(program->stack_b);
	node = program->stack_b;
	previous = node;
	while (previous->next != NULL)
		previous = previous->next;
	position = 0;
	while (node != NULL)
	{
		if (previous->index > index && index > node->index)
			return (position);
		previous = node;
		node = node->next;
		position++;
	}
	return (maximum);
}
