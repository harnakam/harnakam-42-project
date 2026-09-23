/* ************************************************************************** */
/*                                                                            */
/*                                                       :::      ::::::::    */
/*   utils-13_find_maximum_position.c                  :+:      :+:    :+:    */
/*                                                   +:+ +:+         +:+      */
/*   By: harnakam <harnakam@student.42tokyo.jp>    #+#  +:+       +#+         */
/*                                               +#+#+#+#+#+   +#+            */
/*   Created: 2026/07/26 16:14:32 by harnakam         #+#    #+#              */
/*   Updated: 2026/07/26 16:16:16 by harnakam        ###   ########.fr        */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

size_t	find_maximum_position(t_node *stack)
{
	t_node	*node;
	size_t	position;
	size_t	best_position;

	node = stack;
	position = 0;
	best_position = 0;
	while (node != NULL)
	{
		if (node->index > stack->index)
		{
			stack = node;
			best_position = position;
		}
		node = node->next;
		position++;
	}
	return (best_position);
}
